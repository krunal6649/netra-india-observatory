# Changelog

## v0.2-dev (unreleased) — Phase 2: cleaner look and navigation
- **Dark mode by default.** A Light mode button (top right) remains, and printing always uses the light colours.
- **Title:** "नेत्र" with the eye icon, plus "India AI Risk Observatory". No other Devanagari on the site (checked by the smoke test).
- **11 tabs replaced by 4:** Home, Explore, Analysis, About.
  - Explore: one searchable list with a Risks / Incidents / Laws / Measures switch, and one Filters button that hides the
    filters until clicked. Timelines moved into "Show timeline". The risk wheel still opens a single risk area.
  - Analysis: NETRA dossiers, Gap register, Report generator and Model register. The last two are marked "Not built yet".
  - About: Method, Sources and credits (new), Verification status (new), Expert survey, Global evidence.
- **Home:** headline, then one "cases tracked" counter computed from the data (reviewed and unreviewed, with the data
  update date from the new `meta.updated` field). The separate risks, incidents, laws, measures and gaps stat boxes
  are gone. The wheel's centre now shows the 24 risk areas, so the case count appears only once.
- One-line explanation under every heading (checked by the smoke test). Guided tour (5 steps) and Credits buttons.
- **Old links still work:** `#navigator`, `#risks`, `#incidents`, `#governance`, `#mitigations`, `#netra`, `#gaps`,
  `#evidence`, `#survey` and `#about` open the matching new page. New pages have their own links, e.g. `#explore-laws`.
- Law cards now show the Phase 1 fields: Act number, Gazette notifications, court decisions with their own
  verification label, Gazette copy link and date checked.
- **Suggest a correction:** GitHub issue form (`.github/ISSUE_TEMPLATE/correction.yml`) asking only for a public source
  link, date and place; linked in the footer, on About and on each incident and law record. Not for live incident
  reporting; nothing changes until the maintainer reviews it.
- Credits line on Analysis pages and Global evidence; README, link-preview image (`og-image.png`) and README
  screenshot (`netra-hero.png`) updated. `netra-x-16x9.png` and `netra-timeline.png` still show the v0.1 look.
- **Maintainer and contact** box at the top of About › Method (name, title, email, corrections, GitHub), the same
  details under Sources and credits, and a "Contact the maintainer" link in the footer. Email stored as `meta.contact_email`.
- Build: `meta.updated` must be an ISO date and `meta.contact_email` a plain email address. Smoke test rewritten for
  the new pages (79 checks); 2 new unit tests.

## v0.2-dev (unreleased) — Phase 1: verification (data only)
- **Verified (owner checked against the India Code PDF):** G-BNS (Act 45 of 2023; ss.77, 308, 318, 319, 335, 336,
  340, 351, 353, 356) and G-BSA (Act 47 of 2023; ss.61–63; Schedule certificate Parts A and B with hash value).
  The AI-assisted session could not open India Code itself (host blocked), so these rest on the owner's check.
- **G-BSA case added, not verified:** Pune Bar Assn. v. Union of India, 2026 SCC OnLine SC 1297 (22 May 2026),
  upholding s.63(4). Read only through a news report; judgment not read.
- **Still partial, with what is missing stated in each note:**
  G-ITR21 (G.S.R. 139(E) of 25 Feb 2021; r.3(1)(b) replaced by G.S.R. 794(E) of 28 Oct 2022; home-page URL
  replaced by a Gazette-layout copy that has not been opened yet) ·
  G-ITA (s.79A added; s.43A in force until DPDP s.44(2) commences on 13 May 2027) ·
  G-CPA (upgraded from no: Act 35 of 2019, assent 9 Aug 2019, in force 20 Jul 2020 by S.O. 2351(E);
  ss.2(18), 2(28), 2(34), 2(47), 10, 21) ·
  G-ITR26 (G.S.R. 120(E), notified 10 Feb 2026, in force 20 Feb 2026; takedown 36h to 3h on court or government
  order; 2-hour deadline for intimate-image deepfakes; grievances 15 to 7 days; draft Second Amendment pending) ·
  G-DPDP (G.S.R. 843(E)) and G-DPDPR (G.S.R. 846(E)) with the eGazette link
- Verification warnings: 26 → 24
- Build now rejects bad verification values, "verified" records that point at a home page, and malformed Act
  numbers, Gazette notification numbers, dates and case entries. 7 new unit tests.
- New instrument fields (`act_no`, `notifications`, `cases`, `gazette_url`, `checked`) are stored in the data but
  not yet shown on the site; that comes with the Phase 2 redesign.

## v0.1.1 — 2026-10-23 (bug fix)
- Tool tabs no longer hide the last tab on laptop screens: they wrap on wide screens and scroll with a fade hint on phones
- 'Method & sources' tab shortened to 'Method'
- Link previews: Open Graph and Twitter card tags plus a 1200×627 preview image, so LinkedIn and X show a picture
- No data changes. v0.1.0-pilot remains the frozen reference.

## v0.1.0-pilot — 2026-10-22 (frozen)
First public pilot. Kept unchanged as the reference version.

- 11 tools: Overview (risk iris), Navigator, Risk repository, Incident tracker, Governance map, Mitigations,
  NETRA pipeline, Gap register, Global evidence, Expert survey, Method & sources
- Data: 18 risks (MeitY 2025 Guidelines, NITI Aayog RAI Part 1), 12 India incidents, 28 instruments,
  28 mitigations, 10 reporting authorities, 6 gaps, 3 METR reports mapped to Indian law
- Survey: signed-in contributors save directly; anyone else submits a response code the owner imports
- Validator refuses unsafe records (e.g. human review marked done on an unreviewed record)
- Known limits: all codings unreviewed; 26 items rest on secondary sources (see build warnings)

## Planned for v0.2
1. **Report generator** — Report tab (incident, AI model, legal event, risk area, overall India summary) plus
   "Generate report" buttons on incidents, dossiers and risk areas; NETRA structure with a NIST AI RMF
   (Govern / Map / Measure / Manage) section; optional AI-drafted narrative labelled for review; download or copy
2. **Authorities explorer** — treemap: India → Union / State-UT → authority type → authority, with powers, laws,
   linked incidents and reporting routes. Covers **all 28 states and 8 UTs** and about 30 Union bodies.
   Per state/UT: police and cyber crime, High Court and legal aid, rights commissions (human rights, women,
   child rights, consumer), state IT department, state CERT, State Election Commission. Full list in
   `docs/authorities-plan.md`; built Union first, then states with incidents, then the rest
3. **MIT data import (CC BY 4.0)** — AI Risk Repository (1,700+ risks), Mitigations (831), Priority survey results
4. **Weekly incident sync** — AI Incident Database feed filtered for India links, with MIT incident codes; candidates
   arrive unreviewed via pull request
5. **AI model register** — one card per model (developer, release date, what was tested, by whom, results,
   known incidents, Indian law touched), linked to incidents and the report generator. Sources, checked for reuse
   terms on 2026-10-23 (details in `docs/model-sources.md`):
   - **Import:** Epoch AI benchmark data (CC BY 4.0; CSV or `epochai` client) for model list, release dates
     and scores · MITRE ATLAS (Apache 2.0; monthly YAML) for attack techniques and case studies ·
     AVID vulnerability database (MIT licence; GitHub `avidml/avid-db`) for model failure reports ·
     OWASP Top 10 for LLM Applications 2026 (CC BY-SA 4.0; kept in its own file with share-alike notice)
   - **Cite and summarise only (no bulk copy):** METR time-horizon results and reports (no licence on the
     data repo, so headline figures are quoted with a link; ask METR before importing run data) ·
     developer system and model cards (company copyright) · UK AI Security Institute reports (reuse terms
     not confirmed yet)
6. **Housekeeping** — verify the 26 flagged items against official texts; Zenodo DOI for the release

## Later (v0.3+)
- Indian Kanoon API, eGazette, Indian fact-checkers and PIB Fact Check as signals
- OECD AIM and AIAAIC as lead sources
- METR run-level data, if METR grants permission; UK AISI data once reuse terms are confirmed
