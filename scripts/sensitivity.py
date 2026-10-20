#!/usr/bin/env python3
"""sensitivity: show which races' top picks depend on the weights.

Input JSON (write it during Phase 5):
  {"weights": {"climate": 3, "housing": 2, "honesty": 1},
   "races": {"<race id>": {"<candidate>": {"climate": 2, "housing": -1, "honesty": null}}}}

Scores run from -2 (strongly against the user's values) to +2 (strongly for):
  +2 acts on it / leads on it   +1 supports it   0 mixed or neutral
  -1 opposes it                 -2 actively works against it   null no evidence
null counts as 0, and the report lists it. Weights are positive numbers.
Mark a score that rests on thin evidence as {"score": 1, "weak": true}; the
"without weak evidence" variant treats it as null, so you can see whether a
pick depends on it. Give each seat of a multi-seat contest its own race id.

It reranks each race several ways: user weights, equal weights, each issue
dropped in turn, and a dealbreaker view (any -2 on a top-weighted issue rules
a candidate out). Then it
prints races whose top pick changes. Each flip needs a fork or a note.
Strategy (spoiler risk) is not scored here; forks handle it.

Usage: sensitivity.py SCORES.json [--json]
"""
import argparse, json


def val(v, drop_weak=False):
    if isinstance(v, dict):
        return None if (drop_weak and v.get("weak")) else v.get("score")
    return v


def total(scores, weights, drop_weak=False):
    return sum(w * (val(scores.get(k), drop_weak) or 0) for k, w in weights.items())


def top(cands, weights, drop_weak=False):
    if not cands:
        return "no candidates"
    ranked = sorted(cands, key=lambda c: total(cands[c], weights, drop_weak), reverse=True)
    if len(ranked) > 1 and total(cands[ranked[0]], weights, drop_weak) == total(cands[ranked[1]], weights, drop_weak):
        return "tie:" + "/".join(ranked[:2])
    return ranked[0]


def main(path, as_json):
    d = json.load(open(path))
    W = d["weights"]
    equal = {k: 1 for k in W}
    report = {}
    for race, cands in d["races"].items():
        if len(cands) < 2:
            report[race] = {"top": top(cands, W), "flips": {}, "missing": {}, "totals": {}, "note": "unopposed" if cands else "no filer"}
            continue
        base = top(cands, W)
        variants = {"equal weights": top(cands, equal), "without weak evidence": top(cands, W, True)}
        for k in W:
            variants[f"without {k}"] = top(cands, {i: w for i, w in W.items() if i != k})
        # Dealbreaker view: a -2 on any top-weighted issue rules a candidate out.
        hi = max(W.values())
        ok = {c: s for c, s in cands.items()
              if not any(val(s.get(k)) == -2 for k, w in W.items() if w == hi)}
        variants["dealbreakers"] = top(ok, W) if ok else "none acceptable"
        flips = {name: t for name, t in variants.items() if t != base}
        missing = {c: [k for k in W if val(cands[c].get(k)) is None] for c in cands}
        report[race] = {"top": base, "flips": flips,
                        "missing": {c: m for c, m in missing.items() if m},
                        "totals": {c: total(cands[c], W) for c in cands}}
    if as_json:
        print(json.dumps(report, indent=1))
        return
    for race, r in report.items():
        if r.get("note"):
            print(f"{race}: {r['top']}  [{r['note']}]")
            continue
        mark = "TIE" if r["top"].startswith("tie:") else ("FLIPS" if r["flips"] else "stable")
        print(f"{race}: top = {r['top']}  [{mark}]  totals = {r['totals']}")
        for name, t in r["flips"].items():
            print(f"    {name}: -> {t}")
        for c, m in r["missing"].items():
            print(f"    no evidence for {c}: {', '.join(m)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scores")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    main(a.scores, a.json)
