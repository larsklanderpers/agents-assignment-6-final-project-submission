"""Offline ADK adapter experiment with deterministic fixture agents.

These are transport test doubles, not model-backed code reviewers. Workflow API:
https://adk.dev/agents/workflow-agents/parallel-agents/
"""
import asyncio
import json
import time
from typing import Literal

from google.adk.agents import BaseAgent, ParallelAgent
from google.adk.events import Event
from google.adk.runners import InMemoryRunner
from google.genai import types
from pydantic import BaseModel, ConfigDict


ROLES = ("security", "performance", "style", "test_gap")


class Review(BaseModel):
    model_config = ConfigDict(extra="forbid")
    agent_id: Literal["security", "performance", "style", "test_gap"]
    status: Literal["complete"]
    fixture_only: Literal[True]
    findings: list[str]
    started: float
    ended: float


class FixtureReviewer(BaseAgent):
    async def _run_async_impl(self, ctx):
        started = time.monotonic()
        await asyncio.sleep(0.05)
        result = Review(agent_id=self.name, status="complete", fixture_only=True,
                        findings=[], started=started, ended=time.monotonic())
        yield Event(author=self.name, content=types.Content(
            role="model", parts=[types.Part(text=result.model_dump_json())]))


async def run_fixture_review() -> dict:
    parallel = ParallelAgent(name="fixture_review", sub_agents=[
        FixtureReviewer(name=role) for role in ROLES])
    runner = InMemoryRunner(agent=parallel, app_name="ledger_spike")
    session = await runner.session_service.create_session(
        app_name="ledger_spike", user_id="fixture_operator")
    results = {}
    try:
        async for event in runner.run_async(
            user_id="fixture_operator", session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text="Transport fixture only")]),
        ):
            if event.author not in ROLES or not event.content:
                continue
            body = "".join(part.text or "" for part in event.content.parts or [])
            if not body:
                continue
            review = Review.model_validate_json(body)
            if review.agent_id != event.author or event.author in results:
                raise ValueError("Duplicate or mismatched specialist identity")
            results[event.author] = review.model_dump()
        if set(results) != set(ROLES):
            raise ValueError("Missing specialist result")
        # Concurrent branches must share a real interval, not merely finish fast.
        if max(r["started"] for r in results.values()) >= min(r["ended"] for r in results.values()):
            raise ValueError("Specialist execution did not overlap")
        return {role: results[role] for role in ROLES}
    finally:
        await runner.close()


if __name__ == "__main__":
    print(json.dumps(asyncio.run(run_fixture_review()), indent=2))
