#!/usr/bin/env python3
"""Render a "N more marks" board for a Design canvas from a JSON spec.

Each mark is shown large, beside the wordmark, at real favicon sizes (16, 32),
and again in a dark strip at the bottom, so a mark that only works big is
caught on the board rather than after it ships.

    python3 marks_board.py spec.json out/project/Logos.dc.html

Prints the board's width and height for its canvas.json entry.

Spec shape (see ../examples/zewify/marks.json):
  brand, eyebrow, title, intro
  palette: accent, deep, soft, paper, ink, muted, rule, surface,
           dark: { accent, deep, soft, paper }
  fonts:   display { family, css, weight, tracking }, text { family, css }
  marks:   [{ name, tag, blurb, svg }]   svg = body of a 64x64 viewBox

In a mark's svg, {accent} {deep} {soft} {paper} become palette colours (the
dark strip swaps in palette.dark) and {uid} becomes a per-instance suffix, so
clipPath ids never collide when the same mark is drawn four times.
"""
import itertools
import json
import math
import sys

_uid = itertools.count()
COLS = 5


def paint(body, colours):
    out = body.replace('{uid}', str(next(_uid)))
    for key in ('accent', 'deep', 'soft', 'paper'):
        out = out.replace('{' + key + '}', colours[key])
    return out


def svg(body, colours, size):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true">{paint(body, colours)}</svg>'


def main(spec_path, out_path):
    spec = json.load(open(spec_path))
    p, f = spec['palette'], spec['fonts']
    light = {k: p[k] for k in ('accent', 'deep', 'soft', 'paper')}
    dark = p['dark']
    disp = f"'{f['display']['family']}', Georgia, serif"
    text = f"'{f['text']['family']}', system-ui, sans-serif"
    word = (f'<span style="font-family: {disp}; font-weight: {f["display"]["weight"]}; font-size: 24px; '
            f'letter-spacing: {f["display"]["tracking"]}; color: {p["ink"]};">{spec["brand"]}</span>')

    cards = []
    for i, m in enumerate(spec['marks'], 1):
        cards.append(f'''
    <div style="display: flex; flex-direction: column; gap: 16px; padding: 18px; background: {p['surface']}; border: 1px solid {p['rule']}; border-radius: 16px;">
      <div style="height: 196px; display: flex; align-items: center; justify-content: center; background: {p['paper']}; border-radius: 10px;">{svg(m['svg'], light, 124)}</div>
      <div style="display: flex; flex-direction: column; gap: 6px;">
        <div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px;">
          <span style="font-size: 18px; font-weight: 600;">{i:02d} · {m['name']}</span>
          <span style="font-size: 13px; color: {p['muted']}; white-space: nowrap;">{m['tag']}</span>
        </div>
        <p style="margin: 0; font-size: 15px; line-height: 1.5; color: {p['muted']}; min-height: 90px;">{m['blurb']}</p>
      </div>
      <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 14px; border-top: 1px solid {p['rule']};">
        <div style="display: flex; align-items: center; gap: 8px;">{svg(m['svg'], light, 26)}{word}</div>
        <div style="display: flex; align-items: flex-end; gap: 8px;">{svg(m['svg'], light, 16)}{svg(m['svg'], light, 32)}</div>
      </div>
    </div>''')

    darks = ''.join(
        f'<div style="width: 88px; height: 88px; border-radius: 14px; background: {dark["paper"]}; display: flex; align-items: center; justify-content: center;">{svg(m["svg"], dark, 56)}</div>'
        for m in spec['marks'])

    rows = math.ceil(len(spec['marks']) / COLS)
    width, height = 1600, 64 * 2 + 150 + 40 + rows * 470 + (rows - 1) * 20 + 40 + 88 + 40

    fonts = '&amp;'.join(['family=' + f['display']['css'], 'family=' + f['text']['css']])
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{spec['brand']} logo explorations</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&amp;display=swap">
<style>
body{{margin:0;font-family:{text};background:{p['paper']};color:{p['ink']}}}
a{{color:{p['accent']}}}a:hover{{color:{p['deep']}}}
</style>
</helmet>
<div style="width: {width}px; height: {height}px; box-sizing: border-box; padding: 64px; display: flex; flex-direction: column; gap: 40px; background: {p['paper']}; color: {p['ink']}; font-family: {text};">
  <div style="display: flex; flex-direction: column; gap: 10px;">
    <div style="font-size: 15px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {p['muted']};">{spec['eyebrow']}</div>
    <h1 style="margin: 0; font-family: {disp}; font-weight: 400; font-size: 52px; line-height: 1.05; letter-spacing: -0.02em;">{spec['title']}</h1>
    <p style="margin: 0; font-size: 18px; line-height: 1.55; color: {p['muted']}; max-width: 900px;">{spec['intro']}</p>
  </div>
  <div style="display: grid; grid-template-columns: repeat({COLS}, minmax(0, 1fr)); gap: 20px;">{''.join(cards)}
  </div>
  <div style="display: flex; align-items: center; gap: 20px;">
    <span style="font-size: 15px; font-weight: 600; color: {p['muted']}; width: 120px;">On dark</span>
    <div style="display: flex; flex-wrap: wrap; gap: 16px;">{darks}</div>
  </div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{width},"height":{height}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''
    open(out_path, 'w').write(html)
    print(json.dumps({'w': width, 'h': height}))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
