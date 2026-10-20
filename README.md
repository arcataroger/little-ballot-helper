# Little Ballot Helper: a researched, values-based AI voter guide

**Little Ballot Helper is a Claude skill that builds a researched, values-based voter guide for your exact US ballot.** Give it a photo of your sample ballot, and tell it your politics and priorities. It researches every candidate and ballot measure from official sources, endorsements, candidates' own words, forum transcripts and campaign-finance records. Then it ranks each option against *your* values, shows where trusted sources disagree, fact-checks itself, runs a blinded fairness test and builds a shareable web page with citations. It works for any state, county or city, any party or ideology, and both primaries and general elections.

**Who it's for:** US voters of any party or ideology who want a sourced cheat sheet for their own ballot, and people who make voter guides for friends and family. **Not for:** official voter information, campaign mailers or paid persuasion.

**Status:** v0.1.0, an early release, public domain ([CC0](LICENSE)), tested end to end on one county general-election ballot. **Requirements:** Claude Code (recommended) or the Claude app, and Python 3.8+ (preinstalled on macOS). Optional: media tools for forum transcripts (macOS on Apple silicon is best supported).

> **Personal guide, not an official ballot.** The skill never answers voting-logistics questions from memory. Confirm dates, deadlines and drop sites with your county election office.

---

## Contents

- [What you get](#what-you-get)
- [Install](#install)
- [Use](#use)
- [How it works: the methodology](#how-it-works-the-methodology)
- [Why these safeguards: the research](#why-these-safeguards-the-research)
- [Environments and degraded modes](#environments-and-degraded-modes)
- [Repository layout](#repository-layout)
- [FAQ](#faq)
- [Limits](#limits)
- [Contributing](#contributing)

---

## What you get

A single HTML page (or a claude.ai Artifact) with:

- **Quick picks**: one row per race. Settled races show a pick. Contested ones show "Your call," with options to choose from.
- **"Your call" forks**: pros and cons, a few words each, wherever sources you trust split or your voting strategy changes the answer. Two preset buttons flip the strategy races at once: *pragmatic* (block the side you oppose) and *idealistic* (closest match).
- **Race cards**: every candidate in rank order, endorsement pills (+ aligned, − opposed), a per-pick summary that updates with your choice, a head-to-head table, timestamped forum quotes and an evidence ledger.
- **"The other side's best case"**: one respectful sentence per contested race.
- **Ballot measures**: what a yes vote does, what a no vote does, and who funds each side.
- **Methodology, changelog and works cited**: what the AI did, what the human decided, every source with its retrieval date.

---

## Install

### Claude Code (recommended)

This repository is private for now. Until it goes public, cloning needs access to it.

1. Clone this repository into your skills folder:
   ```bash
   git clone https://github.com/arcataroger/little-ballot-helper.git ~/.claude/skills/little-ballot-helper
   ```
2. Start a new Claude Code session.
3. Say something like "help me with my ballot," or type `/little-ballot-helper`.

### Optional media tools (macOS on Apple silicon)

Forum transcripts and PDF reading need a few local tools. The skill checks for them and asks before installing anything.

1. Run `~/.claude/skills/little-ballot-helper/scripts/setup_macos.sh` to see what is missing.
2. Exit code 2 means some tools are missing, not that the script failed. Run it again with `--install` to add ffmpeg, yt-dlp, mlx-whisper, parakeet-mlx and the PDF tools through Homebrew and pipx.

On Windows or Linux, install ffmpeg, yt-dlp, poppler and openai-whisper (`pipx install openai-whisper`); `scripts/transcribe` detects it automatically. faster-whisper and whisper.cpp also work if you transcribe by hand. The skill adapts its steps to what it finds.

### Optional API keys

- `FEC_API_KEY`: a free key from [api.data.gov](https://api.data.gov/signup). Without one, federal campaign-finance lookups stall after a few calls.
- A speech-to-text key (OpenAI, Groq, Deepgram or AssemblyAI): an opt-in fallback for transcribing forums on computers without a fast chip.

---

## Use

1. Start the skill. It first checks your environment and tells you plainly what your setup can and cannot do.
2. Answer a short wizard: your ballot (a photo, a sample-ballot PDF, or your county and city), your broad leaning, your priorities, the sources you trust, your strategy in close races, and how deep to go.
3. Review the source table it builds, and adjust weights.
4. Wait while it researches. A deep run on a full county ballot takes one to two hours on a capable computer.
5. Review the picks. Nothing gets published until you approve.
6. Share the page. About a week before the election, ask for a refresh pass.

---

## How it works: the methodology

The skill runs nine phases. Each one exists to prevent a specific, documented failure.

### Phase 0: Check the environment

The quality of the guide depends heavily on where it runs. The skill probes for a shell, subagents, network access to YouTube and county sites, media tools, the chip type and any API keys. It rates the setup **Full**, **Reduced** or **Minimal**, and warns you before you invest time. A Minimal setup, such as a chat app with no shell, still produces a guide. The skill tells you plainly to treat it as a starting checklist, not a finished guide, and it recommends what would help most.

### Phase 1: The values wizard

The wizard asks for your broad camp first (left, center, right or libertarian), then narrows it. Issue options mix your camp's signature issues with at least two from outside it. Research on voting-advice apps shows that the choice of issues shifts the advice. Each issue appears in the vocabulary your own camp uses. The skill saves your answers to `values.md` and reads them back before it researches anything.

**Terminology rule.** The guide uses plain descriptive terms that say what a policy does ("bans abortion after six weeks"), not either side's branding, except inside quotes.

### Phase 2: Lock the ballot from official sources

Chatbots invent and mix up ballot contents, so the skill builds the ballot only from official data:

1. Your ballot photo or sample ballot.
2. The county voters' pamphlet and official candidate filings, read locally from the PDFs.
3. Google Civic `voterInfoQuery`, where a key and data exist.

Dates, deadlines, drop sites and ID rules come only from the election office, with links. Ballot photos carry personal data, so the skill asks you to delete them once it has extracted the contest list.

### Phase 3: Map the sources

The skill builds a table of every group that endorses or publishes a guide in your area. It tiers them local, then state, then national, and covers three kinds:

- **Your camp's groups**: aligned endorsers.
- **Nonpartisan sources**: the League of Women Voters, local papers, candidate forums.
- **Groups opposed to your top priorities**: their endorsements serve as a warning signal.

Then it verifies each source:

1. It confirms that each group is real, through a committee filing or a track record, and drops paid slate mailers that pose as groups.
2. It rejects endorsement lists from past cycles, and checks that each endorsed candidate is actually on this ballot.
3. It records sources that are unpublished or pulled, and never cites them as current.
4. It notes each source's owner, funding and conflicts of interest.

### Phase 4: Research every race with a symmetric evidence ledger

Parallel subagents research clusters of races. Every candidate in a race gets the same ledger rows:

| Row | Contents |
|---|---|
| Campaign site | URL, or "(no website)" after checking |
| Own words | Questionnaire answers first, then timestamped forum quotes |
| Record | Votes and actions in office |
| Money | Totals and top donors from the FEC or the state portal, with the filing date |
| Endorsements | Every mapped group that took a position |
| Conduct | Court, bar and ethics records, with the candidate's response |
| Priority issues | A position on each of your priorities, or "no statement found" |

Unequal effort can look like a finding, so empty cells stay visible as "not found."

**Forum transcripts** follow a fallback ladder:

1. Written questionnaire answers.
2. YouTube captions.
3. Local Whisper, with silence skipping and a Parakeet fallback for looping or low-confidence spans.
4. A paid transcription API, only with your consent.
5. Skip, with the gap disclosed.

**Competitiveness** comes from this cycle's forecaster ratings, polls and past margins, with dates.

### Phase 5: Rank, fork and test sensitivity

1. The skill scores each candidate on each of your priorities from −2 to +2, using ledger evidence only. It marks thin evidence as weak, and missing evidence as null.
2. It ranks options by weighted score, then adjusts for non-policy criteria you turned on, such as integrity or competence.
3. It runs `sensitivity.py`. This reranks each race with equal weights, with each priority removed, with weak evidence dropped, and with a dealbreaker rule. A race whose top pick flips becomes a fork or gets a note.
4. It finds forks: sources you trust disagree, a sensitivity flip, or a strategy choice that changes the pick.
5. It sets defaults from your strategy, using precise definitions:
   - **Idealistic:** the closest match on your priorities. This can be a major-party candidate.
   - **Pragmatic:** the closest match among candidates who can win.
   - **Mixed:** idealistic in races that this cycle's ratings call safe, and pragmatic in close ones.
6. It writes "the other side's best case" for each contested race.

### Phase 6: Verify and review fairness

Separate subagents run each check, so the reviewer never grades its own work:

1. **Lateral fact-check.** The skill tags every unverified claim and every negative claim about a candidate in the ledgers. A fact-checker traces each one to the original document or recording. Unconfirmed claims get removed, fixed, or labeled "unconfirmed," and never decide a pick.
2. **Quote check.** Every transcript quote gets compared with the audio at its timestamp. Checking a caption quote against the same captions proves nothing, so the guide says when audio was out of reach.
3. **Blinded swap test.** `swap.py` swaps each pick with the runner-up (names, and party labels in partisan races) and strips URLs and IDs that leak identity. A fresh reviewer who never sees your values compares the evidence bar, the tone and the density of negative claims for each candidate. In the author's trial runs, it caught real imbalances in both drafts it saw, including a hand-built guide (see [Limits](#limits)).
4. **Fresh-eyes review.** A second fresh agent sees only the draft and looks for missing sources, unfair wording and gaps.
5. **Staleness check.** Within 48 hours before sharing, the skill rechecks withdrawals, new endorsements, pulled sources and late filings.

### Phase 7: Build the page

The template is a full, dependency-free HTML page:

- Ballot-style ovals mark the picks, under a clear "Not an official ballot" banner.
- Fork and preset logic run in a few dozen lines of vanilla JavaScript, and choices persist in the browser.
- It handles dark mode and has a print layout for the voting booth.
- Every pill shows its stance with a + or − symbol and screen-reader text, not just color.

Two scripts finish the page. `linkify.py` points each source name to its exact endorsement page. `check_links.py` confirms that links load and shows campaign-site titles, so you can verify each site belongs to this year's candidate. Add `--campaign-only` for a fast check of candidate sites alone. The skill strips personal data, and you choose the author line.

### Phase 8: Refresh

About a week before the election, the skill reruns the ballot check, money and endorsements, the staleness check and the page build. It logs each change in the changelog.

---

## Why these safeguards: the research

We designed this skill after surveying voting-advice apps, research on LLMs in elections, and newsroom and fact-checking standards. Here are the key findings and how the skill answers each one.

| Finding | Source | What the skill does |
|---|---|---|
| Chatbots got about half of election questions wrong and invented polling places | [AI Democracy Projects / Proof News, 2024](https://www.pbs.org/newshour/politics/chatbot-info-on-u-s-elections-is-inaccurate-misleading-and-could-keep-voters-from-polls-report-finds) | Official data only for ballot and logistics |
| ChatGPT gave incomplete governor candidate lists 89% of the time | [States United, 2026](https://statesunited.org/?p=10692) | Candidate lists come from official filings |
| Chat models lean left | [Rozado, *PLOS ONE* 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11290627); [Motoki et al., *Public Choice* 2024](https://ueaeprints.uea.ac.uk/id/eprint/92722) | Blinded swap test for every user, of any camp |
| LLMs tell users what they want to hear | [Perez et al. 2022](https://arxiv.org/abs/2212.09251); Sharma et al., ICLR 2024 | The reviewer never sees the user's values |
| The choice of issues shifts voting-advice results | [Lefevere & Walgrave, *Electoral Studies* 2014](https://researchportal.vub.be/en/publications/a-perfect-match-the-impact-of-statement-selection-on-voting-advic/) | The wizard adds issues from outside the user's camp |
| The matching model changes most users' advice | [Louwerse & Rosema, *Acta Politica* 2014](https://tomlouwerse.nl/publication/2014-louwerse-rosema-actapolitica) | A sensitivity check across weightings |
| Proximity matching ignores competence and integrity | [Wagner & Ruusuvirta, *Acta Politica* 2012](https://researchonline.lse.ac.uk/id/eprint/46760) | Optional non-policy criteria |
| LLM voting-advice tools misstated party positions in 25–50% of cases | [Dormuth et al. 2025](https://arxiv.org/abs/2502.15568) | Every position needs a citation |
| The most persuasive AI setups made the most false claims | [Hackenburg et al., *Science* 2025](https://www.ox.ac.uk/news/2025-12-11-study-reveals-how-conversational-ai-can-exert-influence-over-political-beliefs); [Lin et al., *Nature* 2025](https://doi.org/10.1038/s41586-025-09771-9) | Finding-first prose; few claims; no argument stacking |
| Floods of opposing content backfire, but short, respectful counterpoints work | [Bail et al., *PNAS* 2018](https://doi.org/10.1073/pnas.1804840115); [Costello et al., *Science* 2024](https://ide.mit.edu/insights/debunker-chatbot-makes-a-splash-spurs-debate) | One "other side's best case" line per race |
| Endorsement shortcuts mislead low-information voters as races multiply | [Lau & Redlawsk, *AJPS* 2001](https://doi.org/10.2307/2669334) | Down-ballot gaps get stated plainly |
| Fact-checkers judge a source by reading what others say about it | Wineburg & McGrew; [Caulfield (SIFT)](https://pressbooks.pub/webliteracy/?p=24) | Lateral fact-checking against originals |
| Equal questions and labeled non-responses for every candidate | [League of Women Voters guide standards](https://www.lwv.org/sites/default/files/2024-09/Guidelines%20for%20State%20And%20Local%20League%20Debates%20including%20Empty%20Chair%20Debates%20%282024%29.pdf) | Symmetric evidence ledger |
| Repeating a false allegation can still be defamation | The republication rule | Attribution, the candidate's response, no allegations stated as fact |
| Some states regulate imitation sample ballots | e.g. Oregon, West Virginia statutes | "Not an official ballot" banner |

See [`references/safeguards.md`](references/safeguards.md) for the full rule set and citations.

---

## Environments and degraded modes

| Setup | Rating | What changes |
|---|---|---|
| Claude Code on a Mac with Apple silicon, or a PC with an NVIDIA GPU | Full | Nothing: deep research, local transcription, parallel subagents |
| Claude Code on a laptop without a fast chip, or a cloud sandbox | Reduced | Slow or skipped audio transcription; cloud sandboxes often can't reach YouTube |
| A chat app with web search but no shell | Minimal | No transcripts, thin campaign-finance data, no independent reviewer. The skill says so upfront |

Claude cannot transcribe audio itself: its API accepts text, images and PDFs, not audio. Transcripts come from captions, a local model or a separate speech-to-text service.

---

## Repository layout

```
little-ballot-helper/
├── SKILL.md                  # The workflow Claude follows (phases 0–8)
├── references/
│   ├── environment.md        # Phase 0 probes, ratings, transcription ladder, warning text
│   ├── wizard.md             # Values wizard questions and terminology rules
│   ├── research.md           # Source map, ballot format, candidate research, money, transcripts
│   ├── safeguards.md         # Accuracy, fairness, transparency, legal and accessibility rules
│   └── page-spec.md          # Page structure, card parts, pills, fork config
├── scripts/
│   ├── setup_macos.sh        # Check or install media and PDF tools
│   ├── forum_transcripts.sh  # Captions first, then local Whisper, per video
│   ├── captions.py           # YouTube captions to "m:ss text", with rolling-caption dedupe
│   ├── transcribe            # Whisper with silence skip and Parakeet fallback
│   ├── fec.py                # FEC candidate search, totals, donors, outside spending
│   ├── sensitivity.py        # Rerank under alternate weights; flag flips and weak evidence
│   ├── swap.py               # Build the blinded, swapped draft for the fairness test
│   ├── linkify.py            # Link source names to their exact pages
│   └── check_links.py        # Verify links; show campaign-site titles
└── assets/
    └── guide-template.html   # The page template
```

---

## FAQ

**Is it free?**
The skill is free. Running it uses your Claude plan's usage (or API credits), and a deep run on a full ballot uses a lot. Optional paid transcription costs cents per audio hour.

**Does it see my address?**
Only if you give one, and only to find your ballot. The skill never stores or publishes it, and it asks you to delete ballot photos once it has the contest list.

**Is this an AI that tells me how to vote?**
No. You supply the values, and the skill applies them transparently. Where reasonable people who share your values disagree, it shows you the options instead of choosing. You approve every pick before anything gets shared.

**Does it work for conservatives, libertarians and centrists?**
Yes. The wizard, source lists and fairness test treat every camp the same way. The swap test exists partly because chat models lean left by default.

**Does it work outside the United States?**
Not yet. The official-data sources, campaign-finance tools and legal notes are US-specific.

**Can I use it in the Claude app without Claude Code?**
Yes, in a reduced form. The skill warns you about what you lose: transcripts, most campaign-finance data and the independent review.

**Can it tell me where to vote or when ballots are due?**
It links your county and state election offices for that. It never writes voting procedures from memory.

**Is sharing my guide legal?**
In general, an individual sharing an unpaid guide online is not making a campaign expenditure under federal rules. Paying to promote it can trigger disclaimer and reporting rules, and state rules vary. This is not legal advice.

**How much does a run cost?**
A deep run on a full county ballot uses a lot of model time. On a Claude subscription, this comes out of your plan's usage. Paid transcription APIs, if you opt in, typically cost cents per audio hour.

---

## Limits

- One unattended run is shallower than a guide a person researched by hand over days, especially on obscure down-ballot races. In our trial, a clean run matched 10 of 15 picks from a hand-built guide. It missed two down-ballot facts and one forecaster rating, and it caught a withdrawn source and several fairness problems the hand-built guide had missed.
- YouTube rate limits and bot walls can block captions and audio downloads.
- Campaign-finance portals differ by state. The skill writes "not checked" where it cannot reach the data.
- Endorsements change. Use the refresh pass.

---

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md), and use the issue templates to report a wrong fact or a bug.

## License

[CC0 1.0 Universal](LICENSE): public domain dedication. You can copy, modify, distribute and use this work, even commercially, without asking permission or giving credit. Credit is welcome, never required.
