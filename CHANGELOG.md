# Changelog

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
   linked incidents and reporting routes; Union and the 5 states with incidents first
3. **MIT data import (CC BY 4.0)** — AI Risk Repository (1,700+ risks), Mitigations (831), Priority survey results
4. **Weekly incident sync** — AI Incident Database feed filtered for India links, with MIT incident codes; candidates
   arrive unreviewed via pull request
5. **AI model register** — METR time-horizon results and evaluation reports, linked to incidents
6. **Housekeeping** — verify the 26 flagged items against official texts; Zenodo DOI for the release

## Later (v0.3+)
- Indian Kanoon API, eGazette, Indian fact-checkers and PIB Fact Check as signals
- OECD AIM and AIAAIC as lead sources
- Model system cards, UK AI Security Institute, MITRE ATLAS
- Remaining states' authorities
