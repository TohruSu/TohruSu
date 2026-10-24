#!/usr/bin/env python3
"""Generate the terminal / hardware profile banner, offline.

Usage (Python 3.10+, Pillow 11.1.0):
    python -m pip install Pillow==11.1.0
    python assets/generate_hero.py

The committed rasters use installed Segoe UI, Segoe UI Bold, and Consolas.
Fonts are not redistributed. For another platform, supply installed font files:
    python assets/generate_hero.py --sans-font FONT --bold-font FONT --mono-font FONT

Use --review-dir DIR to export a contact sheet and decoded-frame QA report outside
the repository. No network, randomness, frontend, or workflow is needed. Identical
fonts and Pillow/FreeType versions produce identical bytes; review typography
when changing fonts. Only the four hero GIF/PNG assets are written by default.
"""

import argparse
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, __version__ as PILLOW_VERSION

ROOT = Path(__file__).resolve().parent
SCALE = 2
FRAME_MS = 100
DURATION_MS = 10000
BG = "#161B22"
IVORY = "#F0ECE6"
AMBER = "#C9A077"
MUTED = "#AAB4BD"
STEEL = "#697B86"
GRID = "#202B34"
TITLE = "TOHRU"
SUBTITLE = "Software Engineering / Hardware Verification"
AFFILIATION = "Waseda University \u00b7 Kimura Lab"
FOCUS = "$ focus  digital design / verification / optimization"
FONT_PATHS = {}


def mix(a, b, amount):
    amount = max(0.0, min(1.0, amount))
    aa = tuple(bytes.fromhex(a.lstrip("#")))
    bb = tuple(bytes.fromhex(b.lstrip("#")))
    return "#" + "".join(f"{round(x + (y-x)*amount):02x}" for x, y in zip(aa, bb))


def smooth(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


@lru_cache(maxsize=None)
def font(kind, size):
    return ImageFont.truetype(str(FONT_PATHS[kind]), round(size * SCALE),
                              layout_engine=ImageFont.Layout.BASIC)


def text(draw, x, y, value, size, color=IVORY, kind="sans", anchor="lt"):
    xy = (round(x * SCALE), round(y * SCALE))
    bbox = draw.textbbox(xy, value, font=font(kind, size), anchor=anchor)
    width, height = draw.im.size
    if bbox[0] < 0 or bbox[1] < 0 or bbox[2] > width or bbox[3] > height:
        raise ValueError(f"Text clipped: {value!r}; bounds={bbox}")
    draw.text(xy, value, font=font(kind, size), fill=color, anchor=anchor)
    return font(kind, size).getlength(value) / SCALE


def line(draw, points, color, width=1):
    draw.line([(round(x*SCALE), round(y*SCALE)) for x, y in points],
              fill=color, width=max(1, round(width*SCALE)), joint="curve")


def dashed(draw, x, top, bottom, color, dash=2, gap=3):
    for y in range(round(top), round(bottom), dash + gap):
        line(draw, [(x, y), (x, min(y + dash, bottom))], color, 0.65)


@dataclass(frozen=True)
class Layout:
    width: int
    height: int
    pad: int
    header_y: int
    title_baseline: int
    title_size: int
    subtitle_y: int
    subtitle_size: int
    affiliation_y: int
    affiliation_size: int
    focus_y: int
    focus_size: float
    plot_left: int
    plot_right: int
    clock_top: int
    row_step: int
    amplitude: int

    @property
    def plot_bottom(self):
        return self.clock_top + 3*self.row_step + self.amplitude + 14


DESKTOP = Layout(960, 320, 44, 57, 142, 72, 163, 20, 194, 13,
                 250, 13.5, 528, 892, 107, 34, 17)
MOBILE = Layout(480, 336, 26, 25, 96, 60, 117, 18, 145, 13,
                175, 11.5, 28, 411, 210, 26, 12)

# An illustrative registered-output timing sequence, not research or device data.
# Clock rises at n+0.5, falls at n+1.0; active-high reset falls at t=2.
# valid is asserted for two cycles, from rising edge 2.5 to rising edge 4.5.
# Data changes only at rising edges 2.5 (A5) and 3.5 (3C), then is held.
CYCLES = 6
CLOCK_EVENTS = [(i/2, i % 2) for i in range(1, 13)]
RESET_EVENTS = [(2.0, 0)]
VALID_EVENTS = [(2.5, 1), (4.5, 0)]
DATA_EVENTS = [(0, "00"), (2.5, "A5"), (3.5, "3C"), (6, None)]


def time_x(layout, value):
    return layout.plot_left + (layout.plot_right-layout.plot_left)*value/CYCLES


def digital(draw, layout, row, initial, events, color):
    high = layout.clock_top + row*layout.row_step
    low = high + layout.amplitude
    level = initial
    points = [(layout.plot_left, high if level else low)]
    for edge, new_level in events:
        x = time_x(layout, edge)
        points += [(x, high if level else low), (x, high if new_level else low)]
        level = new_level
    points.append((layout.plot_right, high if level else low))
    line(draw, points, color, 1.1)


def signals(draw, layout, strength):
    colors = [mix(GRID, AMBER, strength), mix(GRID, STEEL, strength),
              mix(GRID, AMBER, strength), mix(GRID, MUTED, strength*.8)]
    digital(draw, layout, 0, 0, CLOCK_EVENTS, colors[0])
    digital(draw, layout, 1, 1, RESET_EVENTS, colors[1])
    digital(draw, layout, 2, 0, VALID_EVENTS, colors[2])
    top = layout.clock_top + 3*layout.row_step
    bottom = top + layout.amplitude
    wedge = 4
    for index, ((start, value), (end, _)) in enumerate(zip(DATA_EVENTS, DATA_EVENTS[1:])):
        left, right = time_x(layout, start), time_x(layout, end)
        rail_left = left + (wedge if index else 0)
        rail_right = right - (wedge if end < CYCLES else 0)
        line(draw, [(rail_left, top), (rail_right, top)], colors[3], 1)
        line(draw, [(rail_left, bottom), (rail_right, bottom)], colors[3], 1)
        if index:
            line(draw, [(left-wedge, top), (left+wedge, bottom)], colors[3], 1)
            line(draw, [(left-wedge, bottom), (left+wedge, top)], colors[3], 1)
        size = 9.5 if layout is DESKTOP else 9
        value_width = font("mono", size).getlength(value)/SCALE
        text(draw, (left+right-value_width)/2, top+2.5, value, size,
             mix(BG, MUTED, .70*strength), "mono")


@lru_cache(maxsize=2)
def background(layout):
    image = Image.new("RGB", (layout.width*SCALE, layout.height*SCALE), BG)
    draw = ImageDraw.Draw(image)
    grid_left = 395 if layout is DESKTOP else layout.plot_left
    grid_top = 65 if layout is DESKTOP else 197
    grid_right = 922 if layout is DESKTOP else 451
    for x in range(grid_left, grid_right+1, 21):
        # Slightly quieter grid toward the identity, with no glow or texture.
        intensity = .40 if x < layout.plot_left else .72
        dashed(draw, x, grid_top, layout.plot_bottom+4, mix(BG, GRID, intensity), 1, 2)
    for y in range(grid_top, layout.plot_bottom+6, 20):
        line(draw, [(grid_left, y), (grid_right, y)], mix(BG, GRID, .45), .5)
    for edge in (2.5, 3.5, 4.5):
        dashed(draw, time_x(layout, edge), grid_top, layout.plot_bottom+3,
               mix(BG, STEEL, .28))
    for x, y in ((layout.width-44, 50), (layout.width-44, 269)) if layout is DESKTOP else ((450, 197), (450, 320)):
        line(draw, [(x-7, y), (x+7, y)], mix(BG, STEEL, .40), .65)
        line(draw, [(x, y-7), (x, y+7)], mix(BG, STEEL, .40), .65)
    signals(draw, layout, .16)
    label_size = 12 if layout is DESKTOP else 11
    for row, name in enumerate(("clk", "rst", "valid", "data")):
        text(draw, layout.plot_right+12, layout.clock_top+row*layout.row_step+3,
             name, label_size, mix(BG, MUTED, .70), "mono")
    return image


def render(layout, seconds):
    image = background(layout).copy()
    draw = ImageDraw.Draw(image)
    reset = 1-smooth((seconds-9.2)/.7)
    identity = smooth((seconds-.25)/.8) * reset

    for index in range(3):
        x, y = layout.pad+4+index*16, layout.header_y+4
        color = AMBER if index == 0 else mix(BG, STEEL, .70)
        draw.ellipse(((x-4)*SCALE, (y-4)*SCALE, (x+4)*SCALE, (y+4)*SCALE), fill=color)
    text(draw, layout.pad+56, layout.header_y-1, "~/tohru", 14 if layout is DESKTOP else 13,
         mix(BG, MUTED, .85), "mono")

    # One fixed-width character decodes at a time; surrounding letters never shift.
    active = int((seconds-.1)/.12) if .1 <= seconds < .7 else -1
    for index, letter in enumerate(TITLE):
        prefix_width = font("bold", layout.title_size).getlength(TITLE[:index])/SCALE
        if index == active:
            letter = ("0", "#", "1", "/", "_")[index]
        text(draw, layout.pad+prefix_width, layout.title_baseline, letter,
             layout.title_size, IVORY, "bold", "ls")
    title_width = font("bold", layout.title_size).getlength(TITLE)/SCALE
    text(draw, layout.pad+title_width, layout.title_baseline, ".", layout.title_size,
         AMBER, "bold", "ls")

    text(draw, layout.pad, layout.subtitle_y, SUBTITLE, layout.subtitle_size,
         mix(BG, IVORY, .72+.28*identity))
    text(draw, layout.pad, layout.affiliation_y, AFFILIATION, layout.affiliation_size,
         mix(BG, MUTED, .78+.22*identity), "mono")

    if layout is DESKTOP:
        for start, length, color in ((0, 36, AMBER), (40, 20, STEEL), (64, 12, GRID)):
            line(draw, [(layout.pad+start, 225), (layout.pad+start+length, 225)], color, 2.4)

    progress = max(0.0, min(1.0, (seconds-1.1)/2.5))
    if progress > 0 and reset > 0:
        foreground = image.copy()
        foreground_draw = ImageDraw.Draw(foreground)
        signals(foreground_draw, layout, .16+.84*reset)
        boundary = round(time_x(layout, progress*CYCLES)*SCALE)
        if progress == 1:
            boundary += 2*SCALE  # Include the final clock edge's stroke.
        box = (layout.plot_left*SCALE, (layout.clock_top-2)*SCALE,
               boundary, (layout.plot_bottom+1)*SCALE)
        image.paste(foreground.crop(box), box[:2])
        draw = ImageDraw.Draw(image)
        if progress < 1:
            x = boundary/SCALE
            dashed(draw, x, layout.clock_top-10, layout.plot_bottom,
                   mix(BG, AMBER, .55), 2, 3)
            text(draw, x-3, layout.clock_top-15, "+", 10, mix(BG, AMBER, .7), "mono")

    # A faint complete focus line makes early paused frames useful; its prefix types in.
    prefix = "$ focus  "
    body = FOCUS[len(prefix):]
    prefix_width = text(draw, layout.pad, layout.focus_y, prefix, layout.focus_size, AMBER, "mono")
    text(draw, layout.pad+prefix_width, layout.focus_y, body, layout.focus_size,
         mix(BG, MUTED, .32), "mono")
    count = min(len(body), max(0, math.floor((seconds-3.6)/.9*len(body)+1e-6)))
    if count and reset > 0:
        text(draw, layout.pad+prefix_width, layout.focus_y, body[:count], layout.focus_size,
             mix(mix(BG, MUTED, .32), IVORY, reset), "mono")
    if seconds >= 4.5:
        cursor_x = layout.pad + font("mono", layout.focus_size).getlength(FOCUS)/SCALE + 6
        blink = .40+.60*(.5+.5*math.cos(2*math.pi*(seconds-4.5)/1.4))
        color = mix(BG, AMBER, .25 + .75*blink*reset)
    elif count:
        cursor_x = layout.pad+prefix_width+font("mono", layout.focus_size).getlength(body[:count])/SCALE+3
        color = AMBER
    else:
        cursor_x = layout.pad + font("mono", layout.focus_size).getlength(FOCUS)/SCALE + 6
        color = mix(BG, AMBER, .25)
    # At the end of the fade, match the exact opening cursor brightness.
    if reset == 0:
        color = mix(BG, AMBER, .25)
    draw.rectangle((round(cursor_x*SCALE), round((layout.focus_y-1)*SCALE),
                    round((cursor_x+6)*SCALE), round((layout.focus_y+13)*SCALE)), fill=color)
    return image


def validate_sequence():
    rising = {edge for edge, value in CLOCK_EVENTS if value == 1}
    assert RESET_EVENTS == [(2.0, 0)]
    assert all(edge in rising and edge > 2.0 for edge, _ in VALID_EVENTS)
    assert all(edge in rising and 2.5 <= edge < 4.5 for edge, _ in DATA_EVENTS[1:-1])


def encode(layout, name):
    frames = [render(layout, index*FRAME_MS/1000) for index in range(DURATION_MS//FRAME_MS)]
    # A single palette for all frames avoids palette shimmer; no noisy dithering.
    sample_indices = (0, 4, 9, 16, 24, 32, 40, 48, 64, 96)
    samples = Image.new("RGB", (frames[0].width, frames[0].height*len(sample_indices)))
    for row, index in enumerate(sample_indices):
        samples.paste(frames[index], (0, row*frames[0].height))
    palette = samples.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    gif_path = ROOT/f"{name}.gif"
    indexed[0].save(gif_path, save_all=True, append_images=indexed[1:],
                    duration=FRAME_MS, loop=0, disposal=1, optimize=True,
                    comment=b"TOHRU | Illustrative synchronous timing; not measured research data")
    render(layout, 4.5).quantize(palette=palette, dither=Image.Dither.NONE).convert("RGB").save(
        ROOT/f"{name}.png", optimize=True)
    del frames, indexed, samples
    durations, hashes = [], set()
    with Image.open(gif_path) as gif:
        first = gif.convert("RGB")
        for index in range(gif.n_frames):
            gif.seek(index)
            frame = gif.convert("RGB")
            hashes.add(sha256(frame.tobytes()).hexdigest())
            durations.append(gif.info["duration"])
        assert gif.info.get("loop") == 0
        assert gif.size == (layout.width*SCALE, layout.height*SCALE)
        assert len(hashes) >= 30
        assert sum(durations) == DURATION_MS
        assert ImageChops.difference(first, frame).getbbox() is None, "Loop seam differs"
        assert gif_path.stat().st_size < 2*1024*1024, "GIF exceeds size budget"
        result = dict(file=gif_path.name, dimensions=gif.size, frames=gif.n_frames,
                      unique_frames=len(hashes), duration_ms=sum(durations),
                      bytes=gif_path.stat().st_size, loop=0)
    print(json.dumps(result))
    return result


def review(directory, results):
    directory.mkdir(parents=True, exist_ok=True)
    times_ms = (0, 500, 1200, 2400, 3600, 4500, 7000, 9900)
    sheet = Image.new("RGB", (960*2, 348*4), "#0E1319")
    for tile, time_ms in enumerate(times_ms):
        with Image.open(ROOT/"hero.gif") as gif:
            elapsed = 0
            for frame_index in range(gif.n_frames):
                gif.seek(frame_index)
                elapsed += gif.info["duration"]
                if elapsed > time_ms:
                    break
            frame = gif.convert("RGB").resize((960, 320), Image.Resampling.LANCZOS)
        x, y = (tile % 2)*960, (tile // 2)*348
        sheet.paste(frame, (x, y+28))
        text(ImageDraw.Draw(sheet), x/SCALE+10, y/SCALE+4, f"{time_ms/1000:.1f} s",
             8, MUTED, "mono")
    sheet.save(directory/"contact-sheet.png", optimize=True)
    report = {"assets": results, "pillow": PILLOW_VERSION,
              "fonts": {kind: {"name": path.name, "sha256": sha256(path.read_bytes()).hexdigest()}
                        for kind, path in FONT_PATHS.items()},
              "timing": "Active-high reset falls at t=2; valid high on [2.5,4.5); data changes on rising edges 2.5 and 3.5.",
              "review": "Illustrative signals; not measured or completed research. README body checked separately."}
    (directory/"asset-report.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sans-font", type=Path, default=Path("C:/Windows/Fonts/segoeui.ttf"))
    parser.add_argument("--bold-font", type=Path, default=Path("C:/Windows/Fonts/segoeuib.ttf"))
    parser.add_argument("--mono-font", type=Path, default=Path("C:/Windows/Fonts/consola.ttf"))
    parser.add_argument("--review-dir", type=Path)
    args = parser.parse_args()
    for kind in ("sans", "bold", "mono"):
        path = getattr(args, kind+"_font")
        if not path.is_file():
            parser.error(f"Missing {path}. Supply an installed font using --{kind}-font.")
        FONT_PATHS[kind] = path
    validate_sequence()
    results = [encode(DESKTOP, "hero"), encode(MOBILE, "hero-mobile")]
    if args.review_dir:
        review(args.review_dir, results)


if __name__ == "__main__":
    main()
