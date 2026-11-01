# Changelog

## Version 3 (in progress, branch `v3/verification-first`)

### Step 1: verification
- **Verification log:** [`docs/verification-v3.md`](docs/verification-v3.md) records what was checked, what could not
  be opened, and what is still missing for each record.
- **Laws:** after network access was widened, 6 of the 24 partly verified records were checked against official texts
  and upgraded to verified, each with the source link and what was checked: G-PSA-WP, G-AISI, G-NITI2, G-RBI, G-ICMR
  and G-J-ANIL.
  - Corrections made on the way: the PSA white paper's official title and date (2026-01-23); NITI Part 2's date to
    the month the cover gives (2021-08); the judge's name in the Anil Kapoor order (Prathiba).
  - G-J-ANI stays partly verified: the official orders confirm the judge, dates and that the suit continues, but not
    the judgment's holding.
  - **G-DPDPR verified** against the Gazette of 13 November 2025 (G.S.R. 846(E)), from a copy the maintainer supplied:
    Rule 1(2)-(4) phasing quoted exactly.
  - **G-DPDP verified** against the Gazette of 11 August 2023 (the Act, No. 22 of 2023) and the Gazette of
    13 November 2025, No. 757 (G.S.R. 843(E), the commencement notification). Its status now lists the three
    commencement stages as the notification states them. An earlier one-page summary of G.S.R. 843(E), without
    Gazette header or signature, was not relied on. The record's Gazette link pointed at the Rules file and was removed.
  - G-ITA's s.43A end date is now backed by G.S.R. 843(E); the rest of that record is still to check.
  - **G-CERTIN verified** against the CERT-In Directions of 28 April 2022 (6 hours, 180 days, effective after 60 days).
  - **G-ITR26 verified** against the Gazette of 10 February 2026 (G.S.R. 120(E), in force 20 February 2026). The summary
    was corrected: the 2-hour deadline covers complaints about intimate images or impersonation, including artificially
    morphed images, not only deepfakes.
  - **Partly verified, with checked text but no official link yet:**
    - **G-ITR21:** principal rules checked against the Gazette of 25 February 2021; the full amendment history (2022,
      2023, 2025) is taken from the note to G.S.R. 120(E).
    - **G-ADV-MAR24:** checked against MeitY's signed advisory of 15 March 2024. The unread comparison with the
      1 March version was removed from the summary.
    - **G-ITR21:** a consolidated text 'updated as on 28.10.2022' also confirms that G.S.R. 794(E) replaced rule
      3(1)(a) and (b).
  - **G-ITA verified** on the maintainer's confirmation that the consolidated copy came from meity.gov.in: all twelve
    sections listed, commencement 17 October 2000 (G.S.R. 788(E)), and the s.43A end date from G.S.R. 843(E).
  - **G-ADV-DEC23 verified** against PIB's official release of 26 December 2023 (Release ID 1990542), which quotes the
    advisory; the date was corrected from 23 to 26 December 2023.
  - **G-CCPA-DP verified** against the Gazette of 30 November 2023 (CCPA, F. No. CCPA-1/1/2023-CCPA-(Reg)). The summary
    now says that applying it to AI-personalised designs is NETRA's reading, since the guidelines do not mention AI.
  - **G-CPA:** Act text checked against the Gazette of 9 August 2019 (Act No. 35 of 2019). It stays partly verified until
    S.O. 2351(E), the commencement notification, is seen.
  - The other partly verified records stay as they were; the log names the site that could not be read for each. The Gazette server
    does not send its full certificate chain, and certificate checks were not switched off.
- **Model cards:**
  - The 8 tests that cite MITRE ATLAS were checked against ATLAS data release 2026.10, and the 7 that cite METR against
    METR's own report pages. All 15 summaries are supported.
  - The AML.CS0056 test date on MOD-11 now shows 2026, the precision ATLAS gives (maintainer's decision).
  - MOD-10's release date was removed and marked unverified: its source, a Substack post about ChatGPT, looks unrelated
    (maintainer's decision).
  - Still flagged: the cited ATLAS release, and release-date sources that could not be opened.
  - All 12 cards stay unreviewed.
- **All 13 upgrades confirmed by the maintainer, Krunal Maheshwari, on 2026-11-01.** Each record's note says so, and
  its `checked` date is 2026-11-01.
- Counts now read **17 verified, 11 partly verified** in the README, `CITATION.cff` and `.zenodo.json`. The test of
  build warnings now reads the count from the data.
- Removed mentions of a retired project from the stage note, the global-evidence note and the archived v0.1 page.
- Fixed `tests/test_release.py`, which had been failing on `main` since the README redesign: it now reads the figures
  from the new "At a glance" row and "Status and trust" table.

### Step 2: additive fields

- New optional `assessment` block on incidents. If it is absent, every field counts as "not yet assessed", so the other
  19 cases are unchanged. The block has its own `review` status, which starts as `unreviewed`. The incident's own review
  status does not carry over to it.
- Fields:
  - `ai_role` (confirmed, suspected, not established or not AI), with the source basis;
  - `ai_system` (name, developer, deployer, version);
  - `impact` (who was harmed, harm types, and scale only when a source gives it);
  - `evidence_provenance` (who produced the evidence, who reported it, what it establishes and what it does not);
  - `failure_modes` (OWASP LLM Top 10 with edition year, or MITRE ATLAS);
  - `crosswalk` (NIST AI RMF function, ISO/IEC 42001 or OWASP label, with a 'why').
- Trial cases:
  - IN-INC-20 Grok: AI role confirmed.
  - IN-INC-09 tax tribunal: AI role suspected; the AI system is "not established".
  - IN-INC-14 WotNot: AI role "not AI", from the record's own overclaim check. The owner decides whether the case stays
    in scope.
- No failure mode or crosswalk tags are set on the trial cases: none of their cited sources makes such a mapping.
- Reference lists, names only:
  - `data/owasp_llm_top10.json`: the 2025 and 2026 editions, CC BY-SA 4.0. The numbering differs between editions, so
    every tag carries its year.
  - `data/atlas_techniques.json`: 221 technique IDs from MITRE ATLAS release 2026.10, Apache 2.0, © MITRE.
- `scripts/build.py` adds `check_v3_fields`. It rejects:
  - unknown fields;
  - an AI role without a basis;
  - a failure-mode ID that is not an item of its edition;
  - a failure mode or scale whose source is not one of the incident's own sources;
  - a NIST label that is not Govern, Map, Measure or Manage;
  - a reviewed assessment without a reviewer and date.
- The dossier overview shows a folded "Version 3 assessment" panel on the three trial cases only.
- Tests: `tests/test_v3_fields.py` (13 tests) and three smoke checks.

- After the owner reviewed the trial (2026-11-01):
  - IN-INC-14 (WotNot) stays in NETRA. Its AI role changed from "not AI" to "not established": the case is AI-linked
    through the chatbot product, but the AI's part in the harm is not shown.
  - The assessment was extended to all 22 cases, from each record's own text and cited sources:
    - 12 confirmed (01, 02, 04, 05, 06, 07, 08, 15, 17, 18, 20, 22);
    - 7 suspected (03, 09, 10, 12, 13, 16, 19);
    - 3 not established (11, 14, 21).
    All are unreviewed.
  - Scale is filled only where a cited source gives a figure: cases 03, 11, 12, 14, 19 and 21. View counts, song counts
    and the POSHAN "nearly half" figure are not used as scale, and each such case says why.
  - No failure-mode or crosswalk tags are set yet.
- New page: About › Crosswalk. It explains:
  - the assessment fields;
  - NETRA's NIST AI RMF mapping, which is the same one the case report uses;
  - both OWASP editions side by side;
  - the MITRE ATLAS release;
  - why ISO/IEC 42001 clauses are not mapped (the text is not freely available).

### Deferred to Version 4
- Compare tab, replay standard, test-coverage gap view, and finance and elections sector work.

## v0.2.1-dev — framework page, accurate headline, full name
- **`docs/framework.md`**: the NETRA framework on one page: the 14 stages and their statuses, classification, the seven
  legal labels, review and verification rules, and a description of every dataset file. Linked from the README.
- Home headline now says binding law reaches AI harms **mostly** (not only) through general statutes. NETRA's own data
  includes the IT Rules Amendment, 2026, binding law aimed at synthetic content. Link-preview image and README
  screenshot retaken.
- Full name **Krunal Maheshwari** in the citation file (family name added), Zenodo metadata, data licence, README,
  maintainer line and the reviewer and checker fields of every record.

## v0.2.1-dev — This week in India placement; Whom to approach
- Home order is now: risk wheel, risk-area legend, **This week in India**, then **Whom to approach** (renamed from
  "Who to approach" on the site, tour, README and docs), then the coverage cards.
- Only parts with something in them are shown: no AI cards, Cyber watch or Model watch when empty, and no section
  at all for an empty week. No "nothing this week" wording.
- Subtitle shortened to "… picked automatically. Updated every Saturday." Cards keep the "Auto-selected,
  unreviewed" label.

## v0.2.1-dev — weekly update when GDELT is busy
- Third run (pull request #19, closed): GDELT answered 429 again, after three retries. The workflow now waits
  10 minutes and runs once more when GDELT did not answer.
- Each week records `news_ok`. When the news source failed, Home says "the news source did not answer this week …
  this does not mean nothing happened" instead of "no AI item met the selection rules".

## v0.2.1-dev — weekly selection tuned on the second real run
- Second run (pull request #17): GDELT answered (250 AI and 181 cyber articles) but only 1 AI item qualified, the
  SBI breach story appeared three times, and "hacked to death" was counted as cyber.
- GDELT's spaced punctuation is cleaned ("AI - generated" → "AI-generated", "3 . 75" → "3.75").
- A headline from an Indian outlet now counts as about India unless it names another country ("US" only in capitals).
- Same-story grouping also uses shared key words with figures and specific three-word phrases; phrases made only of
  topic words do not merge different stories.
- Cyber watch ignores violence ("hacked to death"); more harm words (fraudster, swindled, blackmail, morphing and others).
- 6 new unit tests built on invented headlines like the real ones.

## v0.2.1-dev — first weekly run, fixes
- First real run of the weekly update (2026-10-25, pull request #15): METR and MITRE ATLAS worked; GDELT answered
  429 (too many requests) and PIB answered 403 (forbidden) to GitHub's servers, so no news items were found.
- GDELT requests now wait 15 s between queries and retry after 20, 45 and 90 s on a 429, as GDELT's rate limit asks.
- PIB feeds switched off: NETRA does not work around a site that refuses automated access. Method, Credits and
  `scripts/weekly_sources.json` say so. Tests keep PIB feed reading covered with fixtures; new test for the retry.

## v0.2.0 — Phase 7: housekeeping and release files
- **`CITATION.cff` 0.2.0** with repository, site, contact and references (MIT AI Risk Repository, MITRE ATLAS), and a
  matching **`.zenodo.json`** for archiving a release with a DOI. The frozen tag `v0.1.0-pilot` is untouched.
- **README** brought up to date: v0.2 figures with review status, seven-step tour, Who to approach and This week in
  India, contact, how to cite, Sources and credits, Planned for v0.3, a table of documents, and version-tag notes.
- **`docs/roadmap.md`: Planned for v0.3**: live reporting (only with a safe, agreed route), MIT AI Risk Repository
  import, further sources (Epoch AI, AVID, OWASP, system cards, UK AISI, CERT-In, Indian-language news) and
  record-quality work. The old README verification to-do list moved here.
- **About › Method** now shows "Planned for v0.3", with counts computed from the data. Link-preview text updated
  (22 incidents, 391 bodies, 12 model cards, v0.2).
- `LICENSE-DATA.md` covers every data file, including the weekly update and its GDELT credit; `docs/model-sources.md`
  has a status note after Phase 6.
- Tests: `tests/test_release.py` (6 tests) checks that the citation and Zenodo files agree, that the README and
  citation figures match the data, and that every linked document exists; 2 new smoke checks.

### v0.2 in one paragraph
Phases 1–7: law records verified where possible and labelled where not (1); new look and navigation (2); a
Who to approach directory of 391 bodies on an India tile map (3); a report generator with no AI (4); Models and
evaluations with Add a report and the NETRA check (5); a weekly, auto-selected and unreviewed update (6); release
files and documentation (7).

## v0.2-dev (unreleased) — Phase 6: This week in India
- **`scripts/weekly_top5.py`** (standard library, no AI, no key): up to five AI incidents in India from the past seven
  days, a separate **Cyber watch** (never counted as AI) and a **Model watch** (new MITRE ATLAS case studies and METR
  publications). Stories already in NETRA or in an earlier week are left out; fewer than five are shown if fewer
  qualify. NETRA's own summaries; headlines only as link titles; no article text stored.
- Sources in `scripts/weekly_sources.json`: GDELT DOC 2.0 API, PIB press-release RSS, METR RSS, MITRE ATLAS data on
  GitHub. CERT-In is off until an official feed address is confirmed. Each run reports which sources answered.
- **`.github/workflows/weekly.yml`**: every Saturday at 00:00 IST, opens a pull request; never merges.
- **Home: "This week in India"**, with cards labelled "Auto-selected, unreviewed", Cyber watch, Model watch, source
  status, earlier weeks and the GDELT credit. Credits page lists the weekly sources.
- Build validates `data/weekly.json` (at most 5, unreviewed, short own summary, source links, no article text, cyber
  kept apart). `docs/weekly-method.md` explains the rules and limits. Tests: 11 new unit tests with fixture feeds.
- Label `report-suggestion` created for the "Send to NETRA for review" form.

## v0.2-dev (unreleased) — Phase 5 changes after owner feedback
- **Add a report no longer asks visitors for an API key.** The provider, model and key boxes and all browser AI calls
  are removed. Instead the **NETRA check** runs in the browser: keyword matching against the new
  `data/check_terms.json` (NETRA's own lists; validated by the build), showing risk areas with word-for-word passages
  and page numbers, Indian laws named in the report, laws linked in NETRA to the top risk areas (possible only), who
  could act, related gaps and similar India cases. Labelled auto-matched and unreviewed; not an AI, not a legal analysis.
- **Send to NETRA for review**: opens the new `.github/ISSUE_TEMPLATE/report.yml` form prefilled with the title, link
  and check summary (never the file), or an email. AI drafting stays owner-only through the GitHub workflow.
- **Choose file** is a styled button; the file is read as soon as it is chosen and is no longer lost when the form
  redraws. Title, source, date and licence are optional in the page, the script and the workflow.
- **Global evidence moved** from About into Analysis › **Models and evaluations** (formerly Model register), as the
  "By evaluation report" view next to "By model"; a Home card and a tour step point to it. Old `#evidence` and
  `#about-evidence` links open it.
- Fixed a 1-pixel horizontal scroll on phones in two-column forms.

## v0.2-dev (unreleased) — Phase 5: model register and report upload
- **`data/models.json`: 12 model cards** (all unreviewed): GPT-5.6 Sol, HPIM (OpenAI internal), Claude Opus 4.6,
  o3, Claude Opus 4, DeepSeek-R1, Gemini 2.5 Pro (preview), ChatGPT, Gemini (formerly Bard), Microsoft 365 Copilot and
  Copilot Studio, Claude computer use, Grok. Built from the three METR reports already in global evidence (cite and
  summarise only) and eight MITRE ATLAS v5.6.0 case studies (Apache 2.0), linked to India cases IN-INC-05, 08 and 20.
  Release dates only where a cited source gave one; otherwise "not recorded yet".
- Each card keeps **"What the testers found"** apart from **"NETRA's India analysis"** (risk areas, laws labelled
  possible / interpretive question / gap, bodies from the directory, gaps, unknowns, overclaim check saying a test
  result is not evidence of real-world harm).
- **Model reports** in the report generator: Part A "What METR found" (or "What the testers found"), Part B "NETRA's
  India analysis", plus the usual evidence, NIST and review sections.
- **Add a report** (Model register and Report generator): PDF (pdf.js from cdnjs, loaded only for PDFs), Word (.docx,
  read with the browser's own unzip), text or Markdown, read in the browser only. The file is read as soon as it is chosen; title, source, date and
  licence are optional, and anything filled in is checked.
- **AI-assisted Extract, Triage, Draft** with the visitor's own key (Anthropic, or any OpenAI-compatible service),
  after a disclosure that the document leaves the browser; key held in memory only. **Owner-only option:**
  `scripts/ai_draft.py` (standard library) and `.github/workflows/ai-draft.yml`, which opens an unreviewed draft pull
  request. Shared rules in `scripts/ai_prompts.json`.
- **Safeguards:** quotes not found word for word (or not on the stated page) are removed and listed; sentences that
  read as legal conclusions, accusations or review claims are removed; unknown ids are dropped; drafts are always
  "unreviewed"; the build rejects drafts marked reviewed or with unverified quotes.
- Build validates models (links to incidents, laws, bodies, reports, mappings, gaps; release source; overclaim;
  review). Tests: 55 unit tests (13 for the AI draft script, 6 for models), 127 smoke checks, plus a browser test of the
  full upload and AI flow against a fake provider.

## v0.2-dev (unreleased) — Directory links confirmed; tile map wording
- **26 more directory links confirmed by the project owner** on 2026-10-25. All 32 bodies with a link are now verified
  (MeitY, IndiaAI, MIB, Copyright Office, Sanchar Saathi, NALSA, NHRC, NCW, NCPCR, NCDRC, National Consumer Helpline,
  RBI, SEBI, IRDAI, TRAI, CCI, ICMR, BIS, TEC; Delhi, Karnataka, Telangana and Andhra Pradesh High Courts; Delhi,
  Kerala and Karnataka Police; plus the six checked earlier). 359 bodies still have no link and stay "to verify".
- **Tile map kept as it is.** The map and `docs/authorities-plan.md` now state that it shows all 28 states and 8 UTs of
  India, including Jammu and Kashmir, Ladakh and Arunachal Pradesh.

## v0.2-dev (unreleased) — Directory links checked by the owner
- **PIB Fact Check** now links to https://www.pib.gov.in/index.aspx?reg=48&lang=2, opened by the project owner on
  2026-10-25, and is verified.
- **Links removed** because they did not open for the owner on 2026-10-25: NCIIPC (nciipc.gov.in), CDSCO
  (cdsco.gov.in), Kerala High Court (hckerala.gov.in), Bombay High Court (bombayhighcourt.nic.in). Each entry says so
  and stays "to verify" until a working official address is found.

## v0.2-dev (unreleased) — Phase 3 (a): Who to approach directory
- **New `data/authorities.json`: 391 bodies.** 31 Union bodies in the plan's groups (ministries and policy, cyber
  security, platforms and data, courts and legal aid, rights commissions, elections, sector regulators, standards,
  fact-checking), and 10 standard bodies for each of the 28 states and 8 UTs (police and cyber crime, High Court, State
  Legal Services Authority, human rights, women's, child rights and consumer commissions, IT department, state CERT,
  State Election Commission). High Court names come from `docs/authorities-plan.md`.
- **Verification:** 5 bodies are checked by the project owner (NCRP / 1930, GAC, CERT-In, ECI, Supreme Court). 9 have
  links that appeared on official domains in web search (partial). Everything else is "to verify", with a visible
  label; 355 have no link yet rather than a guessed one. The Union and the six states and UTs in cases come first.
- **Home › Who to approach:** drill-down in four steps (Level → Authority → Bodies → body page) with a step indicator,
  breadcrumb and "Back to treemap". Union groups and each place's bodies are squarified treemaps; the 36 states and
  UTs are a grid in alphabetical order. Bodies are coloured by role (enforces, adjudicates, regulates or sets policy,
  supports victims); hovering shows a small card. No case counts are shown, and places are not coloured by cases.
- Each body page: what it can do, laws it may apply, how to report (with phone numbers such as 1930, 14490, 15100,
  1915 where found), official website, date checked, status and source, and a correction link.
- A note puts **1930 / cybercrime.gov.in first for financial cyber fraud** and says what NETRA adds.
- **Tile map for states and UTs:** one square each, placed roughly where it lies in India, coloured by region (North,
  Central, East, North-East, West, South); union territories have a dashed edge and the six places in cases a dot.
  No boundaries are drawn: the authorities plan rules out map boundaries, and official boundary depictions are
  sensitive. Region colours group nearby places and are not official zones.
- Union groups each have their own colour and list their first bodies; treemaps are shorter; empty hover cards fixed.
- Home: removed "Three ways in", which repeated the tabs. The guided tour has a new "Who to approach" step.
- Dossiers: each "Where to report" route has **Open in directory**.
- Build: validates the directory (roles, places, groups, laws, links, verification) and checks that every case's
  reporting route resolves to a body, including state routes such as "Kerala police". 7 new unit tests, 8 new smoke
  checks (all 391 body pages render; treemap tiles fill the box without overlap; no case counts).

## v0.2-dev (unreleased) — Shorter NETRA dossier
- **One case at a time.** The 14-column table of every case no longer sits above the dossier. A **Choose a case**
  drop-down and **Newer / Older** buttons switch cases; "All cases in Explore" goes back to the list.
- **Stage strip:** the 14 NETRA stages collapse into one coloured strip ("7 of 13 done"); click it for the full
  stage-by-stage view.
- **Four tabs:** Overview (what happened, AI's role, what NETRA does not know, overclaim check) · Laws and gaps ·
  Where to report (authorities, 1930 first for financial fraud, location and jurisdiction, court documents) ·
  Evidence (sources and court documents).
- **"Compare all cases by stage"** keeps the old all-cases table, folded away at the bottom.
- **Authorities:** the red "to verify" on every line is replaced by one note above the list and a grey
  "not yet checked" tag. None of the 10 contact routes has been checked against an official site yet.
- The long NETRA method paragraph is no longer repeated here; it remains under About › Method.
- **5 contact routes checked by the project owner on 2026-10-25** and now verified: National Cyber Crime Reporting
  Portal / 1930, Grievance Appellate Committee, CERT-In, Election Commission of India, Supreme Court of India. Their
  "not yet checked" tags are gone.
- **A-COURT** now links to India Code at https://indiacode.gov.in/home (owner's request); it should become each High
  Court's own site in Phase 3. Platform grievance officer, Data Protection Board, state police and sector regulator
  stay "not yet checked" until Phase 3 gives them the right pages.
- Build: an authority marked verified must name who checked it and when; authority links must be https. 2 new unit tests.
- Smoke test: 5 new checks; 104 in total.

## v0.2-dev (unreleased) — Easier Explore for a growing database
- **Compact list** for incidents and laws: one line per record (ID, title, date and place, risk-area dots, severity,
  review or verification status). Click a line to expand a summary with Open dossier and Generate report.
  A **List / Cards** switch keeps the full cards.
- **Sort:** incidents by newest, oldest, most severe, recently added or state; laws by newest, oldest, title or least
  verified first.
- **New incident filters:** state or UT, year, review status (reviewed / unreviewed).
- **Active-filter chips** above the list, each removable with ×, plus Clear all.
- **20 records at a time** with "Show N more", so long lists stay fast. Timeline dots and law links still find records
  beyond the first page.
- **State or UT filter lists all 28 states and 8 union territories** (plus "National or several states"), each with
  its case count, so places with no case yet can still be chosen. The names are stored once in `data/india.json`
  (`states_uts`) for the Phase 3 treemap, match `docs/authorities-plan.md`, and the build rejects a case whose place
  does not start with one of them.
- **Home banner:** removed the "Explore the cases" and "Guided tour" buttons, which repeated the header and tabs.
- **Batch 2 (IN-INC-13 to 22) human-reviewed** by the project owner on 2026-10-25. Home now reads "22 cases tracked ·
  22 reviewed by a person · 0 unreviewed".
- Smoke test: 10 new checks (paging, sorting, filters, all states listed, chips, cards view, law rows, banner);
  99 in total. 2 new unit tests.

## v0.2-dev (unreleased) — Phase 4: report generator
- **Generate report** button on every NETRA dossier, incident card and risk-area page, plus a working
  Analysis › Report generator page (record type and record pickers). Model reports come with Phase 5.
- Reports are **built in the browser from stored data, with no AI**: preview, **Copy report**, **Download Markdown**
  (`netra-report-incident-IN-INC-12.md`) and **Print or save as PDF** (print view hides menus and controls).
- Sections: 1 What happened · 2 Evidence and how to preserve it (sources, court documents, general preservation
  steps, SHA-256 commands, BSA s.63(4) certificate Part A / Part B with hash value from the verified G-BSA record, the
  Pune Bar Assn. case flagged as report-only) · 3 AI's role · 4 Laws that may apply, labelled **Possible**,
  **Interpretive question** or **Gap** · 5 Authority to approach (with the 1930 / cybercrime.gov.in first step for
  financial fraud) · 6 What NETRA does not know · 7 Overclaim check · 8 NIST AI RMF view (Govern, Map, Measure, Manage;
  NETRA's mapping, unreviewed) · 9 Cyber AI Profile: focus-area tag (Secure / Thwart; Defend never auto-tagged) and an
  evidence checklist for CSF 2.0 RS.AN-03, RS.AN-06, RS.AN-07 · 10 Sources and credits · 11 Review status (of the
  record, and a note that the report itself is unreviewed) · "Not legal advice".
- The Cyber AI Profile is cited as **NIST IR 8596, preliminary draft (iprd), December 2025**. NIST text is paraphrased,
  not quoted; the RS.AN wording was checked only against secondary summaries.
- Smoke test: every incident (22) and every risk area (24) report has all required sections and no blank values;
  court links with brackets survive; the renderer escapes HTML and refuses non-https links (89 checks).

## v0.2-dev (unreleased) — Batch 2: ten more cases
- **10 new incidents (IN-INC-13 to IN-INC-22), all unreviewed**, chosen to cover risk areas with few or no cases.
  Each has at least two sources, NETRA stages, unknowns and an overclaim check. Batch is marked `B2`, and the Method
  page says the batch was chosen for coverage, so counts do not show how common each harm is.
  - Privacy & Security: Hyderabad police facial recognition challenge (Telangana HC) · WotNot chatbot file leak
    (Gujarat) · CERT-In alert on AI agents reaching live systems
  - Discrimination & toxicity: AI-generated explicit images of an Assam woman · Grok's Hindi abuse
  - AI system failures: POSHAN Tracker face recognition denying rations · Bengaluru AI traffic camera wrong fines ·
    Haryana family-ID system marking pensioners dead
  - Overreliance: Bombay HC quashes tax order built on non-existent judgments (KMG Wires)
  - Misinformation: Army Chief deepfake after Operation Sindoor
- Cases by risk domain (old → new): 1: 3→7 · 2: 0→5 · 3: 4→6 · 4: 7→10 · 5: 2→4 · 6: 3→4 · 7: 1→6
- Home now reads "22 cases tracked · 12 reviewed by a person · 10 unreviewed".
- **Duplicate check:** the build now rejects a case that cites the same source or court document as an existing
  case (ignoring `www.`, `/amp/` and trailing slashes), or whose title is 75% or more alike, unless a person lists it
  in `distinct_from`. The current 22 cases pass; the closest pair (IN-INC-09 and IN-INC-19) is 54% alike and is two
  different cases. 4 new unit tests.
- **IN-INC-19 (KMG Wires) expanded** from sources supplied by the owner: AY 2023-24, ss.143(3) r/w 144B, about ₹22 crore
  demand, penalty notice under s.274 r/w s.271AAC, suppliers' s.133(6) replies ignored, bench Colabawalla and
  Amit S. Jamsandekar JJ. AI involvement stays 'as reported': summaries differ on whether the court itself found the
  citations AI-generated, and the order has not been read. Case cards now show a `notes` line where present.
- Build: `batch` must look like `B2`. 1 new unit test checks batch 2 is unreviewed, sourced, and covers all 7 domains.

## v0.2-dev (unreleased) — Owner review and court documents
- **All 12 incidents human-reviewed** by the project owner on 2026-10-25, who reported that all looked correct.
  Each record now stores `reviewed_by` and `reviewed_on`, and NETRA stage 11 (Human review) is done. Home now reads
  "12 reviewed by a person · 0 unreviewed".
- **Official court documents** under Location & jurisdiction in each dossier. Only links on a court's own website
  count as official. Found by web search, then opened and checked by the project owner on 2026-10-25:
  IN-INC-02 Delhi High Court order of 20 Sep 2023 in CS(COMM) 652/2023 · IN-INC-08 Delhi High Court order of
  27 Jul 2026 in CS(COMM) 1028/2024. A document shown as checked must name who checked it and when.
  Cases with no document located say so. Petitions filed by parties are usually
  not published by Indian courts, so none are listed.
- Build: a reviewed case needs a reviewer, an ISO review date and S11 done; reviewer fields on an unreviewed case,
  and court documents marked official but not on a .nic.in or .gov.in site, fail the build. 4 new unit tests,
  82 smoke checks.

## v0.2-dev (unreleased) — Phase 2: cleaner look and navigation
- **Dark mode by default.** A sun / moon icon at the top right, grouped with Guided tour and Credits, switches between
  night and day; printing always uses the day colours.
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
