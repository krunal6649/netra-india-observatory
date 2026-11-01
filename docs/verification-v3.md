# Version 3, Step 1: verification log

Date: 2026-11-01. Branch: `v3/verification-first`. Prepared by the AI-assisted session for the maintainer's review.

## What could and could not be opened

The build session's network blocks every Indian government domain tried (`egazette.gov.in`, `indiacode.nic.in`,
`meity.gov.in`, `cert-in.org.in`, `sebi.gov.in`, `rbi.org.in`, `icmr.gov.in`, `tec.gov.in`, `eci.gov.in`,
`delhihighcourt.nic.in`, `consumeraffairs.nic.in`, `niti.gov.in`, `indiaai.gov.in`, `dpiit.gov.in`, `psa.gov.in`),
as well as `metr.org`, `atlas.mitre.org`, `en.wikipedia.org`, `llmreference.com`, `datanorth.ai` and
`bojan.substack.com`. The MITRE ATLAS data on `raw.githubusercontent.com` could be read.

Rule followed: a record is changed only on what a source that was actually opened says. Nothing below has been
upgraded on the strength of memory or secondary summaries.

## 1a. DPDP Act and Rules

| Record | Before | After | Why |
|---|---|---|---|
| G-DPDP (G.S.R. 843(E), commencement) | partly verified | partly verified (unchanged) | The Gazette PDF at egazette.gov.in/WriteReadData/2025/267650.pdf could not be opened from the build session. The commencement dates in the record still rest on secondary summaries. |
| G-DPDPR (G.S.R. 846(E), Rules) | partly verified | partly verified (unchanged) | Same PDF, same reason. The phasing (Rules 1, 2, 17–21 now; Rule 4 after one year; Rules 3, 5–16, 22–23 after 18 months) still rests on law-firm summaries. |

**To finish:** open the PDF and confirm, for each notification:
- the notification date;
- the date each part comes into force, quoted exactly;
- the rule numbers in each phase.

Send those to the maintainer's session, or allow `egazette.gov.in` in the environment's network settings, and the
records will be updated with only what the text says.

## 1b. The 24 partly verified legal records

All 24 stay partly verified, because no official text could be opened. The "what is still missing" column is each
record's own note, unchanged.

| ID | Record | Before | After | What is still missing | Where to check |
|---|---|---|---|---|---|
| G-ITA | Information Technology Act, 2000 | partly verified | partly verified (unchanged) | Enforcement date from India Code. Section list and s.43A end date supplied by the project owner; Gazette copy not checked. s.79A (Examiner of Electronic Evidence) added in v0.2; section contents otherwise summarised from researcher knowledge. | indiacode.nic.in (Act 21 of 2000) |
| G-ITR21 | IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 | partly verified | partly verified (unchanged) | G.S.R. numbers and dates supplied by the project owner. URL is a copy in Gazette layout on a nic.in court website, found by web search; it has not been opened (host blocked from the AI-assisted session's sandbox) and is not the egazette.gov.in original. Missing for 'yes': open and confirm a Gazette copy of G.S.R. 139(E), or replace this link with the egazette.gov.in original. Amendment years 2023 and 2025 in 'status' still rest on the S.S. Rana summary. | egazette.gov.in (G.S.R. 139(E)) |
| G-ITR26 | IT (Intermediary Guidelines and Digital Media Ethics Code) Amendment Rules, 2026 | partly verified | partly verified (unchanged) | G.S.R. number and dates supplied by the project owner; scope agrees across DSCI, Mondaq, IFF and iPleaders summaries. Missing for 'yes': the Gazette PDF of G.S.R. 120(E) has not been opened; URL is a DSCI summary. Draft Second Amendment (2026) not read. | egazette.gov.in (G.S.R. 120(E)) |
| G-ADV-DEC23 | MeitY advisory to intermediaries on prohibited content and deepfakes (23 Dec 2023) | partly verified | partly verified (unchanged) | Date confirmed by JSA summary of the March 2024 advisory. Content per secondary reporting. | meity.gov.in |
| G-ADV-MAR24 | MeitY advisory on AI models and platforms (1 Mar 2024, revised 15 Mar 2024) | partly verified | partly verified (unchanged) | JSA notes the legal basis is ambiguous and enforceability unclear. | meity.gov.in |
| G-CERTIN | CERT-In Directions under s.70B(6) IT Act (No. 20(3)/2022-CERT-In) | partly verified | partly verified (unchanged) | Official PDF URL from multiple secondary sources; PDF not opened. | cert-in.org.in |
| G-DPDP | Digital Personal Data Protection Act, 2023 | partly verified | partly verified (unchanged) | Commencement split per secondary summaries of G.S.R. 843(E). G.S.R. number supplied by the project owner. Missing for 'yes': owner to confirm the Gazette text at gazette_url (not opened by the AI-assisted session; host blocked). | egazette.gov.in/WriteReadData/2025/267650.pdf |
| G-DPDPR | Digital Personal Data Protection Rules, 2025 | partly verified | partly verified (unchanged) | Phasing per Mondaq, AZB and Konfirmity summaries; URL is the AZB summary. G.S.R. number supplied by the project owner. Missing for 'yes': owner to confirm the Gazette text at gazette_url (not opened by the AI-assisted session; host blocked). | egazette.gov.in/WriteReadData/2025/267650.pdf |
| G-CPA | Consumer Protection Act, 2019 | partly verified | partly verified (unchanged) | Act number, assent date, commencement and section numbers supplied by the project owner. Missing for 'yes': the bare Act and S.O. 2351(E) not opened; URL is the India Code home page, not the Act. | indiacode.nic.in; egazette.gov.in (S.O. 2351(E)) |
| G-CCPA-DP | Guidelines for Prevention and Regulation of Dark Patterns, 2023 | partly verified | partly verified (unchanged) | Date from Mondaq headline ('effective 30 November 2023'); text not opened. | consumeraffairs.nic.in or egazette.gov.in |
| G-COPY | Copyright Act, 1957 | partly verified | partly verified (unchanged) | Commencement date from researcher knowledge; s.52(1)(a) reading from iPleaders summary of ANI v OpenAI. | indiacode.nic.in |
| G-DPIIT-WP | DPIIT Working Paper (Part 1) on generative AI and copyright | partly verified | partly verified (unchanged) | Secondary reporting; paper itself not opened. | dpiit.gov.in |
| G-PSA-WP | PSA white paper on techno-legal measures for AI governance | partly verified | partly verified (unchanged) | Date is the news report date. Formal title and paper text not opened. Directly overlaps this observatory’s purpose. | psa.gov.in |
| G-AISI | IndiaAI Safety Institute | partly verified | partly verified (unchanged) | Announcement date not stated on the IndiaAI page; reported as January 2025 elsewhere. | indiaai.gov.in |
| G-NITI2 | Responsible AI for All – Part 2: Operationalizing Principles | partly verified | partly verified (unchanged) | Date from file name; content not read in this session. | niti.gov.in |
| G-RBI | RBI FREE-AI Committee Report (Financial sector) | partly verified | partly verified (unchanged) | Recommendations 1–14 read; 15–26 not read. | rbi.org.in |
| G-SEBI-CP | SEBI consultation paper on guidelines for responsible usage of AI/ML in securities markets | partly verified | partly verified (unchanged) | Secondary summary; whether final guidelines issued not confirmed. | sebi.gov.in |
| G-ICMR | Ethical Guidelines for Application of AI in Biomedical Research and Healthcare | partly verified | partly verified (unchanged) | Title, issuer and year from ICMR page; principles not read. | icmr.gov.in |
| G-TEC | TEC Standard for Fairness Assessment and Rating of AI Systems | partly verified | partly verified (unchanged) | Release date and standard number not stated in the source read. | tec.gov.in |
| G-ECI-24 | ECI advisory on responsible use of social media (2024 general election) | partly verified | partly verified (unchanged) | Described in MediaNama’s Oct 2025 report; original advisory not opened. | eci.gov.in |
| G-ECI-25 | ECI directive on AI-generated campaign content (Bihar 2025) | partly verified | partly verified (unchanged) | Exact issue date not stated in the source; reported 10 Oct 2025. | eci.gov.in |
| G-J-ANIL | Anil Kapoor personality-rights order (Delhi High Court) | partly verified | partly verified (unchanged) | Order itself not read. | delhihighcourt.nic.in |
| G-J-ARIJIT | Arijit Singh v. Codible Ventures LLP (Bombay High Court) | partly verified | partly verified (unchanged) | Order PDF available via Columbia Global Freedom of Expression; not read. | bombayhighcourt.nic.in |
| G-J-ANI | ANI Media Pvt. Ltd. v. OpenAI OpCo LLC, CS(COMM) 1028/2024 (Delhi High Court) | partly verified | partly verified (unchanged) | Neutral citation 2026:DHC:5900 per iPleaders; judgment not read. | delhihighcourt.nic.in |

## 1c. The 12 model cards

Checked: each test summary against the cited source, where it could be opened, and each release date against its
cited source. Review status stays **unreviewed** on all 12.

### Tests based on MITRE ATLAS: checked against ATLAS data release 2026.10

| Card | Case study | Result |
|---|---|---|
| MOD-08 ChatGPT | AML.CS0021 ChatGPT Conversation Exfiltration | Supported: indirect prompt injection on a public website; image markdown carries the conversation to an attacker script. Exercise, May 2023. |
| MOD-08 ChatGPT | AML.CS0022 ChatGPT Package Hallucination | Supported: hallucinated package names an attacker could publish. ATLAS cites Vulcan and Lasso Security research. Exercise, June 2024. |
| MOD-08 ChatGPT | AML.CS0040 Hacking ChatGPT's Memories with Prompt Injection | Supported: injection in a shared Google Doc poisons memory with false facts that persist across sessions. Exercise, February 2024. |
| MOD-09 Gemini (Bard) | AML.CS0029 Google Bard Conversation Exfiltration | Supported: injection in a shared Google Doc; conversation exfiltrated through image markdown; "Google has fixed this vulnerability". 23 November 2023. |
| MOD-10 M365 Copilot | AML.CS0026 Financial Transaction Hijacking with M365 Copilot as an Insider | Supported: email with retrieval content and a prompt injection returns the attacker's bank details as a trusted reference. 8 August 2024. |
| MOD-10 Copilot Studio | AML.CS0037 Data Exfiltration via Agent Tools in Copilot Studio | Supported: prompt injections by email led the agent to exfiltrate customer data. Note: the agent was built by Zenity for the exercise, modelled on a real one; ATLAS records that Microsoft fixed the issue. June 2025. |
| MOD-11 Claude computer use | AML.CS0046 Data Destruction via Indirect Prompt Injection Targeting Claude Computer-Use | Supported: injection in a PDF bypassed guardrails and ran a command to delete the file system. 24 October 2024. |
| MOD-11 Claude computer use | AML.CS0056 Model Distillation Campaigns Targeting Anthropic Claude | Supported: about 24,000 accounts and 16 million queries, attributed by Anthropic to three labs; Anthropic warned distilled models could lack safeguards. **Flag:** ATLAS gives this date at year granularity (2026); the card shows 2026-02-23. Suggest showing "2026" unless Anthropic's own report gives the day. |

The cards cite MITRE ATLAS v5.6.0; the text checked here is release 2026.10, and it supports every summary. Suggest
updating the cited release when the cards are reviewed.

### Tests based on METR: not checked against METR

`metr.org` could not be opened. Each card's figures match NETRA's stored summaries in `data/global_evidence.json`
(TR-001, TR-002, TR-003), but those summaries are themselves unreviewed, so this is a consistency check only.

| Card | Report | Claims to confirm against METR's own page |
|---|---|---|
| MOD-01 GPT-5.6 Sol | TR-001 | about 5% of agents ran on GPT-5.6 Sol; about 700 agents joined the attack; about 7% of reviewed transcripts had spoofed tool calls |
| MOD-02 HPIM | TR-001 | about 95% of agents ran on HPIM; agents recognised the attack was out of scope but usually joined |
| MOD-03 Claude Opus 4.6 | TR-002 | named among the public frontier models considered; findings not attributed to it alone |
| MOD-04 o3, MOD-05 Claude Opus 4, MOD-06 DeepSeek-R1, MOD-07 Gemini 2.5 Pro (preview) | TR-003 | each is among the 21 models in MALT; best monitors caught roughly 80–90% at a 5% false-positive rate; no per-model base rates |

### Release dates

None of the release-date sources could be opened.

| Card | Date on card | Cited source | Flag |
|---|---|---|---|
| MOD-01 GPT-5.6 Sol | 2026-07-09 | DataNorth news page | Secondary source; not opened |
| MOD-03 Claude Opus 4.6 | 2026-02-05 | llmreference.com comparison page | Third-party comparison site, not the developer; not opened |
| MOD-06 DeepSeek-R1 | 2025-01-20 | llmreference.com comparison page | Third-party comparison site, not the developer; not opened |
| MOD-09 Gemini | 2024-02-08 | Wikipedia | Secondary source; not opened |
| MOD-10 M365 Copilot | 2023-11-01 | Substack post "ChatGPT one year later" | **Likely unsupported:** the title is about ChatGPT, not Microsoft 365 Copilot. Replace with Microsoft's own announcement, or mark the date unverified. |
| MOD-02, 04, 05, 07, 11, 12 | not recorded | none | Developer announcement needed if a date is to be shown |

### Other flags

- **MOD-12 Grok** has no evaluator's test; the card rests on the India case IN-INC-20 only. That is within scope (no
  in-house testing), but the card should say plainly that no published evaluation is cited yet.

## What the maintainer needs to do to finish Step 1

1. Allow these domains in the environment's network settings, or download and add the texts to the session:
   - `egazette.gov.in` and `indiacode.nic.in` (most of the 24);
   - the issuing bodies' sites listed in the table;
   - `metr.org`.
2. Decide on the two model-card flags: the AML.CS0056 date, and the MOD-10 release source.
3. Confirm if any card should move from unreviewed after your own reading.
