"""Scene 03: Trainium Architecture -- NeuronCore build-up with data flow animation.

Duration: ~120s
Template: BUILD_UP
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class TrainiumArchScene(Scene):
    """Build NeuronCore piece by piece, then animate data flow through memory hierarchy."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "Trainium Architecture",
            font_size=TITLE_SIZE,
            color=WHITE,
        ).move_to(UP * TITLE_Y)

        self.play(Write(title), run_time=1.2)
        self.wait(HOLD_SHORT)

        # ========================================
        # Phase 1: Build NeuronCore chip outline
        # ========================================
        chip_outline = RoundedRectangle(
            width=7.5, height=4.0,
            corner_radius=0.2,
            color=WHITE,
            stroke_width=2.5,
            fill_opacity=0.03,
        ).move_to(DOWN * 0.3)

        chip_title = safe_text(
            "NeuronCore v2",
            font_size=LABEL_SIZE,
            color=BASELINE_GRAY,
        )
        chip_title.next_to(chip_outline, UP, buff=0.15)

        self.play(Create(chip_outline), Write(chip_title), run_time=1.5)
        self.wait(HOLD_SHORT)

        # ========================================
        # Phase 2: Tensor Engine (center of chip)
        # ========================================
        tensor_engine = labeled_box(
            "Tensor Engine",
            width=2.8, height=1.4,
            color=CHIP_BLUE,
            fill_opacity=0.25,
        ).move_to(LEFT * 1.2 + DOWN * 0.1)

        te_subtitle = safe_text(
            "128x128 Systolic Array",
            font_size=16,
            color=CHIP_BLUE,
        ).next_to(tensor_engine, DOWN, buff=0.12)

        self.play(FadeIn(tensor_engine, scale=0.9), run_time=1.0)
        self.play(Write(te_subtitle), run_time=0.8)
        self.wait(HOLD_SHORT)

        # ========================================
        # Phase 3: SBUF memory (right side, inside chip)
        # ========================================
        sbuf = mem_block(
            "SBUF", "24 MB",
            width=1.8, height=1.4,
            color=SBUF_GREEN,
        ).move_to(RIGHT * 2.0 + DOWN * 0.1)

        self.play(FadeIn(sbuf, shift=LEFT * 0.3), run_time=1.0)
        self.wait(HOLD_SHORT)

        # ========================================
        # Phase 4: PSUM accumulator (below tensor engine)
        # ========================================
        psum = mem_block(
            "PSUM", "2 MB",
            width=2.8, height=0.7,
            color=PSUM_TEAL,
        ).move_to(LEFT * 1.2 + DOWN * 1.6)

        self.play(FadeIn(psum, shift=UP * 0.2), run_time=1.0)
        self.wait(HOLD_SHORT)

        # ========================================
        # Phase 5: HBM (outside chip boundary, far right)
        # ========================================
        hbm = mem_block(
            "HBM", "16 GB",
            width=1.6, height=2.0,
            color=HBM_PURPLE,
        ).move_to(RIGHT * 5.0 + DOWN * 0.3)

        self.play(FadeIn(hbm, shift=LEFT * 0.4), run_time=1.0)
        self.wait(HOLD_SHORT)

        # ========================================
        # Phase 6: DMA arrows (HBM <-> SBUF)
        # ========================================
        dma_to_sbuf = Arrow(
            hbm.get_left(), sbuf.get_right(),
            buff=0.2,
            color=DMA_ORANGE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        dma_to_hbm = Arrow(
            sbuf.get_right(), hbm.get_left(),
            buff=0.2,
            color=DMA_ORANGE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        # Offset arrows vertically so both are visible
        dma_to_sbuf.shift(UP * 0.15)
        dma_to_hbm.shift(DOWN * 0.15)

        dma_label = safe_text(
            "DMA",
            font_size=18,
            color=DMA_ORANGE,
        ).next_to(VGroup(dma_to_sbuf, dma_to_hbm), UP, buff=0.1)

        self.play(
            Create(dma_to_sbuf),
            Create(dma_to_hbm),
            Write(dma_label),
            run_time=1.2,
        )
        self.wait(HOLD_MEDIUM)

        # ========================================
        # Phase 7: Animated data flow dot
        # ========================================
        # Path: HBM -> SBUF -> Tensor Engine -> PSUM -> SBUF -> HBM
        flow_dot = Dot(radius=0.12, color=SPEEDUP_YELLOW)
        flow_dot.set_z_index(10)
        flow_dot.move_to(hbm.get_center())

        waypoints = [
            hbm.get_center(),
            sbuf.get_center(),
            tensor_engine.get_center(),
            psum.get_center(),
            sbuf.get_center(),
            hbm.get_center(),
        ]

        self.play(FadeIn(flow_dot, scale=0.5), run_time=0.5)

        for i in range(len(waypoints) - 1):
            self.play(
                flow_dot.animate.move_to(waypoints[i + 1]),
                run_time=0.8,
                rate_func=smooth,
            )

        self.play(FadeOut(flow_dot), run_time=0.4)
        self.wait(HOLD_SHORT)

        # ========================================
        # Phase 8: Memory hierarchy label
        # ========================================
        # Clear title to make room
        self.play(FadeOut(title), run_time=0.5)

        hierarchy = safe_text(
            "16 GB (slow)  -->  24 MB (fast)  -->  2 MB (fastest)",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).move_to(UP * TITLE_Y)

        self.play(FadeIn(hierarchy, shift=DOWN * 0.2), run_time=1.0)
        self.wait(HOLD_MEDIUM)

        # -- Bottom note --
        note = bottom_note("Three-level data layout: Tile (128x128), Block, Strip")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(
            self,
            chip_outline, chip_title,
            tensor_engine, te_subtitle,
            sbuf, psum, hbm,
            dma_to_sbuf, dma_to_hbm, dma_label,
            hierarchy, note,
        )
        self.wait(0.5)
