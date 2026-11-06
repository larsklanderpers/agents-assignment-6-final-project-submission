"""Bounded persistence experiment; no repository changes or model calls.

Uses the documented LangGraph interrupt/resume pattern:
https://docs.langchain.com/oss/python/langgraph/interrupts
This experiment records a decision only; it does not authorize patch execution.
"""
import argparse
import asyncio
import json
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from spike_adapter import run_fixture_review


class State(TypedDict, total=False):
    candidate: str
    decision: str
    reviews: dict


def analyze(state: State) -> State:
    return {"reviews": asyncio.run(run_fixture_review())}


def gate(state: State) -> State:
    decision = interrupt({"candidate": state["candidate"], "experiment_only": True})
    if decision not in {"approve", "reject"}:
        raise ValueError("Unsupported decision")
    return {"decision": decision}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "resume", "inspect"])
    parser.add_argument("--db", required=True)
    parser.add_argument("--run", default="persistence-spike")
    args = parser.parse_args()
    builder = StateGraph(State)
    builder.add_node("analyze", analyze)
    builder.add_node("gate", gate)
    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", "gate")
    builder.add_edge("gate", END)
    with SqliteSaver.from_conn_string(args.db) as saver:
        graph = builder.compile(checkpointer=saver)
        config = {"configurable": {"thread_id": args.run}}
        if args.action == "start":
            if graph.get_state(config).values:
                raise ValueError("Run already exists; use inspect or resume")
            graph.invoke({"candidate": "fixture-only-no-executable-patch"}, config)
        elif args.action == "resume":
            snapshot = graph.get_state(config)
            if snapshot.next != ("gate",):
                raise ValueError("No pending gate")
            graph.invoke(Command(resume="reject"), config)
        snapshot = graph.get_state(config)
        print(json.dumps({"values": snapshot.values, "next": list(snapshot.next)}))


if __name__ == "__main__":
    main()
