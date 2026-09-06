---
name: "Venue Academic Language Review"
description: "Read-only academic-language pass using the selected venue's current conventions."
---

# Venue Academic Language Review

Use this for the reader-facing pass in Review. Under `cold_read`, read only the
rendered PDF supplied in the isolated workspace; do not search for manuscript
source, HANDOFF, REVIEW, code, or review history. During the later integrated
review, source and venue guidance may be inspected under that operation's wider
contract. Do not edit files and do not create a separate language-review
artifact.

## Inspect

- State clearly what is studied, what is claimed, under which conditions, and
  why the result matters.
- Make the title, abstract, introduction, contributions, results, and conclusion
  express one consistent thesis.
- Preserve the five-sentence, at-least-170-word abstract contract, exact
  headline evidence in the major reader-facing locations, and numerical
  takeaways in figure and table captions.
- Check whether headline, mechanism, disambiguating-control, scope-changing,
  and completeness evidence are visibly prioritized rather than reported as one
  flat experiment inventory.
- Allow a headline number to recur when it serves a different section role.
  Reject repeated matrix recital, not repetition by mechanical count.
- Require Methods, tables, and appendices to retain complete definitions and
  result coverage while prose explains the comparisons that change the current
  inference.
- Prefer confident, precise academic prose over defensive qualification,
  process narration, repeated caveats, and integrity self-praise.
- Request changes to generic openings, filler, repetitive transitions,
  unexplained acronyms, vague method names, or score restatement only when they
  cause ambiguity, needless repetition, or obstruct the argument. Preserve
  numerical restatement that serves the abstract, caption, or conclusion.
  When the surrounding context already explains a comparison, do not require
  another explanation after each number.
- Keep claims faithful to the actual method and evidence.
- Keep internal paths, role names, workflow language, and development history
  out of the manuscript.
- Apply the selected venue's terminology, anonymity conventions, section
  expectations, and reader-facing style.

For each required repair, return the passage or PDF location, the concrete
obstacle to understanding or inference, and the smallest repair goal. A
report-like tone or a preference for different wording alone is insufficient.
Example wording is optional; the Engineer need not copy it verbatim. Return
pass when no substantive reader-facing defect remains; do not manufacture
revisions to demonstrate review effort. The single Engineer resolves findings
with the scientific-loss and visual findings. The integrated Reviewer closes
resolved issues and records the final result only in `paper/REVIEW.md`.
