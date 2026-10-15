# Profile artwork

All artwork is stored locally. The project previews adapt the linked repositories' data and documented design; the remaining graphics are original profile artwork. The profile loads no remote graphics, fonts, statistics cards, or scripts.

- `hero.svg`: desktop banner with a graphite surface, warm ivory text, and muted copper signal trace. The trace is decorative, not benchmark data.
- `hero-mobile.svg`: the same identity in a compact layout, selected below 600 px with GitHub-supported `<picture>` markup. `hero.svg` is the default image.
- `languages.svg`, `web.svg`, `systems.svg`, `applied.svg`: original category pictograms in a shared muted copper tone, not technology logos or proficiency ratings.
- `prompt.gif`: a 24 × 16 px muted copper terminal cursor that changes brightness for four seconds, then rests. It conveys no live status.
- `prompt.svg`: a static alternative selected for reduced-motion preferences; also usable as a direct replacement for the GIF.

The palette uses solid graphite (`#171D24`), slate (`#29333E`), ivory (`#F0ECE5`), copper (`#C49A72`), and steel gray (`#71818B`). Small inline icons and the cursor use darker copper (`#A17D5A`) for contrast against both white and GitHub's dark background; the dim cursor frame uses `#7F7163`. Banner terminal text uses lighter steel (`#AAB5BD`). No gradients are used.

The banner uses system fonts and an opaque graphite background in both GitHub themes. SVG files can be edited as text; core profile information stays in the Markdown rather than depending on the images. Decorative inline images have empty alt text because their adjacent headings provide the label.

To remove motion, change the prompt image's `src` in the root README to `./assets/prompt.svg`. No workflow or runtime dependencies are needed to display these assets.

## Project previews

The six previews in `projects/` share a 960 × 480 canvas, graphite surface, ivory typography, copper accents, and slate borders. The root README displays each at a maximum width of 640 px, scaling down for mobile. Informative alt text supplies the chart or diagram meaning and evidence limits.

### Linux: `projects/linux-ecdf.svg`

Synthetic output, not measured hardware performance. The ECDF is regenerated from the exact [complete CSV fixture](https://github.com/TohruSu/linux-wakeup-latency-benchmark/blob/b41c5a06f044565e6406c727aff12b483221663f/tests/fixtures/schema-v1/complete.csv), retained locally in `projects/data/latency-fixture.csv`. It contains five observations: `[0, 10, 20, 30, 100]` ns. The fraction at 30 ns is `4 / 5 = 0.8`.

This is the same data used by [the repository's ECDF image](https://github.com/TohruSu/linux-wakeup-latency-benchmark/blob/b41c5a06f044565e6406c727aff12b483221663f/docs/images/ecdf-synthetic.png). The profile preview shows the full 0–100 ns distribution rather than that image's 0–30 ns zoom. The denominator remains all five observations. Nanosecond units describe the fixture representation, not measurement accuracy.

### Navigation: `projects/navigation-tracking.svg`

Simulation output, not field-test data. The curves come from [the existing trajectory comparison](https://github.com/TohruSu/autonomous-tractor-navigation-sim/blob/106afc34753a835a9dfc6d08c5ed9f8ae3c6216d/docs/images/tracking-comparison.svg). Its three SVG paths, start/end points, source plot bounds, and rounded RMS cross-track errors are retained in `projects/data/tracking-geometry.json`.

The generator applies one uniform scale and translation to the original curve coordinates; it does not smooth, resample, or recompute trajectories. Both axes retain the original −0.8–7.6 m bounds and equal scale. The displayed errors, Stanley `0.236 m` and Pure Pursuit `0.170 m`, describe only the nominal controllers on the synthetic `left-turn-offset` scenario with a 6 m reference arc and +0.5 m initial offset. They are not a general controller ranking. The original SVG already rounds plotted coordinates and selects samples; this preview preserves that existing representation.

### Jetson: `projects/jetson-architecture.svg`

An architecture illustration, not an application screenshot or hardware output. The diagram follows [the README](https://github.com/TohruSu/jetson-multimodal-emergency-detection/blob/7cc1bd7180a40df802192e7c6fa216df91d5cc04/README.md), [architecture](https://github.com/TohruSu/jetson-multimodal-emergency-detection/blob/7cc1bd7180a40df802192e7c6fa216df91d5cc04/docs/ARCHITECTURE.md), `main.py`, `common/simscript.py`, and `ui/main_window.py` at the same pinned commit.

It shows pose-based fall detection, person-ROI relative depth, speech help keywords, event fusion, and the PyQt5 monitor. Depth adds optional context, not calibrated distance, and is not required for alert escalation. The gray frame connection reflects the UI's separate video display path. This is a conceptual application flow, not a process diagram: real pose/depth share a GPU worker, while synthetic workers read shared scene state rather than passing pose packets to simulated depth.

The original 900 × 560 window uses 12 px status text and several smaller painted labels. A faithful screenshot would make those details unreadable in a compact mobile preview, so the diagram is used instead. It contains no fictional UI, hardware accuracy, timing metrics, or deployment claims.

### Retail: `projects/retail-segmentation.svg`

An original chart based on the independently generated example in the [retail case study](https://github.com/TohruSu/retail-customer-segmentation/blob/6af50c59b9bfe9185302a52227a9f2eb09eef9ae/README.md). The example contains 720 synthetic observations (seed 2026); the documented silhouettes for k=2–5 are 0.178, 0.154, 0.147, and 0.137, respectively. The bars use the same 0–0.2 comparison scale and illustrate weak separation; they are not real survey results. The pinned values and source commit are recorded in `projects/data/sources.json`.

### RoomShelf: `projects/roomshelf-overview.svg`

An architecture illustration of the implemented React → Flask → SQLite flow, based on RoomShelf's [README](https://github.com/TohruSu/roomshelf-catalog-explorer/blob/746765244d7492da7a9f6073cf95191398111483/README.md), [architecture](https://github.com/TohruSu/roomshelf-catalog-explorer/blob/746765244d7492da7a9f6073cf95191398111483/docs/ARCHITECTURE.md), [API](https://github.com/TohruSu/roomshelf-catalog-explorer/blob/746765244d7492da7a9f6073cf95191398111483/docs/API.md), and [operations](https://github.com/TohruSu/roomshelf-catalog-explorer/blob/746765244d7492da7a9f6073cf95191398111483/docs/OPERATIONS.md) at the same reviewed commit.

React keeps applied search, filters, sorting, and pagination in the URL. Comparison selections stay in browser memory, with a limit of three products; `frontend/src/state/CompareProvider.tsx` and `frontend/src/pages/ComparePage.tsx` confirm that the table loads ordinary product details without a dedicated comparison API. Flask serves catalog reads and transactional shortlist writes. `backend/roomshelf/catalog.py`, `shortlist.py`, `models.py`, and `security.py` confirm SQLite-backed products, anonymous sessions, and memberships, with signed sessions and CSRF/Origin validation for shortlist mutations. Source SHA-256 hashes are recorded in `projects/data/sources.json`.

The preview summarizes application responsibilities, not a deployed topology or an application screenshot. RoomShelf's actual [browser captures](https://github.com/TohruSu/roomshelf-catalog-explorer/blob/746765244d7492da7a9f6073cf95191398111483/docs/screenshots/README.md) show a fictional furniture catalog with local illustrations. Diagram labels and connections are defined in the standard-library generator and regenerate offline using the command below.

### AdaptiveQueue: `projects/adaptivequeue-flow.svg`

A decision-flow illustration of the tabular Q-Learning meta-scheduler, based on [AdaptiveQueue's README](https://github.com/TohruSu/adaptivequeue/blob/1bbfc3641c1257faaa4361f9943c5ed2d18b27de/README.md), [simulation design](https://github.com/TohruSu/adaptivequeue/blob/1bbfc3641c1257faaa4361f9943c5ed2d18b27de/docs/simulation.md), and [recorded experiments](https://github.com/TohruSu/adaptivequeue/blob/1bbfc3641c1257faaa4361f9943c5ed2d18b27de/docs/experiments.md). It shows the observed job queue, one of four selectable heuristic policies, and a non-preemptive worker. The stored benchmark evaluates three independently trained models against five baselines on Stable, Bursty, and Mixed workloads. This overview is a diagram of the simulation, not a live scheduler.

## Regeneration

From the profile repository root:

```sh
python3 assets/projects/generate.py
git diff --check
```

The deterministic generator uses only Python's standard library, the retained local inputs, the pinned retail reference values, and the documented architecture labels. It needs no network access, plotting packages, Qt, .NET, model weights, or changes to the linked project repositories. Running it twice produces byte-identical SVGs, preserving all earlier previews.

`projects/data/sources.json` records the reviewed upstream commits and source SHA-256 hashes. The retained fixture and extracted geometry hashes are checked during regeneration. The retail preview uses documented rounded scores; update them only after checking the source analytical report. To refresh a preview, inspect the new upstream evidence, update the retained source data and provenance together, then regenerate and review the result. Architecture labels and connections are defined directly in the generator.
