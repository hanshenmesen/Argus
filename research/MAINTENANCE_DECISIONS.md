# Maintenance decisions

## mission-view-label-fix

- **keep** — `argus_skill/core/mission_view/_reduce_manager.py:113` fallback chain for `life.manager.stage_decision`.
  - Audit category: `fallback_chain`.
  - Evidence: the live task concerns `life.manager.intent.failed`; the flagged chain belongs to stage-decision projection and preserves compatibility with existing structured event fields (`target_stage`, `stage`, `current_stage`). It is not on the failed-intent label path and changing it would exceed this bounded reducer-label increment.
- **simplify** — `life.manager.intent.failed` label projection in `argus_skill/core/mission_view/_reduce_manager.py`.
  - Evidence: no audit heuristic matched this branch, but the reducer previously reused grounding wording for a Manager intent/routing failure. The branch now uses one explicit title for the role, timeline, and role-work projections, avoiding divergent labels for the same public event.
