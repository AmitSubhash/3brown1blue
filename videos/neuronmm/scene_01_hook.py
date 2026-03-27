"""Scene 01: Hook -- Chat demo with slow word generation, then speedup reveal.

Duration: ~30s
Template: FULL_CENTER
Audience: Curious learner (no ML/CS background)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class HookScene(Scene):
    """Hook: show AI generating words painfully slowly, then reveal the speedup."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Phase 1: Chat interface -- user message bubble --
        user_bubble = RoundedRectangle(
            width=7.0, height=1.0, corner_radius=0.25,
            color=CHIP_BLUE, fill_opacity=0.15, stroke_width=2,
        ).move_to(UP * 2.0 + LEFT * 0.5)

        user_icon = safe_text("You", font_size=LABEL_SIZE, color=CHIP_BLUE)
        user_icon.next_to(user_bubble, UL, buff=0.1).shift(RIGHT * 0.3)

        prompt_text = safe_text(
            "Explain how rockets work",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(user_bubble)

        self.play(
            FadeIn(user_bubble, shift=DOWN * 0.2),
            FadeIn(user_icon, shift=DOWN * 0.2),
            run_time=0.8,
        )
        self.play(Write(prompt_text), run_time=1.2)
        self.wait(HOLD_SHORT)

        # -- Phase 2: AI responds word by word, painfully slow --
        ai_bubble = RoundedRectangle(
            width=7.0, height=1.0, corner_radius=0.25,
            color=SBUF_GREEN, fill_opacity=0.08, stroke_width=2,
        ).move_to(UP * 0.3 + LEFT * 0.5)

        ai_icon = safe_text("AI", font_size=LABEL_SIZE, color=SBUF_GREEN)
        ai_icon.next_to(ai_bubble, UL, buff=0.1).shift(RIGHT * 0.3)

        self.play(
            FadeIn(ai_bubble, shift=UP * 0.2),
            FadeIn(ai_icon, shift=UP * 0.2),
            run_time=0.6,
        )

        words = ["Rockets", "work", "by", "pushing", "hot", "gas"]
        word_mobjects: list[Text] = []
        x_cursor = ai_bubble.get_left()[0] + 0.5

        for word in words:
            w = safe_text(word, font_size=BODY_SIZE, color=SPEEDUP_YELLOW)
            w.move_to(
                [x_cursor + w.width / 2, ai_bubble.get_center()[1], 0]
            )
            # Clamp to safe bounds
            if w.get_right()[0] > ai_bubble.get_right()[0] - 0.3:
                break
            word_mobjects.append(w)
            self.play(FadeIn(w, shift=UP * 0.1), run_time=0.5)
            self.wait(0.4)
            # Settle to white after appearing
            self.play(w.animate.set_color(WHITE), run_time=0.2)
            x_cursor = w.get_right()[0] + 0.25

        self.wait(HOLD_SHORT)

        # -- Phase 3: "Every word takes millions of calculations" --
        chat_group = VGroup(
            user_bubble, user_icon, prompt_text,
            ai_bubble, ai_icon, *word_mobjects,
        )
        self.play(chat_group.animate.set_opacity(DIM_OPACITY), run_time=0.8)

        line1 = safe_text(
            "Every word takes millions of calculations",
            font_size=HEADING_SIZE, color=WHITE,
        ).move_to(UP * 0.8)
        self.play(Write(line1), run_time=1.5)
        self.wait(HOLD_MEDIUM)

        line2 = safe_text(
            "What if this could be 2.5x faster?",
            font_size=HEADING_SIZE, color=SPEEDUP_YELLOW,
        ).move_to(ORIGIN)
        self.play(Write(line2), run_time=1.5)
        self.wait(HOLD_MEDIUM)

        self.play(FadeOut(line1), FadeOut(line2), FadeOut(chat_group), run_time=0.8)

        # -- Phase 4: Throughput counter animation --
        speed_label = safe_text(
            "Words generated per second",
            font_size=BODY_SIZE, color=BASELINE_GRAY,
        ).move_to(UP * 1.2)

        tracker = ValueTracker(50)
        counter = DecimalNumber(
            50, num_decimal_places=0,
            font_size=72, color=WHITE,
        ).move_to(ORIGIN)
        counter.add_updater(lambda m: m.set_value(tracker.get_value()))

        unit = safe_text("tokens/s", font_size=LABEL_SIZE, color=BASELINE_GRAY)
        unit.next_to(counter, RIGHT, buff=0.3)
        unit.add_updater(lambda m: m.next_to(counter, RIGHT, buff=0.3))

        self.play(
            Write(speed_label),
            FadeIn(counter, shift=UP * 0.2),
            FadeIn(unit, shift=UP * 0.2),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # Animate 50 -> 93
        self.play(
            tracker.animate.set_value(93),
            counter.animate.set_color(SPEEDUP_YELLOW),
            run_time=2.5,
            rate_func=smooth,
        )
        counter.clear_updaters()
        unit.clear_updaters()
        self.wait(HOLD_SHORT)

        # -- Phase 5: Big speedup reveal --
        speedup = safe_text(
            "2.49x faster",
            font_size=56, color=SPEEDUP_YELLOW,
        ).move_to(DOWN * 1.5)

        self.play(FadeIn(speedup, scale=0.8), run_time=1.0)
        self.wait(HOLD_MEDIUM)

        # -- Phase 6: Bottom note --
        note = bottom_note("NeuronMM -- Song et al., 2025")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(self, speed_label, counter, unit, speedup, note)
        self.wait(0.5)
