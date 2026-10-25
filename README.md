# NETRA India AI Risk Observatory

**🔗 Live site: https://krunal6649.github.io/netra-india-observatory/**  ·  v0.2 (open data, open code)

An open, India-focused record of AI harms, the Indian laws that may apply to them, and the authorities that can act. For each incident it shows what happened, which laws may apply, which authority could act, and what is still unknown, using NETRA, a 14-stage method for analysing AI harm.

![NETRA India AI Risk Observatory](docs/screens/netra-hero.png)

## Who it is for
- **Lawyers and policy researchers:** find incidents, laws and gaps in one place, each with a source link.
- **Journalists and civil society:** see how deepfakes, voice cloning, fake citations and automated decisions map to Indian law.
- **Government bodies and regulators:** see which body can act on a harm, where the law has gaps, and tell us what is wrong or missing.
- **Anyone harmed by AI:** find who to approach. For money lost to cyber fraud, call **1930** or use **cybercrime.gov.in** first.

## Start here (three minutes)
1. Open the [live site](https://krunal6649.github.io/netra-india-observatory/) and press **Guided tour** (top right) for a seven-step walk-through.
2. On **Home**, use **Who to approach**: pick Union or a state on the tile map, then a body. Below it, **This week in India** shows the latest weekly update.
3. Go to **Explore**, switch between Risks, Incidents, Laws and Measures, and search. Click **Filters** to narrow the list.
4. Open an incident's **NETRA dossier** (under **Analysis**), or press **Generate report** on any incident, risk area or model.

## What is in it (v0.2, data updated 2026-10-25)

| Part | Count | Review status |
|---|---|---|
| Indian AI incidents | 22 | All reviewed by the maintainer (Krunal) on 2026-10-25 |
| Laws, rules, advisories and court orders | 28 | 4 verified against official texts; 24 partly verified, each saying what is missing |
| Risks quoted from Indian government frameworks | 18 | Quoted with location |
| Measures | 28 | Quoted or summarised from those instruments |
| Governance gaps | 6 | NETRA analysis |
| Who to approach directory | 391 bodies (31 Union, 10 for each of 36 states and UTs) | 32 official links checked by the maintainer |
| AI model cards | 12 | Unreviewed |
| Weekly update | Up to 5 AI items, Cyber watch, Model watch | Auto-selected, unreviewed |

> **Status:** an independent research project. **Not legal advice.** Codings were drafted with AI assistance; each record says whether a person has reviewed it, and the build refuses a record marked reviewed without a reviewer and date.

**Corrections:** use [Suggest a correction](https://github.com/krunal6649/netra-india-observatory/issues/new?template=correction.yml) (also linked at the bottom of every page). It asks only for a public source link, its date and the place. It is not for reporting live incidents, and nothing changes on the site until the maintainer reviews it.

**Cite as:** Krunal (2026). *NETRA India AI Risk Observatory* (version 0.2.0) [Data set]. https://github.com/krunal6649/netra-india-observatory. See `CITATION.cff`; `.zenodo.json` holds the matching Zenodo record. Data: CC BY 4.0. Code: MIT. Risk taxonomies adapted from the MIT AI Risk Repository (CC BY 4.0), with credit; this project is not affiliated with MIT.

**Contact:** Krunal, Advocate (Bar Council of Gujarat), AI governance researcher · krunal.maheshwari@gmail.com

## How the site is organised

Four sections. Night (dark) mode is the default; the sun / moon button at the top right, beside **Guided tour** and **Credits**, switches to day mode. Printing always uses day colours. Each page has its own link, such as `#explore-laws` or `#analysis-dossiers`.

| Section | What it holds now |
|---|---|
| **Home** | **This week in India** (weekly, auto-selected, unreviewed), headline, one "cases tracked" counter (reviewed and unreviewed, with the data update date), then **Who to approach**: a drill-down directory (Level → Authority → Bodies → body page) of 31 Union bodies and 10 standard bodies for each of the 36 states and UTs, coloured by role (enforces, adjudicates, regulates, supports victims). States and UTs appear on a tile map of India that includes Jammu and Kashmir, Ladakh and Arunachal Pradesh. Then the risk wheel and where incidents outrun binding law |
| **Explore** | One searchable list with a switch: **Risks** (18 quoted from MeitY’s 2025 AI Governance Guidelines and NITI Aayog’s Responsible AI Part 1) · **Incidents** (22 documented in India) · **Laws** (28 statutes, rules, advisories, policy papers, standards and court orders, with Act numbers, Gazette notifications and cases where known) · **Measures** (28, sorted into MIT’s 23 mitigation types). Filters stay hidden until you click **Filters**. Incidents and laws show as a compact list (one line each, click to expand; a **List / Cards** switch keeps the full cards), can be sorted, show 20 at a time with **Show more**, and list active filters as chips you can remove. Incidents can also be filtered by state or UT, year and review status. Clicking the wheel opens one **risk area** with everything for it side by side |
| **Analysis** | **NETRA dossiers**: each incident through the 14 NETRA stages (location and jurisdiction, legal issues T1, authority routing, gaps T2–T3, unknowns, overclaim check) · **Gap register**: 6 gaps tied to incidents and instruments · **Report generator**: a plain report for any incident or risk area, built in the browser from the stored data with no AI; preview, copy, download as Markdown, or print / save as PDF. Each dossier, incident card and risk area has a **Generate report** button · **Models and evaluations**: 12 AI models (by model) and the three METR reports mapped to Indian law (by evaluation report); each model card keeps what the testers found (METR, MITRE ATLAS) apart from NETRA's India analysis, with a Generate report button. **Add a report** (on Models and evaluations and Report generator) reads a PDF, Word, text or Markdown file in your browser only and runs the **NETRA check**: keyword matching against NETRA's own lists (no AI, no key), showing risk areas, Indian laws named or linked, who could act, related gaps and similar India cases, with word-for-word passages. **Send to NETRA for review** opens a prefilled GitHub form or an email |
| **About** | **Method** · **Sources and credits** (every outside source and its licence) · **Verification status** (what has been checked against official texts and what is missing) · **Expert survey** |

Links from v0.1 still work: `#navigator`, `#risks`, `#incidents`, `#governance`, `#mitigations`, `#netra`, `#gaps`, `#evidence`, `#survey` and `#about` open the matching new page.

## How the survey works

- **Anyone can take part.** Signed-in Contributors save answers directly. Everyone else (outside peers, public-link visitors, signed-out readers) clicks "Get my response code" and sends you the short code by email, WhatsApp or any message.
- **You import codes** in the owner-only box on the Expert survey page (About › Expert survey). Paste one or many at once; the same code imported twice counts once. Codes are checked, and anything with invalid values is rejected.
- Codes contain only survey answers, never a name or account.
- Nobody but you sees individual answers. Results go public only when you press "Publish aggregate", and show only once 5+ people have answered with consent.

## Run it on your own computer

Needs Python 3 only.

```
cd netra-india-observatory
python3 scripts/build.py          # checks data, writes dist/index.html
python3 -m unittest discover tests
node tests/smoke.js               # optional, needs Node.js
```

Open `dist/index.html` by double-clicking. Everything works offline except the survey, which needs the published version, and the fonts, which fall back to system fonts.

## Adding data

Edit `data/india.json` (incidents, instruments, risks, mitigations, gaps) or `data/authorities.json` (the Who to approach directory) and run the build. The build refuses:

- a risk without a verbatim quote and location
- an incident without an overclaim check and a "what we do not know" list
- NETRA stage 11 (human review) marked done on an unreviewed record
- unknown risk areas, sectors, instruments or authorities, and non-https sources
- a possible duplicate case: the same source or court document as an existing case, or a title 75% or more alike. If a person has checked that two look-alike cases really differ, list the other id in `distinct_from`
- a directory body with an unknown role, place, group or law, a non-https link, or "verified" without a link, checker and date; and any case whose reporting route does not lead to a body in the directory
- a missing or malformed `meta.updated` date (shown beside the home-page counter; change it whenever the data changes)
- a verification status other than yes / partial / no, or "yes" on a site home page instead of a specific document
- malformed Act numbers ("Act 45 of 2023"), Gazette notification numbers ("G.S.R. 139(E)", "S.O. 2351(E)"), dates, or case entries missing a citation, court, date, holding or verification note

`data/taxonomy.json` holds MIT’s taxonomies (keep the attribution line). `data/global_evidence.json` is the earlier METR pilot.

## Add a report and the NETRA check

On the public site, **Add a report** reads the file in the visitor's browser and runs the **NETRA check**: plain keyword
matching against `data/check_terms.json` (NETRA's own term lists for the 24 risk areas and 28 Indian instruments).
No AI is used, no key is needed and nothing is sent. Every passage shown is copied word for word from the file, and
results are labelled auto-matched, unreviewed and "possible only". **Send to NETRA for review** opens the
`report.yml` issue form (or an email) prefilled with the title, link and check summary, never the file.

## This week in India (weekly update)

Every Saturday at 00:00 IST, **Actions › Weekly update (unreviewed)** runs `scripts/weekly_top5.py` and opens a pull
request with up to five AI incidents in India from the past week, a separate Cyber watch and a Model watch. It uses
free official feeds and APIs (GDELT, PIB, METR, MITRE ATLAS), no AI and no key. Every item is "Auto-selected,
unreviewed"; check each against its sources, delete what is wrong, then merge. Method and limits:
[docs/weekly-method.md](docs/weekly-method.md). It needs *Settings › Actions › General › Allow GitHub Actions to create
and approve pull requests*.

## AI-assisted drafts (owner only)

Commit a `.txt`, `.md` or `.docx` file, then run **Actions › AI draft (unreviewed)**. It runs `scripts/ai_draft.py`
and opens a draft pull request with `data/drafts/<date>-<title>.json`. Title, source, date and licence are optional.
Set it up once: add the repository secret `NETRA_AI_KEY` (optionally the variables `NETRA_AI_PROVIDER`,
`NETRA_AI_MODEL`, `NETRA_AI_BASE`), and turn on *Settings › Actions › General › Allow GitHub Actions to create and
approve pull requests*. Never put a key in the repository or the page.

Safeguards: every quote must appear word for word in the source (and on the stated page), or it is removed;
sentences that read as a legal conclusion, an accusation or a review claim are removed; suggestions that do not match
NETRA's own lists of risk areas, laws and bodies are dropped; and the build refuses any draft marked reviewed.
The instructions and safeguard rules live in `scripts/ai_prompts.json`.

## Sources and credits

Every outside source and its licence is listed on the site under **About › Sources and credits**, in reports, and in
[LICENSE-DATA.md](LICENSE-DATA.md). In short:

- **MIT AI Risk Repository** taxonomies (CC BY 4.0, with attribution). NETRA is not affiliated with or endorsed by MIT.
- **Indian government documents, laws and court orders**, linked to official copies where available.
- **News and legal reporting**, linked only; short facts, no copied text.
- **MITRE ATLAS** case studies (Apache 2.0, © MITRE). **METR** reports are cited and summarised only.
- **GDELT Project**, PIB, METR and MITRE ATLAS feeds for the weekly update.
- **pdf.js** (Apache 2.0, Mozilla) for reading PDFs in the browser. Google Fonts: Newsreader, IBM Plex Sans and Mono,
  Noto Serif Devanagari (SIL OFL 1.1).

## Planned for v0.3

Live reporting (only with a safe, agreed route), an MIT AI Risk Repository import, further sources (Epoch AI, AVID,
OWASP, system cards, UK AISI, CERT-In, Indian-language news) and record-quality work. The full list is in
[docs/roadmap.md](docs/roadmap.md) and on the site under **About › Method**.

## Documents

| File | What it covers |
|---|---|
| [CHANGELOG.md](CHANGELOG.md) | Every change, phase by phase |
| [docs/weekly-method.md](docs/weekly-method.md) | How the weekly update chooses items, and its limits |
| [docs/model-sources.md](docs/model-sources.md) | Model-testing sources and their reuse terms |
| [docs/authorities-plan.md](docs/authorities-plan.md) | How the Who to approach directory is organised |
| [docs/mit-tool-mapping.md](docs/mit-tool-mapping.md) | How NETRA relates to the MIT taxonomies |
| [docs/roadmap.md](docs/roadmap.md) | Planned for v0.3 |
| [LICENSE-DATA.md](LICENSE-DATA.md) | Data licence and third-party terms |

## Version tags

`v0.1.0-pilot` is frozen and never edited. Tag `v0.2.0` on `main` once this release is merged (the maintainer does
this; GitHub's Zenodo integration can then archive it with a DOI).
