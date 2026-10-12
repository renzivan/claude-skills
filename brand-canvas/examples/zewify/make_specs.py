#!/usr/bin/env python3
"""Writes examples/zewify/{marks,fonts}.json — the two specs behind the Zewify
canvas's "ten more marks" and "ten typefaces" boards. Kept as code because the
mark geometry is easier to read and fix here than inside escaped JSON."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE

PALETTE = {
    'accent': '#2f5d50', 'deep': '#1f4238', 'soft': '#8fb3a5', 'paper': '#f7f6f2',
    'ink': '#1b1b19', 'muted': '#5f5e58', 'rule': '#e3e1da', 'surface': '#ffffff',
    'dark': {'accent': '#7fb8a6', 'deep': '#5d9483', 'soft': '#3f6b5e', 'paper': '#111110', 'ink': '#ecebe6'},
}

MARKS = [
    ('Split square', 'Z · negative space', 'A square cut by one diagonal slit. The Z is only the space between the halves.',
     '<path d="M14 14H46L14 46Z" fill="{accent}" stroke="{accent}" stroke-width="3" stroke-linejoin="round"></path>'
     '<path d="M50 22V50H22Z" fill="{accent}" stroke="{accent}" stroke-width="3" stroke-linejoin="round"></path>'),
    ('Origami', 'Z · faceted', 'A Z folded from one strip of paper, in three tones of the same green, with each face catching different light.',
     '<path d="M14 16H50L40 25H14Z" fill="{accent}"></path><path d="M50 16L40 25L14 48L24 39Z" fill="{soft}"></path>'
     '<path d="M24 39H50V48H14Z" fill="{deep}"></path>'),
    ('Constellation', 'Z · dots', 'Seven points: two dark rows joined by a light diagonal of three. It reads as a pattern first, and as a Z on a second look.',
     ''.join(f'<circle cx="{x}" cy="{y}" r="4.6" fill="{{accent}}"></circle>' for x, y in [(17, 17), (32, 17), (32, 47), (47, 47)])
     + ''.join(f'<circle cx="{x}" cy="{y}" r="4.6" fill="{{soft}}"></circle>' for x, y in [(47, 17), (32, 32), (17, 47)])),
    ('River stone', 'Z · organic', 'A soft Z worn into a smooth pebble. It’s the most organic and tactile of the ten.',
     '<path d="M32 8C48 8 57 18 56.5 32C56 47 45 56 31 56C16 56 7.5 46 7.5 32C7.5 17 17 8 32 8Z" fill="{accent}"></path>'
     '<path d="M21 23H40C44.5 23 45.5 27.5 41.5 29.5L23 36.5C18.5 38.5 19.5 42 24 42H43" fill="none" stroke="{paper}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"></path>'),
    ('Window', 'Shape only', 'An arched window with a low moon. It feels like somewhere calm to come back to, and it has no letterform at all.',
     '<path d="M19 50V31A13 13 0 0 1 45 31V50Z" fill="{accent}"></path><circle cx="32" cy="31" r="5.5" fill="{paper}"></circle>'
     '<rect x="12" y="50" width="40" height="3.5" rx="1.75" fill="{soft}"></rect>'),
    ('Tide', 'Shape + Z', 'A circle split by a Z-shaped shoreline into water and sky. It’s calm, and the Z only shows up on a second look.',
     '<defs><clipPath id="tide{uid}"><circle cx="32" cy="32" r="25"></circle></clipPath></defs>'
     '<g clip-path="url(#tide{uid})"><rect width="64" height="64" fill="{soft}"></rect><path d="M0 0H64V41H25L39 23H0Z" fill="{accent}"></path></g>'),
    ('Two rooms', 'Shape only', 'Two soft squares that overlap at one corner: separate products under one roof.',
     '<defs><clipPath id="room{uid}"><rect x="11" y="11" width="29" height="29" rx="7"></rect></clipPath></defs>'
     '<rect x="11" y="11" width="29" height="29" rx="7" fill="{soft}"></rect><rect x="24" y="24" width="29" height="29" rx="7" fill="{accent}"></rect>'
     '<rect x="24" y="24" width="29" height="29" rx="7" fill="{deep}" clip-path="url(#room{uid})"></rect>'),
    ('Stencil', 'Z · monoline', 'A Z made of three separate strokes with small gaps, like a hand-cut stencil. Light and precise.',
     '<path d="M18 19H44M41 26L23 38M20 45H46" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round"></path>'),
    ('Interlock', 'Z · symmetric', 'Two matching corners turned to face each other, so they fit together and outline a Z between them.',
     '<path d="M14 17H45V31" fill="none" stroke="{accent}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"></path>'
     '<path d="M19 33V47H50" fill="none" stroke="{soft}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"></path>'),
    ('Journey', 'Z · line + dot', 'A single line drawn as a Z that stops at a resting point. It suggests a path with somewhere to arrive.',
     '<path d="M18 20H45L19 44H38" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"></path>'
     '<circle cx="48" cy="44" r="4.5" fill="{soft}"></circle>'),
]

CONSTELLATION = MARKS[2][3]
SMALL = ('<rect width="64" height="64" rx="14" fill="{accent}"></rect>'
         + ''.join(f'<circle cx="{x}" cy="{y}" r="5.4" fill="{{paper}}"></circle>' for x, y in [(17, 17), (32, 17), (32, 47), (47, 47)])
         + ''.join(f'<circle cx="{x}" cy="{y}" r="5.4" fill="{{paper}}" fill-opacity="0.5"></circle>' for x, y in [(47, 17), (32, 32), (17, 47)]))

FONTS = [
    ('Newsreader', 'Newsreader:opsz,wght@6..72,500', 500, '-0.02em', 'Editorial serif', 'Literary and composed, and it matches the site’s headings.'),
    ('Fraunces', 'Fraunces:opsz,wght@9..144,500', 500, '-0.02em', 'Soft serif', 'Warm, rounded serifs that echo the round dots. It has a little more personality.'),
    ('Instrument Serif', 'Instrument+Serif', 400, '-0.01em', 'Condensed serif', 'Tall, narrow and elegant. It feels quiet and a bit fashionable.'),
    ('Young Serif', 'Young+Serif', 400, '-0.01em', 'Sturdy serif', 'Heavy and friendly, like an old bookplate. It holds up at small sizes.'),
    ('Geist', 'Geist:wght@500', 500, '-0.03em', 'Neutral sans', 'Precise and very calm, the plainest option. The mark does the talking.'),
    ('Outfit', 'Outfit:wght@500', 500, '-0.02em', 'Geometric sans', 'Round o and e forms that repeat the dot geometry exactly.'),
    ('Figtree', 'Figtree:wght@600', 600, '-0.02em', 'Friendly sans', 'Clear and approachable, with slightly humanist curves. Reads well everywhere.'),
    ('Sora', 'Sora:wght@500', 500, '-0.03em', 'Wide sans', 'Wide and airy. It reads as a modern software company.'),
    ('Plus Jakarta Sans', 'Plus+Jakarta+Sans:wght@600', 600, '-0.03em', 'Modern grotesk', 'Crisp and confident, with tight curves, like an established product studio.'),
    ('Nunito', 'Nunito:wght@700', 700, '-0.01em', 'Rounded sans', 'Rounded terminals that match the dots. The gentlest and most consumer-friendly.'),
]

DISPLAY = {'family': 'Newsreader', 'css': 'Newsreader:opsz,wght@6..72,400;6..72,500', 'weight': 500, 'tracking': '-0.02em'}
TEXT = {'family': 'Instrument Sans', 'css': 'Instrument+Sans:wght@400;500;600'}

os.makedirs(OUT, exist_ok=True)
json.dump({
    'brand': 'Zewify', 'eyebrow': 'Identity · round 2', 'title': 'Ten more marks',
    'intro': 'All ten use one green and its tints and stay calm. Each is shown large, next to the wordmark, and at real favicon sizes of 16 and 32px.',
    'palette': PALETTE, 'fonts': {'display': DISPLAY, 'text': TEXT},
    'marks': [{'name': n, 'tag': t, 'blurb': b, 'svg': s} for n, t, b, s in MARKS],
}, open(os.path.join(OUT, 'marks.json'), 'w'), indent=2, ensure_ascii=False)
json.dump({
    'brand': 'Zewify', 'eyebrow': 'Identity · wordmark', 'title': 'Ten typefaces beside the mark',
    'intro': 'Each option shows the chosen mark with the wordmark on light and dark, plus the headline in the same face. All ten are free and can be self-hosted.',
    'headline': 'Calm, private software for everyday life.',
    'palette': PALETTE, 'text': TEXT, 'mark': {'svg': CONSTELLATION, 'smallSvg': SMALL},
    'fonts': [{'family': f, 'css': c, 'weight': w, 'tracking': t, 'style': s, 'note': n} for f, c, w, t, s, n in FONTS],
}, open(os.path.join(OUT, 'fonts.json'), 'w'), indent=2, ensure_ascii=False)
print('wrote', OUT)
