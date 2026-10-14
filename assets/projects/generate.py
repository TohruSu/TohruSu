#!/usr/bin/env python3
"""Rebuild five profile previews offline using only Python's standard library."""

import csv
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
BG, SURFACE, TEXT = "#171D24", "#29333E", "#F0ECE5"
COPPER, STEEL, MUTED = "#C49A72", "#71818B", "#AAB5BD"
FONT = "ui-sans-serif, 'DejaVu Sans', sans-serif"


def text(x, y, value, size=28, color=TEXT, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
        f"{escape(str(value))}</text>"
    )


def line(x1, y1, x2, y2, color=SURFACE, width=1.5, extra=""):
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="{width}" {extra}/>'
    )


def frame(title, subtitle, label, description):
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="480" '
        'viewBox="0 0 960 480" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        f'<rect x="1" y="1" width="958" height="478" rx="16" fill="{BG}" stroke="{SURFACE}"/>',
        text(36, 51, title, 34, weight=700),
        text(924, 49, label, 24, COPPER, 600, "end"),
        text(38, 85, subtitle, 24, MUTED),
        line(36, 104, 924, 104),
    ]


def write(name, elements):
    (ROOT / name).write_text("\n".join(elements + ["</svg>"]) + "\n", encoding="utf-8")


def latency_preview(sources):
    fixture = DATA / "latency-fixture.csv"
    if hashlib.sha256(fixture.read_bytes()).hexdigest() != sources["linux"]["fixture_sha256"]:
        raise ValueError("Latency source changed; review and update its provenance first.")
    with fixture.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    values = sorted(int(row["latency_ns"]) for row in rows)
    if values != [0, 10, 20, 30, 100]:
        raise ValueError("The documented preview uses the original five-point synthetic fixture.")
    count = len(values)
    svg = frame(
        "Latency distribution",
        "CSV fixture · 5 observations · not hardware measurements",
        "SYNTHETIC",
        "ECDF of synthetic latencies 0, 10, 20, 30, and 100 ns. "
        "Four of five observations are at or below 30 ns; the ECDF there is 0.8.",
    )
    left, top, width, height = 118, 144, 784, 254
    px = lambda value: left + value / 100 * width
    py = lambda value: top + (1 - value) * height
    for value in (0, 0.5, 1):
        svg += [line(left, py(value), left + width, py(value)), text(100, py(value) + 9, f"{value:.1f}", 28, MUTED, anchor="end")]
    for value in (0, 20, 40, 60, 80, 100):
        svg += [line(px(value), top, px(value), top + height), text(px(value), 433, value, 28, MUTED, anchor="middle")]
    points = [(values[0], 0)]
    for index, value in enumerate(values):
        points += [(value, index / count), (value, (index + 1) / count)]
    path = " ".join(f'{"M" if i == 0 else "L"} {px(x):.2f},{py(y):.2f}' for i, (x, y) in enumerate(points))
    area = path + f" L {px(values[-1]):.2f},{py(0):.2f} Z"
    svg += [
        f'<path id="ecdf-area" d="{area}" fill="{COPPER}" fill-opacity="0.08"/>',
        f'<path id="ecdf" d="{path}" fill="none" stroke="{COPPER}" stroke-width="3.5" stroke-linejoin="round"/>',
        f'<circle cx="{px(30):.2f}" cy="{py(0.8):.2f}" r="5" fill="{BG}" stroke="{COPPER}" stroke-width="2.5"/>',
        text(119, 132, "ECDF", 24, MUTED),
        text(442, 265, "4 / 5 at 30 ns", 34, weight=600),
        text(442, 305, "ECDF = 0.8", 28, MUTED),
        text(510, 467, "Wake-up lateness (ns)", 28, MUTED, anchor="middle"),
    ]
    write("linux-ecdf.svg", svg)


def navigation_preview(sources):
    geometry = DATA / "tracking-geometry.json"
    if hashlib.sha256(geometry.read_bytes()).hexdigest() != sources["navigation"]["geometry_sha256"]:
        raise ValueError("Trajectory input changed; review and update its provenance first.")
    data = json.loads(geometry.read_text())
    if data["source_sha256"] != sources["navigation"]["source_svg_sha256"]:
        raise ValueError("Trajectory provenance differs from the reviewed source.")
    svg = frame(
        "Synthetic path tracking",
        "Same +0.5 m start · 6 m left turn · not field data",
        "SIMULATION",
        "Original synthetic reference, Stanley, and Pure Pursuit trajectories. "
        "RMS cross-track errors are 0.236 m and 0.170 m respectively. "
        "All source curve coordinates are retained and scaled uniformly.",
    )
    original = data["plot"]
    left, top, size = 88, 128, 284
    scale = size / original["size"]
    px = lambda value: left + (value - original["min"]) / (original["max"] - original["min"]) * size
    py = lambda value: top + (original["max"] - value) / (original["max"] - original["min"]) * size
    svg += [f'<rect x="{left}" y="{top}" width="{size}" height="{size}" fill="none" stroke="{SURFACE}"/>']
    for value in (0, 2, 4, 6):
        svg += [
            line(px(value), top, px(value), top + size),
            line(left, py(value), left + size, py(value)),
            text(px(value), 444, value, 28, MUTED, anchor="middle"),
            text(72, py(value) + 9, value, 28, MUTED, anchor="end"),
        ]
    svg += [text(230, 469, "X (m)", 26, MUTED, anchor="middle"), text(38, 124, "Y (m)", 26, MUTED)]
    tx, ty = left - original["left"] * scale, top - original["top"] * scale
    svg += [f'<g id="source-trajectories" transform="translate({tx:.8f} {ty:.8f}) scale({scale:.8f})">']
    svg += [
        f'<path id="reference" d="{data["reference_path"]}" fill="none" stroke="{STEEL}" stroke-width="2" '
        'stroke-dasharray="6 5" vector-effect="non-scaling-stroke"/>'
    ]
    for index, curve in enumerate(data["traces"]):
        color = TEXT if index == 0 else COPPER
        svg += [
            f'<path id="trajectory-{index}" d="{curve["path"]}" fill="none" stroke="{color}" '
            'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>',
            f'<circle cx="{curve["endpoint"][0]}" cy="{curve["endpoint"][1]}" r="5" fill="{color}"/>',
        ]
    svg += [f'<circle cx="{data["start"][0]}" cy="{data["start"][1]}" r="5.5" fill="{TEXT}"/>', "</g>"]
    svg += [line(466, 151, 510, 151, STEEL, 2, 'stroke-dasharray="6 5"'), text(528, 160, "Reference path", 28, MUTED)]
    for index, curve in enumerate(data["traces"]):
        y = 229 + index * 106
        color = TEXT if index == 0 else COPPER
        svg += [
            line(466, y - 10, 510, y - 10, color, 3),
            text(528, y, curve["name"], 34, weight=600),
            text(528, y + 38, f'RMS CTE: {curve["rms_cte_m"]} m', 28, MUTED),
        ]
    svg += [text(466, 425, "CTE = cross-track error", 26, MUTED), text(466, 463, "Original simulation geometry", 24, MUTED)]
    write("navigation-tracking.svg", svg)


def node(x, y, width, title, subtitle, height=98, accent=False):
    return [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" '
        f'fill="{SURFACE}" stroke="{COPPER if accent else STEEL}" stroke-width="1.5"/>',
        text(x + width / 2, y + 39, title, 28, weight=600, anchor="middle"),
        text(x + width / 2, y + 73, subtitle, 24, MUTED, anchor="middle"),
    ]


def architecture_preview():
    svg = frame(
        "Multimodal event flow",
        "Documented application design · not a screenshot",
        "ARCHITECTURE",
        "Video and pose generate fall events and person ROIs. Optional relative depth "
        "adds context; speech supplies help keywords. Fusion supplies alerts to PyQt5, "
        "which also displays frames, depth, and health. This is an architecture illustration, not a hardware result.",
    )
    svg += [
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">',
        f'<path d="M 0 0 L 10 5 L 0 10 Z" fill="{COPPER}"/></marker>',
        '<marker id="steel-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">',
        f'<path d="M 0 0 L 10 5 L 0 10 Z" fill="{STEEL}"/></marker></defs>',
        f'<path d="M 308 189 H 342" fill="none" stroke="{COPPER}" stroke-width="2.5" marker-end="url(#arrow)"/>',
        f'<path d="M 174 238 V 294" fill="none" stroke="{STEEL}" stroke-width="2" marker-end="url(#steel-arrow)"/>',
        f'<path d="M 308 343 H 324 V 265 H 408 V 238" fill="none" stroke="{STEEL}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#steel-arrow)"/>',
        f'<path d="M 476 294 V 238" fill="none" stroke="{COPPER}" stroke-width="2.5" marker-end="url(#arrow)"/>',
        f'<path d="M 610 189 H 633 V 259 H 656" fill="none" stroke="{COPPER}" stroke-width="2.5" marker-end="url(#arrow)"/>',
        f'<path d="M 174 140 V 118 H 789 V 207" fill="none" stroke="{STEEL}" stroke-width="1.5" marker-end="url(#steel-arrow)"/>',
    ]
    svg += node(40, 140, 268, "Video / pose", "Fall detection")
    svg += node(40, 294, 268, "Relative depth", "Optional context")
    svg += node(342, 140, 268, "Event fusion", "L1 / L2 alerts", accent=True)
    svg += node(342, 294, 268, "Audio / speech", "Help keywords")
    svg += [
        f'<rect x="656" y="207" width="266" height="123" rx="12" fill="{SURFACE}" stroke="{STEEL}" stroke-width="1.5"/>',
        text(789, 247, "PyQt5 monitor", 28, weight=600, anchor="middle"),
        text(789, 281, "Frames + depth", 24, MUTED, anchor="middle"),
        text(789, 311, "Alerts + health", 24, MUTED, anchor="middle"),
        text(192, 272, "ROI", 24, MUTED),
        text(494, 272, "help", 24, MUTED),
        text(795, 170, "frame", 24, MUTED),
        text(40, 448, "Relative depth adds context; it is not calibrated distance.", 26, MUTED),
    ]
    write("jetson-architecture.svg", svg)



def retail_preview(sources):
    """Render the documented, synthetic k=2..5 silhouette comparison."""
    reference = sources["retail"]
    values = reference["silhouette_by_k"]
    if sorted(values) != ["2", "3", "4", "5"]:
        raise ValueError("Expected four documented candidate cluster counts.")
    if any(not 0 <= float(value) <= 0.2 for value in values.values()):
        raise ValueError("Review changes to the preview scale before regenerating.")

    # Preserve the original retail SVG's metadata and serialization exactly.
    def retail_text(x, y, value, size=28, color=TEXT, weight=None, anchor=None):
        attributes = f' font-weight="{weight}"' if weight is not None else ""
        if anchor is not None:
            attributes += f' text-anchor="{anchor}"'
        return (
            f'<text x="{x}" y="{y}" fill="{color}" '
            f'font-family="ui-sans-serif, DejaVu Sans, sans-serif" '
            f'font-size="{size}"{attributes}>{escape(str(value))}</text>'
        )

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="480" '
        'viewBox="0 0 960 480" role="img" aria-labelledby="title desc">',
        '<title id="title">Retail segmentation diagnostics</title>',
        f'<desc id="desc">Silhouette scores for k two through five on {reference["n_rows"]} '
        'independently generated synthetic retail records: '
        + ", ".join(f'{float(values[k]):.3f}' for k in ("2", "3", "4"))
        + f', and {float(values["5"]):.3f}'
        + '. All scores indicate weak separation.</desc>',
        f'<rect x="1" y="1" width="958" height="478" rx="16" fill="{BG}" stroke="{SURFACE}"/>',
        retail_text(36, 51, "Retail segmentation", 34, weight=700),
        retail_text(924, 49, "SYNTHETIC", 24, COPPER, 600, "end"),
        retail_text(38, 85, f'{reference["n_rows"]} records · seed {reference["seed"]} · PCA + KMeans', 24, MUTED),
        f'<line x1="36" y1="104" x2="924" y2="104" stroke="{SURFACE}" stroke-width="1.5"/>',
    ]
    svg += [
        retail_text(66, 149, "Candidate clusters", 25, MUTED),
        retail_text(410, 149, "Silhouette score", 25, MUTED),
    ]
    for index, k in enumerate(("2", "3", "4", "5")):
        value = float(values[k])
        y = 196 + 61 * index
        width = round(value / 0.2 * 370)
        svg += [
            retail_text(90, y + 27, f"k={k}", 28),
            f'<rect x="410" y="{y}" width="370" height="31" rx="4" fill="{SURFACE}"/>',
            f'<rect x="410" y="{y}" width="{width}" height="31" rx="4" fill="{COPPER if index == 0 else STEEL}"/>',
            retail_text(815, y + 27, f"{value:.3f}", 28),
        ]
    svg.append(retail_text(38, 465, "Weak separation across candidate partitions · illustrative data", 24, MUTED))
    write("retail-segmentation.svg", svg)


def roomshelf_preview():
    svg = frame(
        "RoomShelf application flow",
        "React catalog · Flask API · SQLite persistence",
        "ARCHITECTURE",
        "React keeps catalog search, filters, sorting, and pagination in the URL, "
        "and comparison selections for up to three products in browser memory. "
        "Flask serves catalog reads and shortlist writes, with signed sessions and "
        "CSRF and Origin checks for mutations. SQLite stores products, anonymous "
        "sessions, and shortlist items. Architecture illustration, not an application screenshot.",
    )
    svg += [
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="5" markerHeight="5" orient="auto-start-reverse">',
        f'<path d="M 0 0 L 10 5 L 0 10 Z" fill="{COPPER}"/></marker></defs>',
        f'<path d="M 320 236 H 374" fill="none" stroke="{COPPER}" '
        'stroke-width="2.5" marker-end="url(#arrow)"/>',
        f'<path d="M 620 236 H 680" fill="none" stroke="{COPPER}" '
        'stroke-width="2.5" marker-end="url(#arrow)"/>',
    ]
    for x, width in ((40, 280), (374, 246), (680, 242)):
        svg.append(
            f'<rect x="{x}" y="140" width="{width}" height="246" rx="12" '
            f'fill="{SURFACE}" stroke="{COPPER if x == 374 else STEEL}" stroke-width="1.5"/>'
        )
    svg += [
        text(180, 182, "React catalog", 28, weight=600, anchor="middle"),
        text(180, 220, "Search + filters", 24, MUTED, anchor="middle"),
        text(180, 252, "Sort + page in URL", 24, MUTED, anchor="middle"),
        line(60, 273, 300, 273, STEEL),
        text(180, 310, "Compare up to 3", 26, weight=600, anchor="middle"),
        text(180, 345, "Browser memory", 24, MUTED, anchor="middle"),
        text(497, 182, "Flask API", 28, weight=600, anchor="middle"),
        text(497, 220, "Catalog reads", 24, MUTED, anchor="middle"),
        text(497, 252, "Shortlist writes", 24, MUTED, anchor="middle"),
        line(394, 273, 600, 273, STEEL),
        text(497, 310, "Signed sessions", 24, MUTED, anchor="middle"),
        text(497, 345, "CSRF + Origin", 24, MUTED, anchor="middle"),
        text(801, 182, "SQLite", 28, weight=600, anchor="middle"),
        text(801, 226, "Products", 26, MUTED, anchor="middle"),
        text(801, 270, "Anonymous sessions", 22, MUTED, anchor="middle"),
        text(801, 314, "Shortlist items", 26, MUTED, anchor="middle"),
        text(40, 430, "Comparison selection stays in browser memory.", 26, MUTED),
        text(40, 465, "Anonymous shortlists persist in SQLite.", 26, MUTED),
    ]
    write("roomshelf-overview.svg", svg)


def main():
    sources = json.loads((DATA / "sources.json").read_text())
    latency_preview(sources)
    navigation_preview(sources)
    architecture_preview()
    retail_preview(sources)
    roomshelf_preview()
    print("Regenerated five 960 × 480 previews from local pinned sources; no external packages or network needed.")


if __name__ == "__main__":
    main()
