"""Bounded single-user approval/execution slice for the original test candidate.

No model output can invoke this endpoint. Interactive decisions are required;
the separate simulated test API cannot issue normal interactive approvals.
"""
import argparse
import ast
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import getpass
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tarfile
import threading
import uuid

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langgraph.types import Command, interrupt
from typing import TypedDict

from action_planning import Plan, classify_and_rank

from runtime_paths import ROOT, PROJECT
SOURCE = "collection_ops.py"
TARGET = "tests/test_collection_ops.py"
IMAGE = "python@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f"
POLICY = {"version": "isolated-unittest-v1", "image": IMAGE,
    "allowed_paths": [TARGET], "source_paths": [SOURCE], "network": "none",
    "read_only": True, "user": "65534:65534", "cap_drop": "ALL",
    "no_new_privileges": True, "memory": "128m", "cpus": "0.5", "pids": 32,
    "tmpfs_bytes": 16777216, "timeout_seconds": 30, "max_log_bytes": 65536,
    "tool": "stdlib_unittest", "minimum_candidate_tests": 7,
    "approval_ttl_minutes": 30, "host_mounts": [], "auto_pull": False}


def digest(value):
    data = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def filesystem_path(path):
    """Win32 extended paths keep nested operation evidence visible beyond MAX_PATH."""
    path = Path(path).resolve()
    value = str(path)
    if os.name == 'nt' and not value.startswith('\\\\?\\'):
        value = '\\\\?\\UNC\\' + value[2:] if value.startswith('\\\\') else '\\\\?\\' + value
    return Path(value)


def operation_paths(directory, identity):
    """New operations use short UUID workspaces; old evidence keeps its original layout."""
    root = filesystem_path(directory / 'operations' / identity)
    marker = root / 'workspace-location.json'
    if marker.exists():
        if json.loads(marker.read_text()) != {'layout': 'short-workspace-v1', 'operation_id': identity}:
            raise ValueError('Operation workspace location changed')
        if not re.fullmatch(r'[0-9a-f]{32}', identity):
            raise ValueError('Invalid operation ID')
        home = filesystem_path(PROJECT / 'artifacts/ws' / identity)
    else:
        home = root
    return root, home / 'workspace', home / 'quarantined_workspace'


def now():
    return datetime.now(timezone.utc)


def git(repo, *args, data=None):
    # Git for Windows uses its own long-path handling and rejects Win32 prefixes.
    def git_path(value):
        value = str(value)
        if os.name == 'nt' and value.startswith('\\\\?\\UNC\\'):
            return '\\\\' + value[8:]
        return value[4:] if os.name == 'nt' and value.startswith('\\\\?\\') else value
    result = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "core.longpaths=true", "-C", git_path(repo), *map(git_path, args)], input=data,
        capture_output=True, timeout=20)
    if result.returncode:
        raise ValueError("Git operation failed: " + result.stderr.decode(errors="replace")[:1000])
    return result.stdout


def docker_path():
    import shutil
    path = shutil.which("docker") or r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"
    if not Path(path).is_file():
        raise ValueError("Docker is not installed")
    return path


def preflight():
    docker = docker_path()
    system = subprocess.run([docker, "info", "--format", "{{.OSType}}"],
        capture_output=True, text=True, timeout=15, check=True).stdout.strip()
    if system != "linux":
        raise ValueError("Linux container engine required")
    subprocess.run([docker, "image", "inspect", IMAGE], capture_output=True,
                   timeout=15, check=True)


def patch_content(patch):
    if len(patch) > 32768 or b"\r" in patch:
        raise ValueError("Patch size or encoding rejected")
    lines = patch.decode("utf-8").splitlines(keepends=True)
    if lines[:2] != ["--- /dev/null\n", f"+++ b/{TARGET}\n"]:
        raise ValueError("Only the new allowlisted test file is permitted")
    match = re.fullmatch(r"@@ -0,0 \+1,(\d+) @@\n", lines[2]) if len(lines) > 2 else None
    if not match or int(match[1]) != len(lines) - 3 or any(not l.startswith("+") for l in lines[3:]):
        raise ValueError("Only one valid new-file hunk is permitted")
    content = "".join(l[1:] for l in lines[3:])
    tree = ast.parse(content)
    # Bounded first-slice policy, not a general Python security validator.
    for node in tree.body:
        if isinstance(node, ast.Import) and [a.name for a in node.names] == ["unittest"]:
            continue
        if isinstance(node, ast.ImportFrom) and node.module == "collection_ops" and [a.name for a in node.names] == ["Common_Items"]:
            continue
        if isinstance(node, ast.ClassDef) and len(node.bases) == 1 and ast.unparse(node.bases[0]) == "unittest.TestCase":
            continue
        raise ValueError("Unexpected top-level test code")
    return content.encode()


def binding(manifest):
    return digest(manifest)


def validate(directory, *, repository=None, plan_result=None, review_file=None):
    manifest = json.loads((directory / "manifest.json").read_text())
    patch = (directory / "candidate.patch").read_bytes()
    content = patch_content(patch)
    if digest(patch) != manifest["patch_sha256"] or digest(content) != manifest["new_file_sha256"]:
        raise ValueError("Candidate digest mismatch")
    if manifest["policy"] != POLICY or manifest["policy_sha256"] != digest(POLICY):
        raise ValueError("Runner policy changed; fresh candidate required")
    if manifest["changed_paths"] != [TARGET] or manifest["scope"] != [SOURCE, TARGET]:
        raise ValueError("Scope mismatch")
    plan_result = plan_result or ROOT / "artifacts/plan-spike/result.json"
    current = json.loads(plan_result.read_text())
    plan = Plan.model_validate(current["plan"])
    if digest(plan.model_dump()) != manifest["plan_sha256"] or plan.version != manifest["plan_version"]:
        raise ValueError("Plan revision invalidates approval")
    review_file = review_file or ROOT / "artifacts/live-spike/result.json"
    raw = review_file.read_bytes()
    if digest(raw) != manifest["review_artifact_sha256"] or digest(raw) != current["evidence"]["review_artifact_sha256"]:
        raise ValueError("Review provenance changed")
    review = json.loads(raw)
    roles = {"security", "performance", "style", "test_gap"}
    if set(review["reviews"]) != roles or any(r["status"] != "complete" for r in review["reviews"].values()):
        raise ValueError("All four reviews must be complete")
    if digest(review["source"].encode()) != review["source_sha256"] or review["source"] != current["evidence"]["source"]:
        raise ValueError("Review snapshot mismatch")
    ranked = classify_and_rank(plan, set(current["evidence"]["findings"]))
    if not any(r["action_id"] == manifest["step_id"] and r["ready_for_proposal"] for r in ranked):
        raise ValueError("Action is no longer ready")
    repo = repository or ROOT / "artifacts/first-patch/baseline"
    if git(repo, "status", "--porcelain").strip():
        raise ValueError("Baseline is dirty")
    if git(repo, "rev-parse", "HEAD").decode().strip() != manifest["parent_commit"] or git(repo, "rev-parse", "HEAD^{tree}").decode().strip() != manifest["parent_tree_hash"]:
        raise ValueError("Parent changed; fresh approval required")
    if git(repo, "show", "HEAD:" + SOURCE) != review["source"].encode():
        raise ValueError("Baseline differs from reviewed snapshot")
    git(repo, "apply", "--check", "--whitespace=error", "-", data=patch)
    return manifest


@contextmanager
def run_lock(directory):
    import msvcrt
    with (directory / "run.lock").open("a+b") as handle:
        handle.seek(0)
        handle.write(b"0")
        handle.flush()
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            raise ValueError("Another operator/executor owns this run") from None
        try:
            yield
        finally:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


class Ledger:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS decisions(
              id TEXT PRIMARY KEY, binding TEXT, actor TEXT, mode TEXT, decision TEXT,
              issued TEXT, expires TEXT, comment TEXT, consumed TEXT);
            CREATE TABLE IF NOT EXISTS operations(
              id TEXT PRIMARY KEY, approval TEXT UNIQUE, binding TEXT, state TEXT,
              result TEXT, post_tree TEXT);
        ''')

    def decision(self, manifest, actor, decision, comment="", *, simulated=False, at=None):
        if decision not in {"approve", "reject", "redirect", "defer", "cancel"}:
            raise ValueError("Unsupported decision")
        issued = at or now()
        expiry = issued + timedelta(minutes=POLICY["approval_ttl_minutes"]) if decision == "approve" else None
        identity = uuid.uuid4().hex
        with self.db:
            self.db.execute("INSERT INTO decisions VALUES(?,?,?,?,?,?,?,?,NULL)",
                (identity, binding(manifest), actor, "simulated" if simulated else "interactive",
                 decision, issued.isoformat(), expiry.isoformat() if expiry else None, comment))
        return identity

    def consume(self, approval, manifest, actor, *, simulated=False):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT * FROM decisions WHERE id=?", (approval,)).fetchone()
            if not row or row["binding"] != binding(manifest) or row["actor"] != actor or row["mode"] != ("simulated" if simulated else "interactive") or row["decision"] != "approve":
                raise ValueError("Approval actor, mode, decision or binding mismatch")
            if row["consumed"]:
                operation = self.operation(row["consumed"])
                if not operation or operation["binding"] != binding(manifest):
                    raise ValueError("Approval/operation ledger mismatch")
                self.db.commit()
                return operation
            if datetime.fromisoformat(row["expires"]) <= now():
                raise ValueError("Approval expired; new decision required")
            if self.db.execute("SELECT 1 FROM operations WHERE binding=?", (binding(manifest),)).fetchone():
                raise ValueError("This candidate already has an operation; resume it or prepare a fresh candidate")
            operation_id = uuid.uuid4().hex
            self.db.execute("INSERT INTO operations VALUES(?,?,?,'PREPARED',NULL,NULL)",
                (operation_id, approval, binding(manifest)))
            self.db.execute("UPDATE decisions SET consumed=? WHERE id=? AND consumed IS NULL", (operation_id, approval))
            self.db.commit()
            return self.operation(operation_id)
        except BaseException:
            self.db.rollback()
            raise

    def operation(self, identity):
        row = self.db.execute("SELECT * FROM operations WHERE id=?", (identity,)).fetchone()
        return dict(row) if row else None

    def update(self, identity, state, result=None, post_tree=None):
        with self.db:
            self.db.execute("UPDATE operations SET state=?,result=?,post_tree=COALESCE(?,post_tree) WHERE id=?",
                (state, json.dumps(result) if result is not None else None, post_tree, identity))


# Only these two names are exported; no host mounts, .git, .env or credentials.
def export_source(workspace):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        for name in (SOURCE, TARGET):
            path = workspace / name
            if not path.exists():
                continue
            if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
                raise ValueError("Symlink export rejected")
            data = path.read_bytes()
            if len(data) > 32768:
                raise ValueError("Export exceeds bounded source limit")
            item = tarfile.TarInfo(name)
            item.size, item.mode = len(data), 0o444
            archive.addfile(item, io.BytesIO(data))
    return buffer.getvalue()


BOOTSTRAP = '''import io,json,os,pathlib,sys,tarfile,unittest
root=pathlib.Path('/workspace')
with tarfile.open(fileobj=io.BytesIO(sys.stdin.buffer.read(131072)),mode='r:') as archive:
 for item in archive:
  if item.name not in {'collection_ops.py','tests/test_collection_ops.py'} or not item.isfile():
   raise ValueError('Invalid export')
  path=root/item.name; path.parent.mkdir(parents=True,exist_ok=True)
  path.write_bytes(archive.extractfile(item).read())
(root/'tests').mkdir(exist_ok=True)
os.chdir(root); sys.path.insert(0,str(root))
suite=unittest.defaultTestLoader.discover(str(root/'tests'))
result=unittest.TextTestRunner(verbosity=2).run(suite)
print('LEDGER_RESULT:'+json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped)}),flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
'''

POLICY["bootstrap_sha256"] = digest(BOOTSTRAP.encode())


def container_counts(output):
    # Docker can interleave stdout's marker with a partial stderr progress line.
    # Count every occurrence so an untrusted test cannot spoof an extra result.
    marker = b'LEDGER_RESULT:'
    if output.count(marker) != 1:
        return None
    try:
        counts, _ = json.JSONDecoder().raw_decode(output.split(marker, 1)[1].decode('utf-8'))
        if not isinstance(counts, dict) or any(type(counts.get(key)) is not int or counts[key] < 0
                for key in ('tests', 'failures', 'errors', 'skipped')):
            return None
        return counts
    except (ValueError, UnicodeError):
        return None


def container_check(workspace, log_path, *, baseline=False, policy=None, bootstrap=None, exporter=None):
    policy = policy or POLICY
    bootstrap = bootstrap or BOOTSTRAP
    exporter = exporter or export_source
    docker = docker_path()
    name = "ledger-" + uuid.uuid4().hex
    args = [docker, "run", "--rm", "--pull", "never", "--name", name, "--network", "none",
        "--read-only", "--user", POLICY["user"], "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--memory", policy["memory"], "--cpus", policy["cpus"], "--pids-limit", str(policy["pids"]),
        "--tmpfs", "/workspace:rw,nosuid,nodev,noexec,size=16m,mode=1777",
        "--tmpfs", "/tmp:rw,nosuid,nodev,noexec,size=16m,mode=1777",
        "--env", "PYTHONDONTWRITEBYTECODE=1", "-i", policy["image"], "python", "-I", "-c", bootstrap]
    output, overflow = bytearray(), threading.Event()
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def read_output():
        while chunk := process.stdout.read(4096):
            remaining = policy["max_log_bytes"] - len(output)
            output.extend(chunk[:max(remaining, 0)])
            if len(chunk) > remaining:
                overflow.set()
                process.kill()
                break

    reader = threading.Thread(target=read_output, daemon=True)
    reader.start()
    reason = None
    try:
        payload = exporter(workspace)
        def write_input():
            try:
                process.stdin.write(payload)
                process.stdin.close()
            except (BrokenPipeError, OSError):
                pass
        threading.Thread(target=write_input, daemon=True).start()
        process.wait(timeout=policy["timeout_seconds"])
    except subprocess.TimeoutExpired:
        reason = "timeout"
    finally:
        subprocess.run([docker, "rm", "-f", name], capture_output=True, timeout=15)
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)
        reader.join(timeout=5)
        process.stdout.close()
        if not process.stdin.closed:
            process.stdin.close()
        log_path.write_bytes(bytes(output))
    if reason or overflow.is_set():
        return {"status": reason or "log_limit", "exit_code": process.returncode, "log_sha256": digest(bytes(output))}
    counts = container_counts(bytes(output))
    if counts is None:
        return {"status": "unavailable", "exit_code": process.returncode, "log_sha256": digest(bytes(output))}
    passed = process.returncode == 0 and counts["failures"] == counts["errors"] == counts["skipped"] == 0
    status = "no_tests" if baseline and counts["tests"] == 0 and passed else (
        "passed" if passed and counts["tests"] >= policy["minimum_candidate_tests"] else "failed")
    return {"status": status, "exit_code": process.returncode, **counts, "log_sha256": digest(bytes(output))}


def reconcile_workspace(workspace, manifest, content):
    if git(workspace, "rev-parse", "HEAD").decode().strip() != manifest["parent_commit"]:
        raise ValueError("Workspace parent mismatch")
    if git(workspace, "show", "HEAD:" + SOURCE) != (workspace / SOURCE).read_bytes():
        raise ValueError("Workspace source changed")
    present = {p.relative_to(workspace).as_posix() for p in workspace.rglob('*')
               if p.is_file() and '.git' not in p.relative_to(workspace).parts}
    if present != {SOURCE, TARGET} or (workspace / TARGET).is_symlink() or (workspace / TARGET).read_bytes() != content:
        raise ValueError("Workspace does not match exact candidate")
    git(workspace, "add", "--", TARGET)
    return git(workspace, "write-tree").decode().strip()


def execute(directory, manifest, ledger, approval, actor, *, simulated=False,
            validate_fn=None, check_fn=None, reconcile_fn=None, content_fn=None,
            baseline_repo=None, changed_path=TARGET):
    validate_fn = validate_fn or validate
    check_fn = check_fn or container_check
    reconcile_fn = reconcile_fn or reconcile_workspace
    content_fn = content_fn or patch_content
    if validate_fn(directory) != manifest:
        raise ValueError("Current candidate differs from approved state")
    preflight()
    op = ledger.consume(approval, manifest, actor, simulated=simulated)
    if op["state"] in {"VERIFIED", "FAILED", "AMBIGUOUS", "CANCELLED"}:
        return {"operation_id": op["id"], "state": op["state"], "replayed": True,
                "evidence": json.loads(op["result"]) if op["result"] else None}
    op_root = filesystem_path(directory / "operations" / op["id"])
    op_root.mkdir(parents=True, exist_ok=True)
    if not any((op_root / name).exists() for name in ('workspace', 'quarantined_workspace', 'workspace-location.json')):
        (op_root / 'workspace-location.json').write_text(json.dumps(
            {'layout': 'short-workspace-v1', 'operation_id': op['id']}))
    op_root, workspace, quarantine = operation_paths(directory, op['id'])
    workspace.parent.mkdir(parents=True, exist_ok=True)
    baseline_repo = baseline_repo or ROOT / "artifacts/first-patch/baseline"
    patch = (directory / "candidate.patch").read_bytes()
    content = content_fn(patch)
    if digest(patch) != manifest["patch_sha256"]:
        raise ValueError("Patch changed before execution")
    try:
        baseline_log = op_root / "baseline.json"
        if baseline_log.exists():
            baseline_result = json.loads(baseline_log.read_text())
        else:
            baseline_result = check_fn(baseline_repo, op_root / "baseline.log", baseline=True)
            baseline_log.write_text(json.dumps(baseline_result))
        if baseline_result["status"] not in {"passed", "no_tests"}:
            raise ValueError("Baseline check unavailable or failing")
        if not workspace.exists():
            git(baseline_repo, "clone", "--no-hardlinks", "--no-checkout", str(baseline_repo), str(workspace))
            git(workspace, "-c", "core.autocrlf=false", "checkout", "--detach", manifest["parent_commit"])
        changed = workspace / changed_path
        if not changed.exists() or changed.read_bytes() != content:
            if op["state"] != "PREPARED" or git(workspace, "status", "--porcelain").strip():
                raise ValueError("Ambiguous workspace; no retry application")
            if validate_fn(directory) != manifest:
                raise ValueError("Candidate changed before application")
            git(workspace, "apply", "--whitespace=error", "-", data=patch)
        post_tree = reconcile_fn(workspace, manifest, content)
        if op["post_tree"] and op["post_tree"] != post_tree:
            raise ValueError("Applied tree mismatch")
        ledger.update(op["id"], "APPLIED", post_tree=post_tree)
        candidate_result = check_fn(workspace, op_root / "candidate.log")
        if reconcile_fn(workspace, manifest, content) != post_tree:
            raise ValueError("Workspace changed during validation")
        status = "VERIFIED" if candidate_result["status"] == "passed" else "FAILED"
        result = {"baseline": baseline_result, "candidate": candidate_result,
                  "post_tree": post_tree, "patch_sha256": manifest["patch_sha256"]}
        ledger.update(op["id"], status, result, post_tree)
        if status == "FAILED":
            workspace.rename(quarantine)
        return {"operation_id": op["id"], "state": status, "evidence": result}
    except BaseException as error:
        state = "CANCELLED" if isinstance(error, KeyboardInterrupt) else "AMBIGUOUS"
        ledger.update(op["id"], state, {"error_type": type(error).__name__})
        if workspace.exists():
            workspace.rename(quarantine)
        raise


class State(TypedDict, total=False):
    candidate: dict
    approval_id: str
    outcome: dict


def graph_for(directory, saver, ledger, actor, *, execute_fn=None):
    execute_fn = execute_fn or execute
    def gate(state):
        approval = interrupt({"candidate": state["candidate"], "execution_available": True})
        return {"approval_id": approval}

    def apply_and_verify(state):
        if state["candidate"] != json.loads((directory / "manifest.json").read_text()):
            raise ValueError("Checkpoint/candidate mismatch")
        return {"outcome": execute_fn(directory, state["candidate"], ledger, state["approval_id"], actor)}

    builder = StateGraph(State)
    builder.add_node("gate", gate)
    builder.add_node("execute", apply_and_verify)
    builder.add_edge(START, "gate")
    builder.add_edge("gate", "execute")
    builder.add_edge("execute", END)
    return builder.compile(checkpointer=saver)


def prepare(original=None, *, replacement=False):
    original = original or ROOT / "artifacts/first-patch/candidate-c2a7ed975417"
    from proposal_checks import validate_collection_examples
    literal_checks = validate_collection_examples(patch_content((original / 'candidate.patch').read_bytes()).decode('utf-8'))
    preflight()  # Leave a reusable proposal if Docker is unavailable.
    manifest = json.loads((original / "manifest.json").read_text())
    manifest.setdefault('checks', {})['literal_examples'] = literal_checks
    directory = original.with_name(original.name + ("-exec-" + uuid.uuid4().hex[:8] if replacement else "-exec-v1"))
    if directory.exists():
        raise ValueError("Execution candidate already exists; use review")
    manifest.update(candidate_id=directory.name, run_id=directory.name,
        policy=POLICY, policy_sha256=digest(POLICY), new_file_sha256=digest(patch_content((original / "candidate.patch").read_bytes())))
    directory.mkdir()
    (directory / "candidate.patch").write_bytes((original / "candidate.patch").read_bytes())
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=2))
    validate(directory)
    preflight()
    ledger = Ledger(directory / "ledger.sqlite")
    with SqliteSaver.from_conn_string(str(directory / "checkpoint.sqlite")) as saver:
        graph_for(directory, saver, ledger, "not-yet-approved").invoke(
            {"candidate": manifest}, {"configurable": {"thread_id": manifest["run_id"]}})
    ledger.db.close()
    print("Prepared pending candidate:", directory.name)
    return directory


def review(directory, *, validate_fn=None, execute_fn=None):
    validate_fn = validate_fn or validate
    if not sys.stdin.isatty():
        raise ValueError("Use the local interactive terminal; no piped approvals")
    actor = getpass.getuser()
    with run_lock(directory), SqliteSaver.from_conn_string(str(directory / "checkpoint.sqlite")) as saver:
        manifest = validate_fn(directory)
        preflight()
        ledger = Ledger(directory / "ledger.sqlite")
        try:
            graph = graph_for(directory, saver, ledger, actor, execute_fn=execute_fn)
            config = {"configurable": {"thread_id": manifest["run_id"]}}
            state = graph.get_state(config)
            if state.values.get("candidate") != manifest:
                raise ValueError("Checkpoint/candidate mismatch")
            if state.values.get("outcome"):
                print(json.dumps(state.values["outcome"], indent=2)); return
            if state.next == ("execute",):
                print("Recovering the existing approved operation; no new approval or patch application.")
                graph.invoke(None, config)
                print(json.dumps(graph.get_state(config).values["outcome"], indent=2)); return
            if state.next != ("gate",):
                raise ValueError("Run is not awaiting a decision")
            prior = ledger.db.execute("SELECT decision FROM decisions WHERE binding=? ORDER BY rowid DESC LIMIT 1",
                                      (binding(manifest),)).fetchone()
            if prior and prior["decision"] in {"reject", "redirect", "cancel"}:
                raise ValueError("Prior rejection, redirection or cancellation requires a new candidate")
            print("\nREVIEW LEDGER - HUMAN PATCH DECISION\n")
            print("Operator:", actor, "| Candidate:", manifest["candidate_id"])
            print("Coverage: security, performance, style, test-gap reviews complete (saved evidence).")
            print("Step:", manifest["step_id"], "| Plan version:", manifest["plan_version"])
            print("Parent commit:", manifest["parent_commit"], "\nParent tree:", manifest["parent_tree_hash"])
            print("Patch SHA256:", manifest["patch_sha256"])
            print(manifest.get("risk_summary", "Risk: low test-only change. Intended behavior delta: none."))
            print("Rationale:", manifest["rationale"])
            print("Other plan conflicts remain; this selected action has no blocking conflict.")
            print(manifest.get("acceptance_summary", "Acceptance: >=7 unittest tests pass, no failures/errors/skips, in pinned offline non-root Docker."))
            print("No host mounts or credentials. 128MiB / 0.5 CPU / 32 processes / 30 seconds per check.")
            print("Evidence:", directory / "manifest.json")
            print("\nEXACT DIFF\n" + (directory / "candidate.patch").read_text())
            print("Approve applies ONLY this patch in a disposable workspace and runs isolated tests.")
            print("Baseline and your project checkout stay unchanged. Approval is single use, valid 30 minutes.")
            print("Choices: approve " + manifest["patch_sha256"][:12] + " | reject | redirect | defer | cancel")
            choice = input("Your decision: ").strip()
            expected = "approve " + manifest["patch_sha256"][:12]
            decision = "approve" if choice == expected else choice
            if decision not in {"approve", "reject", "redirect", "defer", "cancel"} or choice == "approve":
                raise ValueError("Decision not recognized; nothing approved")
            comment = input("New constraints: ").strip() if decision == "redirect" else ""
            if decision == "redirect" and not comment:
                raise ValueError("Redirect requires constraints")
            # Recheck after human waiting; snapshot/plan/policy may have changed.
            if validate_fn(directory) != manifest:
                raise ValueError("Candidate changed while waiting")
            decision_id = ledger.decision(manifest, actor, decision, comment)
            if decision != "approve":
                print("Recorded:", decision, "- no patch applied.")
                return
            graph.invoke(Command(resume=decision_id), config)
            print(json.dumps(graph.get_state(config).values["outcome"], indent=2))
            print("Evidence directory:", directory)
        finally:
            ledger.db.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare", "review"])
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
    else:
        review(ROOT / "artifacts/first-patch/candidate-c2a7ed975417-exec-v1")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Stopped safely:", type(error).__name__, str(error)[:300])
        raise SystemExit(1)
