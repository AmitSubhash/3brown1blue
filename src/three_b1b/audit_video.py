"""audit command: automated visual quality checking for multi-scene Manim projects."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import click

from .edit_scene import _discover_scenes, _find_project_dir

# Quality flag -> resolution directory produced by manim.
QUALITY_MAP: dict[str, str] = {
    "l": "480p15",
    "m": "720p30",
    "h": "1080p60",
}

# Percentages of total duration at which frames are extracted.
FRAME_PCTS: tuple[int, ...] = (10, 25, 50, 75, 90)


# ---------------------------------------------------------------------------
# Helpers: ffprobe / ffmpeg
# ---------------------------------------------------------------------------


def _ffmpeg_available() -> bool:
    """Return True if ffmpeg and ffprobe are on PATH."""
    return (
        shutil.which("ffmpeg") is not None
        and shutil.which("ffprobe") is not None
    )


def _get_video_duration(video: Path) -> float | None:
    """Return duration in seconds via ffprobe, or None on failure."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        str(video),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except (KeyError, ValueError, json.JSONDecodeError):
        return None


def _extract_frames(
    video: Path,
    output_dir: Path,
    num_frames: int,
) -> list[Path]:
    """Extract *num_frames* evenly-spaced frames from *video*.

    Parameters
    ----------
    video : Path
        Path to the rendered mp4 file.
    output_dir : Path
        Directory to write frame PNGs into.
    num_frames : int
        How many frames to extract.

    Returns
    -------
    list[Path]
        Paths of successfully extracted frame images.
    """
    duration = _get_video_duration(video)
    if duration is None or duration <= 0:
        return []

    output_dir.mkdir(parents=True, exist_ok=True)

    pcts = FRAME_PCTS[:num_frames]
    extracted: list[Path] = []

    for pct in pcts:
        timestamp = duration * pct / 100.0
        out_path = output_dir / f"frame_{pct:02d}.png"
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{timestamp:.3f}",
            "-i", str(video),
            "-vframes", "1",
            "-q:v", "2",
            str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and out_path.exists():
            extracted.append(out_path)

    return extracted


# ---------------------------------------------------------------------------
# Helpers: video path resolution
# ---------------------------------------------------------------------------


def _find_rendered_video(
    scene_file: Path,
    scene_class: str,
    project_dir: Path,
    res_dir: str,
) -> Path | None:
    """Locate a rendered video for *scene_class*, or return None.

    Parameters
    ----------
    scene_file : Path
        The scene_*.py source file.
    scene_class : str
        Name of the Scene subclass.
    project_dir : Path
        Root of the Manim project.
    res_dir : str
        Resolution directory (e.g. "480p15").

    Returns
    -------
    Path | None
        Path to the mp4 if it exists on disk.
    """
    video = (
        project_dir / "media" / "videos"
        / scene_file.stem / res_dir / f"{scene_class}.mp4"
    )
    return video if video.exists() else None


def _render_scene_for_audit(
    scene_file: Path,
    scene_class: str,
    quality: str,
) -> bool:
    """Render a single scene class and return True on success.

    Parameters
    ----------
    scene_file : Path
        The scene_*.py file.
    scene_class : str
        Name of the Scene subclass to render.
    quality : str
        Manim quality flag (l, m, or h).

    Returns
    -------
    bool
        True if manim returned exit code 0.
    """
    cmd = [
        "manim", f"-q{quality}",
        str(scene_file), scene_class,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Static code analysis checks
# ---------------------------------------------------------------------------


class CheckResult:
    """Outcome of a single static analysis check."""

    def __init__(self, name: str, passed: bool, message: str, line: int | None = None) -> None:
        self.name = name
        self.passed = passed
        self.message = message
        self.line = line

    @property
    def tag(self) -> str:
        return "PASS" if self.passed else "WARN"


def _check_newline_in_text(source: str) -> list[CheckResult]:
    r"""Flag Text() calls containing literal backslash-n."""
    results: list[CheckResult] = []
    for i, line in enumerate(source.splitlines(), 1):
        if re.search(r'Text\([^)]*\\n', line):
            results.append(CheckResult(
                "No \\n in Text()",
                False,
                f"Text() contains \\n at line {i}",
                line=i,
            ))
    if not results:
        results.append(CheckResult("No \\n in Text()", True, "Clean"))
    return results


def _check_bottom_note_animation(source: str) -> list[CheckResult]:
    r"""Bottom notes should use FadeIn, not Write()."""
    results: list[CheckResult] = []
    for i, line in enumerate(source.splitlines(), 1):
        if re.search(r'Write\(.*(?:bottom_note|note\b)', line):
            results.append(CheckResult(
                "Bottom notes use FadeIn",
                False,
                f"Write() on bottom_note at line {i}",
                line=i,
            ))
    if not results:
        results.append(CheckResult("Bottom notes use FadeIn", True, "Clean"))
    return results


def _check_dollar_in_mathtex(source: str) -> list[CheckResult]:
    """MathTex should not contain dollar signs."""
    results: list[CheckResult] = []
    for i, line in enumerate(source.splitlines(), 1):
        if re.search(r'MathTex\([^)]*\$', line):
            results.append(CheckResult(
                "No $ in MathTex()",
                False,
                f"Dollar sign in MathTex at line {i}",
                line=i,
            ))
    if not results:
        results.append(CheckResult("No $ in MathTex()", True, "Clean"))
    return results


def _check_layout_bounds(source: str) -> list[CheckResult]:
    """Flag absolute coordinates that exceed safe bounds."""
    results: list[CheckResult] = []
    # Match patterns like RIGHT * 6, LEFT * 6, UP * 4, DOWN * 4
    coord_pattern = re.compile(
        r'(RIGHT|LEFT)\s*\*\s*([0-9.]+)'
        r'|(UP|DOWN)\s*\*\s*([0-9.]+)',
    )
    for i, line in enumerate(source.splitlines(), 1):
        for m in coord_pattern.finditer(line):
            if m.group(1):  # horizontal
                val = float(m.group(2))
                if val > 5.5:
                    results.append(CheckResult(
                        "Layout bounds",
                        False,
                        f"Possible overflow: {m.group(0)} at line {i}",
                        line=i,
                    ))
            elif m.group(3):  # vertical
                val = float(m.group(4))
                if val > 3.2:
                    results.append(CheckResult(
                        "Layout bounds",
                        False,
                        f"Possible overflow: {m.group(0)} at line {i}",
                        line=i,
                    ))
    if not results:
        results.append(CheckResult("Layout bounds", True, "Within safe area"))
    return results


def _check_title_lifecycle(source: str) -> list[CheckResult]:
    """Verify titles created in a scene are eventually faded out."""
    results: list[CheckResult] = []
    has_title_create = bool(re.search(r'section_title\(', source))
    has_title_fadeout = bool(re.search(r'FadeOut\(.*title', source, re.IGNORECASE))
    has_fade_all = bool(re.search(r'fade_all\(', source))

    if has_title_create and not (has_title_fadeout or has_fade_all):
        results.append(CheckResult(
            "Title lifecycle",
            False,
            "Title created but no FadeOut or fade_all found",
        ))
    else:
        results.append(CheckResult(
            "Title lifecycle",
            True,
            "Titles cleaned up" if has_title_create else "No section_title() calls",
        ))
    return results


def _check_end_cleanup(source: str) -> list[CheckResult]:
    """Scene should end with fade_all() or FadeOut."""
    results: list[CheckResult] = []
    lines = source.rstrip().splitlines()
    # Look in the last 15 lines for cleanup
    tail = "\n".join(lines[-15:]) if len(lines) >= 15 else source
    has_cleanup = bool(
        re.search(r'fade_all\(', tail)
        or re.search(r'FadeOut\(', tail)
    )
    if not has_cleanup:
        results.append(CheckResult(
            "End cleanup",
            False,
            "No fade_all() or FadeOut in final lines",
        ))
    else:
        results.append(CheckResult("End cleanup", True, "Scene ends with cleanup"))
    return results


def _check_dim_opacity(source: str) -> list[CheckResult]:
    """DIM_OPACITY should be 0.1, not 0.3."""
    results: list[CheckResult] = []
    for i, line in enumerate(source.splitlines(), 1):
        if re.search(r'set_opacity\(\s*0\.3\s*\)', line):
            results.append(CheckResult(
                "DIM_OPACITY value",
                False,
                f"set_opacity(0.3) should be 0.1 at line {i}",
                line=i,
            ))
    if not results:
        results.append(CheckResult("DIM_OPACITY value", True, "Clean"))
    return results


def _check_interpolate_color(source: str) -> list[CheckResult]:
    """interpolate_color() args should be wrapped in ManimColor()."""
    results: list[CheckResult] = []
    for i, line in enumerate(source.splitlines(), 1):
        if re.search(r'interpolate_color\(', line):
            # Check if hex strings are used without ManimColor wrapper
            if re.search(r'interpolate_color\(\s*["\']#', line):
                results.append(CheckResult(
                    "interpolate_color wrapping",
                    False,
                    f"Hex string in interpolate_color at line {i} -- wrap in ManimColor()",
                    line=i,
                ))
    if not results:
        results.append(CheckResult("interpolate_color wrapping", True, "Clean"))
    return results


def _check_style_import(source: str) -> list[CheckResult]:
    """Scene should import from utils.style or style."""
    results: list[CheckResult] = []
    has_import = bool(
        re.search(r'from\s+(?:utils\.)?style\s+import', source)
        or re.search(r'import\s+(?:utils\.)?style', source)
    )
    if not has_import:
        results.append(CheckResult(
            "Style import",
            False,
            "No import from style module found",
        ))
    else:
        results.append(CheckResult("Style import", True, "Imports style"))
    return results


def _check_empty_waits(source: str) -> list[CheckResult]:
    """Flag self.wait() not preceded by an animation call."""
    results: list[CheckResult] = []
    lines = source.splitlines()
    animation_pattern = re.compile(
        r'self\.play\(|self\.add\(|FadeIn|FadeOut|Write|Create|Transform',
    )
    for i, line in enumerate(lines):
        if re.search(r'self\.wait\(\s*\)', line):
            # Check if the preceding non-blank line has an animation
            prev_idx = i - 1
            while prev_idx >= 0 and not lines[prev_idx].strip():
                prev_idx -= 1
            if prev_idx >= 0 and not animation_pattern.search(lines[prev_idx]):
                results.append(CheckResult(
                    "Empty waits",
                    False,
                    f"self.wait() without preceding animation at line {i + 1}",
                    line=i + 1,
                ))
    if not results:
        results.append(CheckResult("Empty waits", True, "Clean"))
    return results


# Master list of all check functions.
ALL_CHECKS: list = [
    _check_newline_in_text,
    _check_bottom_note_animation,
    _check_dollar_in_mathtex,
    _check_layout_bounds,
    _check_title_lifecycle,
    _check_end_cleanup,
    _check_dim_opacity,
    _check_interpolate_color,
    _check_style_import,
    _check_empty_waits,
]


def run_checks(source: str) -> list[CheckResult]:
    """Run all static analysis checks on *source* and return results.

    Parameters
    ----------
    source : str
        Python source code of a single scene file.

    Returns
    -------
    list[CheckResult]
        Aggregated results from every check function.
    """
    results: list[CheckResult] = []
    for check_fn in ALL_CHECKS:
        results.extend(check_fn(source))
    return results


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def _generate_report(
    project_name: str,
    scenes: list[dict],
    scene_checks: dict[str, list[CheckResult]],
    frame_map: dict[str, list[Path]],
    frames_dir: Path,
) -> str:
    """Build the full Markdown audit report.

    Parameters
    ----------
    project_name : str
        Human-readable project name.
    scenes : list[dict]
        Scene dicts from _discover_scenes().
    scene_checks : dict[str, list[CheckResult]]
        Mapping of filename -> check results.
    frame_map : dict[str, list[Path]]
        Mapping of scene_stem -> extracted frame paths.
    frames_dir : Path
        Root directory where frames are saved.

    Returns
    -------
    str
        Complete Markdown report.
    """
    total_checks = sum(len(v) for v in scene_checks.values())
    pass_checks = sum(
        sum(1 for r in v if r.passed) for v in scene_checks.values()
    )
    total_frames = sum(len(v) for v in frame_map.values())

    lines: list[str] = [
        f"# Audit Report: {project_name}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Scenes: {len(scenes)}",
        "",
        "## Summary",
        f"- Code checks: {pass_checks}/{total_checks} passed",
        f"- Frames extracted: {total_frames}",
        "",
        "## Code Analysis",
        "",
    ]

    for scene in scenes:
        fname = scene["file"].name
        classes_str = ", ".join(scene["classes"]) if scene["classes"] else "(none)"
        lines.append(f"### Scene {scene['index']}: {fname} ({classes_str})")
        lines.append("")
        checks = scene_checks.get(fname, [])
        if not checks:
            lines.append("- (no checks ran)")
        for r in checks:
            prefix = "PASS" if r.passed else "WARN"
            lines.append(f"- [{prefix}] {r.name}: {r.message}")
        lines.append("")

    lines.append("## Frame Extraction")
    lines.append(f"Frames saved to: {frames_dir}/")
    lines.append("")

    if frame_map:
        for stem, paths in sorted(frame_map.items()):
            names = ", ".join(p.name for p in paths)
            lines.append(f"- {stem}/{names}")
    else:
        lines.append("- (no frames extracted)")

    lines.append("")
    lines.append("Review frames manually for:")
    lines.append("- Text overlap")
    lines.append("- Empty frames (>60% blank)")
    lines.append("- Elements clipped at edges")
    lines.append("- Inconsistent title positioning")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI command
# ---------------------------------------------------------------------------


@click.command()
@click.option(
    "--dir", "-d", "project_dir",
    default=".",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Project directory (auto-detected if omitted).",
)
@click.option(
    "--frames", "-f",
    default=5,
    show_default=True,
    help="Frames to extract per scene.",
)
@click.option(
    "--quality", "-q",
    type=click.Choice(["l", "m", "h"]),
    default="l",
    show_default=True,
    help="Manim render quality.",
)
@click.option(
    "--output", "-o",
    default="audit_report.md",
    show_default=True,
    help="Report output file.",
)
def audit(project_dir: Path, frames: int, quality: str, output: str) -> None:
    """Automated visual quality audit for a Manim project.

    Discovers scenes, checks for rendered videos (renders missing ones),
    extracts frames with ffmpeg, runs static code analysis, and writes
    a Markdown report.

    \b
    Examples:
      3brown1blue audit
      3brown1blue audit --dir videos/neuronmm
      3brown1blue audit --frames 3
      3brown1blue audit --quality l --output report.md
    """
    project_dir = _find_project_dir(project_dir)
    res_dir = QUALITY_MAP[quality]
    has_ffmpeg = _ffmpeg_available()

    click.echo(f"\nAudit: {project_dir.name}")
    click.echo(f"Quality: -{quality} ({res_dir})")

    if not has_ffmpeg:
        click.echo(
            "WARNING: ffmpeg/ffprobe not found -- "
            "frame extraction will be skipped."
        )

    # ----- Step 1: discover scenes ----------------------------------------
    scenes = _discover_scenes(project_dir)
    if not scenes:
        click.echo(f"No scene_*.py files found in {project_dir}")
        return

    click.echo(f"Found {len(scenes)} scene files.\n")

    # ----- Step 2: ensure rendered videos exist ---------------------------
    video_paths: dict[str, Path] = {}  # "stem/Class" -> video path

    for scene in scenes:
        for cls in scene["classes"]:
            key = f"{scene['file'].stem}/{cls}"
            video = _find_rendered_video(
                scene["file"], cls, project_dir, res_dir,
            )
            if video is not None:
                click.echo(f"  Found: {key}")
                video_paths[key] = video
            else:
                click.echo(f"  Rendering: {key} ...")
                ok = _render_scene_for_audit(scene["file"], cls, quality)
                if ok:
                    rendered = _find_rendered_video(
                        scene["file"], cls, project_dir, res_dir,
                    )
                    if rendered is not None:
                        video_paths[key] = rendered
                        click.echo(f"    OK")
                    else:
                        click.echo(f"    Rendered but video not found at expected path")
                else:
                    click.echo(f"    FAILED to render")

    # ----- Step 3: extract frames -----------------------------------------
    frames_dir = project_dir / "audit_frames"
    frame_map: dict[str, list[Path]] = {}

    if has_ffmpeg and video_paths:
        click.echo(f"\nExtracting {frames} frames per scene...")
        for key, video in video_paths.items():
            scene_stem = key.replace("/", "_")
            out_dir = frames_dir / scene_stem
            extracted = _extract_frames(video, out_dir, frames)
            if extracted:
                frame_map[scene_stem] = extracted
                click.echo(f"  {scene_stem}: {len(extracted)} frames")
            else:
                click.echo(f"  {scene_stem}: extraction failed")
    elif has_ffmpeg:
        click.echo("\nNo rendered videos available -- skipping frame extraction.")
    # else: already warned about missing ffmpeg

    # ----- Step 4: static code analysis -----------------------------------
    click.echo("\nRunning code analysis...")
    scene_checks: dict[str, list[CheckResult]] = {}

    for scene in scenes:
        source = scene["file"].read_text()
        checks = run_checks(source)
        scene_checks[scene["file"].name] = checks
        pass_count = sum(1 for c in checks if c.passed)
        total = len(checks)
        status = "OK" if pass_count == total else f"{total - pass_count} warnings"
        click.echo(f"  {scene['file'].name}: {pass_count}/{total} ({status})")

    # ----- Step 5: generate report ----------------------------------------
    report = _generate_report(
        project_name=project_dir.name,
        scenes=scenes,
        scene_checks=scene_checks,
        frame_map=frame_map,
        frames_dir=frames_dir,
    )
    report_path = project_dir / output
    report_path.write_text(report)
    click.echo(f"\nReport written to: {report_path}")
    click.echo("Done!")
