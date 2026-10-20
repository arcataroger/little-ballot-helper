#!/usr/bin/env python3
"""swap: build the blinded, swapped draft for the Phase 6 swap test.

Reads guide.html and a pairs file:
  {"<race id>": {"a": ["Full Name A", "Lastname A"],
                 "b": ["Full Name B", "Lastname B"],
                 "partisan": true}}
"a" is the pick and "b" the runner-up. List longer name forms first.

For each listed race card it:
  1. Removes URLs, data-* attributes and ids (they leak real names).
  2. Removes stance pills' color classes and screen-reader stance text.
  3. Swaps the two candidates' names, and in partisan races also
     Democrat/Republican, Democratic/Republican and (D)/(R).
It writes only those cards to OUT. Give OUT to a reviewer who never sees
values.md. Pronouns are not swapped: tell the reviewer to ignore pronoun
mismatches.

Usage: swap.py guide.html pairs.json OUT.html
"""
import json, re, sys

PARTY = [("Democratic", "Republican"), ("Democrat", "Republican"), ("(D)", "(R)"), ("Dems", "GOP")]


def swap_terms(t, pairs):
    toks = {}
    for i, (x, y) in enumerate(pairs):
        for src, dst, key in ((x, y, f"\x00A{i}\x00"), (y, x, f"\x00B{i}\x00")):
            t = t.replace(src, key)
            toks[key] = dst
    for key, dst in toks.items():
        t = t.replace(key, dst)
    return t


def main(page, pairs_path, out):
    html = open(page, encoding="utf-8").read()
    pairs = json.load(open(pairs_path, encoding="utf-8"))
    cards = []
    for rid, p in pairs.items():
        m = re.search(r'<article class="sheet race" id="%s">.*?</article>' % re.escape(rid), html, re.S)
        if not m:
            print(f"swap: no card with id {rid}", file=sys.stderr)
            continue
        t = m.group(0)
        t = re.sub(r'\s(href|id|data-[\w-]+)="[^"]*"', "", t)
        t = re.sub(r'class="chip (rec|opp)"', 'class="chip"', t)
        t = re.sub(r'<span class="sr">[^<]*</span>', "", t)
        t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        t = swap_terms(t, list(zip(p["a"], p["b"])))
        if p.get("partisan"):
            t = swap_terms(t, PARTY)
        cards.append(t)
    with open(out, "w", encoding="utf-8") as f:
        f.write('<!doctype html><meta charset="utf-8"><title>Draft for review</title><body>\n'
                + "\n\n".join(cards) + "\n</body>\n")
    print(f"swap: wrote {len(cards)} card(s) to {out}")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    main(*sys.argv[1:])
