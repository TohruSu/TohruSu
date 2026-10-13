# Profile artwork

All artwork in this directory is original and stored locally. The profile loads no remote graphics, fonts, statistics cards, or scripts.

- `hero.svg`: desktop banner. The signal trace is decorative, not benchmark data.
- `hero-mobile.svg`: the same identity in a compact layout, selected below 600 px with GitHub-supported `<picture>` markup. `hero.svg` is the default image.
- `languages.svg`, `web.svg`, `systems.svg`, `applied.svg`: original category pictograms, not technology logos or proficiency ratings.
- `prompt.gif`: a 24 × 16 px terminal cursor that changes brightness for four seconds, then rests. It conveys no live status.
- `prompt.svg`: a static alternative selected for reduced-motion preferences; also usable as a direct replacement for the GIF.

The banner uses system fonts and an opaque navy background in both GitHub themes. SVG files can be edited as text; core profile information stays in the Markdown rather than depending on the images. Decorative inline images have empty alt text because their adjacent headings provide the label.

To remove motion, change the prompt image's `src` in the root README to `./assets/prompt.svg`. No workflow or runtime dependencies are needed to display these assets.
