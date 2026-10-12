#!/usr/bin/env python3
"""Add (or resize) one artboard in a Design canvas index without disturbing anything else.

Always run it on the canvas.json you JUST read back from the artifact, never on
your own earlier copy: viewers edit the canvas live, and every key you did not
mean to change (their notes, moves, attachments) must survive.

    python3 add_board.py canvas.json Logos.dc.html 1600 1340 "Logo — ten more marks" [--row-y 0]

The board goes at the right end of the row whose top is --row-y (default 0),
80px after the rightmost board there, and any title note sitting above that
row is widened to span it. Re-running for a board already in the index only
updates its size and title.
"""
import argparse
import json

GAP = 80


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('index')
    ap.add_argument('file')
    ap.add_argument('w', type=int)
    ap.add_argument('h', type=int)
    ap.add_argument('title')
    ap.add_argument('--row-y', type=int, default=0)
    a = ap.parse_args()

    c = json.load(open(a.index))
    boards = c.setdefault('boards', {})
    order = c.setdefault('order', [])

    if a.file in boards:
        boards[a.file].update(w=a.w, h=a.h, title=a.title)
    else:
        row = [b for b in boards.values() if b.get('y') == a.row_y]
        x = max((b['x'] + b['w'] for b in row), default=-GAP) + GAP
        boards[a.file] = {'x': x, 'y': a.row_y, 'w': a.w, 'h': a.h, 'title': a.title}
        order.append(a.file)

    row = [b for b in boards.values() if b.get('y') == a.row_y]
    right = max(b['x'] + b['w'] for b in row)
    for note in c.get('notes', {}).values():
        if note.get('kind') == 'title1' and a.row_y - 400 <= note.get('y', 0) < a.row_y:
            note['maxW'] = max(note.get('maxW', 0), right - note.get('x', 0))

    json.dump(c, open(a.index, 'w'), indent=2, ensure_ascii=False)
    print(json.dumps(boards[a.file]))


if __name__ == '__main__':
    main()
