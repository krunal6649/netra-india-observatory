# NETRA: notes for Claude Code sessions

Read this first. It holds the project's standing rules and where the work stands, so a new session can continue
without the earlier conversation. Last updated 2026-11-01, after release v0.3.1 (Version 3).

## The project

- NETRA (नेत्र) India AI Risk Observatory: an open record of AI-linked harms in India, the Indian laws that may apply,
  and the authorities that can act. Live site: https://krunal6649.github.io/netra-india-observatory/ (GitHub Pages
  from `main`).
- Maintainer: Krunal Maheshwari, Advocate (Bar Council of Gujarat), ORCID 0009-0009-3832-731X. Always write the full
  name "Krunal Maheshwari" in reports. Use they/them unless pronouns are given.
- Dataset DOI (v0.3.1): 10.5281/zenodo.23864343; all versions: 10.5281/zenodo.23864342. Working paper:
  10.5281/zenodo.23865186. Zenodo archives every GitHub release automatically.
- Data CC BY 4.0, code MIT. Research material, not legal advice.

## How to work

- **Never push to `main`.** Work on a new branch, open a pull request, and let the maintainer merge. Tags and releases
  are made by the maintainer on GitHub.
- After every batch of changes, run all three and report the real results:
  `python3 scripts/build.py` · `python3 -m unittest discover tests` · `node tests/smoke.js`.
  Do not chain them with `&&` behind `tail`; check each exit status.
- Small commits with clear messages; record changes in `CHANGELOG.md`.
- The page is one file: `web/template.html`. `scripts/build.py` validates `data/*.json` and writes `dist/index.html`
  and the root `index.html`. Standard-library Python only; a static page; no API key in the repo or the page.

## Standing rules (from the maintainer)

- **Scope:** AI-linked cases only. Do not add cases where AI's role is not established at all (for example a bank
  data leak or a crypto hack with no AI element). A case where an AI product is the setting but its part is unproven
  can stay, marked "not established" (IN-INC-14 WotNot was kept this way by the maintainer).
- **Never invent** citations, dates, section numbers, notification numbers, case names or quotes. If something cannot
  be checked against a primary or official source, mark it unverified and say what is missing.
- Keep confirmed obligations, potential obligations, interpretive questions, gaps and reforms separate.
- Every new or imported record starts `unreviewed`. Never mark anything reviewed unless the maintainer says so, and
  then record `reviewed_by` and the date.
- No in-house model testing or benchmarks: cite other evaluators only. A test abroad is never evidence of harm in India.
- Do not redesign the 14-stage method. New fields are additive and default to "not yet assessed".
- MIT taxonomies stay CC BY 4.0 with credit and no affiliation claim. Do not copy another project's code or branding.
- Do not mention the retired earlier project anywhere.
- Free sources only; respect licences; no scraping against a site's terms. Do not work around a site that refuses
  automated access (no headless browser to get past a bot check), and never disable TLS verification.
- Do not show "not yet checked by a person" sentences on the site; items stay flagged unreviewed in the data.

## Version 3 (v0.3.0 / v0.3.1): what exists

- 28 legal instruments: 17 verified against official texts, 11 partly verified (each note says what is missing).
- 22 incidents, all reviewed by the maintainer. Each has an `assessment` block (its own review status, all
  `unreviewed`): AI role (10 confirmed, 9 suspected, 3 not established), AI system, impact, evidence provenance,
  failure modes, crosswalk.
  - "Confirmed" needs an official body (police, a court, a government fact-check, the operator) to say AI was used.
    The maintainer checked the AI-role call for 01, 04, 06, 15, 16, 17 and 18.
  - Failure-mode tags only where AI's role is confirmed and a cited source describes the facts, each saying it is
    NETRA's reading: IN-INC-15 OWASP Excessive Agency (LLM06:2025, LLM03:2026); 01, 02, 04, 07, 16, 22 MITRE ATLAS
    AML.T0088 Generate Deepfakes. OWASP IDs always carry the edition year.
  - IN-INC-15 rests on CERT-In advisory CIAD-2026-0049, checked on cert-in.org.in.
- Reference lists: `data/owasp_llm_top10.json` (2025 and 2026, CC BY-SA, names only) and
  `data/atlas_techniques.json` (ATLAS 2026.10, Apache 2.0, names only).
- 12 model cards (`data/models.json`), all unreviewed. Release dates for 10 cards are checked against developer pages (2026-11-02); MOD-01 is press-only and MOD-02 is internal.
- About › Crosswalk page; Google Dataset Search description built into the page head from the data.
- Weekly update: `.github/workflows/weekly.yml`, Saturdays 00:00 IST, opens a PR. Items are candidates only;
  nothing becomes a case without the maintainer.

## Open items

1. Official links for the 11 partly verified laws: G-ITR21, G-ADV-MAR24 (MeitY), G-CPA (S.O. 2351(E)), G-J-ANI
   (judgment), G-COPY (India Code), G-DPIIT-WP, G-SEBI-CP, G-TEC, G-ECI-24, G-ECI-25, G-J-ARIJIT.
2. Maintainer review of the 12 model cards. The maintainer sends notes like `MOD-01 ok` or `MOD-03 fix: …`; mark
   "ok" cards reviewed by Krunal Maheshwari with the date, apply fixes and leave those unreviewed.
3. Maintainer review of the 22 assessments.
4. Weekly candidate "Man arrested in Bengal … AI-generated police identity card" (week of 2026-10-24): add as
   IN-INC-23 only after the maintainer supplies the article's details.
5. Version 4 (deferred): Compare view, replay standard, test-coverage gap view, finance and elections sector work.

## Environment notes (cloud sessions)

- Reachable: GitHub (git and the REST API), cert-in.org.in, psa.gov.in, rbi.org.in, niti.gov.in, indiaai.gov.in,
  pib.gov.in, metr.org, raw.githubusercontent.com. Not reachable or refusing: MeitY pages (need a full browser, do not
  bypass), egazette.gov.in (incomplete certificate chain), India Code inner pages (time out), SEBI, ECI, TEC,
  Bombay HC, zenodo.org, github.io.
- `gh pr create` fails (GraphQL is blocked): open PRs with `gh api -X POST repos/krunal6649/netra-india-observatory/pulls`.
  Merging, tags and repository settings cannot be done from a session.
- After pushing a new branch, add a fetch refspec and set its upstream, or the stop hook reports unpushed commits:
  `git config --add remote.origin.fetch "+refs/heads/<b>:refs/remotes/origin/<b>"; git fetch origin; git branch --set-upstream-to=origin/<b>`.
