#!/usr/bin/env python3
"""check_links: confirm that every link in a guide page loads.

It fetches each unique http(s) URL with a browser-like user agent and reports
the status. "Campaign" links (the .name and .cand links) also report the page
title, so you can confirm that the site belongs to this year's candidate.
Exit code 1 if any link fails.

Usage: check_links.py GUIDE.html [--campaign-only] [--workers 8]
"""
import argparse, concurrent.futures as cf, html as htmllib, re, sys, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"


def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read(200_000).decode("utf-8", "replace")
            t = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            return url, r.status, (t.group(1).strip()[:80] if t else ""), r.geturl()
    except urllib.error.HTTPError as e:
        return url, e.code, "", url
    except Exception as e:
        return url, 0, type(e).__name__, url


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page")
    ap.add_argument("--campaign-only", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    html = open(a.page, encoding="utf-8").read()
    campaign = set(re.findall(r'<a class="name" href="(https?://[^"]+)"', html))
    campaign |= set(re.findall(r'<span class="cand"[^>]*><a href="(https?://[^"]+)"', html))
    urls = campaign if a.campaign_only else set(re.findall(r'href="(https?://[^"]+)"', html))
    campaign = {htmllib.unescape(u) for u in campaign}
    urls = {htmllib.unescape(u) for u in urls}
    # Font and preconnect hosts are not pages; skip them.
    urls = {u for u in urls if not re.match(r"https://fonts\.(googleapis|gstatic)\.com/?$", u)}
    bad = 0
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for url, code, title, final in sorted(ex.map(check, sorted(urls)), key=lambda r: r[1]):
            ok = 200 <= code < 400
            # 401/402/403/429 usually mean a paywall or bot wall, not a dead page.
            flag = "OK " if ok else ("?? " if code in (401, 402, 403, 429) else "BAD")
            bad += flag == "BAD"
            extra = f"  title: {title}" if url in campaign else ""
            moved = f"  -> {final}" if final != url else ""
            print(f"{flag} {code:3} {url}{moved}{extra}")
    print(f"{len(urls)} links, {bad} failed", file=sys.stderr)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
