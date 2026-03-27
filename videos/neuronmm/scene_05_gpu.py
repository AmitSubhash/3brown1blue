"""Scene 05: Enter the GPU.

Teaches what a GPU is, why it's faster than a CPU for parallel workloads,
and how data flows through the GPU memory hierarchy.
Duration target: ~120 seconds.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.style import *


class EnterTheGPUScene(Scene):
    """GPU introduction: single vs parallel, architecture, data flow."""

    def construct(self) -> None:
        self.phase_1_key_idea()
        self.phase_2_parallel_processing()
        self.phase_3_gpu_data_flow()

    # -- Phase 1: The Key Idea ------------------------------------------------

    def phase_1_key_idea(self) -> None:
        title: Text = section_title("Enter the GPU")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # CPU: one worker doing one task
        cpu_label: Text = safe_text("CPU", font_size=HEADING_SIZE, color=CHIP_BLUE)
        cpu_label.move_to(ORIGIN + UP * 1.0)
        cpu_box: RoundedRectangle = RoundedRectangle(
            width=2.0, height=2.0, corner_radius=0.15,
            color=CHIP_BLUE, fill_opacity=0.15, stroke_width=2,
        )
        cpu_box.move_to(ORIGIN + DOWN * 0.5)
        cpu_core: Dot = Dot(color=CHIP_BLUE, radius=0.2)
        cpu_core.move_to(cpu_box.get_center())

        self.play(FadeIn(cpu_label), Create(cpu_box), run_time=1.2)
        self.play(FadeIn(cpu_core, scale=0.5), run_time=0.8)

        cpu_desc: Text = safe_text(
            "One powerful worker, one task at a time",
            font_size=BODY_SIZE, color=GRAY_B,
        )
        cpu_desc.next_to(cpu_box, DOWN, buff=0.4)
        self.play(Write(cpu_desc), run_time=1.2)
        self.wait(2)

        # Transition question
        question: Text = safe_text(
            "What if we had THOUSANDS of workers?",
            font_size=HEADING_SIZE, color=ACCENT,
        )
        question.move_to(ORIGIN)
        self.play(
            FadeOut(cpu_label), FadeOut(cpu_box),
            FadeOut(cpu_core), FadeOut(cpu_desc),
            run_time=0.8,
        )
        self.play(FadeIn(question, shift=UP * 0.3), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(question), run_time=0.8)

        # GPU: grid of many small cores
        gpu_label: Text = safe_text("GPU", font_size=HEADING_SIZE, color=SUCCESS_GREEN)
        gpu_label.move_to(UP * 2.2)
        gpu_box: RoundedRectangle = RoundedRectangle(
            width=5.0, height=4.0, corner_radius=0.2,
            color=SUCCESS_GREEN, fill_opacity=0.08, stroke_width=2,
        )
        gpu_box.move_to(DOWN * 0.2)

        # 10x10 grid of tiny dots
        cores: VGroup = VGroup()
        for row in range(10):
            for col in range(10):
                dot: Dot = Dot(
                    color=interpolate_color(ManimColor(CHIP_BLUE), ManimColor(SUCCESS_GREEN), col / 9),
                    radius=0.08,
                )
                dot.move_to(
                    gpu_box.get_center()
                    + LEFT * 2.0 + RIGHT * col * 0.44
                    + UP * 1.6 + DOWN * row * 0.36
                )
                cores.add(dot)

        self.play(FadeIn(gpu_label), Create(gpu_box), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in cores], lag_ratio=0.005), run_time=2.0)
        self.wait(1.5)

        gpu_desc: Text = safe_text(
            "A GPU has thousands of tiny processors called CUDA cores",
            font_size=BODY_SIZE, color=GRAY_B,
        )
        gpu_desc.next_to(gpu_box, DOWN, buff=0.3)
        self.play(Write(gpu_desc), run_time=1.5)
        self.wait(2)

        a100_label: Text = safe_text(
            "NVIDIA A100: 6,912 CUDA cores",
            font_size=LABEL_SIZE, color=SPEEDUP_YELLOW,
        )
        a100_label.next_to(gpu_desc, DOWN, buff=0.25)
        self.play(FadeIn(a100_label, shift=UP * 0.2), run_time=1.0)
        self.wait(2.5)

        fade_all(self, title, gpu_label, gpu_box, cores, gpu_desc, a100_label)
        self.wait(0.5)

    # -- Phase 2: Parallel Processing Visual -----------------------------------

    def phase_2_parallel_processing(self) -> None:
        title: Text = section_title("Parallel Processing")
        self.play(Write(title), run_time=1.2)
        self.wait(1.5)

        # Dual panel layout
        left_label: Text = safe_text("CPU", font_size=HEADING_SIZE, color=CHIP_BLUE)
        left_label.move_to(LEFT_X * UP * 0 + UP * 2.0 + LEFT * 3.0)
        right_label: Text = safe_text("GPU", font_size=HEADING_SIZE, color=SUCCESS_GREEN)
        right_label.move_to(UP * 2.0 + RIGHT * 3.0)

        divider: Line = Line(UP * 2.5, DOWN * 2.0, color=GRAY, stroke_width=1)
        self.play(FadeIn(left_label), FadeIn(right_label), Create(divider), run_time=1.0)

        # CPU side: 8 dots in a column, light up one at a time
        cpu_dots: VGroup = VGroup()
        for i in range(8):
            d: Dot = Dot(color=GRAY_D, radius=0.12)
            d.move_to(LEFT * 3.0 + UP * 1.2 + DOWN * i * 0.45)
            cpu_dots.add(d)
        self.play(LaggedStart(*[FadeIn(d) for d in cpu_dots], lag_ratio=0.05), run_time=0.8)

        cpu_note: Text = safe_text(
            "One multiply at a time",
            font_size=LABEL_SIZE, color=GRAY_B,
        )
        cpu_note.move_to(LEFT * 3.0 + DOWN * 2.6)

        # GPU side: 8x8 grid, light up rows at once
        gpu_dots: VGroup = VGroup()
        for row in range(8):
            for col in range(8):
                d: Dot = Dot(color=GRAY_D, radius=0.08)
                d.move_to(
                    RIGHT * 1.5 + RIGHT * col * 0.38
                    + UP * 1.2 + DOWN * row * 0.38
                )
                gpu_dots.add(d)
        self.play(LaggedStart(*[FadeIn(d) for d in gpu_dots], lag_ratio=0.003), run_time=0.8)

        gpu_note: Text = safe_text(
            "Thousands at once",
            font_size=LABEL_SIZE, color=GRAY_B,
        )
        gpu_note.move_to(RIGHT * 3.0 + DOWN * 2.6)
        self.play(Write(cpu_note), Write(gpu_note), run_time=1.0)

        # Animate CPU: sequential
        for i in range(8):
            self.play(
                cpu_dots[i].animate.set_color(CHIP_BLUE),
                run_time=0.25,
            )

        # Animate GPU: row-by-row (all at once per row)
        for row in range(8):
            row_dots = [gpu_dots[row * 8 + col] for col in range(8)]
            self.play(
                *[d.animate.set_color(SUCCESS_GREEN) for d in row_dots],
                run_time=0.15,
            )

        self.wait(2)

        # Timer comparison
        cpu_time: Text = safe_text(
            "CPU: ~16 million steps",
            font_size=BODY_SIZE, color=DANGER_RED,
        )
        gpu_time: Text = safe_text(
            "GPU: ~16 thousand steps",
            font_size=BODY_SIZE, color=SUCCESS_GREEN,
        )
        cpu_time.move_to(LEFT * 3.0 + DOWN * 1.8)
        gpu_time.move_to(RIGHT * 3.0 + DOWN * 1.8)
        self.play(FadeIn(cpu_time, shift=UP * 0.2), FadeIn(gpu_time, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        summary: Text = safe_text(
            "The GPU does THOUSANDS of multiplications at once",
            font_size=BODY_SIZE, color=WHITE,
        )
        summary.move_to(DOWN * 3.0)
        self.play(FadeIn(summary, shift=UP * 0.2), run_time=1.0)
        self.wait(2)

        fade_all(
            self, title, left_label, right_label, divider,
            cpu_dots, gpu_dots, cpu_note, gpu_note,
            cpu_time, gpu_time, summary,
        )
        self.wait(0.5)

    # -- Phase 3: GPU Data Flow ------------------------------------------------

    def phase_3_gpu_data_flow(self) -> None:
        title: Text = section_title("Inside the GPU")
        self.play(Write(title), run_time=1.2)
        self.wait(1.5)

        # Build architecture diagram -- layered from outer (HBM) to inner (cores)
        # HBM: big box
        hbm: VGroup = labeled_box(
            "HBM (GPU Memory)", width=10.0, height=5.0,
            color=HBM_PURPLE, fill_opacity=0.08,
        )
        hbm.move_to(DOWN * 0.3)
        hbm_cap: Text = safe_text("80 GB, off-chip", font_size=18, color=GRAY_B)
        hbm_cap.next_to(hbm[0], UP, buff=0.1).shift(RIGHT * 2.5)

        # L2 cache: medium box inside HBM
        l2: VGroup = labeled_box(
            "L2 Cache", width=8.0, height=3.6,
            color=SBUF_GREEN, fill_opacity=0.1,
        )
        l2.move_to(DOWN * 0.5)
        l2_cap: Text = safe_text("40 MB, shared", font_size=18, color=GRAY_B)
        l2_cap.next_to(l2[0], UP, buff=0.1).shift(RIGHT * 2.0)

        # SMs: 4 small boxes inside L2
        sms: VGroup = VGroup()
        sm_positions: list = [LEFT * 2.5, LEFT * 0.8, RIGHT * 0.8, RIGHT * 2.5]
        for i, pos in enumerate(sm_positions):
            sm: VGroup = labeled_box(
                f"SM {i}", width=1.4, height=2.0,
                color=CHIP_BLUE, fill_opacity=0.15, font_size=18,
            )
            sm.move_to(DOWN * 0.7 + pos)

            # CUDA cores inside each SM: 3x2 tiny dots
            core_group: VGroup = VGroup()
            for r in range(3):
                for c in range(2):
                    dot: Dot = Dot(color=CHIP_BLUE, radius=0.05)
                    dot.move_to(
                        sm.get_center() + DOWN * 0.15
                        + LEFT * 0.2 + RIGHT * c * 0.4
                        + UP * 0.35 + DOWN * r * 0.35
                    )
                    core_group.add(dot)

            # Shared memory label at bottom of SM
            smem: Text = safe_text("SRAM", font_size=14, color=PSUM_TEAL)
            smem.next_to(sm[0], DOWN, buff=-0.35)

            sms.add(VGroup(sm, core_group, smem))

        # Animate building the diagram layer by layer
        self.play(Create(hbm[0]), Write(hbm[1]), FadeIn(hbm_cap), run_time=1.5)
        self.wait(1)
        self.play(Create(l2[0]), Write(l2[1]), FadeIn(l2_cap), run_time=1.2)
        self.wait(1)

        for sm_group in sms:
            self.play(
                Create(sm_group[0][0]), Write(sm_group[0][1]),
                LaggedStart(*[FadeIn(d, scale=0.3) for d in sm_group[1]], lag_ratio=0.05),
                FadeIn(sm_group[2]),
                run_time=0.8,
            )
        self.wait(2)

        # Speed labels
        speed_labels: list = [
            ("slow", HBM_PURPLE, hbm[0].get_bottom() + DOWN * 0.05 + LEFT * 3.5),
            ("fast", SBUF_GREEN, l2[0].get_top() + UP * 0.05 + LEFT * 2.8),
            ("very fast", CHIP_BLUE, sms[0][0][0].get_top() + UP * 0.2),
        ]
        speed_texts: VGroup = VGroup()
        for label_str, col, pos in speed_labels:
            st: Text = safe_text(label_str, font_size=16, color=col)
            st.move_to(pos)
            speed_texts.add(st)

        # Animate data flow: dot traveling from HBM -> L2 -> SM -> cores
        data_dot: Dot = Dot(color=DMA_ORANGE, radius=0.1)
        data_dot.move_to(hbm[0].get_left() + RIGHT * 0.3)

        self.play(FadeIn(data_dot, scale=0.3), run_time=0.5)

        # HBM -> L2
        self.play(
            data_dot.animate.move_to(l2[0].get_left() + RIGHT * 0.3),
            FadeIn(speed_texts[0], shift=UP * 0.1),
            run_time=1.5,
        )
        # L2 -> SM
        self.play(
            data_dot.animate.move_to(sms[1][0].get_top() + DOWN * 0.2),
            FadeIn(speed_texts[1], shift=UP * 0.1),
            run_time=1.0,
        )
        # SM -> cores (light up)
        self.play(
            data_dot.animate.move_to(sms[1][1][2].get_center()),
            FadeIn(speed_texts[2], shift=UP * 0.1),
            run_time=0.8,
        )
        # Cores light up
        self.play(
            *[d.animate.set_color(SPEEDUP_YELLOW) for d in sms[1][1]],
            run_time=0.6,
        )
        self.wait(1)
        # Cores dim back
        self.play(
            *[d.animate.set_color(CHIP_BLUE) for d in sms[1][1]],
            FadeOut(data_dot),
            run_time=0.6,
        )
        self.wait(1.5)

        power_text: Text = safe_text(
            "The GPU's power comes from parallelism",
            font_size=BODY_SIZE, color=WHITE,
        )
        power_text.move_to(DOWN * 3.0)
        self.play(FadeIn(power_text, shift=UP * 0.2), run_time=1.0)
        self.wait(2)
        self.play(FadeOut(power_text), run_time=0.5)

        note: Text = bottom_note("GPUs: thousands of cores working in parallel on matrix math")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.0)
        self.wait(3)

        fade_all(
            self, title, hbm, hbm_cap, l2, l2_cap,
            sms, speed_texts, note,
        )
        self.wait(0.5)
