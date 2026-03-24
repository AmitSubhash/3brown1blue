---
name: High School Audience Rules
description: Curriculum, pacing, vocabulary, and visual style rules for high school viewers
tags: [manim, audience, high-school]
---

# High School Audience Rules

## Assumed Knowledge

Skip explaining these -- they already know them:
- Basic arithmetic, fractions, percentages
- Linear equations (slope-intercept form)
- Geometric shapes: area, perimeter, volume formulas
- Basic graphing on an x-y plane
- Intuition about "big" and "small" numbers

Do NOT assume:
- Any calculus (no derivatives, integrals, limits)
- Trigonometry beyond sin/cos/tan in right triangles
- Any college-level subject (physics, CS, biology beyond biology class)
- Familiarity with Greek letters beyond pi
- Comfort with abstract notation

## Curriculum Structure

Order: Concrete example first -> observe a pattern -> name the pattern -> generalize -> real-world application.

Never open with a definition. Never open with an equation. Open with something they can touch or visualize: a physical object, a game, a question from daily life.

Scene sequence template:
1. Hook: a surprising question or result (no math yet)
2. Concrete case: work through ONE specific small example by hand
3. Second case: show it again with different numbers -- pattern emerges
4. Pattern scene: isolate the pattern visually, no formula yet
5. Name and formula: now introduce the notation, justified by what they saw
6. Generalization: show the formula works across many cases
7. Real-world payoff: where does this actually show up?

## Misconception Analysis (Required)

High school viewers arrive with strong naive intuitions. Ignoring them guarantees confusion.

Apply the Muller misconception pattern for every major concept:
1. State the wrong intuition explicitly and visually ("You might think...")
2. Show it playing out -- let it fail or produce a contradiction
3. Break it: reveal WHY the intuition is wrong
4. Correct it: show the right mental model with the same visual

Common misconceptions to probe by topic:
- Probability: "50-50 for everything uncertain", streak fallacy
- Geometry: larger perimeter means larger area
- Exponents: "multiplying by 2 twice is the same as multiplying by 4"
- Fractions: "dividing makes things smaller" (fails for fractions < 1)
- Graphs: steeper line always means bigger value

Include at least one misconception scene per video. Label it visually with a "wrong path" color (RED) before the correction.

## Vocabulary and Notation

Preferred vocabulary:
- "times" or "multiplied by", not "multiply by a factor of"
- "speed" not "velocity" unless the distinction is the point
- "grows faster" not "increases at a higher rate"
- "cancel out" not "the terms vanish"
- "plug in" not "substitute"
- "roughly" or "about" not "approximately" for informal estimates

Introducing new terms:
- State it in plain words first, then give the formal name
- Example: "When a shape can be folded onto itself -- that's called symmetry"
- Write the term on screen when you first say it, in a highlight color
- Reuse the term at least twice more so it sticks

Greek letters:
- pi (pi) is fine -- they know it
- sigma for sum: introduce with "this just means add them all up"
- Avoid theta, lambda, phi unless the video is specifically about those
- Never use epsilon or delta without explicit introduction

## Visual Style

Lead with metaphors and physical analogies. Math must be grounded in something tangible before any symbol appears.

Color strategy:
- Assign one color to each concept and use it consistently throughout
- Unknown quantities: YELLOW
- Known/given quantities: BLUE
- Wrong path: RED
- Answer/result: GREEN
- Background annotations: GREY (dimmed)

Metaphors that work well:
- Functions as machines with input/output slots
- Variables as boxes holding a mystery number
- Slope as steepness of a hill you are walking up
- Area as counting unit squares inside a boundary
- Probability as fraction of outcomes on a spinner

Animation density: one idea per screen region at a time. Do not show 4 things simultaneously. Reveal sequentially, dim previous elements when introducing new ones.

Use physical analogy scenes (balance scale for equations, spinner for probability) before abstract diagrams.

## Pacing

Scene count: 5 to 7 scenes total.
Total video length: 8 to 12 minutes.

Hold times:
- After revealing a new concept: 3 seconds minimum
- After a question frame: 3 to 4 seconds (let them think)
- After an equation appears: 3 seconds before continuing
- After a surprise result: 4 seconds (let it land)

Animation speed: run_time=1.5 to 2.0 for most reveals. Never rush a concept introduction.

Narration speed: 120 to 140 words per minute. Slower than adult default. Leave space.

Scene density ramp:
- Scene 1-2: 3 to 4 visible elements (sparse, inviting)
- Scene 3-5: 5 to 8 elements (building)
- Final scene: 3 to 4 elements (resolution)

## Question Frames

Question frames are mandatory -- at least 2 per video. This audience needs to feel smart.

Effective question frames:
- "Which of these two shapes has a larger area?" (show two shapes, pause)
- "What do you think happens if we double the radius?"
- "Before I show you -- guess how many times it grows"
- "Is this graph going up faster or slower than the first one?"

Always pause 3 to 4 seconds after the question. Show a countdown dot animation if the wait exceeds 3 seconds.

After the answer: affirm any viewer who would have gotten it right ("If you said X, you were correct").

## Narration Script Guidance

Tone: curious, enthusiastic, never condescending. Talk like a friend who just discovered something cool, not like a textbook.

Sentence length: short. Max 15 words per sentence for new concepts. Break long explanations across multiple short sentences.

Avoid: "trivially", "obviously", "clearly", "it follows that". These signal to a struggling viewer that they are supposed to already know this.

Use: "here's the key insight", "wait, that's weird", "let's slow down here", "this is the part that trips people up".

Rhetorical questions: use them before every new idea. "But what if we had THREE of these instead of two?"

Use second person throughout: "you can see", "you might be wondering", "notice how you can".

## What NOT to Do

- Do not open with a definition, theorem, or formula
- Do not introduce more than one new symbol per scene
- Do not write an equation without first motivating WHY it's needed
- Do not assume they remember content from the previous scene -- give a one-line recap
- Do not use logarithms, trig functions (beyond basic), or calculus without full scaffolding
- Do not show a 2x2 table of results and expect them to extract the pattern -- walk them through it
- Do not use passive voice in narration ("it can be shown that...")
- Do not skip the physical analogy in favor of jumping to the abstract
- Do not use more than 4 on-screen elements simultaneously without dimming some
