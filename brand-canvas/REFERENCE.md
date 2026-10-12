# Brand canvas — reference

## Canvas mechanics

- One canvas per brand. Its files live under `project/`: the index `project/canvas.json` and one `project/<Name>.dc.html` per artboard.
  Write them under one local folder (`<root>/project/…`) and publish with `root`, `file_path` = the index, `files` = the boards.
- Board files follow the Design type's `format.md` (the create result hands it over): keep `<script src="./support.js"></script>` exactly, give the root element a fixed `width`/`height` equal to the board's entry, include the `data-dc-script` block with a matching `$preview`, inline `style=""` for everything the owner may want to restyle, `<helmet><style>` only for `body` and `a`.
- The only network a board may use is a Google Fonts `css2` `<link>` in `<helmet>` and uploaded assets.
  Product icons and screenshots are uploaded first (`publish` with `url`, `asset: true`, `file_paths`) and referenced by the returned `/_blob/<id>` URL, verbatim.
- Tweaks are levers, not copy: one `accent` colour prop with three or four swatch `options` on the desktop home board is enough.
- Layout: identity row at `y = 0` (Logo, System, then Logos and Wordmark appended to the right), home row at `y = 1600` (Main at `x = 0`, Mobile at `x = 1520`).
  80px between boards in a row; a `title1` note 300px above each row (`"Brand — identity and system"`, `"Home page"`), its `maxW` spanning the row.
- Too tall beats clipped: size a board generously; empty space at its foot is harmless.
- Before every publish to an existing canvas, `read` it: a newer version from the owner's hand edits must be merged onto, never overwritten.

## Board specs

**Logo (1440 × ~1080).** Eyebrow "Identity", title "The ⟨Brand⟩ mark", one-sentence idea of the recommended mark.
Three option cards (mark at ~148px on paper, name, one-line trade-off, a "Recommended" chip on one).
A row of three lockups: on light, on dark, on the accent.
Favicon at real 16/32/64px, and the rules: wordmark face, weight, tracking, sentence case, clear space, how the second tone relates to the first.

**System (1440 × ~1180).** Light tokens and dark tokens as swatches with name and hex (paper, ink, ink-muted, rule, accent).
Each product's own colours with their source file named ("From `brand.ts`"), marked as used only inside that product's card.
A type specimen: display sizes in the display face, lead/body/buttons in the text face, with sizes and weights written under each.

**Home — desktop (1440 wide) and phone (390 wide).** Header (lockup + three nav links), hero (eyebrow, display headline, lead, primary and secondary buttons), products (one card per product **in that product's identity**: its icon, its name in its own wordmark face, status chip, one-liner, three facts, platforms, action), principles (three, each with a stroke icon), footer (brand + tagline, Products, Company, Support, © line).
Phone: same content stacked, full-width 52px buttons, 44px tap targets, body 17px or more.

**Ten more marks (1600 wide)** and **ten typefaces (1600 wide)**: generated; see the scripts' docstrings.
The typeface board also shows the mark at 16/32/64 and, if the mark crowds at 16px, a small-size build (mark on the accent tile, slightly heavier) next to it.

## Quality bar

- Measure contrast instead of eyeballing it: text 4.5:1, large text (≥ 24px, or ≥ 18.7px bold) 3:1. White on a mid orange is about 3:1 — usable only for large bold text; use the product's darker step for small links.
- Smallest body size 18px on desktop, 17px on phone; the owner's 2560px DPR-1 display makes anything smaller unreadable.
- Every mark is judged at 16px. Fine strokes, many small dots and thin gaps fail there; say so on the board and offer a small-size build.
- Pick a nameable direction and hold it: one accent and its tints, a toned paper ground, one display face and one text face.
  Avoid AI tropes: gradient washes, left-border cards, emoji, Inter or Roboto as the voice.
- Every mark and colour has a dark-scheme version on the board, not just a promise of one.

## Copy rules learned the hard way

- **Nothing invented.** No team, headcount, history, testimonials, reply-time promises or statistics. Principles ("we don't sell data") are public promises — flag them for the owner to accept.
- **No filler asides.** A line like "Each lives on its own address at …" adds nothing and goes stale; cut it.
- **Legal lines do not go in the footer.** Governing law belongs in the Terms; the footer is "© ⟨year⟩ ⟨Brand⟩" and links. An About page says "an independent studio based in ⟨country⟩", not legal language.
- **A brand is not a company until it is registered.** Never write Inc., Ltd., "registered" or "our team" unless that is true.
- **Each product card states only what that product ships today**, sourced from its repo; a feature that is specced but unbuilt is not on the board.
- **Not for sale until it is for sale:** a pre-launch product says "Coming soon" and shows no price or store link.

## Picking and applying

- When the owner picks, restate the choice in one line and update every instance in one pass; then present the next stage.
- When the wordmark face is chosen, the headings follow it (one serif, not two); the text face stays.
- The finished canvas is the visual spec for the build: point the implementation spec at its URL and copy its exact tokens.
