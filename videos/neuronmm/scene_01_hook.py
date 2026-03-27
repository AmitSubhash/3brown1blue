"""Scene 01: Hook -- NeuronMM title reveal and key speedup result.

Duration: ~45s
Template: FULL_CENTER
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class HookScene(Scene):
    """Paper hook: title, animated throughput counter, 2.49x speedup."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Phase 1: Title reveal --
        title = safe_text(
            "NeuronMM",
            font_size=56,
            color=CHIP_BLUE,
        ).move_to(UP * TITLE_Y)

        subtitle = safe_text(
            "High-Performance Matmul for LLM Inference",
            font_size=HEADING_SIZE,
            color=WHITE,
        ).next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.2)
        self.play(Write(subtitle), run_time=1.5)
        self.wait(HOLD_MEDIUM)

        # -- Phase 2: Transition -- fade title group up, prepare result area --
        self.play(
            title.animate.scale(0.7).move_to(UP * 3.0),
            FadeOut(subtitle, shift=UP * 0.3),
            run_time=1.0,
        )

        # -- Phase 3: Trainium chip icon --
        chip_rect = RoundedRectangle(
            width=2.5,
            height=1.2,
            corner_radius=0.15,
            color=CHIP_BLUE,
            fill_opacity=0.15,
            stroke_width=2,
        ).move_to(UP * 1.2 + LEFT * 2.5)

        chip_label = safe_text(
            "Trainium",
            font_size=LABEL_SIZE,
            color=CHIP_BLUE,
        ).move_to(chip_rect)

        chip = VGroup(chip_rect, chip_label)
        self.play(FadeIn(chip, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(HOLD_SHORT)

        # -- Phase 4: Animated throughput counter --
        throughput_label = safe_text(
            "Throughput (tokens/s):",
            font_size=BODY_SIZE,
            color=BASELINE_GRAY,
        ).move_to(UP * 1.2 + RIGHT * 1.8)

        tracker = ValueTracker(49.69)
        counter = DecimalNumber(
            49.69,
            num_decimal_places=2,
            font_size=48,
            color=SPEEDUP_YELLOW,
        ).next_to(throughput_label, DOWN, buff=0.4)
        counter.add_updater(
            lambda m: m.set_value(tracker.get_value())
        )

        self.play(
            Write(throughput_label),
            FadeIn(counter, shift=UP * 0.2),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # Animate counter from baseline to optimized
        self.play(
            tracker.animate.set_value(92.52),
            run_time=3.0,
            rate_func=smooth,
        )
        counter.clear_updaters()
        self.wait(HOLD_SHORT)

        # -- Phase 5: Speedup callout --
        speedup = safe_text(
            "2.49x faster",
            font_size=56,
            color=SPEEDUP_YELLOW,
        ).move_to(DOWN * 0.8)

        self.play(
            FadeIn(speedup, scale=0.8),
            run_time=1.0,
        )
        self.wait(HOLD_MEDIUM)

        # -- Phase 6: Bottom note --
        note = bottom_note("Song et al., arXiv:2510.25977, 2025")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(self, title, chip, throughput_label, counter, speedup, note)
        self.wait(0.5)
