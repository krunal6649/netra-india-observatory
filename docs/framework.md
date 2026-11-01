# The NETRA framework

NETRA is a working framework for recording an AI harm in India, reading it against Indian law, and routing it to the
bodies that can act. This page sets out the framework in one place so that others can reuse it: the method, the labels,
the review rules and the datasets. The observatory at https://krunal6649.github.io/netra-india-observatory/ is one
working use of it.

Maintainer: Krunal Maheshwari. Data under CC BY 4.0, code under MIT. Research material, not legal advice.

## 1. The method: 14 stages

Every incident is traced through the same stages, recorded in `netra.stages` on each incident.

| # | Stage | What it settles |
|---|---|---|
| S01 | Real-world signal | That a harm has been reported somewhere public |
| S02 | Intake | That it is recorded with its sources |
| S03 | Triage | Whether it falls within scope, and how severe it looks |
| S04 | Harm verification | Whether the harm is confirmed, and by what source |
| S05 | Evidence capture | Which primary evidence exists: court orders, FIR details, platform notices |
| S06 | Forensic reconstruction | What happened technically, where that can be known |
| S07 | AI role and causation | What part an AI system played |
| S08 | Location and jurisdiction | Where the incident, victim, accused, agency and platform are |
| S09 | Legal analysis (T1) | Which Indian laws may apply (T1: legal issues) |
| S10 | Authority routing | Which bodies can act, and in what order |
| S11 | Human review | That a named person has reviewed the record |
| S12 | Mitigation | What was done to stop or reduce the harm |
| S13 | Retest | Whether the fix held, where that applies |
| S14 | Policy and system feedback (T2–T3) | Which governance or system gaps the case shows |

Each stage carries one status: `done`, `partial`, `draft`, `secondary` (from secondary sources only), `open`,
`contested`, `possible` or `n/a`. A record cannot mark S11 `done` unless it names its reviewer and review date.

Version 3 adds an `assessment` block to an incident: AI role, AI system, impact, evidence
provenance, failure modes and a standards crosswalk. If a field is absent, it counts as "not yet assessed". The block
has its own review status, and a failure-mode tag needs one of the incident's own sources to support it. The Crosswalk page under About explains each field and how it maps to NIST AI RMF, OWASP, MITRE ATLAS and ISO/IEC 42001.

Every dossier also ends with two fields:

- **What NETRA does not know** (`netra.unknowns`): the facts the sources do not give.
- **Overclaim check** (`netra.overclaim`): what the record must not say, for example "do not describe the arrested
  person as guilty; the source reports an arrest, not a conviction".

Stage names follow the NETRA lifecycle as stated by the researcher; the "what it settles" lines are short
summaries for this page. Have a second reader check them before citing.

## 2. Classification

Risks, incidents and measures are sorted using the MIT AI Risk Repository taxonomies (CC BY 4.0, with attribution;
NETRA is not affiliated with or endorsed by MIT):

- **Domain taxonomy:** 7 domains and 24 risk areas, used in `domains` on every record.
- **Causal taxonomy:** entity (human or AI), intent (intentional or unintentional) and timing (before or after
  deployment).
- **Mitigation taxonomy:** 4 groups of safety measures.

NETRA adds three of its own scales:

- **severity**, from 1 to 5: negligible, minor, moderate, major, severe;
- 9 **harm types**;
- 12 **sectors**.

## 3. Legal labels

The framework keeps confirmed obligations, potential obligations, interpretive questions, gaps and reforms apart, and
never merges them. When a report is mapped to Indian provisions, each mapping takes one of seven labels:

| Label | Meaning |
|---|---|
| Confirmed legal obligation | The provision clearly applies |
| Potentially applicable obligation | It may apply; applicability has not been decided |
| Interpretive question | It is unsettled how the provision applies |
| Possible legal gap | The law may not reach the problem |
| Governance or implementation gap | The law exists but is not working in practice |
| Proposed law reform | A change that has been proposed |
| Assessed – likely not applicable | Considered and set aside |

Model cards use a shorter set: **possible**, **interpretive question** and **gap**.

Each legal instrument records its **force**:

- hard law, judicial;
- soft law (with its kind: recommendations, Model Code of Conduct, binding effect disputed);
- institutional;
- proposal.

## 4. Review and verification rules

- **No invented citations.** Section numbers, dates, Gazette notification numbers, case names and quotes come only
  from a source.
- **Verification** of a legal record is `yes`, `partial` or `no`.
  - `yes` needs a specific official document, not a site's home page.
  - `partial` must say what is missing.
- **Review status** is one of `unreviewed`, `source_checked`, `human_reviewed` or `published`.
  - New and imported records start as `unreviewed`.
  - A reviewed record must name its reviewer and date.
  - Automated tools can never mark a record reviewed.
- **No duplicates.** A new case is refused if it shares a source or court document with an existing case, or if its
  title is 75% or more alike. The exception is when a person records the two as distinct (`distinct_from`).
- **Official documents from official sites.** A court document must come from an official `.nic.in` or `.gov.in` site.
- **Tests are not harm.** A model evaluation done abroad is never treated as evidence of harm in India. A model
  card keeps "what the testers found" apart from "NETRA's India analysis".
- **Automation is labelled.** The weekly update and the in-browser report check use plain keyword rules, not AI.
  - Their results are auto-selected and unreviewed.
  - They quote sources word for word, and store no article text.

`scripts/build.py` enforces these rules: a record that breaks one stops the site from being published.

## 5. The datasets

All data is open JSON in `data/`.

| File | Holds | Main fields |
|---|---|---|
| `india.json` · `incidents` | 22 Indian AI incidents | `id`, `title`, `date`, `state`, `systems`, `developer`, `deployer`, `harm`, `harm_types`, `severity`, `affected`, `domains`, `entity`, `intent`, `timing`, `sectors`, `response`, `instruments`, `sources`, `netra`, `review`, `reviewed_by`, `reviewed_on` |
| `india.json` · `instruments` | 28 laws, rules, advisories, standards and court orders | `id`, `title`, `issuer`, `type`, `force`, `date`, `status`, `provisions`, `summary`, `url`, `verified`, `note`, plus Act numbers, Gazette notifications and cases where known |
| `india.json` · `risks` | 18 risks quoted from Indian government frameworks | `framework`, `locator`, `quote`, `title`, `domain`, `entity`, `intent`, `timing` |
| `india.json` · `mitigations` | 28 measures from those instruments | `source`, `locator`, `quote`, `category`, `actor`, `force` |
| `india.json` · `gaps` | 6 governance gaps | `title`, `type`, `basis`, `incidents`, `instruments` |
| `authorities.json` | 391 bodies: 31 Union, and 10 for each of 36 states and UTs | `name`, `level`, `place`, `group`, `role` (enforces, adjudicates, regulates, supports victims), `can_do`, `how_to_report`, `laws`, `url`, `verified`, `checked_by`, `checked_on` |
| `models.json` | 12 AI model cards | `tests` (what the testers found), `netra` (risk areas, laws with labels, authorities, gaps, unknowns, overclaim), `incidents`, `review` |
| `global_evidence.json` | 3 METR reports mapped to 14 Indian provisions | `reports`, `instruments`, `mappings`, `classifications` |
| `taxonomy.json` | The MIT taxonomies, NETRA's scales and the 14 stages | `domains`, `causal`, `mitigation`, `severity`, `harm_types`, `sectors`, `netra_stages` |
| `check_terms.json` | Keyword lists for the in-browser report check | `risk_areas`, `instruments` |
| `weekly.json` | The weekly update, last 12 weeks | `top`, `cyber`, `models`, `sources`, `notes` |
| `owasp_llm_top10.json` | OWASP Top 10 for LLM Applications, 2025 and 2026 editions (names only, CC BY-SA 4.0) | `editions` |
| `atlas_techniques.json` | MITRE ATLAS technique IDs and names, release 2026.10 (Apache 2.0, © MITRE) | `techniques` |

## 6. Reusing the framework

- To apply NETRA to another country or sector, keep sections 1 to 4 and replace the instruments, authorities and
  states with your own. The build script checks the same rules.
- Cite the framework as: Maheshwari, K. (2026). *NETRA India AI Risk Observatory* (version 0.3.1) [Data set].
  https://github.com/krunal6649/netra-india-observatory
- Corrections and suggestions are welcome through the repository's issue forms.
