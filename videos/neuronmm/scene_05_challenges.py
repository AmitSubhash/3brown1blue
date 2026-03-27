"""Scene 05: Three Critical Challenges.

Builds three challenge cards showing why naive SVD execution
on hardware is problematic: I/O bottleneck, recomputation, transpose.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


def challenge_card(
    number: int,
    title_text: str,
    border_color: str,
    diagram_elements: list,
    stat_text: str,
    width: float = 3.3,
    height: float = 4.0,
) -> VGroup:
    """Build a single challenge card with border, title, diagram, and stat."""
    card = RoundedRectangle(
        width=width, height=height, corner_radius=0.15,
        color=border_color, fill_opacity=0.08, stroke_width=2.5,
    )
    # Card number badge
    badge = Circle(radius=0.22, color=border_color, fill_opacity=0.3, stroke_width=1.5)
    badge_num = safe_text(str(number), font_size=18, color=border_color)
    badge_num.move_to(badge)
    badge_group = VGroup(badge, badge_num)
    badge_group.move_to(card.get_corner(UL) + RIGHT * 0.35 + DOWN * 0.35)

    # Title
    card_title = safe_text(
        title_text, font_size=LABEL_SIZE, color=border_color, max_width=width - 0.5,
    )
    card_title.next_to(badge_group, RIGHT, buff=0.2)

    # Diagram area (centered in card)
    diagram = VGroup(*diagram_elements)
    diagram.move_to(card.get_center() + UP * 0.15)
    if diagram.width > width - 0.5:
        diagram.scale_to_fit_width(width - 0.5)
    if diagram.height > height * 0.45:
        diagram.scale_to_fit_height(height * 0.45)

    # Stat label at bottom of card
    stat = safe_text(
        stat_text, font_size=16, color=WHITE, max_width=width - 0.4,
    )
    stat.move_to(card.get_bottom() + UP * 0.55)

    return VGroup(card, badge_group, card_title, diagram, stat)


def _build_io_diagram() -> list:
    """I/O bottleneck: X*U -> [HBM write] -> [HBM read] -> Y*V."""
    xu_box = labeled_box("X*U", width=1.0, height=0.55, color=MATRIX_U, font_size=16)
    hbm_w = labeled_box("HBM", width=0.8, height=0.55, color=DANGER_RED, font_size=14)
    hbm_r = labeled_box("HBM", width=0.8, height=0.55, color=DANGER_RED, font_size=14)
    yv_box = labeled_box("Y*V", width=1.0, height=0.55, color=MATRIX_V, font_size=16)

    row = VGroup(xu_box, hbm_w, hbm_r, yv_box).arrange(RIGHT, buff=0.15)

    # Red arrows for HBM transfers
    arr1 = Arrow(
        xu_box.get_right(), hbm_w.get_left(), buff=0.05,
        color=DANGER_RED, stroke_width=2, max_tip_length_to_length_ratio=0.3,
    )
    arr2 = Arrow(
        hbm_w.get_right(), hbm_r.get_left(), buff=0.05,
        color=DANGER_RED, stroke_width=2, max_tip_length_to_length_ratio=0.3,
    )
    arr3 = Arrow(
        hbm_r.get_right(), yv_box.get_left(), buff=0.05,
        color=DANGER_RED, stroke_width=2, max_tip_length_to_length_ratio=0.3,
    )

    write_lbl = safe_text("write", font_size=12, color=DANGER_RED)
    write_lbl.next_to(arr1, UP, buff=0.05)
    read_lbl = safe_text("read", font_size=12, color=DANGER_RED)
    read_lbl.next_to(arr3, UP, buff=0.05)

    return [row, arr1, arr2, arr3, write_lbl, read_lbl]


def _build_recomp_diagram() -> list:
    """Recomputation: naive fusion recomputes Y blocks 16x."""
    naive_box = labeled_box(
        "Naive Fusion", width=1.6, height=0.5, color=DMA_ORANGE, font_size=15,
    )
    # Multiplier block
    mult_rect = RoundedRectangle(
        width=1.2, height=0.5, corner_radius=0.08,
        color=DMA_ORANGE, fill_opacity=0.25, stroke_width=1.5,
    )
    mult_text = safe_text("16x redo", font_size=16, color=DMA_ORANGE)
    mult_text.move_to(mult_rect)
    mult_group = VGroup(mult_rect, mult_text)

    col = VGroup(naive_box, mult_group).arrange(DOWN, buff=0.25)

    arrow_down = Arrow(
        naive_box.get_bottom(), mult_group.get_top(), buff=0.08,
        color=DMA_ORANGE, stroke_width=2, max_tip_length_to_length_ratio=0.25,
    )
    recomp_lbl = safe_text("recomputes Y blocks", font_size=13, color=GRAY_B)
    recomp_lbl.next_to(arrow_down, RIGHT, buff=0.1)

    return [col, arrow_down, recomp_lbl]


def _build_transpose_diagram() -> list:
    """Transpose overhead: Y needs transpose between matmuls."""
    y_box = Rectangle(
        width=1.4, height=0.9, color=MATRIX_Y,
        fill_opacity=0.25, stroke_width=2,
    )
    y_lbl = safe_text("Y", font_size=20, color=MATRIX_Y)
    y_lbl.move_to(y_box)
    y_dim = safe_text("[BM x r]", font_size=13, color=GRAY_B)
    y_dim.next_to(y_box, DOWN, buff=0.08)

    yt_box = Rectangle(
        width=0.9, height=1.4, color=MATRIX_Y,
        fill_opacity=0.25, stroke_width=2,
    )
    yt_lbl = safe_text("Y^T", font_size=18, color=MATRIX_Y)
    yt_lbl.move_to(yt_box)
    yt_dim = safe_text("[r x BM]", font_size=13, color=GRAY_B)
    yt_dim.next_to(yt_box, DOWN, buff=0.08)

    row = VGroup(
        VGroup(y_box, y_lbl, y_dim),
        VGroup(yt_box, yt_lbl, yt_dim),
    ).arrange(RIGHT, buff=0.6)

    t_arrow = Arrow(
        y_box.get_right(), yt_box.get_left(), buff=0.15,
        color=HBM_PURPLE, stroke_width=2.5, max_tip_length_to_length_ratio=0.2,
    )
    t_label = safe_text("transpose", font_size=14, color=HBM_PURPLE)
    t_label.next_to(t_arrow, UP, buff=0.06)

    systolic_note = safe_text(
        "systolic array requires T", font_size=12, color=GRAY_B,
    )
    systolic_note.next_to(row, DOWN, buff=0.15)

    return [row, t_arrow, t_label, systolic_note]


class ThreeChallengesScene(Scene):
    """Present the three critical challenges of naive SVD on hardware."""

    def construct(self) -> None:
        # ── Title ──
        title = safe_text(
            "Three Critical Challenges", font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        # ── Build three cards ──
        card1 = challenge_card(
            number=1,
            title_text="I/O Bottleneck",
            border_color=DANGER_RED,
            diagram_elements=_build_io_diagram(),
            stat_text="65% more DMA transfer, 2x HBM traffic",
        )
        card2 = challenge_card(
            number=2,
            title_text="Recomputation",
            border_color=DMA_ORANGE,
            diagram_elements=_build_recomp_diagram(),
            stat_text="11x slower (18.06ms vs 1.57ms)",
        )
        card3 = challenge_card(
            number=3,
            title_text="Transpose Overhead",
            border_color=HBM_PURPLE,
            diagram_elements=_build_transpose_diagram(),
            stat_text="Costly intermediate transpose",
        )

        cards = VGroup(card1, card2, card3).arrange(RIGHT, buff=0.35)
        cards.move_to(DOWN * 0.2)

        # Scale if needed to stay within safe bounds
        if cards.width > SAFE_WIDTH - 0.4:
            cards.scale_to_fit_width(SAFE_WIDTH - 0.4)

        # ── Animate cards one by one ──
        self.play(FadeIn(card1, shift=UP * 0.4))
        self.wait(HOLD_MEDIUM)

        self.play(FadeIn(card2, shift=UP * 0.4))
        self.wait(HOLD_MEDIUM)

        self.play(FadeIn(card3, shift=UP * 0.4))
        self.wait(HOLD_MEDIUM)

        # ── Highlight all three simultaneously ──
        highlight_anims = []
        for card in [card1, card2, card3]:
            border = card[0]  # The RoundedRectangle
            highlight_anims.append(
                border.animate.set_stroke(width=4.0, color=HIGHLIGHT)
            )
        self.play(*highlight_anims, rate_func=there_and_back, run_time=1.5)
        self.wait(HOLD_SHORT)

        # ── Bottom note ──
        note = bottom_note("All three must be solved simultaneously")
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(HOLD_LONG)

        # ── Cleanup ──
        all_objs = [title, card1, card2, card3, note]
        self.play(*[FadeOut(m) for m in all_objs])
        self.wait(0.3)
