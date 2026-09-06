---
name: "Using generated imagery in a paper figure"
description: "Optionally generate a visual element that carries no scientific claim when the configured image route is available."
---

# Using generated imagery in a paper figure

Use this only after *Choosing how to draw a research figure* establishes that
generative imagery helps a conceptual figure and model API status reports an available
image route. It is optional; the paper can proceed without it.

Use image generation for a background, texture, or non-semantic icon. Scientific
labels, numbers, arrows, boundaries, and claim-bearing geometry must remain
editable and deterministic in the final figure.

1. Write a prompt grounded in the current paper and forbid unsupported content.
2. Generate one candidate with `python -m argus_skill.tools.image_api generate`.
3. Inspect the actual output for accidental text, watermarks, logos, misleading
   symbolism, or content not supported by the paper.
4. Place only the useful non-semantic asset into the editable figure source.

Keep the prompt only when it is needed to regenerate the included asset. Do not
create registration files or separate visual-review reports. The final visual
judgment is made in the single visual assessment during Review.
