# NETRA India AI Risk Observatory (pilot v0.1)

An India-focused counterpart to the MIT AI Risk Initiative’s tools, joined to the NETRA incident pipeline. It is an independent research project. It reuses MIT’s **taxonomies** under CC BY 4.0 with credit, and does not copy MIT’s name, logo, design, text or code.

**Not legal advice.** All codings were drafted with AI assistance and are unreviewed.

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

`data/taxonomy.json` holds MIT’s taxonomies (keep the attribution line). `data/global_evidence.json` is the earlier METR pilot.

## Verification to-do

1. Read official texts for every instrument marked "verify" (26 warnings in the build output).
2. Read the PSA white paper in full — it proposes a national AI incident database, which overlaps this project.
3. Capture primary evidence (court orders, public FIR details, platform notices) for each NETRA dossier.
4. Add risks from RBI FREE-AI recommendations 15–26, ICMR and SEBI.
5. Have a second coder check taxonomy and severity codes.
6. Check stage names against the NETRA v0.3 core workbook.
