# Maintainer guide

These notes are for the person running the repository. The main [README](../README.md) is for readers.

## How the survey works

- **Anyone can take part.** Signed-in Contributors save answers directly. Everyone else (outside peers, public-link visitors, signed-out readers) clicks "Get my response code" and sends you the short code by email, WhatsApp or any message.
- **You import codes** in the owner-only box on the Expert survey page (About › Expert survey). Paste one or many at once; the same code imported twice counts once. Codes are checked, and anything with invalid values is rejected.
- Codes contain only survey answers, never a name or account.
- Nobody but you sees individual answers. Results go public only when you press "Publish aggregate", and show only once 5+ people have answered with consent.

## Adding data

Edit `data/india.json` (incidents, instruments, risks, mitigations, gaps) or `data/authorities.json` (the Whom to approach directory) and run the build. The build refuses:

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

## Version 3 assessments

Each incident has an optional `assessment` block with its own `review` status. A missing field means "not yet
assessed". The fields are explained on the site under About › Crosswalk. The build refuses:

- an AI role that is not confirmed, suspected, not established or not AI, or that has no `basis`;
- a failure-mode ID that is not an item of its edition (`data/owasp_llm_top10.json`, `data/atlas_techniques.json`),
  or whose name does not match;
- a failure mode or a scale whose `source` is not one of the incident's own sources;
- a NIST crosswalk label other than GOVERN, MAP, MEASURE or MANAGE, or a crosswalk entry without a `why`;
- an assessment marked reviewed without `reviewed_by` and a date, and any unknown field.

Rules used so far: "confirmed" needs an official body (police, a court, a government fact-check, the operator) to say
AI was used. Failure-mode tags go only on confirmed cases, where a cited source describes the facts, and each tag
says it is NETRA's reading.

## Reviewing model cards and assessments

Open each card under Analysis › Models and evaluations and check five things:

1. Is each law labelled possible, interpretive question or gap, with nothing claiming a law applies?
2. Are the authorities the right ones to approach in India?
3. Does the overclaim check say that a test abroad is not harm in India?
4. Is anything important missing from "not known"?
5. Is the release date blank or wrong?

Send notes such as `MOD-01 ok` or `MOD-03 fix: …` to a Claude Code session on this repository. Cards marked "ok" are
recorded as reviewed by you, with the date. Fixed cards stay unreviewed until you pass them.

## Releases and DOIs

Zenodo archives every GitHub release automatically: publish a release on `main` with a new tag (for example
`v0.3.2`). Before releasing, raise the version in `CITATION.cff`, `.zenodo.json`, the README and
`docs/framework.md`. Current DOIs:

- dataset v0.3.1: 10.5281/zenodo.23864343;
- all versions: 10.5281/zenodo.23864342;
- working paper: 10.5281/zenodo.23865186.

`CLAUDE.md` holds the standing rules and open items for AI-assisted sessions.

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
