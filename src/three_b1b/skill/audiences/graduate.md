---
name: Graduate Audience Rules
description: Curriculum, pacing, vocabulary, and visual style rules for graduate and researcher viewers
tags: [manim, audience, graduate]
---

# Graduate Audience Rules

## Assumed Knowledge

Skip explaining all of these -- do not even gloss them:
- The full standard mathematical toolkit: real analysis, probability theory, linear algebra, optimization
- Core ML/CS/domain fundamentals: backpropagation, PCA, attention mechanism, dynamic programming, etc.
- Standard research methodology: ablation studies, baselines, significance testing
- How to read a paper: related work sections, architecture diagrams, loss function tables
- The dominant methods in the field for the last 5 years

Do NOT assume:
- They have read this specific paper
- They know the exact notation this paper uses
- They are aware of the specific sub-problem being solved here
- They have worked with this exact architecture or dataset

The opening line should establish "what problem this solves that existing methods do not" -- not what problem it solves in the abstract.

## Curriculum Structure

Skip background entirely. Start with the delta: what is new, what was wrong before, what this paper changes.

Scene sequence template:
1. Problem framing: state the specific gap in existing work -- precisely
2. Key insight: the central technical idea in 1 to 2 sentences, with visual proof
3. Method: the full technical mechanism -- dense, complete, no hand-waving
4. Theoretical or empirical support: why does this work? proof sketch or key experiments
5. Limitations and failure modes: where does it break? what assumptions are hiding?
6. Positioning: how does this relate to concurrent/prior work?
7. Open questions: what does this not solve? (optional but valued by researchers)

The "what's novel" scene must come first. A graduate viewer will lose patience if they sit through 3 minutes of background they have already read in 20 papers.

## Misconception Analysis (Required)

Graduate viewers carry misconceptions from overfit pattern-matching across papers. Target expert-level errors.

Apply the Muller misconception pattern:
1. State the plausible expert belief explicitly ("The standard assumption is...")
2. Show the scenario where this belief leads to a wrong prediction or failed experiment
3. Identify the precise assumption that breaks
4. Correct with the new framing this paper provides

Graduate-level misconception patterns to probe:
- "More data always helps" (fails under distribution shift, adversarial cases)
- "Larger model is always more capable" (capability-compute tradeoffs, emergent failures)
- "The loss curve captures model quality" (metric-behavior gap)
- "Adding a regularization term is equivalent to adding a prior" (only under specific conditions)
- "Attention is inherently quadratic" (there are linear approximations -- when are they valid?)
- "This method generalizes because it worked on 3 benchmarks" (benchmark overfitting)

Place the misconception scene at the first point where an expert would be tempted to shortcut the argument. Do not put it at the beginning.

## Vocabulary and Notation

Use full technical vocabulary throughout. No apologies, no glossing standard terms.

Notation:
- Use the paper's notation exactly -- state it once, then use it without re-definition
- If the paper uses non-standard notation, flag it: "Note they write W^T where most use W^top"
- Subscripts, superscripts, tensor indices: all fine, no explanation needed
- Information-theoretic quantities (KL divergence, mutual information, entropy): no intro
- Complexity classes, VC dimension, PAC learning framework: no intro

When introducing a new definition unique to this work, state it precisely and formally, then provide a one-line geometric or mechanistic gloss. Not the reverse.

Avoid:
- Informal paraphrases that lose precision ("roughly, the loss is smaller when...")
- Dropping the formal definition in favor of intuition only -- this audience will look it up and notice if your intuition is slightly wrong
- Using "basically" or "essentially" for anything non-trivially approximate

## Visual Style

Dense, information-rich, fast-paced. Lean toward equations and precise diagrams over metaphors.

Metaphors: use sparingly and only when they provide geometric insight not available from the formal presentation. If you use one, mark it explicitly as an analogy, not as the mechanism.

Equation presentation:
- Show complete equations, not simplified versions
- Use dim-and-reveal to decompose complex expressions, but move fast (0.5s per reveal)
- Annotate terms with short precise labels (not "this part", but "query projection W_Q")

Diagram standards:
- Architecture diagrams must match the paper's figures exactly in structure
- Include dimension annotations on weight matrices and tensors
- Show data flow with typed shapes (batch x seq x d_model)

Color usage:
- Reserve color for functional distinction, not decoration
- Novel contribution highlighted in YELLOW
- Existing baselines / prior work in BLUE or GREY
- Failure modes / limitations in RED
- Attention or energy flow: heat map gradient (BLUE to RED)

Allow 10+ visible elements on screen simultaneously when showing full pipeline diagrams. Graduate viewers can parse complex layouts.

## Pacing

Scene count: 10 to 12 scenes total.
Total video length: 12 to 18 minutes.

Hold times:
- After a key result: 1 second
- After a full equation: 1 to 1.5 seconds
- After a question frame: 2 seconds (they think fast)
- After a limitation or failure mode: 1.5 seconds

Animation speed: run_time=0.5 to 1.0 for most steps. 1.5 only for the central insight reveal.

Narration speed: 165 to 185 words per minute. Brisk academic lecture pace.

Do not slow down for standard derivation steps. Speed up through "and therefore..." chains. Slow down only for the novel step.

## Question Frames

Include at least 2 question frames, positioned at the hardest technical decision points.

Effective question frames for graduate audiences:
- "Why does the authors' choice of loss function matter here? What would go wrong with MSE?" (pause)
- "This architecture has a critical design choice. Can you identify it?" (show diagram)
- "Given these two experimental conditions, which would you expect to have lower variance?" (show setup)
- "Where in this derivation does the Gaussian assumption enter?" (show multi-step proof)

Pause duration: 2 seconds. They do not need more -- they either know it immediately or they are working through it quickly.

Do not frame questions as easy recalls. Graduate viewers disengage when asked to recall basics. Frame questions around design decisions and trade-offs, not definitions.

## Narration Script Guidance

Tone: peer-to-peer research discussion. Collegial, precise, willing to critique. You are presenting at a lab meeting, not lecturing undergrads.

Use hedged technical language: "The authors claim X, though the ablation on Y is not entirely convincing", "This bound is tight when..., but not in general."

Be willing to say when something is wrong or incomplete in the paper. Graduate viewers trust a narrator who identifies weaknesses more than one who presents everything as polished.

Sentence structure: allow longer, multi-clause sentences for technical content. Short sentences for emphasis on key results.

Avoid: "As we can see", "clearly", "obviously", "it is easy to show" -- these are wasted syllables for this audience. Get to the substance.

Say "the paper claims" vs "the paper shows" -- signal your own epistemic stance on results.

## What NOT to Do

- Do not explain backpropagation, PCA, attention, or any standard method from scratch
- Do not use analogies designed for non-specialists ("think of attention like a spotlight")
- Do not spend more than 30 seconds on related work unless a direct comparison is the point
- Do not smooth over limitations -- graduate viewers will think less of you for omitting them
- Do not present benchmark results without noting the dataset or evaluation protocol
- Do not present the paper as unambiguously correct -- maintain critical distance
- Do not oversimplify an equation to make it fit the animation -- show the real thing
- Do not treat the Muller misconception as optional -- without it, experts leave with their prior beliefs reinforced
- Do not end with "and that's how it works!" -- end with what remains open or contested
