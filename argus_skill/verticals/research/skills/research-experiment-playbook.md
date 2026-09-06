---
name: "Developing an idea through experiments"
description: "The guide that defines Experiment: implement the selected Idea faithfully and develop it through adaptive experiments until the evidence supports a strong paper."
---

# Developing an idea through experiments

## What Experiment should establish

Turn the selected idea into a real implementation and develop it until
representative evidence supports a scoped thesis with scientific value.
Building the method and running the experiments happen in this one stage:
the experimental design changes in place as evidence arrives; it is never
a frozen plan handed down from somewhere else.
Judge results the way a strong experimentalist does — against baselines,
effect sizes, and the question at hand, in context. Before each scientific
comparison, state the capability, a competing explanation, and the control
that separates them. Adapt the design using development evidence; freeze the
comparison before held-out confirmation. Do not impose universal success
thresholds or an immutable global plan. Report what the evidence supports.
A credible improvement in any meaningful dimension can carry the
contribution; the target is a result that a top reviewer would remember,
not a complete-looking experiment matrix.

## How to develop the evidence

1. Read the research notes in `RESEARCH_NOTES.md` and trace every load-bearing thesis element to concrete
   code, configuration, data, outputs, and information boundaries.
2. Inspect the strongest relevant official implementations. Clone and run a
   fixed public revision when compiling, adapting, or comparing its code; reuse
   maintained components instead of reimplementing them from a paper summary.
   Also survey the released code of recent papers in the same area — including
   ones the experiments will not compare against — and read the high-quality
   ones as reference implementations: how they structure the training and
   evaluation code, which libraries they build on, and how they handle the
   details a paper summary glosses over. Borrowing a proven pattern from a
   strong recent codebase beats inventing one.
   For training and inference infrastructure this is the rule, not a
   preference: RL post-training, preference optimization such as DPO,
   distributed training, and serving all go through an established framework
   (veRL, OpenRLHF, TRL, LLaMA-Factory, vLLM, or the released baseline's own
   stack). A hand-rolled training loop or serving path is slower, subtly
   wrong in ways that contaminate every result built on it, and convinces no
   reviewer — write custom infrastructure only when that infrastructure is
   itself the contribution being studied.
3. Set up a clean project-local environment before writing method code: the
   project gets its own virtual environment on the system interpreter, with
   dependencies installed and pinned there — never in the framework
   environment, and never inherited from another project's leftovers. Install
   the complete toolchain the method actually needs and confirm each piece
   runs: compilers, the CUDA toolkit and driver-compatible libraries,
   profilers, and domain toolkits — kernel-optimization work in particular
   depends on many of these (nvcc, Triton, CUTLASS, Nsight and friends), and a
   missing or mismatched one quietly invalidates every measurement built on
   top of it.
4. Implement the method and baseline through real entry points under comparable
   data, compute, information, and evaluator access. Build the strongest
   faithful version of the idea, not the easiest version that can pass a local
   check.
5. Run only the smallest engineering checks needed to establish imports,
   shapes, branches, numerical behavior, and end-to-end wiring, then run a
   known detectable positive control through the same evaluator path.
6. Develop the method with real models or systems and the strongest
   same-information baselines required by the claim. Use public or official
   benchmarks where relevant; small tasks built from explicit executable rules
   are valid scientific experiments when they isolate the claimed capability.
   Choose models for task competence and claim scope, not release date.
7. Keep every run reproducible from its code, explicit configuration, command,
   and raw output.
8. Treat weak results as optimization signals. Change the method,
   implementation, benchmark, baseline, controls, or scale when development
   evidence identifies a concrete reason — the design and the runs live
   together here precisely so this revision is cheap.
9. Separate small engineering diagnostics from claim-bearing experiments.
   Stop repeating micro-benchmarks once they no longer change the next decision.
10. Use held-out confirmation after method and evaluation choices stabilize.

Choose sample counts from coverage of independent items and the precision
needed for the claim; explain the choice in the research notes. Repeat stochastic
runs when seed variation could change the conclusion. Rerunning deterministic
comparisons adds no independent evidence.

Scale the evidence to the claim, not to the first configuration that ran. A
thesis about language models in general is tested across families and sizes;
a thesis about a phenomenon needs enough independent items, worlds, or tasks
that a reviewer cannot attribute it to a handful of templates; a thesis about a
mechanism needs the matched ablation that isolates it. Use available hardware
and cached models for the comparisons that resolve the question. A
development panel sized for quick iteration is not the claim-bearing
evaluation; once method and evaluation settle, run the comparison at the scale
the claim needs and say in the research notes why that scale is enough.

When the decisive comparison goes against the mechanism, because a matched
ablation or the strongest same-information baseline wins on fresh evidence,
the next move is not another variant of the same objective. Return to the
evidence and ask what it does establish: often the evaluation built to test
the mechanism is itself the finding, or the refutation is the result the field
needs, provided that evaluation is at claim scale. Re-derive the thesis,
confirm it on untouched data, and carry that thesis into Paper. A further repair round
on the same mechanism needs a concrete, diagnosed cause; repeated development
on the same panels is not confirmation, however many cycles it took.

Plan only on resources that are actually in hand. Human participants, ethics
approval, paid annotation, credentials, external services, or compute the
operator has not supplied cannot be scheduled as work in an autonomous
campaign; raise the need once, then design the claim around what can be
executed here. Never stand in for missing evidence with fabricated,
placeholder, or projected results: not in the runs, not in the research notes, and
never in a manuscript.

Choose benchmarks that expose the method's mechanism and real advantage rather
than convenient saturated tasks. A benchmark the project builds itself is part
of the claim: write down where every label comes from, check that a constant
answer does not already score well, and make sure the targets it is meant to
separate are separable on its items before any model is scored on it. Follow surprising positive evidence when it
reveals a stronger contribution, then confirm it on untouched data. Keep
relevant losses visible internally, but do not let defensive edge-case coverage
replace the main result.

Check real external, numerical, persistence, and security boundaries. Inside
the controlled implementation, trust established invariants. Do not add
redundant guards, fallback chains, reports, wrappers, or abstractions merely to
make the project look robust.

Do not freeze a global experiment plan, reopen Idea selection, hide relevant
losses, or present unfinished development as a negative result; a negative or
boundary thesis is a paper only when its evidence is as complete as a positive
one would need.

## When the evidence is ready for Paper

Enter Paper when Reviewer judges that credible evidence improves at least one
scientifically meaningful dimension. Do not require a hard numeric margin,
wins on every headline metric, or dominance over every strong baseline. Keep
uncertainty, relevant losses, and tradeoffs visible, and scope the thesis to
what improved. Manager alone advances the stage.

## Research notes

When the entry bar is met, replace the research notes at project-root
`RESEARCH_NOTES.md`, beginning with `# Research notes — Experiment stage`.
Include the thesis, winning comparisons, strongest
baseline, relevant limitations, confirmed figures/data, and minimum
reproducibility pointers needed by Paper. Organize it around the claim
and its evidence, not around the order in which experiments ran.

## When another skill would help

Start with this guide. Open one specialist skill only for the current
decision, then return here. Do not read all the sources in advance.

| When needed | Open | Use it for |
|---|---|---|
| The thesis may have drifted from code | `engineer/hypothesis-implementation-contract.md` | Map the selected mechanism to the executed path |
| A fresh Reviewer must verify execution fidelity | `reviewer/claim-to-code-trace.md` | Trace claim-critical calls and formulas |
| Training or large inference infrastructure is required | `engineer/training-infrastructure-guide.md` | Select and reuse maintained frameworks |
| A fresh project environment must be set up | `engineer/project-environment-management.md` | Create the project venv and install the ML stack cleanly |
| A concrete dependency or resource may block execution | `engineer/environment-readiness.md` | Check only the resources this implementation uses |
| The method is below its baseline | `engineer/research-grind.md` | Diagnose and improve the largest live gap |
| The run may be misconfigured | `engineer/suspect-the-setup.md` | Separate setup failure from method evidence |
| A mechanism needs one decisive ablation | `engineer/ablation-planner.md` | Choose only claim-changing ablations |
| Raw evidence or evaluator behavior is disputed | `reviewer/reading-the-evidence.md` | Inspect code, configuration, evaluator, and rows |
| The next experiment or Paper decision is unclear | `reviewer/experiment-results-review.md` | Independently judge what the evidence supports and what remains to learn |
| Results must become a precise claim | `engineer/result-to-claim.md` | Relate direct evidence to the strongest supported thesis |
| Confirmed results need tables or figures | `engineer/research-results-analysis-and-figures.md` | Produce claim-bearing paper visuals |

Specialist Skills answer one implementation or experiment question. They do not
define a global plan, stage transition, or parallel report.
