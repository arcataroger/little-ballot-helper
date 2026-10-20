# Safeguards

Each rule names the failure it prevents. Pass sections 1–3 to every research subagent.

## 1. Accuracy

1. **Official data for facts about the election itself.** Take the ballot, candidate lists, dates, deadlines, drop sites and ID rules only from election offices. Chatbots got about half of election questions wrong in a 2024 audit and invented polling places (AI Democracy Projects/Proof News). A 2026 Common Cause report caught chatbots naming the wrong propositions and misstating a runoff.
2. **Full candidate lists.** ChatGPT gave incomplete governor lists 89% of the time in a 2026 States United test. Use filings, not news.
3. **Primary sources first.** Rank sources: official records and candidates' own words, then reporting, then advocacy, then Wikipedia. Trace each claim to its origin, not a summary (lateral reading; SIFT).
4. **Exact wording.** Check a claim word for word. Split compound claims and check each part (PolitiFact method).
5. **Dates on everything.** Record when you retrieved each source. Put the "as of" date on the page.
6. **This cycle only.** Search results and model memory surface last cycle's endorsement lists. Reject any list whose page does not name this election's year.
7. **No model memory for positions.** LLM-based voting-advice tools disagreed with parties' own answers in 25–50% of cases (Dormuth et al. 2025). Cite each position.

## 2. Even-handedness

1. **Symmetric ledger.** Run the same checks for every candidate in a race, and show "not found." Unequal effort looks like a finding (League of Women Voters equal-treatment rules).
2. **Visibility bias.** Low-publicity candidates get thin coverage. Search their questionnaires before you call them blank.
3. **Right of reply.** Before you print a negative claim, find the candidate's response and include it.
4. **Single-source rule.** A negative claim with one source, or an anonymous one, gets the label "unconfirmed" and never decides a pick.
5. **Swap test.** Chat models lean left (Rozado 2024; Motoki 2024) and echo the user's views (Perez 2022; Sharma 2024). A fresh reviewer, who never sees the values profile, gets the draft with the pick and the runner-up swapped (names, plus party labels in partisan races). It compares the evidence bar, the tone and the density of negative claims. Run it for every user, of any camp.
6. **Counter-view line.** Opposing-content floods backfire (Bail 2018), but short, respectful, evidence-based engagement works (Costello 2024). One sentence per contested race, in the other side's best terms.
7. **Restraint.** The most persuasive AI setups made the most false claims (Hackenburg 2025, *Science*; Lin 2025, *Nature*). Lead with findings, keep claims few, and avoid stacking arguments.

## 3. Method transparency

1. **Publish the profile.** Show the priorities, weights and matching rule (Lausanne Declaration on voting-advice applications; Louwerse & Rosema 2014 found that the matching model changes most users' advice).
2. **Sensitivity check.** Rerun the picks with equal weights and with each priority removed. Report races that flip.
3. **Non-policy criteria.** Proximity matching ignores competence and integrity (Wagner & Ruusuvirta 2012). Show them when the user turned them on.
4. **Down-ballot gaps.** Say plainly when no aligned group spoke on a race. Endorsement shortcuts mislead low-information voters as races multiply (Lau & Redlawsk 2001).
5. **Facts vs. judgment.** Label checked facts as facts and rankings as the voter's judgment. The voter is the final decider.
6. **Specific AI disclosure.** State what the AI did (search, transcription, drafting, review) and what the human decided (values, sources, every pick) (AP and Reuters AI policies).
7. **Corrections.** Keep a dated changelog. Offer an anonymous contact for error reports (IFCN code; FactCheck.org).

## 4. Legal hygiene (not legal advice; rules vary by state)

1. **Not a ballot.** Some states regulate imitation sample ballots. Oregon requires "NOT FOR OFFICIAL USE" on altered sample ballots, and West Virginia treats deceptive imitations as a felony. Put "Personal guide — not an official ballot" at the top. Never copy the official ballot layout exactly, and never imply that a group endorsed a pick it did not.
2. **Unpaid sharing.** Under federal rules, an individual's unpaid online activity is not an expenditure, and FEC disclaimers apply to paid ads (11 CFR 100.94, 110.11). Tell the user that paying to promote the guide can trigger federal or state disclaimer and reporting rules. Some states set low thresholds, such as Washington's $1,000 for independent expenditures. Never promise an exemption.
3. **Allegations.** Repeating someone else's false claim can still be defamation (the republication rule). Attribute each allegation and link to it. Prefer court and agency records, include the denial, and never state an allegation as fact. Never name private individuals.
4. **Quotes.** Keep quotes short and linked. Never reproduce whole articles or questionnaires.
5. **No synthetic media.** Never make images, audio or video of candidates. About 30 states regulate election deepfakes, and Minnesota's law covers unpaid sharing.
6. **Privacy.** Keep the user's address, name, email and voter ID out of the guide and out of URLs.

## 5. Accessibility and reach

1. Meet WCAG 2.2 AA: text labels on every pill (not color alone), semantic tables and headings, visible focus, and 4.5:1 contrast.
2. Use plain language: short sentences and common words, and define terms (Center for Civic Design field guides).
3. Offer a print layout for the voting booth.
4. If the county must provide materials in other languages (Voting Rights Act Section 203), offer a translated version labeled "machine translation." Link the official translated ballot.

## Research behind these rules

- AI Democracy Projects/Proof News, "Seeking Reliable Election Information," 2024.
- AlgorithmWatch & AI Forensics, Bing Chat elections audit, 2023.
- States United, chatbot candidate-list test, 2026. Common Cause CITED report, 2026.
- Rozado, *PLOS ONE* 2024. Motoki et al., *Public Choice* 2024. Perez et al. 2022 (arXiv 2212.09251). Sharma et al., ICLR 2024.
- Dormuth et al. 2025 (arXiv 2502.15568). Chalkidis 2024 (arXiv 2407.08495).
- Hackenburg et al., *Science* 2025. Lin et al., *Nature* 2025. Hackenburg & Margetts, *PNAS* 2024.
- Louwerse & Rosema, *Acta Politica* 2014. Lefevere & Walgrave, *Electoral Studies* 2014. Wagner & Ruusuvirta, *Acta Politica* 2012. Garzia & Marschall (eds.), Lausanne Declaration, 2014.
- Lupia, *APSR* 1994. Lau & Redlawsk, *AJPS* 2001.
- Bail et al., *PNAS* 2018. Costello, Pennycook & Rand, *Science* 2024.
- IFCN Code of Principles. SPJ Code of Ethics. Caulfield, SIFT. Wineburg & McGrew, lateral reading.
- FEC, internet communications guidance. Center for Civic Design, *Field Guides to Ensuring Voter Intent*. W3C WCAG 2.2.
