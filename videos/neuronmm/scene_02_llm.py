"""Scene 02: What is an LLM -- autocomplete analogy, word-by-word generation.

Duration: ~75s
Template: BUILD_UP
Audience: Curious learner (no ML/CS background)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class WhatIsLLMScene(Scene):
    """Teach what an LLM does: autocomplete on steroids, one word at a time."""

    def _phone_key(
        self,
        label: str,
        width: float = 1.4,
        height: float = 0.6,
        color: str = BASELINE_GRAY,
    ) -> VGroup:
        """Create a phone-keyboard-style suggestion pill."""
        pill = RoundedRectangle(
            width=width, height=height, corner_radius=0.15,
            color=color, fill_opacity=0.15, stroke_width=2,
        )
        txt = safe_text(label, font_size=LABEL_SIZE, color=color)
        txt.move_to(pill)
        if txt.width > width - 0.2:
            txt.scale_to_fit_width(width - 0.2)
        return VGroup(pill, txt)

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "How AI Chatbots Work",
            font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(title), run_time=1.2)
        self.wait(HOLD_MEDIUM)

        # =====================================================
        # Phase 1: The autocomplete analogy
        # =====================================================
        phone_frame = RoundedRectangle(
            width=5.0, height=2.2, corner_radius=0.3,
            color=BASELINE_GRAY, fill_opacity=0.05, stroke_width=2,
        ).move_to(UP * 0.8)

        phone_label = safe_text(
            "Your phone keyboard",
            font_size=LABEL_SIZE, color=BASELINE_GRAY,
        ).next_to(phone_frame, UP, buff=0.2)

        typed_word = safe_text(
            "How",
            font_size=HEADING_SIZE, color=WHITE,
        ).move_to(phone_frame.get_center() + UP * 0.4)

        self.play(
            FadeIn(phone_frame, shift=UP * 0.2),
            FadeIn(phone_label),
            run_time=1.0,
        )
        self.play(Write(typed_word), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Autocomplete suggestions
        sug_are = self._phone_key("are", color=SBUF_GREEN)
        sug_about = self._phone_key("about", color=SBUF_GREEN)
        sug_do = self._phone_key("do", color=SBUF_GREEN)
        suggestions = VGroup(sug_are, sug_about, sug_do).arrange(
            RIGHT, buff=0.3,
        ).move_to(phone_frame.get_center() + DOWN * 0.4)

        self.play(
            FadeIn(sug_are, shift=UP * 0.1),
            FadeIn(sug_about, shift=UP * 0.1),
            FadeIn(sug_do, shift=UP * 0.1),
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        # Explanation line
        analogy_text = safe_multiline(
            "Your phone predicts the next word.",
            "AI chatbots do the same thing -- but MUCH better.",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(DOWN * 1.5)

        self.play(Write(analogy_text[0]), run_time=1.2)
        self.wait(HOLD_SHORT)
        self.play(Write(analogy_text[1]), run_time=1.5)
        self.wait(HOLD_LONG)

        # Fade Phase 1
        phone_group = VGroup(
            phone_frame, phone_label, typed_word,
            suggestions, analogy_text,
        )
        self.play(FadeOut(phone_group), run_time=0.8)

        # =====================================================
        # Phase 2: Word-by-word generation demo
        # =====================================================
        prompt_label = safe_text(
            "Prompt:", font_size=LABEL_SIZE, color=BASELINE_GRAY,
        ).move_to(UP * 2.0 + LEFT * 4.5)

        prompt = safe_text(
            "The capital of France is",
            font_size=BODY_SIZE, color=WHITE,
        )
        prompt.next_to(prompt_label, RIGHT, buff=0.3)

        self.play(
            FadeIn(prompt_label),
            Write(prompt),
            run_time=1.2,
        )
        self.wait(HOLD_SHORT)

        # AI "thinking" indicator
        think_circle = Circle(
            radius=0.35, color=DMA_ORANGE,
            fill_opacity=0.15, stroke_width=2,
        ).move_to(UP * 0.5)
        think_label = safe_text(
            "thinking...", font_size=LABEL_SIZE, color=DMA_ORANGE,
        ).next_to(think_circle, RIGHT, buff=0.2)

        self.play(
            FadeIn(think_circle, scale=0.5),
            FadeIn(think_label),
            run_time=0.6,
        )
        # Pulse the thinking circle
        self.play(
            think_circle.animate.scale(1.3).set_opacity(0.3),
            run_time=0.8,
            rate_func=there_and_back,
        )

        # Output word
        output1 = safe_text(
            "Paris",
            font_size=42, color=SPEEDUP_YELLOW,
        ).move_to(DOWN * 0.5)

        self.play(
            FadeOut(think_circle), FadeOut(think_label),
            FadeIn(output1, scale=0.7),
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        # Second round
        prompt2_text = safe_text(
            "Paris is known for the",
            font_size=BODY_SIZE, color=WHITE,
        )
        prompt2_text.next_to(prompt_label, RIGHT, buff=0.3)

        self.play(
            FadeOut(prompt), FadeOut(output1),
            run_time=0.5,
        )
        self.play(Write(prompt2_text), run_time=1.0)

        # Think again
        think_circle2 = think_circle.copy().move_to(UP * 0.5)
        think_label2 = safe_text(
            "thinking...", font_size=LABEL_SIZE, color=DMA_ORANGE,
        ).next_to(think_circle2, RIGHT, buff=0.2)

        self.play(
            FadeIn(think_circle2, scale=0.5),
            FadeIn(think_label2),
            run_time=0.6,
        )
        self.play(
            think_circle2.animate.scale(1.3).set_opacity(0.3),
            run_time=0.8,
            rate_func=there_and_back,
        )

        output2 = safe_text(
            "Eiffel",
            font_size=42, color=SPEEDUP_YELLOW,
        ).move_to(DOWN * 0.5)

        self.play(
            FadeOut(think_circle2), FadeOut(think_label2),
            FadeIn(output2, scale=0.7),
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        key_insight = safe_text(
            "It predicts ONE word at a time, millions of times",
            font_size=BODY_SIZE, color=SPEEDUP_YELLOW,
        ).move_to(DOWN * 1.8)

        self.play(Write(key_insight), run_time=1.5)
        self.wait(HOLD_LONG)

        # Fade Phase 2
        self.play(
            FadeOut(prompt_label), FadeOut(prompt2_text),
            FadeOut(output2), FadeOut(key_insight),
            run_time=0.8,
        )

        # =====================================================
        # Phase 3: What's inside the "thinking"
        # =====================================================
        self.play(FadeOut(title), run_time=0.5)

        zoom_title = safe_text(
            "What happens inside the AI's brain?",
            font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(zoom_title), run_time=1.2)
        self.wait(HOLD_SHORT)

        # Simple pipeline: Input -> [Giant Math] -> Output
        input_box = labeled_box(
            "Words In", width=2.0, height=0.9,
            color=MATRIX_X, font_size=LABEL_SIZE,
        ).move_to(LEFT * 4.0)

        math_box = labeled_box(
            "Giant Math", width=3.0, height=1.2,
            color=DMA_ORANGE, font_size=BODY_SIZE,
            fill_opacity=0.25,
        ).move_to(ORIGIN)

        output_box = labeled_box(
            "Next Word", width=2.0, height=0.9,
            color=SBUF_GREEN, font_size=LABEL_SIZE,
        ).move_to(RIGHT * 4.0)

        arrow1 = pipeline_arrow(input_box, math_box, color=WHITE)
        arrow2 = pipeline_arrow(math_box, output_box, color=WHITE)

        self.play(
            FadeIn(input_box, shift=RIGHT * 0.2),
            run_time=0.8,
        )
        self.play(
            Create(arrow1),
            FadeIn(math_box, shift=RIGHT * 0.2),
            run_time=0.8,
        )
        self.play(
            Create(arrow2),
            FadeIn(output_box, shift=RIGHT * 0.2),
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        # Label the math
        matmul_label = safe_text(
            "Matrix Multiplication",
            font_size=BODY_SIZE, color=SPEEDUP_YELLOW,
        ).next_to(math_box, DOWN, buff=0.4)

        self.play(Write(matmul_label), run_time=1.2)
        self.wait(HOLD_MEDIUM)

        every_word = safe_multiline(
            "And it happens for",
            "EVERY. SINGLE. WORD.",
            font_size=BODY_SIZE, color=DANGER_RED,
        ).move_to(DOWN * 2.2)

        self.play(Write(every_word[0]), run_time=1.0)
        self.wait(0.5)
        self.play(Write(every_word[1]), run_time=1.5)
        self.wait(HOLD_LONG)

        # -- Bottom note --
        note = bottom_note(
            "Large Language Models: AI systems that predict the next word"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(
            self, zoom_title, input_box, math_box, output_box,
            arrow1, arrow2, matmul_label, every_word, note,
        )
        self.wait(0.5)
