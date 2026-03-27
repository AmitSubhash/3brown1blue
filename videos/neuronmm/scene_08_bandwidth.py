"""Scene 08: The Fundamental Problem.

Highway analogy for the bandwidth bottleneck, LLM utilization reality,
and the two approaches -- motivating custom accelerators.
Duration target: ~75 seconds.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.style import *


class BandwidthBottleneckScene(Scene):
    """Bandwidth bottleneck: highway analogy, utilization, two paths."""

    def construct(self) -> None:
        self.phase_1_highway_analogy()
        self.phase_2_llm_utilization()
        self.phase_3_two_approaches()

    # -- Phase 1: Highway Analogy ----------------------------------------------

    def phase_1_highway_analogy(self) -> None:
        title: Text = section_title("The Fundamental Problem")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # Wide highway: compute lanes
        highway: Rectangle = Rectangle(
            width=9.0, height=2.0,
            color=CHIP_BLUE, fill_opacity=0.12, stroke_width=2,
        )
        highway.move_to(UP * 0.3)

        # Lane lines inside
        lanes: VGroup = VGroup()
        for i in range(1, 6):
            lane: DashedLine = DashedLine(
                LEFT * 4.5 + UP * (0.3 + 1.0 - i * 0.4),
                RIGHT * 4.5 + UP * (0.3 + 1.0 - i * 0.4),
                color=GRAY_D, stroke_width=1, dash_length=0.2,
            )
            lanes.add(lane)

        hw_label: Text = safe_text(
            "Compute Lanes: 312 TFLOPS", font_size=LABEL_SIZE, color=CHIP_BLUE,
        )
        hw_label.next_to(highway, UP, buff=0.15)

        self.play(Create(highway), Create(lanes), Write(hw_label), run_time=1.5)
        self.wait(1)

        # Narrow on-ramp: data highway
        onramp: Rectangle = Rectangle(
            width=1.8, height=0.5,
            color=HBM_PURPLE, fill_opacity=0.2, stroke_width=2,
        )
        onramp.next_to(highway, LEFT, buff=0.0).shift(DOWN * 0.4)

        onramp_label: Text = safe_text(
            "Data On-Ramp: 2 TB/s", font_size=18, color=HBM_PURPLE,
        )
        onramp_label.next_to(onramp, DOWN, buff=0.15)

        self.play(Create(onramp), Write(onramp_label), run_time=1.0)
        self.wait(1.5)

        # Cars (data dots) stuck at on-ramp
        cars_queued: VGroup = VGroup()
        for i in range(8):
            car: Dot = Dot(color=DMA_ORANGE, radius=0.08)
            car.move_to(onramp.get_left() + LEFT * 0.3 + LEFT * i * 0.35)
            cars_queued.add(car)

        # Few cars on the wide highway (mostly empty)
        cars_on_hw: VGroup = VGroup()
        for i in range(3):
            car: Dot = Dot(color=DMA_ORANGE, radius=0.08)
            car.move_to(highway.get_center() + LEFT * 1.5 + RIGHT * i * 2.5)
            cars_on_hw.add(car)

        self.play(
            LaggedStart(*[FadeIn(c, scale=0.5) for c in cars_queued], lag_ratio=0.08),
            LaggedStart(*[FadeIn(c, scale=0.5) for c in cars_on_hw], lag_ratio=0.1),
            run_time=1.2,
        )
        self.wait(1)

        # Annotations
        stuck: Text = safe_text(
            "Data stuck at the on-ramp!", font_size=LABEL_SIZE, color=DANGER_RED,
        )
        stuck.next_to(cars_queued, DOWN, buff=0.3)
        empty: Text = safe_text(
            "Highway mostly empty", font_size=LABEL_SIZE, color=GRAY_B,
        )
        empty.next_to(highway, DOWN, buff=0.6)

        self.play(FadeIn(stuck, shift=UP * 0.1), FadeIn(empty, shift=UP * 0.1), run_time=1.0)
        self.wait(2)

        explain1: Text = safe_text(
            "The GPU can do 312 TRILLION operations per second",
            font_size=BODY_SIZE, color=WHITE,
        )
        explain1.move_to(DOWN * 2.6)
        self.play(FadeIn(explain1, shift=UP * 0.2), run_time=1.0)
        self.wait(2)

        explain2: Text = safe_text(
            "But can only FEED it 2 TB of data per second",
            font_size=BODY_SIZE, color=HBM_PURPLE,
        )
        explain2.move_to(DOWN * 2.6)
        self.play(ReplacementTransform(explain1, explain2), run_time=1.0)
        self.wait(2)

        explain3: Text = safe_text(
            "The on-ramp is the bottleneck, not the highway",
            font_size=BODY_SIZE, color=ACCENT,
        )
        explain3.move_to(DOWN * 2.6)
        self.play(ReplacementTransform(explain2, explain3), run_time=1.0)
        self.wait(2.5)

        fade_all(
            self, title, highway, lanes, hw_label,
            onramp, onramp_label, cars_queued, cars_on_hw,
            stuck, empty, explain3,
        )
        self.wait(0.5)

    # -- Phase 2: LLM Utilization Reality --------------------------------------

    def phase_2_llm_utilization(self) -> None:
        title: Text = section_title("LLM Inference Reality")
        self.play(Write(title), run_time=1.2)
        self.wait(1.5)

        # Utilization meter
        meter_bg: RoundedRectangle = RoundedRectangle(
            width=8.0, height=1.2, corner_radius=0.15,
            color=GRAY_D, fill_opacity=0.15, stroke_width=2,
        )
        meter_bg.move_to(UP * 0.5)

        # 30% fill
        meter_fill: RoundedRectangle = RoundedRectangle(
            width=2.4, height=1.0, corner_radius=0.12,
            color=DANGER_RED, fill_opacity=0.4, stroke_width=0,
        )
        meter_fill.align_to(meter_bg, LEFT).shift(RIGHT * 0.1)
        meter_fill.move_to(
            meter_bg.get_left() + RIGHT * (2.4 / 2 + 0.1),
            coor_mask=np.array([1, 0, 0]),
        )
        meter_fill.set_y(meter_bg.get_y())

        # Percentage label
        pct: Text = safe_text("~30%", font_size=HEADING_SIZE, color=DANGER_RED)
        pct.move_to(meter_fill.get_center())

        # Scale marks
        marks: VGroup = VGroup()
        for frac, label_str in [(0.25, "25%"), (0.5, "50%"), (0.75, "75%"), (1.0, "100%")]:
            x_pos: float = meter_bg.get_left()[0] + 0.1 + frac * 7.8
            mark: Line = Line(
                UP * 0.1 + RIGHT * x_pos,
                DOWN * 0.1 + RIGHT * x_pos,
                color=GRAY, stroke_width=1,
            )
            mark.set_y(meter_bg.get_bottom()[1])
            ml: Text = safe_text(label_str, font_size=14, color=GRAY)
            ml.next_to(mark, DOWN, buff=0.1)
            marks.add(VGroup(mark, ml))

        meter_label: Text = safe_text(
            "GPU Utilization During LLM Inference",
            font_size=BODY_SIZE, color=WHITE,
        )
        meter_label.next_to(meter_bg, UP, buff=0.3)

        self.play(
            Write(meter_label),
            Create(meter_bg),
            FadeIn(marks),
            run_time=1.2,
        )
        self.play(
            GrowFromEdge(meter_fill, LEFT),
            FadeIn(pct),
            run_time=1.5,
        )
        self.wait(2)

        idle_msg: Text = safe_text(
            "70% of the time, the cores are WAITING for data",
            font_size=BODY_SIZE, color=DANGER_RED,
        )
        idle_msg.move_to(DOWN * 1.5)
        self.play(FadeIn(idle_msg, shift=UP * 0.2), run_time=1.2)
        self.wait(2.5)

        need: Text = safe_text(
            "We need: faster memory, or smarter data management",
            font_size=BODY_SIZE, color=ACCENT,
        )
        need.move_to(DOWN * 2.5)
        self.play(FadeIn(need, shift=UP * 0.2), run_time=1.2)
        self.wait(2.5)

        fade_all(
            self, title, meter_bg, meter_fill, pct,
            marks, meter_label, idle_msg, need,
        )
        self.wait(0.5)

    # -- Phase 3: Two Approaches -----------------------------------------------

    def phase_3_two_approaches(self) -> None:
        title: Text = section_title("Two Paths Forward")
        self.play(Write(title), run_time=1.2)
        self.wait(1.5)

        # Left path: faster memory
        left_box: VGroup = labeled_box(
            "Faster Memory", width=3.5, height=1.8,
            color=BASELINE_GRAY, fill_opacity=0.12,
        )
        left_box.move_to(LEFT * 3.0 + UP * 0.2)

        left_desc: VGroup = safe_multiline(
            "Limited by physics",
            "Extremely expensive",
            font_size=LABEL_SIZE, color=GRAY_B,
        )
        left_desc.next_to(left_box, DOWN, buff=0.3)

        # Right path: smarter data management
        right_box: VGroup = labeled_box(
            "Smarter Data Management", width=3.5, height=1.8,
            color=SUCCESS_GREEN, fill_opacity=0.15,
        )
        right_box.move_to(RIGHT * 3.0 + UP * 0.2)

        right_desc: VGroup = safe_multiline(
            "Architectural innovation",
            "This is what NeuronMM does",
            font_size=LABEL_SIZE, color=SUCCESS_GREEN,
        )
        right_desc.next_to(right_box, DOWN, buff=0.3)

        # "OR" in center
        or_text: Text = safe_text("OR", font_size=HEADING_SIZE, color=GRAY)
        or_text.move_to(UP * 0.2)

        self.play(FadeIn(left_box, shift=RIGHT * 0.3), FadeIn(left_desc), run_time=1.2)
        self.play(FadeIn(or_text), run_time=0.5)
        self.play(FadeIn(right_box, shift=LEFT * 0.3), FadeIn(right_desc), run_time=1.2)
        self.wait(2)

        # Highlight right path
        highlight_rect: SurroundingRectangle = SurroundingRectangle(
            VGroup(right_box, right_desc),
            color=SUCCESS_GREEN, buff=0.2, corner_radius=0.15,
            stroke_width=3,
        )
        self.play(
            Create(highlight_rect),
            left_box.animate.set_opacity(DIM_OPACITY),
            left_desc.animate.set_opacity(DIM_OPACITY),
            or_text.animate.set_opacity(DIM_OPACITY),
            run_time=1.2,
        )
        self.wait(1.5)

        question: Text = safe_text(
            "What if we built a chip with MORE control over memory?",
            font_size=BODY_SIZE, color=ACCENT,
        )
        question.move_to(DOWN * 2.2)
        self.play(FadeIn(question, shift=UP * 0.3), run_time=1.2)
        self.wait(2.5)

        note: Text = bottom_note(
            "The key insight: reduce data movement, not just increase compute"
        )
        self.play(
            FadeOut(question),
            FadeIn(note, shift=UP * 0.2),
            run_time=1.0,
        )
        self.wait(3)

        fade_all(
            self, title, left_box, left_desc, or_text,
            right_box, right_desc, highlight_rect, note,
        )
        self.wait(0.5)
