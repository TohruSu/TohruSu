# Profile artwork

All artwork in this directory is original and stored locally. The profile loads no remote graphics, fonts, statistics cards, or scripts.

- `hero.svg`: desktop banner with a graphite surface, warm ivory text, and muted copper signal trace. The trace is decorative, not benchmark data.
- `hero-mobile.svg`: the same identity in a compact layout, selected below 600 px with GitHub-supported `<picture>` markup. `hero.svg` is the default image.
- `languages.svg`, `web.svg`, `systems.svg`, `applied.svg`: original category pictograms in a shared muted copper tone, not technology logos or proficiency ratings.
- `prompt.gif`: a 24 × 16 px muted copper terminal cursor that changes brightness for four seconds, then rests. It conveys no live status.
- `prompt.svg`: a static alternative selected for reduced-motion preferences; also usable as a direct replacement for the GIF.

The palette uses solid graphite (`#171D24`), slate (`#29333E`), ivory (`#F0ECE5`), copper (`#C49A72`), and steel gray (`#71818B`). Small inline icons and the cursor use darker copper (`#A17D5A`) for contrast against both white and GitHub's dark background; the dim cursor frame uses `#7F7163`. Banner terminal text uses lighter steel (`#AAB5BD`). No gradients are used.

The banner uses system fonts and an opaque graphite background in both GitHub themes. SVG files can be edited as text; core profile information stays in the Markdown rather than depending on the images. Decorative inline images have empty alt text because their adjacent headings provide the label.

To remove motion, change the prompt image's `src` in the root README to `./assets/prompt.svg`. No workflow or runtime dependencies are needed to display these assets.
