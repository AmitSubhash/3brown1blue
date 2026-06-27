"""Shared style constants for a Manim video project.

Copy this file to your project's utils/style.py and customize the palette.
Import in every scene file: from utils.style import *
"""

# Manim's API is used via `from manim import *`, the framework's standard idiom.
# ruff: noqa: F403, F405

from manim import *

# ── Color Palette ────────────────────────────────────────────────
# Assign semantic meaning to colors. Keep consistent across all scenes.
# Viewers learn the vocabulary: "blue = input" carries between scenes.
C = {
    "primary": BLUE_C,
    "secondary": RED_C,
    "accent": YELLOW_C,
    "positive": GREEN_C,
    "negative": RED_D,
    "highlight": PURE_YELLOW,
    "dim": GRAY,
    "label": GRAY_B,
}

# ── Font Sizes ───────────────────────────────────────────────────
TITLE_SIZE = 56
SUBTITLE_SIZE = 36
BODY_SIZE = 32
LABEL_SIZE = 24
EQ_SIZE = 44
EQ_SMALL = 32

# ── Timing (seconds) ────────────────────────────────────────────
HOLD_SHORT = 1.0
HOLD_MEDIUM = 2.0
HOLD_LONG = 3.0


# ── Reusable Components ─────────────────────────────────────────

def labeled_box(
    label: str,
    width: float = 2.5,
    height: float = 1.0,
    color: str = BLUE_C,
    font_size: int = LABEL_SIZE,
    fill_opacity: float = 0.2,
) -> VGroup:
    """Labeled rectangle for pipeline/architecture diagrams.

    The label sits at the box center. If placing child elements inside,
    offset them DOWN * 0.3 from center to avoid covering the label.
    """
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.1,
        color=color, fill_opacity=fill_opacity, stroke_width=2,
    )
    text = Text(label, font_size=font_size, color=color)
    text.move_to(rect)
    if text.width > width - 0.3:
        text.scale_to_fit_width(width - 0.3)
    return VGroup(rect, text)


def pipeline_arrow(start, end, color=WHITE, stroke_width=3) -> Arrow:
    """Arrow between pipeline boxes. Uses buff=0.25 to avoid tip crowding."""
    return Arrow(
        start.get_right(), end.get_left(),
        buff=0.25, color=color, stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.15,
    )


# ── Text Helpers (learned from production audits) ────────────

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
    """Centered multi-line text. Each line is a separate Text object.

    Manim's Text('line1\\nline2') left-aligns lines relative to each
    other. This helper creates separate Text objects and arranges them
    with center=True so the block is properly centered.

    Usage:
        msg = safe_multiline("Line one", "Line two", "Line three")
        msg.move_to(ORIGIN)
    """
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
    """Bottom annotation with width safety.

    Animate with FadeIn(note, shift=UP*0.2), NOT Write().
    Write() creates ugly partial-stroke frames on small text.
    """
    t = Text(text, font_size=LABEL_SIZE, color=color)
    if t.width > 12.0:
        t.scale_to_fit_width(12.0)
    return t.to_edge(DOWN, buff=0.5)


# ── Scene Helpers ────────────────────────────────────────────

def fade_all(scene: Scene, *mobjects) -> None:
    """FadeOut multiple mobjects at once."""
    if mobjects:
        scene.play(*[FadeOut(m) for m in mobjects])


def story_bridge(scene: Scene, text: str) -> None:
    """Brief transition text connecting two narrative phases."""
    bridge = Text(text, font_size=BODY_SIZE, color=C["highlight"])
    scene.play(FadeIn(bridge, shift=UP * 0.3))
    scene.wait(HOLD_MEDIUM)
    scene.play(FadeOut(bridge, shift=UP * 0.3))


# ── 3Blue1Brown entity-color binding ────────────────────────────
# Bind ONE color to a math entity, reuse it for the symbol AND its
# geometric avatar (pi is the same red as the arc it traces).
# See rules/color-palettes.md and rules/explanation-design.md.
ENTITY = {
    "pi": "#FC6255",  # pi, and the arc it traces
    "i": "#3FB4C9",  # i / variable z, the rotate-90 action
    "real": "#F9E04C",  # real part, horizontal component
    "imag": "#E15FCB",  # imaginary part, vertical component
    "path": "#83C167",  # motion / series / velocity vectors
    "position": "#3FB4C9",  # position vectors
    "active": "#F9E04C",  # active term, current point, swept parameter
    "grid": "#3C5A6E",  # background grid (low opacity)
}


def glow_dot(
    point, color: ManimColor | str = ENTITY["active"], radius: float = 0.06
) -> VGroup:
    """Active-point marker: a small core dot over a faint larger glow."""
    glow = Dot(point, radius=radius * 3, color=color).set_opacity(0.25)
    core = Dot(point, radius=radius, color=color)
    return VGroup(glow, core)


def role_annotation(
    part: Mobject,
    role: str,
    color: ManimColor | str = ENTITY["active"],
    side=DOWN,
    font_size: int = LABEL_SIZE,
) -> VGroup:
    """Box a sub-expression in its color and label what it DOES.

    The visual form of "give your characters motivation": box e^{it} and
    label it "Position", box i and label it "Rotate 90". Recolors the part
    to match. Returns VGroup(box, label); play Create/FadeIn on it.
    """
    part.set_color(color)
    box = SurroundingRectangle(part, color=color, buff=0.08)
    label = Text(role, font_size=font_size, color=color).next_to(box, side, buff=0.15)
    return VGroup(box, label)


def vector_walk(points, to_point, color: ManimColor | str = ENTITY["path"]) -> VGroup:
    """Tip-to-tail arrows through a sequence of partial sums (a series as motion).

    points: ordered list of values (e.g. complex partial sums).
    to_point: a mapper from value to a scene coordinate, e.g. plane.n2p.
    Returns a VGroup of arrows; reveal with LaggedStart(GrowArrow, ...).
    """
    coords = [to_point(p) for p in points]
    return VGroup(
        *[
            Arrow(
                coords[k - 1],
                coords[k],
                buff=0,
                color=color,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25,
            )
            for k in range(1, len(coords))
        ]
    )
