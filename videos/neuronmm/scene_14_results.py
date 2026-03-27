"""Scene 14: Results -- how much faster, and does quality hold up?

Duration target: ~75s
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class ResultsScene(Scene):
    def construct(self) -> None:
        # ---- Title ----
        title = section_title("How Much Faster?")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # ==================================================================
        # Phase 1 -- Speed comparison with animated bars
        # ==================================================================
        self.play(FadeOut(title))

        bar_width = 8.0
        bar_height = 0.6

        # Standard bar
        std_bg = RoundedRectangle(
            width=bar_width, height=bar_height, corner_radius=0.1,
            color=BASELINE_GRAY, fill_opacity=0.1, stroke_width=2,
        ).shift(UP * 1.0)
        std_label = safe_text("Standard", font_size=LABEL_SIZE, color=BASELINE_GRAY)
        std_label.next_to(std_bg, LEFT, buff=0.3)
        std_speed = safe_text("1x speed", font_size=LABEL_SIZE, color=BASELINE_GRAY)
        std_speed.next_to(std_bg, RIGHT, buff=0.3)

        # NeuronMM bar
        nmm_bg = RoundedRectangle(
            width=bar_width, height=bar_height, corner_radius=0.1,
            color=SPEEDUP_YELLOW, fill_opacity=0.1, stroke_width=2,
        ).shift(DOWN * 0.5)
        nmm_label = safe_text("NeuronMM", font_size=LABEL_SIZE, color=SPEEDUP_YELLOW)
        nmm_label.next_to(nmm_bg, LEFT, buff=0.3)

        self.play(
            FadeIn(std_bg), FadeIn(std_label), FadeIn(std_speed),
            FadeIn(nmm_bg), FadeIn(nmm_label),
            run_time=1.2,
        )
        self.wait(1.5)

        # Fill bars simultaneously
        # Standard fills to 40% (1x), NeuronMM fills to 100% (2.49x)
        std_fill = RoundedRectangle(
            width=0.01, height=bar_height - 0.1, corner_radius=0.08,
            color=BASELINE_GRAY, fill_opacity=0.5, stroke_width=0,
        ).align_to(std_bg, LEFT).shift(RIGHT * 0.05)

        nmm_fill = RoundedRectangle(
            width=0.01, height=bar_height - 0.1, corner_radius=0.08,
            color=SPEEDUP_YELLOW, fill_opacity=0.5, stroke_width=0,
        ).align_to(nmm_bg, LEFT).shift(RIGHT * 0.05)

        self.add(std_fill, nmm_fill)

        std_target_width = bar_width * 0.40
        nmm_target_width = bar_width * 0.98

        std_fill_final = RoundedRectangle(
            width=std_target_width, height=bar_height - 0.1, corner_radius=0.08,
            color=BASELINE_GRAY, fill_opacity=0.5, stroke_width=0,
        ).align_to(std_bg, LEFT).shift(RIGHT * 0.05)

        nmm_fill_final = RoundedRectangle(
            width=nmm_target_width, height=bar_height - 0.1, corner_radius=0.08,
            color=SPEEDUP_YELLOW, fill_opacity=0.5, stroke_width=0,
        ).align_to(nmm_bg, LEFT).shift(RIGHT * 0.05)

        self.play(
            Transform(std_fill, std_fill_final),
            Transform(nmm_fill, nmm_fill_final),
            run_time=3.0,
            rate_func=linear,
        )

        # Flash result
        flash_txt = safe_text(
            "2.49x faster!",
            font_size=TITLE_SIZE, color=SPEEDUP_YELLOW,
        ).shift(DOWN * 2.2)
        self.play(FadeIn(flash_txt, scale=1.3), run_time=1.2)

        nmm_speed = safe_text("2.49x speed", font_size=LABEL_SIZE, color=SPEEDUP_YELLOW)
        nmm_speed.next_to(nmm_bg, RIGHT, buff=0.3)
        self.play(FadeIn(nmm_speed), run_time=0.8)
        self.wait(3)

        # Clean up phase 1
        phase1 = VGroup(
            std_bg, std_label, std_speed, std_fill,
            nmm_bg, nmm_label, nmm_speed, nmm_fill,
            flash_txt,
        )
        self.play(FadeOut(phase1), run_time=1.2)

        # ==================================================================
        # Phase 2 -- What that means in practice
        # ==================================================================
        practice_title = safe_text(
            "What That Means In Practice",
            font_size=HEADING_SIZE, color=ACCENT,
        ).to_edge(UP, buff=0.5)
        self.play(Write(practice_title), run_time=1.2)

        # Two chat windows side by side
        def chat_window(
            header: str, words: str, header_color: str, x_pos: float
        ) -> VGroup:
            bg = RoundedRectangle(
                width=4.5, height=3.0, corner_radius=0.2,
                color=header_color, fill_opacity=0.08, stroke_width=2,
            ).shift(RIGHT * x_pos)
            h = safe_text(header, font_size=HEADING_SIZE, color=header_color)
            h.next_to(bg, UP, buff=0.15)
            w = safe_text(words, font_size=BODY_SIZE, color=header_color)
            w.move_to(bg)
            return VGroup(bg, h, w)

        before_win = chat_window("Before", "~50 words/sec", BASELINE_GRAY, -2.8)
        after_win = chat_window("After", "~93 words/sec", SPEEDUP_YELLOW, 2.8)

        self.play(FadeIn(before_win), run_time=1.2)
        self.wait(1.5)
        self.play(FadeIn(after_win), run_time=1.2)
        self.wait(2)

        double_txt = safe_text(
            "Nearly DOUBLE the speed of generating text",
            font_size=BODY_SIZE, color=WHITE,
        ).shift(DOWN * 2.5)
        self.play(Write(double_txt), run_time=1.3)
        self.wait(2)

        # Animated counter 50 -> 93
        counter_val = ValueTracker(50)
        counter_display = always_redraw(
            lambda: safe_text(
                f"{int(counter_val.get_value())} words/sec",
                font_size=TITLE_SIZE, color=SPEEDUP_YELLOW,
            ).shift(DOWN * 0.5)
        )
        self.add(counter_display)
        self.play(counter_val.animate.set_value(93), run_time=2.0, rate_func=smooth)
        self.wait(2)

        phase2 = VGroup(practice_title, before_win, after_win, double_txt)
        self.remove(counter_display)
        self.play(FadeOut(phase2), FadeOut(counter_display), run_time=1.2)

        # ==================================================================
        # Phase 3 -- Does quality suffer?
        # ==================================================================
        quality_title = safe_text(
            "Critical question: is the AI still as smart?",
            font_size=HEADING_SIZE, color=ACCENT,
        ).to_edge(UP, buff=0.5)
        self.play(Write(quality_title), run_time=1.3)
        self.wait(2)

        # 4 model cards
        model_names = ["Llama 1B", "Llama 3B", "Qwen 1.7B", "Qwen 4B"]
        cards = VGroup()
        for name in model_names:
            card_bg = RoundedRectangle(
                width=2.4, height=2.0, corner_radius=0.15,
                color=CHIP_BLUE, fill_opacity=0.1, stroke_width=2,
            )
            model_lbl = safe_text(name, font_size=LABEL_SIZE, color=CHIP_BLUE)
            model_lbl.next_to(card_bg.get_top(), DOWN, buff=0.3)
            check = Text("✓", font_size=36, color=SUCCESS_GREEN)
            check.move_to(card_bg.get_center())
            delta = safe_text("< 0.1% change", font_size=16, color=GRAY_B)
            delta.next_to(card_bg.get_bottom(), UP, buff=0.25)
            cards.add(VGroup(card_bg, model_lbl, check, delta))

        cards.arrange(RIGHT, buff=0.3).next_to(quality_title, DOWN, buff=0.7)
        # Ensure cards fit in safe width
        if cards.width > SAFE_WIDTH:
            cards.scale_to_fit_width(SAFE_WIDTH)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.2),
            run_time=1.5,
        )
        self.wait(2)

        yes_txt = safe_text(
            "Yes! Less than 0.1% accuracy difference",
            font_size=BODY_SIZE, color=SUCCESS_GREEN,
        ).next_to(cards, DOWN, buff=0.5)
        self.play(Write(yes_txt), run_time=1.3)
        self.wait(2)

        smart_txt = safe_text(
            "The AI is just as smart, but much faster",
            font_size=BODY_SIZE, color=WHITE,
        ).next_to(yes_txt, DOWN, buff=0.3)
        self.play(Write(smart_txt), run_time=1.3)
        self.wait(2)

        note = bottom_note("Tested on 4 AI models across 9 different tasks")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        fade_all(self, quality_title, cards, yes_txt, smart_txt, note)
        self.wait(0.5)
