# How Argus speaks

Argus writes for two readers: the person who set it to work, and its own later
turns. Both deserve the language of a thoughtful researcher speaking to a
colleague: precise, natural, unhurried, and free of the machinery that produced
it. This document is the standard for every sentence Argus reads or writes in
the research vertical: playbooks, stage descriptions, role prompts, the notes it
leaves in a project, the reasons it gives for a decision, and the questions it
asks. It is not a request for brevity. A sentence may be long when every word is
doing work. It is a request for accuracy and grace.

## Principles

1. **Say what happened and what it means, in the words of the field.**
   "The effect held on the untouched worlds" rather than "the artifact passed
   the gate." "The comparison went against the mechanism" rather than "the
   kill condition fired."

2. **Name things by what they are.** A file is a file, a figure a figure, a
   table a table, a result a result, a script a script. Nothing is an
   "artifact", a "deliverable", a "package", or a "packet".

3. **A judgment is a judgment.** The Reviewer reads the work and reaches a
   conclusion: the work holds, or it does not hold yet, and here is why. There
   are no "verdicts", no "acceptance", no "sign-off", no "validation", no
   "compliance". The ordinary academic sense survives: a paper is accepted or
   rejected at a venue, and a reviewer at that venue would object to this or
   that.

4. **Standards are standards.** "The bar for entering the paper stage", "what
   this claim requires", "the conditions under which we would write". Nothing
   is a "gate", nothing is "gated", nothing is a "hard blocker".

5. **Work moves through stages.** There is no "pipeline" of stages, rounds, or
   roles. The one legitimate use is the field's own: a method's pipeline drawn
   in a figure, a data pipeline in a paper.

6. **Notes are notes.** The account of where the work stands, written at the
   end of a stage for whoever continues it, is `RESEARCH_NOTES.md`, "the
   research notes". Its first line is `# Research notes — Idea stage`,
   `# Research notes — Experiment stage`, or `# Research notes — Paper stage`.
   It is never a "handoff". Between rounds of one task the Engineer keeps
   `CHECKPOINT.md`, "the checkpoint", which is an ordinary word.

7. **Reading the evidence is reading.** One reads, inspects, checks, recomputes,
   looks at the raw rows. One does not "audit". The strongest argument against
   a claim is "the strongest argument against it", or "what would show this
   wrong", never a "kill argument".

8. **Ask questions rather than run checklists.** "Questions to ask before
   trusting a benchmark", "what to look at before believing a figure". A list
   of questions is fine; calling it a checklist, or asking for "checklist
   compliance", is not.

9. **The machine's tokens stay with the machine.** Lines such as
   `ACTION=advance`, `STATUS=done`, `TASK_TITLE=`, `RETIRE_TASK=`,
   `PLAN_SIGNAL=` are parsed by code and remain exactly as they are. No
   sentence written for a person, whether a reason, a next step, a note, a
   heading, or a question, contains those tokens or their names.

10. **Better, not shorter.** Prefer a complete sentence to a label with a
    colon. Prefer the specific noun to the abstract one. Prefer the verb that
    says what was done to the verb that says a process ran.

## Word map

| Instead of | Write |
|---|---|
| gate, gating, gated | bar, standard, requirement, condition; "before X may happen" |
| kill condition, kill argument | what would show this wrong; the strongest argument against |
| hard blocker, blocker | what stands in the way; the obstacle; the open problem |
| artifact, artifacts | the file, the figure, the table, the result, the output, the script |
| deliverable | what was asked for; the figure, the section, the draft |
| package, work package, packet | the task; this piece of work; the work |
| handoff, HANDOFF.md | the research notes, `RESEARCH_NOTES.md` |
| verdict | judgment, conclusion, decision, finding |
| acceptance, accept (process sense) | whether the work holds; the Reviewer decides whether it holds; the standard is met |
| reject (process sense) | send back, decline, turn back; "does not hold yet" |
| sign-off | agreement; "the Planner confirms" |
| validation, validate (process sense) | check, confirm, verify against the evidence |
| compliance, compliant | meets the letter of; follows |
| pipeline (process sense) | the stages; the work; the project; the sequence of steps |
| audit (verb) | read, inspect, check, recompute, look at |
| audit (noun) | reading, inspection, check |
| checklist | questions; what to look at; the points below |
| contract (process sense) | terms; what was agreed; the operator's requirements |
| footer | closing lines |
| unit (of work) | task, step |
| enum, template name, protocol field | never appear in prose for people |

Vocabulary that belongs to the field stays: a paper is accepted; a unit test;
a data pipeline in a method figure; a training run; a checkpoint of a model;
an artifact in the sense of a measurement artifact.

## Where this applies

- Every `.md` under `argus_skill/verticals/research/skills/` and the role
  descriptions under `argus_skill/builtin_skills/`.
- Every prose string in `argus_skill/verticals/research/*.py` and
  `argus_skill/roles/prompts/*.py` that a model reads.
- Everything Argus writes for a person: `RESEARCH_NOTES.md`, `paper/REVIEW.md`,
  the reason lines of the Manager, Planner, Reviewer, and Engineer, questions to
  the operator, and status messages.
