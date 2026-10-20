#!/usr/bin/env python3
"""captions: fetch YouTube captions as plain "m:ss text" lines.

Auto-caption timestamps can lead or trail the words by up to ~10 s. Link
quotes a few seconds early.

Steps:
  1. Ask yt-dlp for manual English subtitles, then auto-generated ones (VTT).
  2. Back off and retry on HTTP 429 (YouTube rate-limits caption requests).
  3. Collapse rolling auto-captions: each line keeps only the words it adds.
  4. Write <video id>.txt. On failure, exit 2 so the caller falls back to
     downloading audio and running scripts/transcribe.

Usage: captions.py URL [URL...] [-o OUTDIR] [--lang en] [--retries 2] [--id VIDEO_ID]
"""
import argparse, glob, os, re, subprocess, sys, time


def fetch(url, outdir, lang, retries):
    wait = 20
    for attempt in range(retries + 1):
        p = subprocess.run(
            ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
             "--sub-langs", f"{lang}.*,{lang}", "--sub-format", "vtt",
             "-o", os.path.join(outdir, "%(id)s.%(ext)s"), url],
            capture_output=True, text=True)
        if "429" not in p.stderr:
            return p
        if attempt < retries:
            print(f"rate-limited; waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
            wait *= 2
    return p


def ts(h, m, s):
    return int(h) * 3600 + int(m) * 60 + float(s)


def vtt_to_lines(path):
    """Rolling auto-captions repeat earlier words in later cues. Emit only the
    words that extend what we already wrote (longest suffix/prefix overlap)."""
    text = open(path, encoding="utf-8").read()
    out, tail = [], []          # tail: the last ~60 words already emitted
    for block in text.split("\n\n"):
        m = re.search(r"(\d+):(\d+):([\d.]+) -->", block)
        if not m:
            continue
        body = block[m.end():].split("\n", 1)[-1]
        body = re.sub(r"<[^>]+>", "", body)
        words = " ".join(l.strip() for l in body.splitlines() if l.strip()).split()
        if not words:
            continue
        k = next((k for k in range(min(len(words), len(tail)), 0, -1)
                  if tail[-k:] == words[:k]), 0)
        new = words[k:]
        if new:
            t = int(ts(*m.groups()))
            out.append(f"{t // 60}:{t % 60:02d} {' '.join(new)}")
            tail = (tail + new)[-60:]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+")
    ap.add_argument("-o", "--outdir", default=".")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--id", help="video id for a single non-YouTube URL (forum_transcripts.sh passes it)")
    ap.add_argument("--retries", type=int, default=2,
                    help="retries on HTTP 429 (waits 20 s, 40 s, ...)")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    failed = 0
    for url in a.urls:
        vid = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
        vid = a.id if (a.id and len(a.urls) == 1) else (vid.group(1) if vid else None)
        if not vid:
            got = subprocess.run(["yt-dlp", "--get-id", url], capture_output=True, text=True).stdout.split()
            vid = got[0] if got else re.sub(r"\W+", "_", url)[-40:]
        fetch(url, a.outdir, a.lang, a.retries)
        vtts = sorted(glob.glob(os.path.join(a.outdir, f"{vid}*.vtt")),
                      key=lambda f: ("orig" in f, len(f)))  # prefer manual subs
        if not vtts:
            print(f"{vid}: no captions; fall back to scripts/transcribe", file=sys.stderr)
            failed += 1
            continue
        lines = vtt_to_lines(vtts[0])
        with open(os.path.join(a.outdir, vid + ".txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"{vid}: {len(lines)} lines from {os.path.basename(vtts[0])}", file=sys.stderr)
    sys.exit(2 if failed else 0)


if __name__ == "__main__":
    main()
