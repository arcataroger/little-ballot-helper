# Page spec

Start from `assets/guide-template.html`. It is a full HTML document that works standalone or as a claude.ai Artifact. It holds the styles, the fork and preset script, and one example of each card type. Replace every `{{...}}`, then delete the template comments.

## Structure, top to bottom

1. **Banner**: "Personal voter guide · Not an official ballot · Not endorsed by any group named here." Keep it even though the ovals look ballot-like.
2. **Header**: the eyebrow (county · election · date), a two-to-four-word title, a last-updated line and a one-sentence lede.
3. **Official info box**: the voting method, the return deadline and links to the county and state election offices, copied from those offices.
4. **Collapsed folds** (`<details class="sheet fold">`): how to read the guide (with the pill key), whose values these are, and terms.
5. **Quick picks**: the two preset buttons and a Race / Pick / Notes table. A fork row reads "Your call: A, B, or leave blank," with each name in a `.cand[data-c]` span.
6. **Race sections** by level (federal, state, county, city, district, measures). Use one `<article class="sheet race" id="...">` per race.
7. **Methodology**: values and weights, source tiers, strategy, sensitivity results, who made it (AI vs. human roles), the research process with counts, known limits and an error-report contact.
8. **Changelog**: dated entries.
9. **Works cited**: grouped lists that share one continuous counter. Give each entry its retrieval date.
10. **Footer**: "Personal guide, not an official ballot," the as-of date and the election office link.

## Race card parts

- `.race-head`: the office name and a chip for competitiveness or "Sources split."
- `.ranks`: every candidate in rank order, including those the user opposes. Each line has the name (linked to the campaign site, or followed by `(no website)`), a `.meta` line for party and incumbency, and `.endorse` pills.
- `.fork` (fork races only): the question, two or three `.opt` buttons with `data-pick`, and an optional blank link. Give each `.ranks li` in a fork race `data-c` equal to its option ID, so the filled oval follows the choice.
- `.why`:
  - the background
  - one `.ifpick[data-when]` per option
  - a head-to-head `.h2h` table (fork races), with rows for the user's priorities first
  - the evidence ledger
  - the counter-view line
  - forum quotes with timestamped links
  - "Who recommends what"
  - a sources line
- Measures: a large YES/NO, then "A yes vote means…" and "A no vote means…," then the funders on each side. The template has an example.
- Multi-seat contests: one card with a sub-list per seat. The template has an example.
- In fork races, candidates who are not options keep their rank line but get no `data-c`.
- The evidence ledger and the head-to-head table must not repeat each other. In fork races, keep the head-to-head and fold ledger-only rows (money, conduct, own words) into it.

## Pills

- `.chip.rec`: groups aligned with the user's values.
- `.chip.opp`: groups that oppose them (shown red). This includes the opposing party and groups opposed to the user's top priorities.
- A pill's text names the group. The CSS adds + or −, and hidden text states the stance for screen readers. Define every abbreviation in the key.

## Fork config

Edit the `guide-config` JSON at the bottom:

- `defaults`: one option ID per fork race, taken from the wizard.
- `presets.pragmatic` and `presets.idealistic`: only the forks where strategy decides. Clicking a lit preset resets its races to the defaults.
- `storageKey`: unique per guide. Bump the version when the option IDs change.

## Writing

- Lead with findings. Use short sentences, plain words and active voice.
- Use plain descriptive terms (see `wizard.md`, "Terminology").
- Never write "vote for X because I think." Write "Picks X because [user priority]: [evidence]."
- Each card must stand alone. Assume the reader reads only that card.
- Give pros and cons a few words each.

## Publishing

1. Load the `artifact-design` skill if you publish as a claude.ai Artifact. Otherwise save the HTML file.
2. Run `scripts/linkify.py guide.html links.json` and `scripts/check_links.py guide.html`.
3. Search the page for the user's name, email, street address and voter ID. Remove any you find.
4. Check the page at phone width (375 px) and in print preview.
5. Show the user the picks. Publish only after they approve.
