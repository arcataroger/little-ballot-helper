# Wizard

Ask with AskUserQuestion. Each call takes at most four questions with two to four options each, and the tool adds "Other" automatically. So round 1 is one call, and round 2 usually takes two calls. Tailor round 2 to round 1. Never assume a leaning from the user's location, name or anything else.

## Round 1: who and where

1. **Ballot.** "How should I get your ballot?"
   - Upload photos or a PDF of my ballot or sample ballot
   - Look it up: I'll give county and city (and precinct or district if I know it)
   - I'll paste the races
2. **Leaning.** "Broadly, where are you?" Refine in round 2.
   - Left of center
   - Center / independent / cross-pressured
   - Right of center
   - Libertarian
   If the user picks "Other" (Green, populist, single-issue, etc.), take their words as given.
3. **Strategy.** "In close races, how do you weigh beating the side you oppose against voting for your closest match?"
   - Mixed: idealistic in safe races, pragmatic in close ones (Recommended)
   - Pragmatic: block the side I oppose
   - Idealistic: closest match, always
   - Show me both and I'll decide per race
4. **Depth and audience.** "How deep, and who will read it?"
   - Quick, just for me
   - Standard, for me and family/friends (Recommended)
   - Deep, for sharing widely
   - Standard, just for me

## Round 2: values

First refine the camp with one question, with four options drawn from the round-1 answer:

- Left: democratic socialist or Green · progressive Democrat · mainstream Democrat · left-leaning independent
- Center: centrist Democrat · centrist Republican · independent, issue by issue · moderate who votes split tickets
- Right: center-right / business Republican · conservative · populist / MAGA Republican · religious conservative
- Libertarian: Libertarian Party · libertarian-leaning Republican · classical liberal independent · civil-libertarian left

For a primary, also ask which party's ballot the user will vote (or whether it's an open or top-two primary).

Build the issue options from the user's camp. Include issues from several dimensions, not only the camp's signature ones: the research shows that issue selection shifts the advice. Offer issues as multiSelect, in two questions if needed.

Issue menu: choose about eight that fit the camp, and include at least two from outside its signature list. Use plain descriptive terms. Where camps name an issue differently, show the label the user's camp uses: "abortion access" or "protecting unborn life," "border security" or "immigrant rights."

- Abortion and reproductive health
- LGBTQ+ rights
- Climate and environment
- Housing costs and homelessness
- Taxes and government spending
- Public safety and policing
- Immigration
- Guns
- Health care
- Labor and wages
- Education and schools
- Civil liberties and surveillance
- Election administration and democracy
- Religious liberty
- Parental rights in schools
- Size of government and regulation
- Second Amendment / gun rights
- Corruption and money in politics
- Local growth, land use and water
- Tech, AI and data centers

Then ask:

5. **Priorities.** "Which issues matter most?" (multiSelect). Follow up in plain text: "Rank your top three, or say if they're equal."
6. **Trusted sources.** "Any group, paper or person whose guide you trust most?" (free text: offer "No, use your judgment" and "I'll name some"). Ask how much extra weight to give them: a tiebreaker, or a strong voice.
7. **Dealbreakers and non-policy criteria.** "Does anything rule a candidate out, or matter beyond issues?" (multiSelect):
   - Honesty and conduct records
   - Experience and competence
   - Backing from groups I oppose
   - Who funds them (corporate, union, party-machine or out-of-state money)
8. **Extras.** "Anything to add or turn off?" (multiSelect):
   - Strongest case for the other side in each contested race (on by default)
   - A version in another language
   - A printable version to take to the booth
   - Light notes on a secondary topic (name it)

## Save the profile

Write `values.md` like this. Keep it free of personal data.

```markdown
# Voter profile (as of YYYY-MM-DD)
- Ballot: <county>, <city>, <election name and date>; source: <photo|sample ballot|lookup>
- Camp: <user's words>
- Strategy: <mixed|pragmatic|idealistic|per race>
- Depth: <quick|standard|deep>; audience: <self|friends|public>
- Priorities (ranked): 1. ... 2. ... 3. ...; also: ...
- Trusted sources: <names> (weight: <tiebreaker|strong>)
- Non-policy criteria: ...
- Counter-view lines: <on|off>; terms: plain descriptive
- Extras: ...
```

Read it back in three or four plain sentences and ask: "Is this right?" Fix it before you research.

## Terminology

Default to plain descriptive terms that say what a policy does: "bans abortion after six weeks," "lets police share plate-reader data with federal agents." Avoid either camp's branding ("pro-life," "pro-choice," "death tax," "gun safety") except inside quotes and group names. If the user asks for their camp's vocabulary, use it, and note the choice in the methodology.
