---
name: Industry Audience Rules
description: Curriculum, pacing, vocabulary, and visual style rules for industry practitioners
tags: [manim, audience, industry]
---

# Industry Audience Rules

## Assumed Knowledge

Assume practical competence, not academic depth:
- Working knowledge of the tools and frameworks dominant in their domain
- Ability to read code and architecture diagrams
- Familiarity with benchmark metrics and production constraints (latency, throughput, cost)
- Understanding of the engineering tradeoffs in their field
- Experience with deployment and real-world failure modes

Do NOT assume:
- They have read any research papers or academic literature
- They are comfortable with mathematical proofs or derivations
- They have time to spare -- they are watching this to learn something actionable
- They care about the theoretical elegance of a solution
- They will watch again; it needs to land in one pass

## Curriculum Structure

Order: Problem -> Solution -> How it works (brief) -> Results / Benchmarks -> How to adopt.

The opening must establish a concrete pain point they have felt personally or a tool they need. Never open with "This paper introduces a novel approach." Open with "If you have ever hit this problem, there is now a better way to handle it."

Scene sequence template:
1. Problem: a concrete, relatable production pain point (1 scene)
2. Solution exists: the high-level claim -- what does this actually do better?
3. How it works: mechanism, kept to what is necessary to trust the solution
4. Benchmarks and results: numbers, comparisons, real workloads if available
5. Tradeoffs and constraints: where does it fail? what does it cost?
6. How to adopt: concrete steps, existing implementations, integration guidance
7. Summary: one-slide recap of when to use it and when not to

Skip: mathematical derivations unless they directly explain a practical tradeoff. Skip: related work. Skip: theoretical proofs of convergence.

## Misconception Analysis (Required)

Industry practitioners often have heuristics that were correct in a past context but have been superseded. Target these.

Apply the Muller misconception pattern:
1. Name the common heuristic explicitly ("The standard advice has been to...")
2. Show the scenario where it produces a worse outcome or breaks silently
3. Explain why: what changed in the environment, scale, or problem setup that breaks the old rule
4. Correct: show the new guidance and when to apply it

Common industry misconceptions to probe:
- "Bigger batch size is always faster" (memory-throughput tradeoff, gradient noise at large batch)
- "Quantization always degrades quality significantly" (modern INT8/FP8 methods are near-lossless in many cases)
- "You need a large dataset to fine-tune" (LoRA, PEFT, few-shot approaches)
- "Caching is enough to solve latency" (cache invalidation, cold start, memory pressure)
- "More model parallelism is always better at scale" (communication overhead, pipeline bubbles)
- "The open-source model is always the practical choice" (licensing, support, total cost of ownership)

The misconception scene should be close to where the viewer would be making a real decision -- not abstract.

## Vocabulary and Notation

Industry terms are fine and preferred: latency, throughput, SLA, inference cost, token budget, batch size, quantization, VRAM, TTL, CI/CD pipeline.

Avoid academic jargon without grounding: do not say "the posterior distribution over parameters" -- say "the model's uncertainty about its weights." Do not say "asymptotically optimal" -- say "works better at scale."

Mathematical notation: minimize. If an equation is unavoidable, label every term in plain English directly on the diagram.

When you must show math:
- Show the practical interpretation beside it: "This term is what makes it expensive to run"
- Never show a derivation -- show only the final form and what it implies operationally
- Use concrete numbers alongside symbols: "If N=10,000 tokens, this term grows quadratically -- that is 100x the cost at 1,000 tokens"

Frame results as decisions: not "accuracy improves by 3.2 points" but "3.2 points better accuracy means fewer human review escalations."

## Visual Style

Clean, focused, demo-adjacent. Prioritize clarity over visual complexity. Every element on screen should answer "so what can I do with this?"

Visual priorities in order:
1. Before/after comparisons (old approach vs new, side by side)
2. Benchmark bar charts with real workload labels
3. Architecture diagrams with operational annotations (not just boxes -- include latency or cost numbers)
4. Concrete configuration snippets or pseudocode
5. Decision flowcharts ("Use this when..., do not use this when...")

Color conventions:
- Old/worse approach: RED or muted GREY
- New/better approach: GREEN or BLUE
- Cost/constraint: ORANGE
- Neutral reference: WHITE

Benchmark charts must include:
- Axis labels with units
- Comparison baseline clearly labeled
- Hardware or environment context (e.g., "A100, batch=32, FP16")

Do not use abstract mathematical diagrams as primary visuals. An industry viewer looking at a loss landscape plot will ask "what does this mean for my deployment?" -- answer that question on screen, not just in narration.

Use simple flowcharts and pipeline diagrams over symbolic formalism. If there is an open-source implementation, show the import and the function signature.

## Pacing

Scene count: 6 to 8 scenes total.
Total video length: 8 to 12 minutes.

Hold times:
- After a key result or benchmark: 2 seconds
- After a surprising comparison: 2.5 seconds
- After a question frame: 2 to 3 seconds
- After an actionable recommendation: 2 seconds

Animation speed: run_time=0.8 to 1.2 for most reveals. Do not linger on setup.

Narration speed: 155 to 175 words per minute. Confident, direct.

Front-load value: the viewer should know the practical upshot within the first 90 seconds. If they stop watching at 2 minutes, they should still have learned something useful.

Do not pad. If a point has been made, move on. Repetition wastes the viewer's time budget.

## Question Frames

Include at least 2 question frames, targeted at real decisions they would face.

Effective question frames for industry:
- "Would you use this in production today? Before I tell you the limitations, make a call." (pause)
- "Which of these two serving configurations would you pick for a latency-critical API?" (show two setups with numbers)
- "Given this throughput curve, at what batch size does it stop being worth it?" (show the chart, pause)
- "This approach claims 3x speedup. What is the catch?" (pause, then reveal the tradeoff)

Pause duration: 2 to 2.5 seconds. These are experienced practitioners -- they form opinions quickly.

The "what is the catch" frame is particularly effective for this audience. They are accustomed to vendor claims overstating results. Asking them to identify the catch before you reveal it signals that you will give them an honest assessment.

## Narration Script Guidance

Tone: direct, practitioner-to-practitioner. Skip the academic hedging. Make clear, bounded claims.

Be opinionated: "This is production-ready for batch inference, not for low-latency serving. Here is why." Industry viewers value a strong take more than exhaustive caveats.

Use conditional framing: "If your bottleneck is memory bandwidth, this helps. If it is compute-bound, look elsewhere."

Sentence structure: short and declarative for recommendations. Longer explanatory sentences only for the mechanism.

Avoid: "this is a fascinating direction", "the authors propose", "it remains to be seen". These are academic hedges with no operational value.

Use: "here is what this means for your stack", "in practice", "before you deploy this", "the gotcha is".

End every recommendation with a concrete conditional: "Use this when X. Do not use it when Y."

## What NOT to Do

- Do not spend 3 or more minutes on mathematical foundations unless they directly explain a cost or constraint the practitioner will hit
- Do not present benchmark results without hardware context and comparison baselines
- Do not omit limitations -- an industry viewer who deploys based on your video and hits an undisclosed failure will not trust you again
- Do not use academic paper framing: no "we propose", no "extensive experiments demonstrate", no "the rest of this video is organized as follows"
- Do not skip the adoption guidance -- "how do I actually use this?" is the primary question
- Do not assume they care about the theoretical novelty -- they care about "is it better than what I am using now?"
- Do not end without a concrete recommendation on when to use and when to skip
- Do not show code without explaining what it does in one sentence first
