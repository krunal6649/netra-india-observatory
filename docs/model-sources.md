# AI model testing sources for v0.2

Checked 2026-10-23. Re-check terms before each import; licences can change.

| Source | What it gives | Reuse terms (as checked) | Use in v0.2 |
|---|---|---|---|
| [Epoch AI benchmarks](https://epoch.ai/benchmarks/use-this-data) | Model list, release dates, benchmark scores | CC BY 4.0 for Epoch's data; benchmark questions and external data keep their own licences | **Import** (CSV zip or `pip install epochai`), credit Epoch AI |
| [MITRE ATLAS](https://github.com/mitre-atlas/atlas-data) | Attack tactics, techniques, real case studies on AI systems | Apache License 2.0 (LICENSE file, © MITRE); monthly YAML releases | **Import** `dist/ATLAS-latest.yaml`, keep notice |
| [AVID database](https://github.com/avidml/avid-db) | Reports of model failures and vulnerabilities | MIT License (LICENSE file); last commit March 2026 | **Import** reports, credit AVID; flag as possibly slow-moving |
| [OWASP Top 10 for LLM Applications](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10) | Ten security risk categories for LLM apps (2026 list) | CC BY-SA 4.0 | **Import** as a separate file; share-alike applies to that file and anything derived from it |
| [METR](https://metr.org/) | Time-horizon results, model evaluation reports | Site says "All rights reserved"; the [data repo](https://github.com/METR/eval-analysis-public) has no LICENSE file (README points to one that is missing) | **Cite and summarise**: headline figures quoted with link. Ask METR before importing run data |
| Developer system / model cards | What each developer tested and found | Company copyright | **Cite and summarise** with link |
| [UK AI Security Institute](https://www.aisi.gov.uk/research/aisi-frontier-ai-trends-report-2025) | Frontier AI Trends Report (Dec 2025), trend-level findings | Not stated on the page; copyright page did not load | **Cite and summarise** until reuse terms are confirmed |

Not used: AVID's Hugging Face organisation has no public datasets.

## Status after Phase 5 (2026-10-25)

- **Used:** METR (three reports already in `data/global_evidence.json`, cite and summarise only) and **MITRE ATLAS v5.6.0**
  (eight case studies summarised in `data/models.json`, Apache 2.0). Twelve model cards in all, every one unreviewed.
- **Not yet used:** Epoch AI (its data site was not reachable from the build sandbox, so release dates come from cited
  developer or press pages, or are left blank), AVID and OWASP. Planned for v0.3.
- Each card keeps "what the testers found" apart from "NETRA's India analysis", and says that a test result is not
  evidence of real-world harm.

Rules carried over from v0.1: every imported record arrives unreviewed; nothing is shown as a legal conclusion
without human review; each record keeps its source link and licence.

## Status after Phase 6 (2026-10-25)

- The weekly update (`scripts/weekly_top5.py`) now lists **new** MITRE ATLAS case studies and METR publications each
  Saturday under Model watch, unreviewed. MITRE ATLAS has moved to release 2026.09 (format v6, 73 case studies);
  NETRA's twelve cards still use the eight v5.6.0 case studies until they are reviewed and updated.
- Epoch AI, AVID and OWASP remain planned for v0.3 (see `docs/roadmap.md`).
