# Environment check (Phase 0)

## Probes

Run what the tools allow. Never print API keys; test only whether they exist.

| Capability | How to check | Why it matters |
|---|---|---|
| Shell | A Bash tool exists | Scripts, PDFs, campaign-finance portals, media |
| Subagents | An Agent/Task tool exists | Parallel research; an independent swap test and review |
| Page output | An Artifact tool exists, or files can be written | Shareable page vs. a chat table |
| Network | `curl -sI -m 10 https://www.youtube.com`, the county election site, `https://api.open.fec.gov` | Cloud sandboxes often block sites or get bot-walled |
| Media tools | `scripts/setup_macos.sh` (or `which ffmpeg yt-dlp`) | Captions and audio |
| Chip | `uname -sm`; `sysctl -n machdep.cpu.brand_string`; `nvidia-smi -L`; memory via `sysctl hw.memsize` or `free -g` | Local transcription speed |
| Transcription keys | `[ -n "$OPENAI_API_KEY" ]`, `GROQ_API_KEY`, `DEEPGRAM_API_KEY`, `ASSEMBLYAI_API_KEY` | Paid fallback, opt-in only |
| FEC key | `[ -n "$FEC_API_KEY" ]` | Without one, federal money lookups stall after a few calls |

If there is no shell, you cannot detect the hardware. Ask once: "What computer are you on (for example, a Mac with an M-series chip, a Windows laptop, or a phone)? Forum transcripts need either a fast chip or a paid transcription service, so this decides how deep the guide can go."

Claude cannot transcribe audio itself. Its API takes text, images and PDFs, not audio or video. So transcripts always come from captions, a local model or a separate speech-to-text service.

## Ratings

| Rating | Typical setup | Depth cap | What the guide loses |
|---|---|---|---|
| Full | Claude Code (or a similar agent tool) on a Mac with Apple silicon or a PC with an NVIDIA GPU, with open network | Deep | Nothing |
| Reduced | A shell without a fast chip (most Windows or Intel laptops), or a cloud code sandbox | Standard | Slow or skipped audio transcription; cloud sandboxes often cannot reach YouTube or some county sites |
| Minimal | A chat app with web search but no shell, or no subagents | Quick | See below |

What a Minimal guide loses, in the user's terms:

- No forum transcripts. Candidates' spoken words appear only through news reports.
- Weak campaign-money data. State portals need scripts, so the guide shows "not checked."
- More risk of missed or wrong candidates, because the official PDFs are harder to read.
- No independent fairness review. The same model writes and checks, so bias goes uncaught more often.
- Fewer sources overall, with thinner down-ballot coverage.

## Transcription ladder

Use the first step that works, and record which step each forum reached.

1. Written own words first: Vote411 answers and newspaper questionnaires. They need no compute, and they are often a better source than a live forum.
2. Captions: `scripts/captions.py`, through `forum_transcripts.sh`.
3. Local transcription:
   - Apple silicon: mlx-whisper (`scripts/transcribe`), about 1.5–2 seconds per audio minute.
   - Other systems: openai-whisper, which `scripts/transcribe` detects automatically (it uses a GPU when PyTorch sees one). faster-whisper or whisper.cpp are faster alternatives, run by hand.
   - CPU only: use a small model. Estimate the time first (roughly real time or slower), and ask before starting a long batch.
4. A paid speech-to-text API with the user's own key. Do this only with consent and a cost estimate (typically cents per audio hour).
5. Skip. Use news coverage of the forum, and list "forum not transcribed" in the known limits.

## Warning message

Keep it to one short message. Example for a Minimal setup:

> Before we start: this chat can search the web, but it can't run scripts or read forum videos. Your guide will miss candidates' spoken answers and most campaign-money data. Down-ballot races may be thin, and no independent reviewer will check it for bias. Treat it as a starting checklist, not a finished guide.
>
> For a much better guide, run this in Claude Code (or your AI provider's coding agent) on a computer, ideally a Mac with an M-series chip. Want to continue here with a quick guide, or switch first?

For a Full setup, one line is enough: "Your setup supports a full-depth guide."
