"""Scene 07: GPU Memory -- The Bottleneck.

Teaches HBM, bandwidth vs compute, and arithmetic intensity.
Duration target: ~90 seconds.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.style import *


class GPUMemoryDeepDiveScene(Scene):
    """HBM deep dive: bandwidth problem, arithmetic intensity."""

    def construct(self) -> None:
        self.phase_1_what_is_hbm()
        self.phase_2_bandwidth_problem()
        self.phase_3_arithmetic_intensity()

    # -- Phase 1: What is HBM? ------------------------------------------------

    def phase_1_what_is_hbm(self) -> None:
        title: Text = section_title("GPU Memory: The Bottleneck")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # GPU chip in center with HBM stacks around it
        gpu_chip: VGroup = labeled_box(
            "GPU Die", width=2.5, height=2.5,
            color=CHIP_BLUE, fill_opacity=0.25,
        )
        gpu_chip.move_to(ORIGIN + UP * 0.2)

        # HBM stacks: 4 tall rectangles around the chip (like towers)
        hbm_stacks: VGroup = VGroup()
        stack_positions: list = [
            LEFT * 2.8, RIGHT * 2.8, UP * 2.3, DOWN * 1.9,
        ]
        for pos in stack_positions:
            # Vertical stack of layers
            stack: VGroup = VGroup()
            for layer in range(4):
                rect: Rectangle = Rectangle(
                    width=0.8, height=0.2,
                    color=HBM_PURPLE, fill_opacity=0.3 + layer * 0.1,
                    stroke_width=1.5,
                )
                rect.move_to(gpu_chip.get_center() + pos + UP * layer * 0.22)
                stack.add(rect)
            hbm_stacks.add(stack)

        self.play(FadeIn(gpu_chip), run_time=1.0)
        self.play(
            LaggedStart(
                *[LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in s], lag_ratio=0.1)
                  for s in hbm_stacks],
                lag_ratio=0.2,
            ),
            run_time=2.0,
        )
        self.wait(1)

        hbm_label: Text = safe_text(
            "HBM = High Bandwidth Memory",
            font_size=BODY_SIZE, color=HBM_PURPLE,
        )
        hbm_label.move_to(DOWN * 2.5)
        self.play(FadeIn(hbm_label, shift=UP * 0.2), run_time=1.0)
        self.wait(2)

        desc1: Text = safe_text(
            "Stacks of memory chips RIGHT NEXT to the GPU",
            font_size=BODY_SIZE, color=GRAY_B,
        )
        desc1.move_to(DOWN * 2.5)
        self.play(ReplacementTransform(hbm_label, desc1), run_time=1.0)
        self.wait(2)

        specs: Text = safe_text(
            "A100: 80 GB of HBM, 2 TB/s bandwidth",
            font_size=BODY_SIZE, color=SPEEDUP_YELLOW,
        )
        specs.move_to(DOWN * 2.5)
        self.play(ReplacementTransform(desc1, specs), run_time=1.0)
        self.wait(2)

        question: Text = safe_text(
            "That sounds fast... but is it enough?",
            font_size=BODY_SIZE, color=WHITE,
        )
        question.move_to(DOWN * 2.5)
        self.play(ReplacementTransform(specs, question), run_time=1.0)
        self.wait(2.5)

        fade_all(self, title, gpu_chip, hbm_stacks, question)
        self.wait(0.5)

    # -- Phase 2: The Bandwidth Problem ----------------------------------------

    def phase_2_bandwidth_problem(self) -> None:
        title: Text = section_title("Compute vs Memory Time")
        self.play(Write(title), run_time=1.2)
        self.wait(1.5)

        # Matrix size context
        matrix_info: Text = safe_text(
            "A 4096x4096 matrix = 64 MB of data (at FP16)",
            font_size=BODY_SIZE, color=GRAY_B,
        )
        matrix_info.move_to(UP * 1.8)
        self.play(Write(matrix_info), run_time=1.2)
        self.wait(2)

        load_info: Text = safe_text(
            "Loading it from HBM takes 0.03 ms",
            font_size=BODY_SIZE, color=HBM_PURPLE,
        )
        load_info.next_to(matrix_info, DOWN, buff=0.4)
        self.play(Write(load_info), run_time=1.2)
        self.wait(1.5)

        compute_info: Text = safe_text(
            "Computing on it takes only 0.02 ms",
            font_size=BODY_SIZE, color=SUCCESS_GREEN,
        )
        compute_info.next_to(load_info, DOWN, buff=0.4)
        self.play(Write(compute_info), run_time=1.2)
        self.wait(2)

        self.play(
            FadeOut(matrix_info), FadeOut(load_info), FadeOut(compute_info),
            run_time=0.8,
        )

        # Dual panel bar comparison
        compute_bar_label: Text = safe_text(
            "Compute time", font_size=LABEL_SIZE, color=SUCCESS_GREEN,
        )
        mem_bar_label: Text = safe_text(
            "Memory time", font_size=LABEL_SIZE, color=DANGER_RED,
        )

        compute_bar: Rectangle = Rectangle(
            width=2.0, height=0.8,
            color=SUCCESS_GREEN, fill_opacity=0.4, stroke_width=2,
        )
        mem_bar: Rectangle = Rectangle(
            width=3.0, height=0.8,
            color=DANGER_RED, fill_opacity=0.4, stroke_width=2,
        )

        compute_bar.move_to(LEFT * 2.5 + UP * 0.3)
        mem_bar.move_to(RIGHT * 2.0 + UP * 0.3)
        compute_bar_label.next_to(compute_bar, UP, buff=0.2)
        mem_bar_label.next_to(mem_bar, UP, buff=0.2)

        compute_val: Text = safe_text("0.02 ms", font_size=LABEL_SIZE, color=WHITE)
        mem_val: Text = safe_text("0.03 ms", font_size=LABEL_SIZE, color=WHITE)
        compute_val.move_to(compute_bar)
        mem_val.move_to(mem_bar)

        self.play(
            Create(compute_bar), Write(compute_bar_label), FadeIn(compute_val),
            run_time=1.0,
        )
        self.play(
            Create(mem_bar), Write(mem_bar_label), FadeIn(mem_val),
            run_time=1.0,
        )
        self.wait(2)

        verdict: Text = safe_text(
            "The GPU finishes computing BEFORE the next data arrives",
            font_size=BODY_SIZE, color=DANGER_RED,
        )
        verdict.move_to(DOWN * 1.0)
        self.play(FadeIn(verdict, shift=UP * 0.2), run_time=1.2)
        self.wait(2)

        # Idle cores visual
        idle_text: Text = safe_text(
            "Cores sit idle, waiting for data",
            font_size=BODY_SIZE, color=GRAY_B,
        )
        idle_text.move_to(DOWN * 2.0)

        idle_cores: VGroup = VGroup()
        for i in range(12):
            d: Dot = Dot(color=GRAY_D, radius=0.1)
            d.move_to(DOWN * 2.8 + LEFT * 2.75 + RIGHT * i * 0.5)
            idle_cores.add(d)

        self.play(Write(idle_text), run_time=1.0)
        self.play(
            LaggedStart(*[FadeIn(d) for d in idle_cores], lag_ratio=0.05),
            run_time=0.8,
        )
        self.wait(2.5)

        fade_all(
            self, title, compute_bar, compute_bar_label, compute_val,
            mem_bar, mem_bar_label, mem_val, verdict, idle_text, idle_cores,
        )
        self.wait(0.5)

    # -- Phase 3: Arithmetic Intensity -----------------------------------------

    def phase_3_arithmetic_intensity(self) -> None:
        title: Text = section_title("Arithmetic Intensity")
        self.play(Write(title), run_time=1.2)
        self.wait(1.5)

        # Definition
        defn: Text = safe_text(
            "We measure this with arithmetic intensity",
            font_size=BODY_SIZE,
        )
        defn.move_to(UP * 1.8)
        self.play(Write(defn), run_time=1.2)
        self.wait(1.5)

        formula: MathTex = MathTex(
            r"\text{AI} = \frac{\text{FLOPs (math done)}}{\text{Bytes moved}}",
            font_size=EQ_SIZE,
        )
        formula.move_to(UP * 0.6)
        self.play(Write(formula), run_time=1.5)
        self.wait(2.5)

        # Two outcomes
        high_ai: VGroup = VGroup(
            safe_text("High AI", font_size=HEADING_SIZE, color=SUCCESS_GREEN),
            safe_text("Compute-bound (good!)", font_size=LABEL_SIZE, color=GRAY_B),
            safe_text("GPU cores stay busy", font_size=LABEL_SIZE, color=SUCCESS_GREEN),
        ).arrange(DOWN, buff=0.15)
        high_ai.move_to(LEFT * 3.0 + DOWN * 1.2)

        low_ai: VGroup = VGroup(
            safe_text("Low AI", font_size=HEADING_SIZE, color=DANGER_RED),
            safe_text("Memory-bound (bad!)", font_size=LABEL_SIZE, color=GRAY_B),
            safe_text("Cores waiting for data", font_size=LABEL_SIZE, color=DANGER_RED),
        ).arrange(DOWN, buff=0.15)
        low_ai.move_to(RIGHT * 3.0 + DOWN * 1.2)

        self.play(FadeIn(high_ai, shift=UP * 0.3), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(low_ai, shift=UP * 0.3), run_time=1.0)
        self.wait(2)

        # Highlight the key takeaway
        takeaway: Text = safe_text(
            "LLM inference is MEMORY-BOUND",
            font_size=HEADING_SIZE, color=DANGER_RED,
        )
        takeaway.move_to(DOWN * 2.8)
        self.play(
            FadeIn(takeaway, shift=UP * 0.3),
            low_ai[0].animate.set_color(SPEEDUP_YELLOW),
            run_time=1.2,
        )
        self.wait(2)

        self.play(FadeOut(takeaway), run_time=0.5)

        note: Text = bottom_note(
            "Arithmetic intensity: the ratio of computation to memory access"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.0)
        self.wait(3)

        fade_all(self, title, defn, formula, high_ai, low_ai, note)
        self.wait(0.5)
