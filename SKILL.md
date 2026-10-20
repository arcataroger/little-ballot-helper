---
name: little-ballot-helper
license: CC0-1.0
description: Build a researched, values-based voter guide for one person's actual US ballot — every race, proposition and judge retention ranked against the user's own political leaning and priorities, with endorsements, candidates' own words, campaign money, forum transcripts, fact-checks and a shareable web page with citations. Use this whenever someone wants help deciding how to vote, asks "who should I vote for", says their ballot arrived, shares a photo of their ballot or sample ballot, wants a slate or cheat sheet for an upcoming election, wants to compare political candidates or ballot measures against their values, or wants to make a voter guide for friends and family — any US state, county or city, any party or ideology, primary or general.
---

# Little Ballot Helper

A researched, values-based AI voter guide.

Build a voter guide for one real US ballot, ranked by the user's values, with every claim sourced.

The user owns the values and the final picks. You do the research, show the evidence evenly, and say where reasonable people in their camp split. Never pick a side from your own views.

Chatbots fail at elections in documented ways: wrong facts, incomplete candidate lists, a left lean and agreement with whatever the user believes. So this workflow puts official data first, runs the same checks on every candidate, and tests its own fairness. Read `references/safeguards.md` before Phase 3; it explains each rule.

## Files

Create one working folder per guide, named `ballot-<county>-<election date>/` unless the user names one. Keep everything in it, including subagents' scratch files (in `work/`):

| File | Made in | Holds |
|---|---|---|
| `environment.md` | Phase 0 | What this runtime can and cannot do |
| `values.md` | Phase 1 | The voter profile (no personal data) |
| `ballot.md` | Phase 2 | Contests, candidates, official links, as-of date |
| `sources.md`, `links.json` | Phase 3 | The source map; source names mapped to their URLs |
| `ledger/<race>.md` | Phase 4 | One evidence ledger per race |
| `transcripts/` | Phase 4 | Forum transcripts |
| `scores.json` | Phase 5 | Input for `sensitivity.py` |
| `pairs.json` | Phase 6 | Pick and runner-up per contested race, for `swap.py` |
| `guide.html` | Phase 7 | The page |

Ballot photos carry the voter's name, address and barcodes. Delete them, or ask the user to, once `ballot.md` exists.

## Workflow

Copy this checklist into your task list, then work through it in order.

1. Check the environment and warn the user (Phase 0).
2. Run the wizard (Phase 1).
3. Lock the ballot from official sources (Phase 2).
4. Map the sources (Phase 3).
5. Research every race (Phase 4).
6. Rank, fork and test sensitivity (Phase 5).
7. Verify and review fairness (Phase 6).
8. Build and publish the page (Phase 7).
9. Offer a refresh pass (Phase 8).

### Phase 0: Check the environment

The guide's quality depends heavily on where it runs. Find out first, and tell the user plainly before they invest time.

1. Probe without asking. Read `references/environment.md` for the checks: shell, subagents, Artifact tool, network reach, media tools, chip and memory, and transcription keys (check that a key exists; never print it).
2. If you cannot detect the hardware, for example in a chat app, ask one short question. Explain why: forum transcripts need a fast local chip or a paid transcription service.
3. Rate the environment Full, Reduced or Minimal with the table in `references/environment.md`.
4. Send one short warning before the wizard:
   - Say what works, what doesn't, and how that changes the guide.
   - For Reduced or Minimal, say clearly that results will be much weaker, and list the losses. Recommend treating a Minimal result as a starting checklist, not a finished guide.
   - List the best fixes, ranked by payoff. Examples: install an agentic coding tool from the user's AI provider (Claude Code for Claude users), run on a stronger computer, or add a transcription API key.
5. Let the user continue at the capped depth or switch environments first. Write `environment.md`, and repeat its limits in the guide's methodology.

### Phase 1: Wizard

Read `references/wizard.md` and ask its questions with AskUserQuestion, in short rounds. Without that tool, ask the same questions as a short numbered list. If the user supplies answers or a `values.md` up front, use them and ask only what is missing. Then:

1. Save the answers to `values.md`.
2. Read the profile back in three or four lines, and get a yes before you research.

If the user already gave some answers, skip those questions. If the user declines the wizard, use sensible defaults and state them in the methodology.

### Phase 2: Lock the ballot

The ballot drives everything, and models get it wrong. Build it from official data, not from memory or news.

1. Get the ballot from photos, a PDF sample ballot, or the user's county and city. Use an address only to find the ballot; never store or publish it.
2. For a primary, confirm which party's ballot the user gets (closed, semi-closed or open primary rules).
3. Cross-check every contest against the county election office's sample ballot or voters' pamphlet. Pamphlets are often large compressed or scanned PDFs: download them and use `pdftotext` (or OCR) rather than a web fetch. Google Civic `voterInfoQuery` needs an API key; skip it without one.
4. Take each candidate list from the official filing. Mark unopposed races, write-in-only seats and seats with no filer.
5. Take dates, deadlines, drop sites, ID rules and the voting method from the state or county election office only, and link them. Never write voting procedures from model memory.
6. Write `ballot.md` in the format in `references/research.md`, section 1. Give every contest a race ID, and every multi-seat contest one ID per seat. Link each fact to its official source.

### Phase 3: Map the sources

Read `references/research.md`, section "Source map". Build `sources.md`: a table of groups that endorse or publish guides in this locale, tiered local, then state, then national. Cover three kinds:

- The user's camp: aligned groups.
- Nonpartisan sources: the League of Women Voters, local papers, forums.
- Groups opposed to the user's top priorities: their endorsements are a warning signal.

For a centrist, "opposed" means opposed to a top priority, not a whole camp. In a primary, every candidate may share the user's camp; there, the ledger and the sensitivity check carry the comparison. Then:

1. Confirm that each group exists through a committee filing or a track record. Drop paid slate mailers that pose as groups.
2. Reject any endorsement list from a prior election cycle. Check that the page names this election's year, and that each endorsed candidate is on this ballot; primary-season lists often keep losers.
3. If a source is unpublished, pulled or not yet out, record its status and date in `sources.md`. Never cite a pulled source as current. Cite an archived copy (web.archive.org) only with a note that the group withdrew it, and ask the user how to weigh it.
4. Record "leave it blank" advice as a position, the same as an endorsement.
5. Note each source's owner, funding and known conflicts.
6. Write `links.json` (`{"generic": {name: url}, "per_race": {race_id: {name: url}}}`), pointing each source name to its exact endorsement page.
7. Show the user the table, and let them adjust weights before you research. Only the main agent can ask; subagents return their questions in their reports.

### Phase 4: Research every race

Use parallel subagents, one per cluster of races (federal, state, county, city, measures). Pass each one the safeguards in `references/safeguards.md`, sections 1–3, and `references/research.md`. Fill one **evidence ledger** per race, with the same rows for every candidate:

| Row | What to fill |
|---|---|
| Campaign site | URL, or "(no website)" after checking |
| Own words | Questionnaire answers (Vote411, local papers), then forum quotes with timestamps |
| Record | Votes, actions in office, professional record |
| Money | Totals and top donors from the FEC or the state portal, with the filing date |
| Endorsements | Every mapped group that took a position, with a link |
| Conduct | Court, bar, ethics records, with the candidate's response |
| Priority issues | Position on each wizard priority, or "no statement found" |

Write "not found" rather than guessing. Empty cells are information. Tag each claim not yet checked against its original `[unverified]`, and each negative claim about a candidate `[neg]`; the Phase 6 fact-check collects these tags. A subagent that cannot spawn its own subagents does the reading itself.

For forums and debates, follow `references/research.md`, section "Transcripts". `scripts/forum_transcripts.sh` handles captions, audio download and local transcription in one call.

For each contested partisan race, record competitiveness from forecasters, polls or past margins, with dates. Phase 5 needs it for spoiler risk.

### Phase 5: Rank, fork and test sensitivity

1. Score each candidate on each priority from −2 (strongly against the user's values) to +2 (strongly for). Use `null` where there is no evidence, and mark scores that rest on thin evidence as weak. Save the scores as `scores.json`, in the format that `scripts/sensitivity.py --help` shows. Base each score on ledger evidence only.
2. Rank every option by the weighted scores. Then adjust for non-policy criteria the user turned on, such as conduct or competence, and say so in the card. Candidates' own words and records count most, then the user's trusted groups, then other aligned groups, then news.
3. Run `scripts/sensitivity.py scores.json`. Turn every race whose top pick flips into a fork or a note.
4. Find the **forks**: races where aligned sources split, a sensitivity flip, or a strategy choice that changes the pick. Typical forks are protest vote vs. blocking the other side, purity vs. electability, and two flawed candidates. Write two or three options for each fork:
   - Give each option a 3–6 word label.
   - Give it two pros and two cons of a few words each.
   - Add "leave it blank" where the user's sources suggest it.
5. Set each fork's default from the wizard answers:
   - "Idealistic" means the closest match on the user's priorities, which is not always a third-party candidate. A major-party candidate who leads on the top priorities can be the idealistic pick.
   - "Pragmatic" means the closest match among candidates who can win.
   - "Mixed" means idealistic where a cited forecaster or past margin shows a safe race, and pragmatic in close ones. Base "safe" on this cycle's ratings, not last cycle's margin.
   Build two presets that set only the strategy forks: pragmatic and idealistic.
6. Write a **strongest case for the other side** for each contested race: one respectful sentence in the opposing view's best terms. Skip it if the user turned it off.
7. Write short, finding-first prose. Persuasive density is not the goal: the most persuasive AI text tends to be the least accurate.

### Phase 6: Verify and review fairness

Run each check as a separate subagent, so the reviewer is not the writer.

1. **Fact-check.** Collect every `[unverified]` and `[neg]` claim from the ledgers and the draft. Have a subagent check each one laterally against the original document or recording. Remove or fix what it cannot confirm. Label single-source claims "unconfirmed," and never let them decide a pick.
2. **Quote check.** Compare every transcript quote with the audio at its timestamp. Treat `[suspect]` lines as unverified. Checking a caption quote against the same captions proves nothing, so say "checked against captions only" where audio is out of reach. If YouTube blocks downloads, ask the user before using browser cookies (`yt-dlp --cookies-from-browser`).
3. **Swap test.** Write `pairs.json` (format: `scripts/swap.py --help`). Run `scripts/swap.py` to swap the picked candidate and the runner-up in each contested card (names, and party labels in partisan races). Give the output to a fresh reviewer, and withhold `values.md`. Ask whether each candidate gets the same evidence bar, the same tone and the same density of negative claims. Fix every imbalance it reports. Without subagents, run the review yourself in a fresh pass, and label it a self-review in the methodology.
4. **Fresh-eyes review** (Deep level). Give another fresh subagent only the draft. Ask it for missing sources, unfair wording and gaps, with the user's values held fixed. If the user has another vendor's model set up, offer it as a second reviewer.
5. **Staleness check.** Within 48 hours before sharing, recheck withdrawals, new endorsements, pulled sources and late filings.

### Phase 7: Build the page

Read `references/page-spec.md`, then copy `assets/guide-template.html` to `guide.html` and fill it. Load the `artifact-design` skill if you publish as an Artifact. The page needs:

1. A "Personal guide — not an official ballot" banner, a last-updated date and the user's values profile.
2. Quick picks, with "Your call" options for forks and two preset buttons.
3. Race cards with endorsement pills, the fork, per-pick summaries, a head-to-head table, the evidence ledger and the counter-view line.
4. A methodology section that names what the AI did and what the human decided.
5. A changelog, an official-info box linking the election office, and a continuous works-cited list.

Then do the following:

1. Run `scripts/linkify.py guide.html links.json`.
2. Run `scripts/check_links.py guide.html`. Treat "??" lines (paywalls, bot walls) as fine after a manual look.
3. View the page at phone width (375 px) and in print preview. Fix overflow and hidden content.
4. Strip all personal data: no address, name, email or voter ID.
5. Let the user choose the author line. "Anonymous voter, with AI assistance" works well.
6. Show the user the picks, and publish only after they approve. The user is the final decider, and the page says so.

### Phase 8: Refresh

About a week before the election, offer to rerun Phase 2, the money and endorsement rows from Phase 4, the Phase 6 staleness check and Phase 7. Log each change in the changelog.

## Scripts

Run these scripts; don't read them into context. Each one prints usage with `--help`. They target macOS on Apple Silicon; on other systems, find equivalent tools and follow the same flow.

| Script | Use |
|---|---|
| `setup_macos.sh [--install]` | Check or install ffmpeg, yt-dlp, mlx-whisper, parakeet-mlx and PDF tools. Ask before installing |
| `forum_transcripts.sh [--no-captions] OUTDIR 'URL'...` | Get a timestamped transcript per video: captions first, then local Whisper. Quote URLs |
| `captions.py`, `transcribe` | The two halves of the step above, for one-off use |
| `fec.py search\|totals\|donors\|outside` | Federal campaign-finance summaries with coverage dates |
| `sensitivity.py scores.json` | Races whose top pick flips under other weights, or rests on weak evidence |
| `swap.py guide.html pairs.json out.html` | Build the blinded, swapped draft for the swap test |
| `linkify.py guide.html links.json` | Link source names to their exact pages |
| `check_links.py guide.html` | Confirm that links load; show campaign-site titles |

## Depth levels

The wizard sets the level, and Phase 0 caps it. Scale the work, not the safeguards: every level runs Phase 2, the fact-check and the swap test.

| Level | Adds | Typical use |
|---|---|---|
| Quick | Endorsements, news, official ballot | Small ballot, or a fast first pass |
| Standard | Campaign finance, questionnaires, caption transcripts | Most ballots |
| Deep | Audio transcription, conduct records, source conflicts, fresh-eyes review | Contested local races, guides for sharing |

## Search

Use built-in WebSearch and WebFetch. If they hit a limit or a page blocks you, use any search API the user configured in their CLAUDE.md. Never print an API key.

## Things this skill never does

- Generate images, audio or video of candidates.
- Write mass-mailing or targeted persuasion material. The guide is a personal document that people share by choice.
- Promise that sharing, or paying to boost, the guide is legally exempt. See `references/safeguards.md`, section 4.
- State an unproven allegation as fact.
