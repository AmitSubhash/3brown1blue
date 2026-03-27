"""Scene 09: AI Accelerators -- TPU, Trainium, and why custom chips exist.

Duration: ~75s
Template: FULL_CENTER
Audience: Curious learner
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class AIAcceleratorsScene(Scene):
    """Introduce custom AI accelerators: TPU, Trainium, and why they exist."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = section_title("Beyond GPUs: AI Accelerators")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # ===== Phase 1: Why custom chips? =====
        gpu_box = labeled_box("GPU", width=3.5, height=1.2, color=BASELINE_GRAY)
        gpu_box.move_to(UP * 1.0)
        self.play(FadeIn(gpu_box, shift=UP * 0.3), run_time=1.2)

        gpu_desc = safe_text(
            "Great at many things", font_size=BODY_SIZE, color=GRAY_B,
        ).next_to(gpu_box, DOWN, buff=0.3)
        self.play(Write(gpu_desc), run_time=1.2)
        self.wait(2)

        # List of GPU capabilities
        capabilities = ["Gaming", "Rendering", "AI math", "Simulation", "Crypto"]
        cap_texts: list[Text] = []
        for i, cap in enumerate(capabilities):
            col = SUCCESS_GREEN if cap == "AI math" else WHITE
            t = safe_text(cap, font_size=LABEL_SIZE, color=col)
            cap_texts.append(t)

        cap_group = VGroup(*cap_texts).arrange(RIGHT, buff=0.5)
        cap_group.next_to(gpu_desc, DOWN, buff=0.4)
        if cap_group.width > SAFE_WIDTH:
            cap_group.scale_to_fit_width(SAFE_WIDTH)
        self.play(
            *[FadeIn(ct, shift=UP * 0.15) for ct in cap_texts],
            run_time=1.3,
        )
        self.wait(2)

        # Question
        question = safe_text(
            "What if we removed everything EXCEPT AI math?",
            font_size=BODY_SIZE, color=ACCENT,
        ).next_to(cap_group, DOWN, buff=0.5)
        self.play(Write(question), run_time=1.5)
        self.wait(2)

        # Cross out non-AI capabilities one by one
        crosses: list[VGroup] = []
        for ct in cap_texts:
            if ct.text != "AI math":
                cross = Cross(ct, stroke_color=DANGER_RED, stroke_width=3)
                crosses.append(cross)

        for cross in crosses:
            self.play(Create(cross), run_time=0.5)
            self.wait(0.3)

        self.wait(2)

        # Conclusion
        accel_text = safe_text(
            "An AI accelerator: one thing, extremely well",
            font_size=BODY_SIZE, color=CHIP_BLUE,
        ).next_to(question, DOWN, buff=0.4)
        self.play(Write(accel_text), run_time=1.5)
        self.wait(3)

        # Fade Phase 1
        fade_all(
            self, gpu_box, gpu_desc, cap_group, question, accel_text,
            *crosses,
        )

        # ===== Phase 2: The landscape =====
        tpu_box = labeled_box(
            "Google TPU", width=3.0, height=1.2, color="#4285F4",
        )
        trainium_box = labeled_box(
            "AWS Trainium", width=3.0, height=1.2, color=CHIP_BLUE,
        )
        custom_box = labeled_box(
            "Custom Silicon", width=3.0, height=1.2, color=BASELINE_GRAY,
        )

        chips = VGroup(tpu_box, trainium_box, custom_box).arrange(RIGHT, buff=0.8)
        chips.move_to(UP * 0.5)

        # Labels underneath
        tpu_sub = safe_text(
            "Google", font_size=18, color=GRAY_B,
        ).next_to(tpu_box, DOWN, buff=0.2)
        trainium_sub = safe_text(
            "Amazon", font_size=18, color=GRAY_B,
        ).next_to(trainium_box, DOWN, buff=0.2)
        custom_sub = safe_text(
            "Apple, Meta, ...", font_size=18, color=GRAY_B,
        ).next_to(custom_box, DOWN, buff=0.2)

        self.play(
            *[FadeIn(c, shift=UP * 0.3) for c in [tpu_box, trainium_box, custom_box]],
            *[FadeIn(s, shift=UP * 0.2) for s in [tpu_sub, trainium_sub, custom_sub]],
            run_time=1.3,
        )
        self.wait(2)

        # Highlight Trainium
        highlight_rect = SurroundingRectangle(
            trainium_box, color=ACCENT, buff=0.15, stroke_width=3,
        )
        self.play(Create(highlight_rect), run_time=1.2)
        self.wait(2)

        # ===== Phase 3: Trainium's pitch =====
        # Fade title to make room
        self.play(FadeOut(title))

        pitch_lines = safe_multiline(
            "95 TFLOPS of AI compute",
            "Similar to an A100 GPU",
            "But at roughly 60% of the cost",
            font_size=BODY_SIZE, color=WHITE, line_buff=0.35,
        ).move_to(DOWN * 1.8)

        for line in pitch_lines:
            self.play(Write(line), run_time=1.2)
            self.wait(1.5)

        self.wait(2)

        # Cost comparison bars
        fade_all(
            self, chips, tpu_sub, trainium_sub, custom_sub,
            highlight_rect, pitch_lines,
        )

        cost_title = safe_text(
            "Cost Comparison", font_size=HEADING_SIZE, color=WHITE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(cost_title), run_time=1.2)

        # GPU bar (taller = more expensive)
        gpu_bar = Rectangle(
            width=2.0, height=3.0,
            color=BASELINE_GRAY, fill_opacity=0.35, stroke_width=2,
        ).move_to(LEFT * 2.0 + DOWN * 0.3)
        gpu_label = safe_text(
            "GPU", font_size=BODY_SIZE, color=BASELINE_GRAY,
        ).next_to(gpu_bar, DOWN, buff=0.2)
        gpu_cost = safe_text(
            "$$", font_size=HEADING_SIZE, color=DANGER_RED,
        ).move_to(gpu_bar)

        # Trainium bar (shorter = cheaper)
        tr_bar = Rectangle(
            width=2.0, height=1.8,
            color=CHIP_BLUE, fill_opacity=0.35, stroke_width=2,
        )
        tr_bar.align_to(gpu_bar, DOWN)
        tr_bar.set_x(RIGHT_X - 1.5)
        tr_label = safe_text(
            "Trainium", font_size=BODY_SIZE, color=CHIP_BLUE,
        ).next_to(tr_bar, DOWN, buff=0.2)
        tr_cost = safe_text(
            "$", font_size=HEADING_SIZE, color=SUCCESS_GREEN,
        ).move_to(tr_bar)

        self.play(
            FadeIn(gpu_bar, shift=UP * 0.3),
            FadeIn(gpu_label),
            FadeIn(gpu_cost),
            FadeIn(tr_bar, shift=UP * 0.3),
            FadeIn(tr_label),
            FadeIn(tr_cost),
            run_time=1.3,
        )
        self.wait(3)

        # Catch line
        catch = safe_text(
            "The catch? Harder to program. That's where NeuronMM helps.",
            font_size=BODY_SIZE, color=ACCENT,
        ).move_to(DOWN * 2.8)
        self.play(Write(catch), run_time=1.5)
        self.wait(3)

        # Bottom note
        note = bottom_note(
            "AI accelerators: sacrifice generality for speed and cost efficiency"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        # Cleanup
        fade_all(
            self, cost_title, gpu_bar, gpu_label, gpu_cost,
            tr_bar, tr_label, tr_cost, catch, note,
        )
