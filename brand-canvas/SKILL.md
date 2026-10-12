---
name: brand-canvas
description: Builds a brand identity and website visual design as a claude.ai Design canvas, in approved stages — round-one marks with lockups and favicons, a colour and type system, home page mockups at desktop and phone width, then ten more marks, the owner's pick (with their own edits carried through), ten wordmark typefaces beside it, and the choices applied back to the mockups. Use when someone wants a logo, brand identity, visual direction, wordmark or font options, or a "visual design for the site" for a company, product or app, or asks for a canvas like the Zewify one.
---

# Brand canvas

Produces one Design canvas that grows board by board as the owner decides.
A finished example lives in [examples/zewify/](examples/zewify/) — the six boards, `canvas.json`, and the specs behind the two generated boards.
Board specs, canvas mechanics and the quality bar are in [REFERENCE.md](REFERENCE.md); read it before the first board.

## Before any board

1. Gather the brief **one question at a time**, each multiple choice with a recommended option first, labelled "(Recommended)":
   who it is for and what the site must make them believe; which products appear; the feel (quiet studio / bold startup / matched to a product); hard rules (e.g. never name a person, no invented facts); contact and jurisdiction if the site needs them.
2. Read every product's own repo for its real colours, icon, fonts and features. **Every claim on a board must trace to a source**; missing facts become `[PLACEHOLDER]`, never invented copy.
3. `Artifact` → `action: "quickstart"`, `intent: "design"`, then create the canvas with the returned `type_url`, a `title`, and `auto_open: "after_first_write"`. Follow the type's own instructions for the file shapes; where they disagree with this skill, the type wins.

## Stages — stop and wait for the owner after each

| Stage | Boards (file) | Owner decides |
|---|---|---|
| 1. Direction | `Logo.dc.html` (3 marks, lockups on light/dark/accent, favicon 16/32/64, rules) · `System.dc.html` (light and dark tokens, product colours, type specimen) · `Main.dc.html` (home, 1440) · `Mobile.dc.html` (home, 390) | the feel, and whether to explore more marks |
| 2. More marks | `Logos.dc.html`, from `scripts/marks_board.py` | which mark; they may hand-edit it on the canvas |
| 3. Pick | edit `Logos.dc.html`; swap the mark into `Main`/`Mobile` | confirms the mark and its small-size build |
| 4. Wordmark | `Wordmark.dc.html`, from `scripts/type_board.py` | the typeface |
| 5. Apply | update `Main`, `Mobile`, `System` to the chosen face | the canvas is the spec for the build |

Each stage ends with a short reply: the link, what is on the new board, **three picks with one-line reasons**, and what the owner should check.
Do not render or screenshot the canvas to verify it unless the owner asks (the Design type forbids it).

## Generating the two big boards

```bash
python3 scripts/marks_board.py marks.json <root>/project/Logos.dc.html     # prints {"w","h"}
python3 scripts/type_board.py fonts.json <root>/project/Wordmark.dc.html
python3 scripts/add_board.py <freshly-read canvas.json> Logos.dc.html <w> <h> "Logo — ten more marks"
```

Write the spec JSON first ([examples/zewify/make_specs.py](examples/zewify/make_specs.py) shows both shapes).
Draw marks on a 64-unit grid with the `{accent}` `{deep}` `{soft}` `{paper}` tokens, never literal colours, so the dark strip recolours itself.
Ten marks must differ in **kind**, not just detail: negative space, faceted, dots, organic, shape-only, monoline, symmetric, line-and-dot — and at least two with no letterform at all.

## Every revision

1. **Read before you write.** `Artifact` `read` the index and every board you will touch from the live artifact; the owner edits it by hand between turns.
2. Diff their copy against yours before editing, and **say what they changed** ("you turned the two corner dots sage — that makes the whole diagonal light").
3. When they edit one instance of a mark, carry the edit to every instance: lockup, favicons, dark strip, mockup headers and footers.
4. Publish only the files you changed; send `canvas.json` only when the layout changes, built with `add_board.py` on the copy you just read.

## Do not

- Put a second serif beside the chosen one; when the wordmark face changes, headings follow it.
- Put product colours in the company chrome — they belong inside that product's card only.
- Leave an approved mockup claim that the product no longer supports; re-check facts when a product changes.
