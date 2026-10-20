#!/usr/bin/env python3
"""linkify: link source names in a guide page to their specific pages.

Reads a JSON map:
  {"generic": {"Source name": "https://..."},
   "per_race": {"<article id>": {"Source name": "https://race-specific..."}}}

It links only text nodes inside race cards (<article class="sheet race">),
and only the first mention per paragraph, table cell or list item. It skips
links, headings, buttons, summaries, pills (.chip), .endorse, .sources, .meta
and .eyebrow. It rewrites the file in place and prints the count.

Usage: linkify.py GUIDE.html LINKS.json
"""
import json, re, sys

SKIP_TAGS = {"a", "h1", "h2", "h3", "h4", "button", "summary", "script", "style", "th"}
SKIP_CLASSES = ("chip", "sources", "endorse", "eyebrow", "meta")
RESET = {"p", "td", "li"}
VOID = {"br", "img", "meta", "link", "input", "hr", "wbr"}


def link_chunk(chunk, table):
    if not table:
        return chunk
    names = sorted(table, key=len, reverse=True)
    pat = re.compile(r"(?<![\w-])(" + "|".join(re.escape(n) for n in names) + r")(?![\w-])")
    out, stack, used, skipdepth = [], [], set(), 0
    for tok in re.split(r"(<[^>]+>)", chunk):
        if tok.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)([^>]*)>", tok)
            if m:
                close, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
                cls = re.search(r'class="([^"]*)"', attrs)
                cls = cls.group(1).split() if cls else []
                skippy = tag in SKIP_TAGS or any(c in SKIP_CLASSES for c in cls)
                if not close and tag not in VOID and not attrs.rstrip().endswith("/"):
                    stack.append(skippy)
                    skipdepth += skippy
                    if tag in RESET:
                        used = set()
                elif close and stack:
                    skipdepth -= stack.pop()
            out.append(tok)
            continue
        if skipdepth or not tok.strip():
            out.append(tok)
            continue

        def rep(m):
            n = m.group(1)
            if n in used:
                return n
            used.add(n)
            return f'<a href="{table[n]}">{n}</a>'
        out.append(pat.sub(rep, tok))
    return "".join(out)


def main(path, links_path):
    links = json.load(open(links_path, encoding="utf-8"))
    s = open(path, encoding="utf-8").read()
    parts = re.split(r'(<article class="sheet race" id="[^"]+">.*?</article>)', s, flags=re.S)
    for i, part in enumerate(parts):
        m = re.match(r'<article class="sheet race" id="([^"]+)">', part)
        if m:
            table = dict(links.get("generic", {}))
            table.update(links.get("per_race", {}).get(m.group(1), {}))
            parts[i] = link_chunk(part, table)
    new = "".join(parts)
    open(path, "w", encoding="utf-8").write(new)
    print("links added:", new.count("<a ") - s.count("<a "))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
