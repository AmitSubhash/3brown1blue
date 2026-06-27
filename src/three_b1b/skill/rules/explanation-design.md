---
name: Explanation Design
description: Choosing WHAT to explain and WHY before you animate. Three principles for designing a math explanation (from Grant Sanderson's "Designing Math", Config 2026)
tags: [manim, design, pedagogy, explanation, 3b1b, grant-sanderson, motivation]
---

# Explanation Design

The other design rules tell you HOW to render a thing well. This file is upstream of them:
it tells you WHAT to explain and WHY, before any mobject exists. Read this first when you are
deciding the content of a scene, then use animation-design-thinking.md for pacing and
visual-design-catalog.md for the concrete recipes.

Source: Grant Sanderson's talk "Designing Math" (Config 2026). His framing: a mathematician
and a designer are doing the same job. Both are "awash in a situation with an abundance of
choice and a large potential for complexity, trying to find a clear path through it." Whenever
there is an abundance of choice, that is where design is most needed. Explaining one idea is a
design problem, and you make three design decisions in order.

## The core move: one object, several representations, one question each

A single mathematical object can be visualized many different ways. Each way answers a
different question. The design act is choosing the representation that fits the question you
are answering right now, not picking one picture and forcing it to do everything.

Grant's worked example is e^{i*pi} = -1, shown three ways:
- as a spiraling sum of vectors that lands on -1 (answers "what does it look like?")
- as a point moving in a circle because velocity is a 90-degree rotation of position
  (answers "why is it true?")
- as a global warping of the whole plane, rolling vertical lines into circles
  (answers "how is it used?", here for an artistic application)

Before you script a scene, write down the question this scene answers. Then pick the
representation built for that question. If a later scene asks a different question about the
same object, build a different representation and let the viewer feel both at once. Combining
a "what" view with a "why" view is what produces mystery plus satisfying resolution.

## Principle 1: Treat it as a visual design challenge. Ask "what does it look like?"

For any abstract expression, the cheapest high-yield question is literally "what does this
look like?" Grant: "there is a lot of low-hanging fruit simply asking the question, what does
it look like." The difference it makes to a learner is "the difference between sitting in a
room in silence trying to read sheet music versus listening to the song."

Caveats he states plainly: not every piece of math must be visualized, and the visual is not
always the best explanation. But asking the question costs nothing and usually pays.

How to apply when scripting:
- Take each symbol and give it a picture before composing them. pi is the distance halfway
  around a unit circle. i is the action of rotating by 90 degrees. e is the infinite
  polynomial. Establish each image, THEN show what happens when you combine them.
- Turn the abstract claim into something on screen you can point at (here, a sum of vectors
  laid tip to tail that spirals inward to a specific point). See catalog pattern 28.
- This view shows WHAT is being claimed. It usually does not show why. That is Principle 2.

This is the upstream version of "geometry before algebra" (visual-design-principles.md #1):
that rule says show the shape first; this principle says go find the shape in the first place.

## Principle 2: Give your characters motivation. Explain WHY, not just WHAT.

"Before you ever try to prove something, it is always a good idea to believe that it is true."
So do not ask "why is this true?" first. Ask "why does it WANT to be true?" Build belief and
intuition, then rigor.

The mechanism: take each component of what you are explaining (each symbol of an equation,
each clause of a theorem) and name its reason for existence, the one thing it wants to do.
Grant: "If you were writing a novel, it is never going to work unless each one of the
characters has a clearly defined motivation. The same is true in math. Give your characters
motivation." And: motivation "is often the difference between a proof and an explanation."

Worked example: e^t becomes a position that moves in time, whose defining rule is that its
velocity always equals its position (that is the reason e exists). A constant in front
rescales the velocity (2 means runaway growth twice as fast, -0.5 means decay toward zero). An
i in front means velocity is a 90-degree rotation of position (the reason i exists), and the
only motion obeying that rule is travel around a circle at unit speed. After pi seconds you
are halfway around, at -1. "How could it have ever been otherwise?"

How to apply when scripting:
- For each symbol, write its one-line "reason for existence" before you animate anything.
- Render those reasons ON the equation: box each part in its semantic color and label what it
  DOES in plain language ("Position", "Velocity", "Rotate 90 degrees"). This is the visual form
  of giving a character motivation. See catalog pattern 27 and the role_annotation helper in
  templates/style.py.
- When an object is defined by a rule plus a starting state, set up the initial condition and
  the rule, then "play time forward" and let the consequence emerge. A vector field that draws
  velocity as a transform of position makes the resulting motion feel inevitable. See catalog
  pattern 29.

## Principle 3: The most memorable application is the most surprising one.

"Education 101 is that before anybody is going to learn from you, they have to want to learn.
You have to motivate the subject. And often the best motivation is some form of application."

We usually reach for applications in science or technology, and those are good. The third
principle sharpens it: when you have a choice of applications, the surprising, left-field one
sticks. Grant: "sometimes the most memorable application is the most surprising one... when
you see how it does, it burns in your brain just a little bit longer."

He motivates imaginary exponentials for a room of designers not with signal processing or
quantum mechanics, but with M.C. Escher's "Print Gallery." Treat the picture's pixels as
complex numbers, take the logarithm of the image, rotate in that log space, then exponentiate,
and you reproduce Escher's impossible spiral. That gives a third way to see e^z: as a global
warping of the whole plane (catalog patterns 30, 31, 32, 33).

How to apply when scripting:
- Open the topic with the application, not the definition. Motivation comes first.
- Match the application to the audience, then push past the obvious one. Ask "what is the most
  unexpected place this idea shows up?" and lead with that.

## The closing frame

Grant ends by noting these are only three of easily seven-plus principles, and that everyone
who designs anything is, at minimum, a teacher trying to communicate as clearly as they can.
Treat each explanation as a design problem with an abundance of choice, and spend real effort
choosing the clear path through it.

## Scripting checklist (use before writing a scene)

1. What single question does this scene answer? Write it in one sentence.
2. Which representation of the object is built for that question? (what-does-it-look-like,
   why-does-it-want-to-be-true, how-is-it-used)
3. Does each symbol have a stated reason for existence? Can I show that reason on screen?
4. Am I building belief before proof (intuition first, rigor second)?
5. Is the topic motivated by an application, and is it the most surprising one available?
6. If a later scene reuses this object, does it switch to a different representation rather
   than repeat this one?

## Further lessons (second pass through the talk)

A closer look at the talk surfaces craft moves underneath the three headline principles.

1. One deep example beats a survey. Grant explains a single equation and revisits it three
   times rather than touring many topics. Depth plus reincorporation transfers better than
   breadth. When you script, pick one rich example and mine it from several angles.

2. Assume maximal curiosity. "I am not going to treat the design community any different than
   I would treat a math community." Do not water the idea down. Explain the real thing and
   trust the audience to follow; that respect is itself motivating.

3. Be honest about discovery versus definition. The series for e^x is a discovered fact for
   real inputs, then becomes a definition by choice when you extend to complex inputs. Grant
   names the move ("a little sleight of hand") instead of hiding it. Flag when you are proving
   something versus when you are choosing a convention.

4. Match the application to the audience, then pick the surprising one. Electrical engineers
   get signal processing, physicists get quantum mechanics, designers get Escher. Same idea,
   audience-tuned motivation, and the unexpected choice is the one that sticks (Principle 3).

5. Give a glimpse and scope honestly. When the full story is 45 minutes and you have 3, say so,
   give the 10,000-foot view, and point to the complete treatment. Better than cramming the
   whole thing or skipping it.

6. Credit your sources out loud. "I do not deserve the credit... de Smit and Lenstra." Naming
   where the idea came from is part of an honest explanation, not an aside.

7. Two complementary views give mystery plus resolution. One representation shows WHAT is
   claimed, another shows WHY it must hold; holding both at once is the satisfying part. Design
   the pair, not just one picture.

8. Let the visual carry the meta-point. Grant states each principle aloud while the math stays
   on screen. He never cuts to a bulleted "Principle 1" slide. Keep the example up; narrate the
   lesson over it.

9. Practice your own principles at the top level. The talk opens with the designer-and-
   mathematician analogy, an application-first hook for the talk itself. Motivate the whole
   piece the way you motivate any single topic.

## Quick reference

| Principle | Question it answers | Visual form | Catalog patterns |
|-----------|--------------------|-------------|------------------|
| 1. Visual design challenge | What does it look like? | Find the picture for the abstract claim | 28 |
| 2. Give characters motivation | Why does it want to be true? | Box each part, label its job; rule + initial condition, play time forward | 27, 29 |
| 3. Surprising application | How is it used? | A global/transform view tied to an unexpected use | 30, 31, 32, 33 |
