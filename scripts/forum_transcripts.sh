#!/bin/bash
# forum_transcripts.sh: get a timestamped transcript for each video URL.
#   forum_transcripts.sh [--no-captions] OUTDIR URL [URL...]
# Quote each URL ('https://www.youtube.com/watch?v=...'); zsh treats ? as a glob.
# For each URL: try YouTube captions (captions.py). If none, download audio with
# yt-dlp and transcribe it locally (transcribe). Writes OUTDIR/<id>.txt with
# "m:ss text" lines and prints one status line per video.
# Works with any site yt-dlp supports (YouTube, Vimeo, Facebook, many local TV sites).
set -uo pipefail
usage() { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
caps=1; [ "${1:-}" = --no-captions ] && { caps=0; shift; }
[ $# -ge 2 ] || usage
case $1 in -*) usage ;; esac
HERE=$(cd "$(dirname "$0")" && pwd)
out=$1; shift
mkdir -p "$out/audio"
n=$#; i=0
for url in "$@"; do
  i=$((i + 1)); printf "[%d/%d] " "$i" "$n"
  id=$(yt-dlp --get-id "$url" 2>/dev/null | head -1)
  [ -n "$id" ] || { echo "FAIL  $url  (yt-dlp cannot read it)"; continue; }
  if [ -s "$out/$id.txt" ]; then echo "SKIP  $id  (already done)"; continue; fi
  if [ $caps = 1 ] && python3 "$HERE/captions.py" "$url" --id "$id" -o "$out" 2>>"$out/log.txt"; then
    echo "CAPS  $id  $(wc -l < "$out/$id.txt") lines"; continue
  fi
  # Captions failed: fall back to audio. Retry on rate limits with growing waits.
  for wait in 0 30 90; do
    sleep $wait
    yt-dlp --no-progress -q -x --audio-format m4a -o "$out/audio/%(id)s.%(ext)s" "$url" >>"$out/log.txt" 2>&1 && break
  done
  audio=$(ls "$out/audio/$id".* 2>/dev/null | head -1)
  [ -n "$audio" ] || { echo "FAIL  $id  (no captions, audio download failed; see log.txt)"; continue; }
  if "$HERE/transcribe" "$audio" -o "$out" 2>>"$out/log.txt"; then
    echo "WHSP  $id  $(wc -l < "$out/$id.txt") lines (local Whisper)"
  else
    echo "FAIL  $id  (transcription failed; see log.txt)"
  fi
done
