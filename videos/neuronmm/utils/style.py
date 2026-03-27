"""Shared style constants for NeuronMM explainer video.

Domain: Computer Architecture / ML Systems
Audience: Graduate researchers
"""

from manim import *

# -- Semantic Color Palette --
# Hardware / architecture
CHIP_BLUE = "#4A90D9"
HBM_PURPLE = "#9B59B6"
SBUF_GREEN = "#2ECC71"
PSUM_TEAL = "#1ABC9C"
DMA_ORANGE = "#E67E22"

# Performance / results
SPEEDUP_YELLOW = "#F1C40F"
BASELINE_GRAY = "#95A5A6"
DANGER_RED = "#E74C3C"
SUCCESS_GREEN = "#27AE60"

# Matrix / math
MATRIX_X = "#3498DB"       # input activation
MATRIX_W = "#E74C3C"       # weight matrix
MATRIX_U = "#2ECC71"       # SVD factor U
MATRIX_V = "#F39C12"       # SVD factor V
MATRIX_Y = "#9B59B6"       # intermediate

# General
HIGHLIGHT = PURE_YELLOW
DIM_OPACITY = 0.1
ACCENT = "#F1C40F"

# -- Font Sizes --
TITLE_SIZE = 42
HEADING_SIZE = 34
BODY_SIZE = 28
LABEL_SIZE = 22
EQ_SIZE = 36
SMALL_EQ = 26

# -- Layout --
TITLE_Y = 3.0
BOTTOM_Y = -3.2
LEFT_X = -3.5
RIGHT_X = 3.5
SAFE_WIDTH = 12.0
SAFE_HEIGHT = 6.0

# -- Timing --
HOLD_SHORT = 1.0
HOLD_MEDIUM = 2.0
HOLD_LONG = 3.0


# -- Text Helpers --

def safe_text(
    text: str,
    font_size: int = BODY_SIZE,
    color=WHITE,
    max_width: float = 12.0,
) -> Text:
    """Single-line text with automatic width capping."""
    t = Text(text, font_size=font_size, color=color)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


def safe_multiline(
    *lines: str,
    font_size: int = BODY_SIZE,
    color=WHITE,
    line_buff: float = 0.3,
    max_width: float = 12.0,
) -> VGroup:
    """Centered multi-line text. Each line is a separate Text object."""
    texts = []
    for line in lines:
        t = Text(line, font_size=font_size, color=color)
        if t.width > max_width:
            t.scale_to_fit_width(max_width)
        texts.append(t)
    return VGroup(*texts).arrange(DOWN, buff=line_buff, center=True)


def section_title(text: str, color=WHITE) -> Text:
    """Section title at standard top position."""
    return Text(text, font_size=TITLE_SIZE, color=color).to_edge(UP, buff=0.5)


def bottom_note(text: str, color=YELLOW) -> Text:
    """Bottom annotation. Animate with FadeIn(shift=UP*0.2), NOT Write()."""
    t = Text(text, font_size=LABEL_SIZE, color=color)
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t.to_edge(DOWN, buff=0.5)


# -- Diagram Helpers --

def labeled_box(
    label: str,
    width: float = 2.5,
    height: float = 1.0,
    color: str = CHIP_BLUE,
    font_size: int = LABEL_SIZE,
    fill_opacity: float = 0.2,
) -> VGroup:
    """Labeled rectangle for pipeline/architecture diagrams."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.1,
        color=color, fill_opacity=fill_opacity, stroke_width=2,
    )
    text = Text(label, font_size=font_size, color=color)
    text.move_to(rect)
    if text.width > width - 0.3:
        text.scale_to_fit_width(width - 0.3)
    return VGroup(rect, text)


def mem_block(
    label: str,
    capacity: str,
    width: float = 2.0,
    height: float = 0.8,
    color: str = SBUF_GREEN,
) -> VGroup:
    """Memory block with label and capacity annotation."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.1,
        color=color, fill_opacity=0.25, stroke_width=2,
    )
    name = Text(label, font_size=LABEL_SIZE, color=color)
    cap = Text(capacity, font_size=18, color=GRAY_B)
    name.move_to(rect).shift(UP * 0.12)
    cap.move_to(rect).shift(DOWN * 0.18)
    if name.width > width - 0.3:
        name.scale_to_fit_width(width - 0.3)
    return VGroup(rect, name, cap)


def pipeline_arrow(start, end, color=WHITE, stroke_width=3) -> Arrow:
    """Arrow between pipeline boxes with safe buffering."""
    return Arrow(
        start.get_right(), end.get_left(),
        buff=0.25, color=color, stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.15,
    )


def matrix_rect(
    label: str,
    rows: int,
    cols: int,
    color: str,
    width: float = 1.5,
    height: float = 1.0,
) -> VGroup:
    """Matrix rectangle with label and dimension annotation."""
    rect = Rectangle(
        width=width, height=height,
        color=color, fill_opacity=0.3, stroke_width=2,
    )
    name = Text(label, font_size=LABEL_SIZE, color=color)
    dim = Text(f"[{rows}x{cols}]", font_size=16, color=GRAY_B)
    name.move_to(rect)
    dim.next_to(rect, DOWN, buff=0.15)
    return VGroup(rect, name, dim)


# -- Scene Helpers --

def fade_all(scene: Scene, *mobjects) -> None:
    """FadeOut multiple mobjects at once."""
    if mobjects:
        scene.play(*[FadeOut(m) for m in mobjects])


def story_bridge(scene: Scene, text: str) -> None:
    """Brief transition text between narrative phases."""
    bridge = Text(text, font_size=HEADING_SIZE, color=ACCENT)
    scene.play(FadeIn(bridge, shift=UP * 0.3))
    scene.wait(HOLD_MEDIUM)
    scene.play(FadeOut(bridge, shift=UP * 0.3))
