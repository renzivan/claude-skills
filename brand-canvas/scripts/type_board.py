#!/usr/bin/env python3
"""Render an "N typefaces beside the mark" board for a Design canvas.

Every candidate sets the wordmark next to the chosen mark on light and on dark,
plus the brand's headline in the same face, so the pairing is judged where it
will live rather than as a bare type specimen.

    python3 type_board.py spec.json out/project/Wordmark.dc.html

Prints the board's width and height for its canvas.json entry.

Spec shape (see ../examples/zewify/fonts.json):
  brand, eyebrow, title, intro, headline
  palette: as in marks_board.py
  text:    { family, css }                 the board's own UI face
  mark:    { svg, smallSvg? }              64x64 bodies, same {accent}/{soft}/
                                           {deep}/{paper} tokens; smallSvg is
                                           the favicon build, if there is one
  fonts:   [{ family, css, weight, tracking, style, note }]
           css is the Google Fonts css2 `family=` value, e.g. "Fraunces:opsz,wght@9..144,500"
"""
import json
import math
import sys

COLS = 5


def paint(body, c):
    for key in ('accent', 'deep', 'soft', 'paper'):
        body = body.replace('{' + key + '}', c[key])
    return body.replace('{uid}', '0')


def svg(body, c, size):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true">{paint(body, c)}</svg>'


def main(spec_path, out_path):
    s = json.load(open(spec_path))
    p = s['palette']
    light = {k: p[k] for k in ('accent', 'deep', 'soft', 'paper')}
    dark = p['dark']
    ui = f"'{s['text']['family']}', system-ui, sans-serif"
    mark, small = s['mark']['svg'], s['mark'].get('smallSvg')

    cards = []
    for i, f in enumerate(s['fonts'], 1):
        ff = f"'{f['family']}', system-ui, sans-serif"
        cards.append(f'''
    <div style="display: flex; flex-direction: column; gap: 14px; padding: 18px; background: {p['surface']}; border: 1px solid {p['rule']}; border-radius: 16px;">
      <div style="height: 132px; display: flex; align-items: center; justify-content: center; gap: 12px; background: {p['paper']}; border-radius: 10px;">
        {svg(mark, light, 40)}<span style="font-family: {ff}; font-weight: {f['weight']}; font-size: 44px; letter-spacing: {f['tracking']}; line-height: 1; color: {p['ink']};">{s['brand']}</span>
      </div>
      <div style="height: 64px; display: flex; align-items: center; justify-content: center; gap: 9px; background: {dark['paper']}; border-radius: 10px;">
        {svg(mark, dark, 24)}<span style="font-family: {ff}; font-weight: {f['weight']}; font-size: 25px; letter-spacing: {f['tracking']}; line-height: 1; color: {dark.get('ink', '#ecebe6')};">{s['brand']}</span>
      </div>
      <div style="font-family: {ff}; font-weight: {f['weight']}; font-size: 23px; line-height: 1.2; letter-spacing: {f['tracking']}; color: {p['ink']}; min-height: 56px;">{s['headline']}</div>
      <div style="display: flex; flex-direction: column; gap: 6px; padding-top: 12px; border-top: 1px solid {p['rule']};">
        <div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px;">
          <span style="font-size: 17px; font-weight: 600;">{i:02d} · {f['family']}</span>
          <span style="font-size: 13px; color: {p['muted']}; white-space: nowrap;">{f['style']}</span>
        </div>
        <span style="font-size: 13px; color: {p['muted']};">Weight {f['weight']} · tracking {f['tracking'].replace('-', '−')}</span>
        <p style="margin: 0; font-size: 15px; line-height: 1.5; color: {p['muted']}; min-height: 68px;">{f['note']}</p>
      </div>
    </div>''')

    sizes = ''.join(
        f'<div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">{svg(mark, light, n)}<span style="font-size: 13px; color: {p["muted"]};">{n}px</span></div>'
        for n in (16, 32, 64))
    small_block = ''
    if small:
        builds = ''.join(
            f'<div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">{svg(small, light, n)}<span style="font-size: 13px; color: {p["muted"]};">{n}px</span></div>'
            for n in (16, 32, 64))
        small_block = f'''
      <div style="width: 1px; background: {p['rule']};"></div>
      <div style="display: flex; flex-direction: column; gap: 10px;">
        <span style="font-size: 14px; font-weight: 600;">Small-size build</span>
        <div style="display: flex; align-items: flex-end; gap: 16px;">{builds}</div>
      </div>'''

    rows = math.ceil(len(s['fonts']) / COLS)
    width, height = 1600, 64 * 2 + 190 + 36 + rows * 530 + (rows - 1) * 20 + 40
    links = '&amp;'.join(['family=' + f['css'] for f in s['fonts']] + ['family=' + s['text']['css']])
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{s['brand']} wordmark typefaces</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{links}&amp;display=swap">
<style>
body{{margin:0;font-family:{ui};background:{p['paper']};color:{p['ink']}}}
a{{color:{p['accent']}}}a:hover{{color:{p['deep']}}}
</style>
</helmet>
<div style="width: {width}px; height: {height}px; box-sizing: border-box; padding: 64px; display: flex; flex-direction: column; gap: 36px; background: {p['paper']}; color: {p['ink']}; font-family: {ui};">
  <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px;">
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <div style="font-size: 15px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: {p['muted']};">{s['eyebrow']}</div>
      <h1 style="margin: 0; font-size: 52px; font-weight: 600; line-height: 1.05; letter-spacing: -0.02em;">{s['title']}</h1>
      <p style="margin: 0; font-size: 18px; line-height: 1.55; color: {p['muted']}; max-width: 820px;">{s['intro']}</p>
    </div>
    <div style="display: flex; gap: 28px; padding: 18px 22px; background: {p['surface']}; border: 1px solid {p['rule']}; border-radius: 14px;">
      <div style="display: flex; flex-direction: column; gap: 10px;">
        <span style="font-size: 14px; font-weight: 600;">Mark, as drawn</span>
        <div style="display: flex; align-items: flex-end; gap: 16px;">{sizes}</div>
      </div>{small_block}
    </div>
  </div>
  <div style="display: grid; grid-template-columns: repeat({COLS}, minmax(0, 1fr)); gap: 20px;">{''.join(cards)}
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
