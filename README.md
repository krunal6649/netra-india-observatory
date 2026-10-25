# NETRA India AI Risk Observatory

**🔗 Live site: https://krunal6649.github.io/netra-india-observatory/**  ·  Pilot v0.1 (open data, open code)

An open, India-focused map of AI risks, real incidents and the laws that apply to them. For each incident it shows what happened, which laws may apply, which authority could act, and what is still unknown, using NETRA, a 14-stage method for analysing AI harm.

![NETRA India AI Risk Observatory](docs/screens/netra-hero.png)

## Who it is for
- **Lawyers and policy researchers:** find incidents, laws and gaps in one place, each with a source link.
- **Journalists and civil society:** see how deepfakes, voice cloning, fake citations and automated decisions map to Indian law.
- **Government bodies and regulators:** see where complaints currently have no clear authority, and tell us what is wrong or missing.

## Start here (three minutes)
1. Open the [live site](https://krunal6649.github.io/netra-india-observatory/) and look at the **risk wheel** on the home page.
2. Click any risk area to see India's related **incidents, laws and gaps** side by side.
3. Open an incident and read its **NETRA dossier**: location, applicable law, authority, and "what NETRA does not know".

## What is in it (pilot v0.1)
18 risks quoted from government frameworks · 12 documented Indian incidents · 28 laws, rules, advisories and court orders · 28 mitigation measures · 10 reporting authorities · 6 legal and policy gaps.

> **Status:** an independent research project. **Not legal advice.** All codings were drafted with AI assistance and are marked *unreviewed* until a person checks them. 24 legal items are still being verified against official texts (see CHANGELOG).

**Feedback:** corrections and suggestions are welcome through [GitHub Issues](https://github.com/krunal6649/netra-india-observatory/issues).

**Cite as:** see `CITATION.cff`. Data: CC BY 4.0. Code: MIT. Risk taxonomies adapted from the MIT AI Risk Repository (CC BY 4.0), with credit; this project is not affiliated with MIT.

## The tools

| Tool | MIT equivalent | What the India version holds now |
|---|---|---|
| Overview | Home page | Counts and a coverage table showing where incidents exist without binding law |
| Navigator | AI Risk Navigator | Pick any of the 24 risk areas and see India’s risks, incidents, laws, measures and gaps together |
| Risk repository | AI Risk Repository | 18 risks quoted from MeitY’s 2025 AI Governance Guidelines and NITI Aayog’s Responsible AI Part 1 |
| Incident tracker | AI Incident Tracker | 12 documented India incidents (deepfakes, voice cloning, fake citations, welfare algorithm, copyright) |
| Governance map | AI Governance map | 28 Indian statutes, rules, advisories, policy papers, standards and court orders |
| Mitigations | AI Risk Mitigations | 28 required or recommended measures, sorted into MIT’s 23 mitigation types |
| NETRA pipeline | *(new)* | Every incident run through the 14 NETRA stages: location and jurisdiction, legal issues (T1), authority routing, gaps (T2–T3), unknowns and overclaim check |
| Gap register | *(new)* | 6 gaps, each tied to incidents and instruments |
| Global evidence | *(new)* | The three METR reports from the earlier pilot, mapped to Indian law |
| Expert survey | Priority Risks survey | A live survey for Indian practitioners; results only from real answers |
| Method & sources | About | What was read, what is verified, and the verification to-do list |

## How the survey works

- **Anyone can take part.** Signed-in Contributors save answers directly. Everyone else (outside peers, public-link visitors, signed-out readers) clicks "Get my response code" and sends you the short code by email, WhatsApp or any message.
- **You import codes** in the owner-only box on the Survey tab. Paste one or many at once; the same code imported twice counts once. Codes are checked, and anything with invalid values is rejected.
- Codes contain only survey answers, never a name or account.
- Nobody but you sees individual answers. Results go public only when you press "Publish aggregate", and show only once 5+ people have answered with consent.

## Run it on your own computer

Needs Python 3 only.

```
cd netra-india
python3 scripts/build.py          # checks data, writes dist/index.html
python3 -m unittest discover tests
node tests/smoke.js               # optional, needs Node.js
```

Open `dist/index.html` by double-clicking. Everything works offline except the survey, which needs the published version.

## Adding data

Edit `data/india.json` (incidents, instruments, risks, mitigations, gaps) and run the build. The build refuses:

- a risk without a verbatim quote and location
- an incident without an overclaim check and a "what we do not know" list
- NETRA stage 11 (human review) marked done on an unreviewed record
- unknown risk areas, sectors, instruments or authorities, and non-https sources
- a verification status other than yes / partial / no, or "yes" on a site home page instead of a specific document
- malformed Act numbers ("Act 45 of 2023"), Gazette notification numbers ("G.S.R. 139(E)", "S.O. 2351(E)"), dates, or case entries missing a citation, court, date, holding or verification note

`data/taxonomy.json` holds MIT’s taxonomies (keep the attribution line). `data/global_evidence.json` is the earlier METR pilot.

## Verification to-do

1. Read official texts for every instrument marked "verify" (24 warnings in the build output; each note says what is missing).
2. Read the PSA white paper in full — it proposes a national AI incident database, which overlaps this project.
3. Capture primary evidence (court orders, public FIR details, platform notices) for each NETRA dossier.
4. Add risks from RBI FREE-AI recommendations 15–26, ICMR and SEBI.
5. Have a second coder check taxonomy and severity codes.
6. Check stage names against the NETRA v0.3 core workbook.
