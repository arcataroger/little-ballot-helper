#!/bin/bash
# setup_macos.sh: check (and optionally install) the media tools on macOS / Apple Silicon.
#   setup_macos.sh          -> report what is installed and what is missing
#   setup_macos.sh --install -> install the missing pieces with Homebrew and pipx
# Other OSes: install ffmpeg, yt-dlp and openai-whisper (or faster-whisper) with your package manager.
set -uo pipefail
want_install=${1:-}
missing=()
have() { command -v "$1" >/dev/null 2>&1; }
report() { if have "$1"; then printf "ok      %-14s %s\n" "$1" "$(command -v "$1")"; else printf "MISSING %-14s %s\n" "$1" "$2"; missing+=("$1"); fi; }

[ "$(uname -s)" = Darwin ] || { echo "Not macOS. Install ffmpeg, yt-dlp and a Whisper CLI yourself."; exit 1; }
[ "$(uname -m)" = arm64 ] || echo "note: Intel Mac; mlx-whisper needs Apple Silicon. Use openai-whisper instead."
report brew        "https://brew.sh"
report ffmpeg      "brew install ffmpeg"
report yt-dlp      "brew install yt-dlp"
report pipx        "brew install pipx && pipx ensurepath"
report mlx_whisper "pipx install mlx-whisper"
report parakeet-mlx "pipx install parakeet-mlx   (optional fallback model)"
report pdftotext   "brew install poppler        (read voters' pamphlets)"
report ocrmypdf    "brew install ocrmypdf       (optional: scanned measure text)"

[ ${#missing[@]} -eq 0 ] && { echo "All tools present."; exit 0; }
[ "$want_install" = --install ] || { echo "Run with --install to add the missing tools (ask the user first)."; exit 2; }
have brew || { echo "Install Homebrew first: https://brew.sh"; exit 1; }
for t in "${missing[@]}"; do
  case $t in
    ffmpeg|yt-dlp|pipx|ocrmypdf) brew install "$t" ;;
    pdftotext) brew install poppler ;;
    mlx_whisper)  pipx install mlx-whisper || pipx install --python "$(brew --prefix)/bin/python3.12" mlx-whisper ;;
    parakeet-mlx) pipx install parakeet-mlx ;;
  esac
done
pipx ensurepath >/dev/null 2>&1 || true
echo "Done. Open a new shell if pipx tools are not on PATH yet."
