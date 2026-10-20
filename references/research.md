# Research playbook

## Contents
1. Official data
2. Source map
3. Candidate research
4. Campaign finance
5. Transcripts
6. Competitiveness
7. Ballot measures
8. Data source status

## 1. Official data

Official data comes first, for the ballot, the candidate list and all voting logistics.

1. County election office: sample ballot, voters' pamphlet, candidate filings, drop-site list, canvass reports from past elections.
2. Secretary of State: statewide measures, official measure text, the fiscal impact statement, deadlines.
3. Google Civic Information API `voterInfoQuery` (needs a free API key) for contests by address where it has data. Google retired its representatives lookup in April 2025. Election and division lookups remain.
4. For logistics, the user can check vote.org, CanIVote.org or TurboVote. Link the state or county page in the guide.
5. Read official PDFs locally: download them, then run `pdftotext -layout`. For scanned pages, run `ocrmypdf` first. Web fetchers often fail on large compressed pamphlets.

`ballot.md` format:

```markdown
# Ballot: <city>, <county>, <state>. <election>, <date>
As of YYYY-MM-DD. Sources: <key> = <official URL>, ...

## <race-id>: <Office as printed>
- Seats: 1 · Vote for: 1 · Partisan: yes/no · Incumbent: <name or none>
- Candidates (ballot order): <Name> (<party or "nonpartisan">) [src: KEY p. N]; ...
- Notes: unopposed / write-in only / no filer
```

Use one race ID per seat, for example `swcd-zone-1`. For measures, record the official ballot title and the yes and no committees.

## 2. Source map

Build one table: group, camp, tier (local, state or national), what it publishes (endorsements, guide, questionnaire, scorecard), link, owner or funder, and conflicts.

Where to look, by type:

| Type | Examples to search for in the locale |
|---|---|
| Nonpartisan | League of Women Voters (Vote411, forums, pamphlets), local papers' questionnaires, Ballotpedia, local TV forums, chambers and rotary forums |
| Party | County and state party endorsement lists, for both major parties and minor ones |
| Issue groups | Reproductive-rights and anti-abortion groups, LGBTQ+ groups, environmental groups (LCV state affiliates, Sierra Club chapters), gun groups on both sides, taxpayer groups, business PACs, realtors and builders, police and fire unions |
| Labor | State AFL-CIO or labor federation, teachers' unions, SEIU, building trades |
| Ideological | DSA chapters, Working Families, Indivisible, Our Revolution, Justice Democrats on the left. Club for Growth, Americans for Prosperity, FreedomWorks, Heritage Action, state Family Policy councils, SBA Pro-Life America, NRA and Gun Owners of America, state Chamber of Commerce PACs, and county Republican parties on the right. The Libertarian Party, Young Americans for Liberty and state Libertarian caucuses for libertarians. Centrist groups such as No Labels and local "balance" PACs |
| Media | Editorial boards, alt-weeklies, statewide outlets. Note each one's owner |
| Individuals | Local bloggers and voter-guide authors; weight them low unless the user trusts them |

Rules:

1. Search "<county> <year> endorsements", "<group> <state> <year> endorsements", "<race> forum", "<city> voter guide <year>".
2. Confirm that each group is real (a committee filing, a website with history). Drop paid slate mailers.
3. Weight local over state over national for local races. National groups count more in federal races.
4. Use expert source-reliability ratings as weak priors for factual reliability only. Do not use left–right "bias charts" to discount advocacy groups; the user chose a camp.
5. Record the date of each group's list. Many groups publish late.

## 3. Candidate research

Run the same steps for every candidate in a race, so the evidence ledger stays symmetric.

1. Campaign site: search, confirm it is this year's race and the right person, and record the URL or "(no website)".
2. Own words: Vote411 answers, newspaper questionnaires, forum transcripts, op-eds, social posts. Quote short passages with links.
3. Record: votes (OpenStates for state legislators, congress.gov for federal), actions in office, and professional history.
4. Conduct: state bar discipline search (for lawyers and judges), court records, ethics commission rulings, police misconduct databases where they exist. Always include the candidate's response or denial.
5. Priority issues: one line per wizard priority, or "no statement found (searched X, Y)".

## 4. Campaign finance

1. Federal: run `scripts/fec.py`. `search` finds the candidate ID; `totals`, `donors` and `outside` give money raised, top donor employers and independent expenditures. Set `FEC_API_KEY` (free at api.data.gov); `DEMO_KEY` allows only a few calls. Also check OpenSecrets for outside groups.
2. State and local: the state portal. Each one differs, and many need a session cookie, a CSRF token or form posts. Write one small helper in `work/` and share it with every subagent, rather than letting each agent write its own. Match candidates by full name and office, never last name alone. Record the filing date covered.
3. Report totals, the share from small donors where the data allows, and the top five donors or donor types. Flag money from groups the user opposes.
4. FollowTheMoney's state data stops at 2024. Use it only for history.
5. If you cannot reach the data, write "not checked." Never estimate.

## 5. Transcripts

The scripts below target macOS on Apple silicon. On other systems, find equivalents yourself (ffmpeg, yt-dlp, and a Whisper build such as faster-whisper or whisper.cpp), and follow the transcription ladder in `environment.md`. Start with candidates' written questionnaire answers: they cost nothing and often beat forum quotes.

1. Run `scripts/setup_macos.sh` to see which tools exist. If any are missing, ask the user, then run `scripts/setup_macos.sh --install`.
2. Find forums on YouTube, local TV sites, League chapters, public-access channels and podcasts. Search with `yt-dlp --flat-playlist --print "%(id)s %(title)s" "ytsearch20:<city> <office> forum <year>"`. List a channel with `.../channel/<id>/videos`; @handle URLs sometimes 404.
3. Run `scripts/forum_transcripts.sh OUTDIR 'URL' ['URL'...]`, quoting each URL. Add `--no-captions` once YouTube starts returning HTTP 429, to skip straight to audio. For each video, it tries captions first (`captions.py`, with backoff on HTTP 429). If that fails, it downloads the audio and runs `scripts/transcribe`. It prints one status line per video, and it skips videos already done, so reruns are cheap.
4. `transcribe` skips long silences, which stops Whisper's "Thank you." loops. It re-transcribes looping or low-confidence spans with Parakeet. It writes `ID.txt` ("m:ss text", tagged `[parakeet]` or `[suspect]`) and `ID.json`. On an M-series Mac, large-v3-turbo runs at about 1.5–2 seconds per audio minute.
5. Read each transcript in full, in a subagent where you can. Pull quotes with timestamps, and link `https://www.youtube.com/watch?v=ID&t=SECONDSs`.
6. Fix obvious mishearings only. Before publishing, check each quote against the audio, and treat `[suspect]` lines as unverified.

## 6. Competitiveness

1. Federal and statewide: Cook Political Report, Sabato's Crystal Ball, Inside Elections, and recent public polls with dates and sample sizes.
2. Local: past margins from the county canvass, primary results, registration splits.
3. Rate each partisan race safe, likely, lean or toss-up, and cite the basis.
4. Spoiler logic: under plurality voting, a third-party vote risks electing the user's least-liked candidate only when the race is close and the third party draws from the user's side. Under ranked-choice voting, the risk mostly vanishes, so say which system applies.

## 7. Ballot measures

1. Read the official text and the fiscal statement, not only summaries.
2. List the official "yes" and "no" committees and their top funders.
3. Explain what a yes vote does and what a no vote does in one plain sentence each. Measure wording often makes "yes" and "no" confusing.

## 8. Data source status (as of late 2026; recheck)

| Source | Status |
|---|---|
| Google Civic `voterInfoQuery` | Free with a key; patchy for local races |
| Ballotpedia | Free site; paid API |
| Vote411 | Free site, no public API |
| FEC API | Free with an api.data.gov key |
| OpenStates (Plural) v3 | Free; legislators and bills only |
| MIT Election Lab | Precinct returns; local returns for 2018 and 2020 only |
| FollowTheMoney / OpenSecrets | State data through 2024 |
| Democracy Works / TurboVote | Logistics; API access by request |
