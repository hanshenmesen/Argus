"""Research-owned role prompts and explicit stage context loading."""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path

from .library_preparation import STAGE_PLAYBOOK_PATHS

_HANDOFF_STAGES = frozenset({"idea", "experiment", "paper"})
_CONTEXT_CHAR_LIMIT = 32_000

# Stages whose work actually touches compute: sizing an idea, then building
# and running experiments. Paper/review prose does not need it.
_COMPUTE_STAGES = frozenset({"idea", "experiment"})
_HARDWARE_CACHE_SECONDS = 60.0
_hardware_cache: tuple[float, str] | None = None


def _query_local_gpus() -> list[str]:
    if shutil.which("nvidia-smi") is None:
        return []
    try:
        proc = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=index,name,memory.total,memory.used",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    lines: list[str] = []
    for row in proc.stdout.strip().splitlines():
        parts = [part.strip() for part in row.split(",")]
        if len(parts) != 4:
            continue
        index, name, total_mib, used_mib = parts
        try:
            total_gb = int(total_mib) / 1024
            used_gb = int(used_mib) / 1024
        except ValueError:
            continue
        lines.append(
            f"- GPU {index}: {name}, {total_gb:.0f} GB memory "
            f"({used_gb:.0f} GB currently in use)"
        )
    return lines


def local_hardware_block() -> str:
    """Describe the compute this machine actually has, so ideas and
    experiments are sized to it.

    Purely informational — it never blocks anything. Cached briefly so prompt
    rendering does not shell out on every turn; fail-soft to an empty string
    on machines without GPUs or without ``nvidia-smi``.
    """
    global _hardware_cache
    now = time.monotonic()
    if _hardware_cache is not None and now - _hardware_cache[0] < _HARDWARE_CACHE_SECONDS:
        return _hardware_cache[1]
    gpu_lines = _query_local_gpus()
    if not gpu_lines:
        _hardware_cache = (now, "")
        return ""
    cpu_count = os.cpu_count() or 0
    cpu_line = f"- {cpu_count} CPU cores" if cpu_count else ""
    block = (
        "## Compute available on this machine\n"
        + "\n".join(line for line in (*gpu_lines, cpu_line) if line)
        + "\n\n"
        "Experiments run locally on this hardware. Size the work to it rather "
        "than assuming a small machine: real training and evaluation runs on "
        "these GPUs are expected, several GPUs can be used at once when a run "
        "benefits, and batch sizes, model scale, and evaluation sets should "
        "use the memory that is actually free. Prefer the GPUs with the most "
        "free memory and leave others' running jobs undisturbed."
    )
    _hardware_cache = (now, block)
    return block


def _hardware_block_for_stage(stage: str) -> str:
    return local_hardware_block() if stage in _COMPUTE_STAGES else ""


def active_context_paths(stage: str) -> tuple[str, ...]:
    """Return the only normal cross-stage context path for ``stage``."""
    normalized = str(stage or "").strip().lower()
    if normalized in _HANDOFF_STAGES:
        return ("HANDOFF.md",)
    if normalized == "review":
        return ("paper/REVIEW.md",)
    return ()


def _stage_playbook_block(stage: str) -> str:
    playbook = STAGE_PLAYBOOK_PATHS.get(stage)
    if not playbook:
        return ""
    resolved = Path(__file__).resolve().parent / "skills" / playbook
    return (
        "## Authoritative stage playbook\n"
        f"Playbook: `{playbook}`. Open `{resolved}` before acting. It is "
        f"the single workflow playbook for `{stage}`. Other Skills are optional "
        "tools: they cannot redefine the stage, its completion bar, the handoff, or "
        "project-visible artifacts."
    )


def active_research_context(stage: str, project_root: Path | None) -> str:
    if project_root is None:
        return ""
    paths = active_context_paths(stage)
    if not paths:
        return ""
    relative = paths[0]
    path = Path(project_root) / relative
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        text = ""
    if not text.strip():
        return (
            "## Active research context\n"
            f"The only normal cross-stage context for `{stage}` is `{relative}`, "
            "and it is currently absent or empty. Do not substitute historical "
            "research files or search the project for an older handoff."
        )
    if len(text) > _CONTEXT_CHAR_LIMIT:
        text = text[:_CONTEXT_CHAR_LIMIT].rstrip() + "\n[context truncated]"
    return (
        "## Active research context\n"
        f"Loaded only from `{relative}`:\n\n{text.strip()}\n\n"
        "Treat this as the current upstream summary, not as permission to crawl "
        "historical artifacts. Open an older file only if this document explicitly "
        "names it for a concrete dispute."
    )


def academic_paper_review_block() -> str:
    return (
        "## Integrated final paper review\n"
        "Act as the independent post-repair Reviewer required by the Review playbook. "
        "Judge the current complete paper rather than Engineer or Planner confidence. "
        "Follow direct claim-critical references to executed code, explicit "
        "configuration, raw rows, the real evaluator, positive controls, strong "
        "same-information baselines, citations, "
        "and primary sources. Use the host's current independent page-by-page and cold-read "
        "assessments when supplied; do not launch duplicate passes or repeat their whole-paper "
        "inspection. Resolve a concrete contradiction with a targeted check. When no current "
        "assessment is supplied, inspect every rendered page, figure, and table at publication "
        "size. Report scientific correctness and importance, rendered layout, visual "
        "quality, academic argument and language, and venue compliance. Do not load "
        "HANDOFF.md or recursively crawl old reports or history. Put all three results "
        "inside the verdict's `REASON=` value as "
        "`Scientific: ... | Visual: ... | Language: ...`; do not leave them only in prose "
        "before the verdict. Do not edit files or change stage state. Never reopen "
        "selection or move backward. "
        + paper_reviewer_standard()
        + " For each required "
        "narrative repair, identify its location, the concrete obstacle to understanding "
        "or inference, and the smallest repair goal. Calling prose report-like, "
        "unacademic, or less fluent is insufficient by itself. Close resolved findings; "
        "request another revision only for a remaining or newly introduced defect."
    )


def paper_writing_standard() -> str:
    """The one writing standard every paper-facing prompt shares.

    It deliberately fixes no quota. The selected venue's strong accepted papers
    are the reference, and the claim decides how long, how numerical, and how
    hedged each passage should be.
    """
    return (
        "The standard is a strong accepted paper at the selected venue, the kind the "
        "exemplar skill has you read; there is no house quota for sentences, words, "
        "numbers, or caption format. Let the claim decide the form. The abstract is as "
        "long and as numerical as the venue's norm and the claim require: a large "
        "speedup is stated as a speedup, a narrow margin is stated with its "
        "uncertainty, and a mechanism finding may need no number at all. In prose, "
        "give a number the precision the comparison needs, usually two or three "
        "significant digits, and keep full precision in tables; a paragraph that has "
        "become a list of numbers has stopped arguing. A caption tells the reader what "
        "to see: a number when the number is the point, a pattern when the pattern is "
        "the point. Say plainly what the evidence establishes, state each limit once "
        "where it matters, and hedge a sentence only when the evidence for that "
        "sentence is uncertain. Think in evidence roles (headline, mechanism, control, "
        "scope, completeness) while deciding what goes where, but those words, and "
        "every workflow word such as bounded, certified, gate, artifact, mission, "
        "round, handoff, validator, or audit, never appear in the manuscript. A clear "
        "thesis that a method helps only under identified conditions, or that an "
        "expected effect does not hold, is a legitimate paper when its evidence is as "
        "complete as a positive result would need; what is not allowed is presenting "
        "unfinished development as a finding."
    )


def paper_reviewer_standard() -> str:
    """How the Reviewer applies the writing standard: as a venue reviewer, not a checker."""
    return (
        "Judge the writing as a reviewer at the selected venue would: would this be "
        "accepted, and what would a careful reader object to? Do not enforce an "
        "abstract length, sentence count, number density, or caption format; a longer "
        "or shorter abstract, more or fewer numbers, and a headline figure that recurs "
        "across sections are all fine when they serve the argument at that venue. "
        "Object when a claim outruns its evidence, when a reader cannot recover the "
        "central finding, when a number's meaning is unclear from its context, when "
        "prose recites a result matrix instead of arguing, when hedging or limitation "
        "lists stand in for a clear statement, or when internal workflow vocabulary "
        "appears. Do not ask for more hedging than the evidence requires, and do not "
        "ask for a number where a plain statement is clearer."
    )


def _paper_narrative_packaging_block() -> str:
    return (
        "## Paper writing standard\n"
        + paper_writing_standard()
        + " Keep the complete scientific evidence: complete definitions and matrices "
        "live in Methods, tables, or the Appendix, and prose selects the comparisons "
        "that change the current inference and explains why. A headline number may "
        "recur in the abstract, introduction, results, caption, and conclusion when it "
        "does each location's job; do not copy a flat method-by-dataset-by-metric "
        "recital across sections. Translate any gate, validator, artifact-status, or "
        "evidence-chain language into the scientific question, the result, the "
        "alternative explanation resolved, and the resulting inference."
    )


def _planner_fragment(stage: str, project_root: Path | None) -> str:
    return "\n\n".join(
        block
        for block in (
            _stage_playbook_block(stage),
            active_research_context(stage, project_root),
            _hardware_block_for_stage(stage),
            (
                "## Planner responsibility\n"
                f"Plan only the highest-value unresolved work in `{stage or '(unknown)'}` "
                "under the stage playbook. Keep repairs in the current stage, avoid "
                "ceremonial tasks, and leave stage transitions to Manager."
            ),
        )
        if block
    )


def _narrative_editor_block() -> str:
    return (
        "## Fresh-context Narrative Editor\n"
        "Keep the current manuscript as the starting point. Inspect it and the latest "
        "actionable Reviewer findings supplied for this round; edit only a located "
        "problem that impairs reader understanding or the argument. Use the current "
        "paper, `HANDOFF.md` evidence roles, and the venue drafting contract. Do not "
        "search review history or internal diagnostic reports, or copy reviewer-response "
        "wording into the manuscript. Preserve clear content, structure, and wording. "
        "Prefer adding a missing explanation or adjusting local sentence order; explain "
        "why a local repair is insufficient before reorganizing a section or the paper. "
        "If no concrete problem needs repair, report that no manuscript change is needed "
        "and return to Reviewer without editing. Preserve every number, comparison "
        "direction, claim scope, adverse result, material uncertainty, decisive control, "
        "and the complete method/result coverage. Within the affected passage, clarify "
        "what the evidence establishes using only supported inferences; keep other "
        "evidence in its existing carrier. "
        "You may propose moving unique content in your final handoff, but you may not "
        "unilaterally remove it or change its scientific meaning. Keep the abstract's "
        "claims and evidence; its length and shape follow the venue and the claim, not a "
        "quota. Compile when "
        "manuscript inputs changed or the rendered PDF is missing or stale; reuse a "
        "current PDF when no input changed."
    )


def _engineer_fragment(
    stage: str,
    project_root: Path | None,
    operation: str,
) -> str:
    narrative_edit = operation == "narrative_edit"
    # HANDOFF supplies evidence roles; current repair feedback arrives through
    # the normal round context. Do not preload REVIEW.md or historical reports.
    context = active_research_context(
        "paper" if narrative_edit else stage,
        project_root,
    )
    stage_policy = (
        "## Engineer responsibility\n"
        "Execute the current playbook directly. Use code, explicit configuration, raw "
        "outputs, figures, bibliography, manuscript source, and rendered output as work "
        "products. Do not create substitute handoffs or process reports, and do not "
        "change stage state. The host runs independent preliminary paper reviews after your "
        "turn; do not spawn a second scientific, visual, or cold-read review team."
    )
    narrative_packaging = (
        _paper_narrative_packaging_block()
        if stage == "paper" or narrative_edit
        else ""
    )
    return "\n\n".join(
        block
        for block in (
            _stage_playbook_block(stage),
            context,
            _hardware_block_for_stage(stage),
            narrative_packaging,
            (
                "## On-demand method figure\n"
                "Only when a method pipeline needs drawing, open "
                "engineer/research-svg-pipeline.md and use "
                "python -m argus_skill.verticals.research.pipeline_figure. "
                "Reuse an existing suitable figure; do not invoke the component every "
                "round or for prose-only edits. The current Engineer designs the SVG "
                "from code and manuscript; no separate model call is needed. Include "
                "the vector PDF after the Introduction, targeting page 2 or 3 in the "
                "compiled paper, and keep the editable SVG source."
                if stage == "paper" and not narrative_edit else ""
            ),
            _narrative_editor_block() if narrative_edit else "",
            stage_policy,
        )
        if block
    )


def _reviewer_fragment(
    stage: str,
    scope: str,
    project_root: Path | None,
    operation: str,
) -> str:
    if operation == "cold_read":
        return (
            "## Rendered-PDF cold read\n"
            "Read only `paper/main.pdf` in the isolated working directory. Do not "
            "look for TeX, HANDOFF, REVIEW.md, code, evidence files, history, or "
            "internal diagnostics. Judge whether the PDF makes one central finding "
            "recoverable after the first page; whether sections advance rather than "
            "replay a flat matrix; whether headline, mechanism, control, scope, and "
            "completeness evidence have visible hierarchy; whether the scientific meaning "
            "of key comparisons is clear from the passage and necessary context; and "
            "whether figures and numerical captions "
            "answer a scientific question rather than resemble a dashboard. "
            + paper_reviewer_standard()
            + " Dense science and complete controls are not defects by themselves. "
            "Do not demand another explanation after "
            "each number when the context already supplies it. For each required repair, "
            "return a PDF location, a concrete obstacle to understanding or inference, "
            "and the smallest repair goal. A report-like tone or a preference for "
            "smoother wording alone is insufficient. Pass when no substantive "
            "reader-facing defect remains."
        )
    if operation == "science_loss_check":
        return (
            "## Scientific semantic-loss comparison\n"
            "Compare the immutable before/after manuscript snapshots named in the "
            "assignment. Judge scientific meaning and coverage, not sentence identity. "
            "Verify headline evidence, exact values and directions, claims and scope, "
            "complete methods/baselines/controls/result matrices, adverse or null "
            "findings, uncertainty, reproduction detail, the abstract's claims and "
            "evidence, and what each caption tells the reader. A move from prose to "
            "a clear table, Methods, Appendix, caption, or cross-reference is not loss. "
            "Any veto must name the exact lost reasoning step or its missing carrier. "
            "Do not edit either snapshot."
        )
    if stage == "review" or scope == "final_submission":
        policy = academic_paper_review_block()
    else:
        policy = (
            "## Reviewer responsibility\n"
            "Independently judge the current work against the stage playbook and direct "
            "evidence. Separate implementation defects from scientific evidence, name "
            "the smallest decisive repair, and do not change stage state."
        )
    return "\n\n".join(
        block
        # Live HANDOFF/REVIEW contents belong to the Reviewer's round delta, not
        # this static policy fragment used to decide whether a session resumes.
        for block in (_stage_playbook_block(stage), policy)
        if block
    )


def render_role_prompt_fragment(
    *,
    role: str,
    operation: str,
    stage: str,
    scope: str,
    project_root: Path | None,
) -> str:
    """Render only policy owned by the Research vertical."""
    normalized_role = str(role or "").strip().lower()
    normalized_operation = str(operation or "").strip().lower()
    normalized_stage = str(stage or "").strip().lower()
    normalized_scope = str(scope or "").strip().lower().replace("-", "_")
    if normalized_role == "planner":
        return _planner_fragment(normalized_stage, project_root)
    if normalized_role == "engineer":
        return _engineer_fragment(
            normalized_stage,
            project_root,
            normalized_operation,
        )
    if normalized_role == "reviewer":
        return _reviewer_fragment(
            normalized_stage,
            normalized_scope,
            project_root,
            normalized_operation,
        )
    if normalized_role == "manager":
        return (
            _stage_playbook_block(normalized_stage)
            + "\n\n"
            + active_research_context(normalized_stage, project_root)
            + "\n\n## Forward-only stage authority\n"
            "Research stages never roll back. Hold the current stage and schedule "
            "repairs there, or advance when its checklist is satisfied."
        ).strip()
    return ""


__all__ = [
    "academic_paper_review_block",
    "paper_reviewer_standard",
    "paper_writing_standard",
    "active_research_context",
    "active_context_paths",
    "local_hardware_block",
    "render_role_prompt_fragment",
    "STAGE_PLAYBOOK_PATHS",
]
