# ARGUS-P1-02 / P1-03 controlled live experiment

Date: 2026-08-07
Primary matrix baseline: `bc553f04`
Session follow-up fix: `c7f44522`
Skill follow-up fix: `8100d2ae`
Backend/model: Pi 0.84.1 via GitHub Copilot, `gpt-5-mini`, low reasoning
Runs: 20 primary + 17 diagnostic/follow-up real provider runs, all sequential

## Method

Two small Python repositories were generated from identical frozen baselines per run:

- strict scalar/iterable normalization;
- ordered case-insensitive header merging.

The session experiment used a required three-round protocol so every policy had the
same intended work: repository map, first bounded repair, final repair. Each policy
ran both tasks twice (`n=4` per policy). Success required both Reviewer `done` and an
external held-out evaluator, not only visible tests.

The Skill experiment used one-turn tasks with incomplete visible tests. The relevant
condition exposed one high-fit Engineer Skill plus one unrelated SQL Skill. The
control exposed only the unrelated Skill. Each condition ran both tasks twice
(`n=4`). Raw provider/tool traces were used to count actual Skill reads and repeated
repository reads.

## P1-02 results

| Policy | Runs | Reviewer done | Held-out pass | Joint success | Mean wall time | Mean explicit prompt estimate | Mean repeated repo reads | Mean Engineer repeated reads | Mean provider cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fresh | 4 | 3/4 | 3/4 | 2/4 | 185.9 s | 13,434 tok | 7.75 | 4.75 | $0.02860 |
| mission | 4 | 4/4 | 4/4 | 4/4 | 158.8 s | 8,934 tok | 4.50 | 0.50 | $0.02993 |
| rolling (rotate after 2 turns) | 4 | 2/4 | 2/4 | 1/4 | 161.3 s | 10,173 tok | 4.25 | 2.00 | $0.02558 |

Compared with `fresh`, mission-scoped sessions produced:

- 14.6% lower wall time;
- 33.5% lower explicit prompt estimate;
- 41.9% fewer repeated repository reads;
- 89.5% fewer repeated Engineer reads;
- higher joint success in this sample (4/4 versus 2/4).

The trade-off was 43.8% more provider-reported input tokens and 4.7% higher cost,
mostly from the retained/cached conversation context. Prompt reduction therefore did
not translate into lower total provider input. The two-turn rolling boundary was not
safe: rotation caused stale-stage confusion in observed runs and joint success fell
to 1/4.

**Initial decision:** keep production default unchanged and advance `mission` to a
larger real-project canary. The original rolling policy (`max_turns=2`) was not
shippable. Follow-up diagnosis found that rotated Engineer/Reviewer sessions could
restart an earlier stage, write a relative duplicate checkpoint, or omit the exact
`STATUS` line despite a usable natural verdict. `c7f44522` now sends full static
context plus an explicit current-round/approval handoff on rotation, requires the
canonical absolute checkpoint path, and tolerantly reads a natural `Verdict:` label.
One post-fix run on each task passed both Reviewer and held-out checks (2/2). This is
a repair smoke test, not enough evidence to change the production default or replace
the original table.

## P1-03 results

| Condition | Runs | Reviewer done | Held-out pass | Useful Skill opened | Wrong Skill opened | Mean wall time | Mean explicit prompt estimate | Mean provider cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unrelated-only control | 4 | 4/4 | 0/4 | 0/4 | 0/4 | 63.6 s | 4,767 tok | $0.01034 |
| relevant + unrelated | 4 | 4/4 | 4/4 | 4/4 | 1/4 | 81.3 s | 4,859 tok | $0.01228 |

The relevant Skill body was actually read in every treatment run; this was not a
prompt-only exposure. The four treatment runs read 3,794 useful Skill bytes in total.
One run also opened the 294-byte unrelated SQL Skill, so false reuse was non-zero
(1/4). Control agents did not open the unrelated Skill, yet every control Reviewer
returned `done`; all four then failed held-out checks. This demonstrates both a real
quality gain from on-demand Skill use and a gap in Reviewer acceptance when visible
tests are incomplete.

Treatment overhead versus control was:

- 27.8% higher wall time;
- 1.9% higher explicit prompt estimate;
- 18.8% higher provider cost;
- 62.6% higher provider-reported input tokens, almost entirely cached context
  (uncached input increased only 2.5%).

An additional best-case oracle baseline injected the one known-relevant Skill body
without charging matcher/selection cost (`n=4`). It also passed held-out checks 4/4
and averaged 73.4 s, 4,796 explicit prompt tokens, and $0.01156. The initial
explicitly-cued on-demand condition was 10.8% slower, used 1.3% more explicit prompt,
18.8% more provider input, and cost 6.2% more than this oracle injection. The extra
read/tool inference erased progressive-disclosure savings for these ~1 KiB Skills.
The oracle baseline is intentionally favorable and is not implementable without
selection knowledge.

More importantly, two natural-incidence follow-ups removed the explicit instruction
to inspect Skills. The useful body was opened 0/2 and held-out checks passed 0/2,
even though native paths and high-fit descriptions were available. This means the
current coding-agent-native contract supports on-demand use but does not reliably
trigger it on this model. A stronger compact discovery instruction removed the one
observed adjacent false read in a single verification run, but did not fix natural
invocation.

**Revised decision:** retain the implementation behind its current default, but do
not mark P1-03 complete. Prompt-cost and natural-use acceptance are not met.
`8100d2ae` now requires the coding agent to make one native description relevance
decision before its first repository tool, opens only clearly matching bodies, and
omits empty general roots from the native loader. This is an agent-owned decision,
not a harness matcher. Per operator direction, no further model experiment was run;
behavior will be observed in normal missions. A fair future comparison must include
selection cost in the injection baseline.

## Limitations

- One backend/model and two controlled repositories; these are real coding-agent
  calls, not production user trajectories.
- Four primary runs per condition and two post-fix rolling smoke runs expose large
  failures but do not estimate a stable population effect.
- Initial Skill treatment explicitly requested inspection; the later natural probe
  had only two runs and found 0/2 useful opens.
- Wall time includes provider variance. Runs were sequential, not simultaneous.
- Raw traces remain local because they contain machine paths and provider session
  material; only aggregate, disclosure-safe results belong in the repository.

## Next experiment

1. Replay `fresh` and `mission` on disclosure-safe slices of two real projects.
2. Expand the repaired rolling handoff from its 2/2 smoke test to the full matrix.
3. Repeat Skill A/B on at least ten naturally occurring tasks without an explicit
   “inspect Skills” instruction and compare at least two models.
4. Measure bytes opened and false reuse by role, and gate Reviewer acceptance with
   held-out or independently generated edge cases where available.
