---
name: Undergrad Audience Rules
description: Curriculum, pacing, vocabulary, and visual style rules for undergraduate viewers
tags: [manim, audience, undergrad]
---

# Undergrad Audience Rules

## Assumed Knowledge

Skip explaining these -- they already know them:
- Single and multivariable calculus (derivatives, integrals, gradients, Jacobians)
- Linear algebra (vectors, matrix multiplication, eigenvalues, least squares)
- Basic probability and statistics (expectation, variance, Bayes' theorem)
- Programming fundamentals
- 1 to 2 courses in the video's subject domain (they have seen the basics)

Do NOT assume:
- Deep specialization in the exact sub-field
- Familiarity with cutting-edge literature (papers from the last 3 years)
- Comfort with highly abstract proof techniques (epsilon-delta, measure theory)
- Expert intuition -- they can follow arguments but still need visual grounding

## Curriculum Structure

Standard 3b1b arc: Hook -> Brief Background -> Core Method -> Results -> Takeaway.

The background section should be brief (1 scene max). They have taken the prereqs. Spend your time budget on the novel content.

Scene sequence template:
1. Hook: a concrete surprising result or unsolved-feeling question
2. Setup: establish notation and frame the problem (1 scene, dense but fast)
3. Core idea: the central insight -- spend 2 to 3 scenes here
4. Mechanism: how the insight works mechanically -- show the math
5. Edge cases or subtleties: one scene on where intuition breaks down
6. Results / payoff: what this enables
7. Takeaway: one-sentence synthesis, pointer to deeper material

Skip: lengthy definitions of calculus, matrix multiplication, or probability. A sentence of "recall that..." at most.

## Misconception Analysis (Required)

Undergrads have learned formal machinery but have misconceptions about when it applies. Target these specifically.

Apply the Muller misconception pattern:
1. Show the wrong belief (often a plausible overextension of a simpler rule)
2. Construct a case where it fails -- visually
3. Diagnose why: identify which assumption of the simpler rule was violated
4. Correct: show the right version and how it reduces to the simple case when assumptions hold

Common undergrad misconception patterns:
- "More complex model is always better" (overfitting)
- "Eigenvalues of a product = product of eigenvalues" (only for commuting matrices)
- "Gradient descent always converges" (non-convex, learning rate sensitivity)
- "If the p-value < 0.05, the effect is real" (multiple testing, effect size confusion)
- "A higher-order polynomial fit is more accurate"

Include one misconception scene, ideally at the point where the audience would most likely make the error themselves. Red-path / green-path visual structure works well here.

## Vocabulary and Notation

Standard mathematical notation is fine -- no need to spell out sigma notation or integral signs.

Domain terms: introduce with a one-phrase gloss on first use only. "The Jacobian -- the matrix of all partial derivatives -- tells us..." Then use the term freely after.

Notation standards:
- Bold for vectors and matrices is expected
- Subscripts and superscripts need no explanation
- Greek letters are fine: alpha, beta, lambda, theta, epsilon all need no introduction
- Big-O notation: fine without introduction

Avoid:
- Inventing non-standard notation to "simplify" -- it creates more confusion
- Using the same symbol for two different things across scenes
- Switching notation mid-video (pick one convention and hold it)

Introduce paper-specific notation explicitly: "The authors write W_Q for the query weight matrix. We will use the same notation."

## Visual Style

Balance of intuition and formalism -- this is the 3b1b sweet spot. Equations are necessary and welcome, but always motivated by a visual argument first.

Structure for each concept:
1. Visual / geometric intuition (no symbols)
2. Notation overlaid on the visual
3. Algebraic manipulation if needed
4. Return to the visual to interpret the result

Color conventions (consistent across video):
- Formal definition / equation terms: WHITE or BLUE_B
- Key insight highlight: YELLOW
- Problematic or wrong region: RED
- Correct / desired outcome: GREEN
- Background reference material: GREY (dimmed)

Use split-screen layouts for before/after, intuition/formalism comparisons. Undergrads can parse two panels simultaneously.

Equations: use dim-and-reveal decomposition to walk through complex expressions. Never drop a 6-term equation cold.

Graphs and plots: include axis labels and units. This audience notices missing labels. Use ValueTracker-animated plots for parameter sensitivity.

## Pacing

Scene count: 8 to 10 scenes total.
Total video length: 10 to 15 minutes.

Hold times:
- After revealing a concept: 2 seconds standard
- After an equation appears: 2 seconds before proceeding
- After a question frame: 3 seconds
- After a surprising result: 2 to 3 seconds

Animation speed: run_time=1.0 to 1.5 for standard reveals. run_time=0.5 acceptable for brief recap steps.

Narration speed: 150 to 165 words per minute. Adult conversational pace.

Scene density ramp:
- Scene 1-2: 4 to 6 elements
- Scene 3-7: 7 to 12 elements
- Final scene: 4 to 5 elements (synthesis, clean)

## Question Frames

Include at least 2 question frames per video. Target the conceptual hinge points -- where intuition and formalism would diverge.

Effective question frames for undergrads:
- "Before we derive this, what would you expect to happen as N grows?"
- "Which of these two optimization landscapes is easier to navigate?" (show two)
- "What's the computational cost of this approach? Take a guess."
- "Can you spot the problem with this derivation?" (show a flawed step)

Pause duration: 2.5 to 3 seconds. They think faster than high school viewers but still need time.

The "flawed derivation" frame is particularly effective: show a step-by-step proof with one incorrect step. Ask viewers to find it. This builds critical reading skills.

## Narration Script Guidance

Tone: collegial, intellectually honest, enthusiastic about the material. Treat the viewer as a smart peer who is slightly behind you in the specific topic.

Use "we" framing: "We want to find...", "What we are really asking is...", "Notice that we have..."

Sentence length: medium. Up to 20 words for explanatory sentences. Short for punchlines.

Use hedged language appropriately: "This is not quite right, but it builds the right intuition", "We are sweeping some measure-theoretic details under the rug here."

Avoid: over-simplification ("think of it like a box") for concepts they should handle rigorously. They will find it patronizing.

Say "recall" not "as you know" -- the former acknowledges they may need a reminder, the latter assumes they remember perfectly.

## What NOT to Do

- Do not spend more than one scene on prerequisites they covered in courses
- Do not define a derivative, an integral, or a dot product -- they know these
- Do not use kindergarten metaphors for concepts they have studied formally (do not say "think of a matrix as a spreadsheet")
- Do not omit notation -- this audience expects to see the math written out
- Do not skip the visual motivation in favor of jumping straight to equations either
- Do not use informal approximations without flagging them ("this is approximate because...")
- Do not end a scene without a clear transition statement -- they expect logical connective tissue
- Do not assume they remember scene 1 details by scene 8 -- restate key symbols briefly
