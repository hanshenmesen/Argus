# Argus Memory Design

Argus memory is a layered, file-backed system that turns execution into resumable state and reusable knowledge.

## Memory Layout

```text
Operator memory   — what the operator wants and permits
Curated memory    — what later work should reuse
Working memory    — where current work stands
Execution memory  — what happened
```

**Execution memory** is the project’s observable event history: lifecycle events, selected progress, role outputs, verdicts, costs, and provider I/O when enabled (`life/event_log.py`). Hidden provider reasoning is unavailable. In the default `signal` mode, Argus retains selected high-value events rather than every progress message.

**Working memory** is the resumable state of projects and missions: backlog, frontier, checkpoint, reviewed handoffs, and role-session capsules (`life/context_packet.py`, `core/role_session.py`). It lets a later role continue from the current frontier without replaying the full trajectory.

**Curated memory** is knowledge selected for reuse: Wiki pages hold declarative project knowledge, Skills hold procedures, and failure-experience capsules preserve verified lessons from unsuccessful missions (`wiki/store.py`, `skills/layered.py`, `life/failure_experience.py`). Its scope may be project, vertical, or shared profile.

**Operator memory** stores directives, preferences, capabilities, and revocations in OperatorContext (`core/operator_context.py`). Each store writes under the root supplied by its caller, which may be a project state directory or the shared global root. Mission/project/global labels control projection and precedence; they do not copy records between stores. Mission preludes using `MemoryBundle.root` read the shared global-root store (`life/memory.py`, `life/supervisor/_mission_execution_runtime.py`), so operator memory is not necessarily project-local.

## How Memory Is Produced

```text
execution
  → observable events
  → frontier, checkpoint, and handoffs
  → post-mission curation
  → retrieval by later roles
```

While roles work, Argus records observable events. At execution boundaries, it compresses current state into the frontier, checkpoint, handoffs, and role capsules. After settlement, stable facts can enter the Wiki, reusable procedures can enter Skills, and verified failures can become failure experience. Later roles retrieve each layer according to project, mission, role, and authority.


The original layout reference is `lbx154/Argus` commit `ae2daa1fbc2c918b4e7126151fe55eb68fd0cb98`; the OperatorContext storage-root description was checked against main on 2026-09-06.
