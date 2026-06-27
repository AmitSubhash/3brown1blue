---
name: Pedagogy Checklist
description: A checklist for judging when an explanation is pedagogically done, not just rigorously done (from Grant Sanderson's JMM 2023 award lecture, the SoME rubric, and interviews)
tags: [manim, pedagogy, exposition, checklist, 3b1b, grant-sanderson, teaching]
---

# A Pedagogy Checklist for Math Exposition

explanation-design.md decides WHICH representation answers a question. This file is about a
different question: how do you know an explanation is finished? It distills Grant Sanderson's
JPBM Communications Award lecture (Joint Mathematics Meetings 2023, "Raising the Ceiling and
Lowering the Floor of Math Exposition", aka "Math's pedagogical curse"), his Summer of Math
Exposition judging rubric, and two interviews.

## The core problem: rigor has a "done" test, pedagogy does not

Math gives the writer a satisfying, binary completion test that no other field has: every
definition unambiguous, every referenced object previously defined, every claim justified.
"It's like a compiler checking code." Grant's warning is that this gift is also a curse (his
Midas analogy): because the rigor checklist is so clean and so satisfying to complete, it is
easy to call a piece "done" the moment it is rigorous, when it is not yet pedagogically done.
Rigor and clarity are not opposites (the best authors achieve both), but the pull of the
definite makes us "lose sight of the other forms of completion that are just as worthy."

The remedy he proposes: keep a SECOND checklist, for pedagogical clarity, and treat finishing
it with the same seriousness as finishing the rigor. The list below is his, plus what it maps
to elsewhere in this skill. Treat it as items to check before you call a scene or a video done.

## The checklist

1. **Does each definition have a motivating example?** A reason you would want to define it,
   given before the theorem, not after. (Pairs with explanation-design.md Principle 2: give
   each symbol a motivation.)

2. **Do the proofs/derivations feel rediscoverable?** The viewer should feel they anticipated
   the next step, "validating rather than feeling like you are the one who has to validate
   that the monument you were handed does the thing being claimed." Build a path of
   rediscovery. (Pairs with the Config-talk lesson "believe it before you prove it".)

3. **Does it feel personal?** An actual person with some emotion and personality, not a neutral
   voice. More engagement means better retention. (See visual-design-principles.md #12,
   emotional anchoring.)

4. **Are the core ideas given diagrams?** "If something should be illustrated, is it
   illustrated?" This is the whole premise of 3Blue1Brown. Two corollaries Grant stresses:
   the diagram is often for the AUTHOR as much as the student (making it elicits new
   intuitions and deepens your own understanding, the whiteboard-versus-couch effect), and it
   does not have to be polished (a pencil sketch goes a long way).

5. **Are abstractions preceded by concrete examples?** Think in layers of abstraction
   (quantities, numerals, algebra, functions, vector spaces, ...). For a first encounter,
   populate the mind with data one layer BELOW the target before stating the target, even when
   the target is the goal. His worked example: teach the difference of squares by first
   factoring numbers and noticing the pattern (class A), not by stating x^2 - y^2 = (x+y)(x-y)
   and assigning a worksheet (class B). The trap is that the expert thinks top-down (the
   abstraction is fastest for them), so the abstraction-first lesson feels natural to write and
   is exactly wrong for the newcomer. (Pairs with visual-design-principles.md #1 geometry
   before algebra, and #10 concrete values.)

6. **Does the lesson start with a motivating question or problem, before the instruction?**
   Grant cites Manu Kapoor's "Productive Failure in Learning Math": one class got instruction
   then problem solving, the other got the problem first then instruction. He reports the
   problem-first group scored far higher on conceptual understanding and transfer (procedural
   skill was about equal). Struggling with a problem first makes the answer stick. In video
   this is hard (viewers are passive), so it pairs best with a real "stop and think" prompt.
   (See catalog pattern 15, Question Frame, and visual-design-principles.md #7.)

7. **Is there a compelling reason the audience cares to listen?** Motivation is the zeroth
   item. Hook through a pre-existing interest (his Wordle video was a Trojan horse for
   information theory). And note clarity itself can GENERATE interest: a compelling diagram
   pulls in people who did not care about the topic before.

## Cross-cutting techniques

- **Raise the ceiling while lowering the floor.** Accessibility and expert interest are not a
  tradeoff. Making the Riemann zeta function legible for newcomers (animate every input on the
  plane) is exactly what made the analytic-continuation boundary "scream at you," surfacing
  fresh questions for experts. Done right, lowering the floor raises the ceiling.

- **Visual-first authoring.** The lesson can come FROM the visual, not the other way around.
  Grant made the zeta video because playing with the visualization gave him the framing: "It
  wasn't that I wrote a script and then put some cartoon to it." Workflow note: this complements
  the storyboard-first workflow in animation-design-thinking.md rather than contradicting it.
  The IDEA and framing can come from playing with visuals; the narration structure is still
  written before the final render.

- **"How would you draw this?" inside-out.** Even with no a-priori insight, take an important
  formula and unpack it from the innermost part outward, demanding an image for each piece, as
  if you had to "communicate non-linguistically." His Fourier transform video was essentially
  this. Reserve it for the few formulas that deserve the deep dive; it is too slow for every
  line. (Renders as catalog pattern 27, role-labeled equation boxes.)

- **Discovery fiction.** A friend's term Grant endorses: invent a plausible sequence of
  flawed-idea, fix, new-flaw, fix that leads to a construct, to motivate why an "arbitrary"
  definition exists. It need not match real history, and most intermediate objects are
  discarded, which is fine if you are honest that they are steps along the way.

- **Honest hand-waving.** On the maxim "teach the truth, nothing but the truth, but never the
  whole truth": be explicit when you simplify. Grant points to Feynman flagging simplifying
  assumptions as he made them. Limit the scope of a claim, tip your hat to exceptions, and set
  the expectation that epiphany is rare and not seeing it the first time is fine. Avoid
  "obviously" and "clearly." (Extends the Config-talk lesson on discovery versus definition.)

- **Length is not the enemy.** A longer path of rediscovery can give a result more staying
  power. The enemy is verbosity, not length.

## The SoME rubric (a second lens for "is it good?")

His Summer of Math Exposition entries are judged on four criteria (verbatim from the rules):

- **Motivation**: "By the end of the introduction it should be clear why the topic matters and
  why someone should be excited to learn about it."
- **Clarity**: "Jargon should be explained, the goals of the lesson should be easy to
  understand with minimal background knowledge, and the presentation should show care for
  people who might be new to the topic."
- **Novelty**: "The idea doesn't have to be brand new, but the presentation should feel fresh,
  either by breathing new life into a familiar topic, or shining a light on a hidden gem,
  overlooked, or obscure idea that deserves more attention."
- **Memorability**: "Something should make the piece stick with the audience, even months
  later, whether that's the beauty of the presentation, the enthusiasm of the presenter, or a
  mind-blowing 'aha!' moment."

Novelty and Memorability are the two least represented elsewhere in this skill, so weight them.

## Process notes (from interviews)

- **Test the explanation on a real person before you build it.** In the David Perell interview
  Grant says one-on-one conversations or "sample lessons" in the ideation phase are important,
  and that however much he does them, "it's not enough." Watch where a single listener lights
  up or gets confused, then build to that.
- **Problem-solving content and expository content are different.** Grant separates videos that
  solve a problem (the endpoint is known, the script almost writes itself) from expository
  videos (the endpoint is a feeling of understanding, much harder to script). Sample-lesson
  testing matters most for the expository kind.
- **Engagement lives in the interplay of usefulness and story.** His TEDxBerkeley answer to
  "what makes people engage with math" is "neither the usefulness nor the story, but
  understanding the bizarre way that they intertwine." Curiosity-driven math tends to come back
  around usefully (Hardy's number theory becoming cryptography; his block-collision puzzle
  turning out to share math with a quantum search algorithm). Pairs with Config Principle 3.

## Sources

- JMM 2023 JPBM Communications Award lecture, Grant Sanderson: https://youtu.be/UOuxo6SA8Uc
- Summer of Math Exposition rules: https://some.3b1b.co/rules
- David Perell interview "Math for the Masses": https://youtu.be/3cv2UVlTo8g
- TEDxBerkeley "What Makes People Engage With Math": https://youtu.be/s_L-fp8gDzY

## Quick reference

| # | Checklist item | Maps to |
|---|----------------|---------|
| 1 | Motivating example before each definition | explanation-design Principle 2 |
| 2 | Proofs feel rediscoverable | "believe it before you prove it" |
| 3 | Feels personal | principles #12 emotional anchoring |
| 4 | Core ideas have diagrams (also for the author) | the whole skill |
| 5 | Abstractions preceded by concrete examples | principles #1, #10 |
| 6 | Motivating problem before instruction | catalog #15, principles #7 |
| 7 | A reason the audience cares | explanation-design Principle 3 |
