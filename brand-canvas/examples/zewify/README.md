# Example: the Zewify canvas

The canvas this skill was distilled from: https://claude.ai/artifact/Sv3QZUHP69zj8raxtfKdJL

| Stage | Board |
|---|---|
| 1 | `boards/Logo.dc.html`, `boards/System.dc.html`, `boards/Main.dc.html`, `boards/Mobile.dc.html` (shown here as they ended, after stage 5) |
| 2 | `boards/Logos.dc.html` — from `marks.json` |
| 3 | the owner turned Constellation's two corner dots sage on the canvas; the edit was carried to every instance |
| 4 | `boards/Wordmark.dc.html` — from `fonts.json`; Fraunces was picked |

`make_specs.py` regenerates `marks.json` and `fonts.json`.
The `/_blob/…` image URLs in `Main` and `Mobile` resolve only inside that canvas; a new canvas uploads its own product icons.
