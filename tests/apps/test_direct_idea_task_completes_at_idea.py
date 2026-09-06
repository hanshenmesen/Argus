"""A direct ideation task completes at the idea stage; it never marches into experiment.

idea-01 (s-0b1c7fa1, 2026-09-04) was an "identify and select one research idea"
objective routed as a direct research task. Its Reviewer accepted the ideation
package, the Manager advanced idea -> experiment -> paper on that verdict, and
the campaign then spent twelve missions re-running the same ideation objective
while the Manager held Paper for a manuscript nobody had asked for. The direct
completion path now closes the objective where its deliverable lives.
"""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from argus_skill.apps._runtime_stage_transition import StageTransitionMixin
from argus_skill.core.models import ReviewDecision
from argus_skill.core.pipeline_state import read_pipeline_state
from argus_skill.manager import Manager
from argus_skill.skills.vertical_select import persist_vertical


class _Sink:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def handle_event(self, event: dict) -> None:
        self.events.append(event)


def test_direct_ideation_verdict_completes_the_idea_stage(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    workdir = tmp_path / "worktree"
    workdir.mkdir()
    persist_vertical(
        state_root,
        "research",
        workflow_mode="direct",
        research_target_level="exploratory",
    )
    assert read_pipeline_state(state_root).get("current_stage") == "idea"

    runtime = SimpleNamespace(
        manager=Manager(project_root=state_root, execution_workdir=workdir, runner=object()),
        _artifact_root=state_root,
        _manager_session_root=state_root,
    )
    review = ReviewDecision(
        status="done",
        reason="The ideation package passes independent review; the selected direction is precise.",
        next_action="",
        research_result={
            "result_class": "new_candidate",
            "correctness_status": "verified",
            "novelty_status": "unverified",
            "significance_status": "unverified",
            "statement_fidelity_status": "passed",
            "evidence": ["research/candidates.md"],
        },
    )
    decision = StageTransitionMixin._decide_stage_transition(
        runtime,
        rounds_list=[SimpleNamespace(review=review)],
        workdir=workdir,
        sink=_Sink(),
        root_task_id="idea-direct",
        mission_scope="bounded",
        stage_closing=True,
    )

    assert decision["action"] == "complete"
    assert decision["target_stage"] == "idea"
    state = read_pipeline_state(state_root)
    assert state["current_stage"] == "idea"
    assert state["current_verdict"] == "certified"
