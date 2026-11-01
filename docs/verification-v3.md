# Version 3, Step 1: verification log

Date: 2026-11-01. Branch: `v3/verification-first`. Prepared by the AI-assisted session for the maintainer's review.

## What could and could not be opened

First pass (before the maintainer widened network access): the build session's network blocked every Indian government domain tried (`egazette.gov.in`, `indiacode.nic.in`,
`meity.gov.in`, `cert-in.org.in`, `sebi.gov.in`, `rbi.org.in`, `icmr.gov.in`, `tec.gov.in`, `eci.gov.in`,
`delhihighcourt.nic.in`, `consumeraffairs.nic.in`, `niti.gov.in`, `indiaai.gov.in`, `dpiit.gov.in`, `psa.gov.in`),
as well as `metr.org`, `atlas.mitre.org`, `en.wikipedia.org`, `llmreference.com`, `datanorth.ai` and
`bojan.substack.com`. The MITRE ATLAS data on `raw.githubusercontent.com` could be read.

Rule followed: a record is changed only on what a source that was actually opened says. Nothing below has been
upgraded on the strength of memory or secondary summaries.

## 1a. DPDP Act and Rules

| Record | Before | After | Why |
|---|---|---|---|
| G-DPDP (Act; G.S.R. 843(E), commencement) | partly verified | **verified** | Act text checked against the Gazette of 11 August 2023 (Part II s.1, No. 25, CG-DL-E-12082023-248045). Commencement checked against the Gazette of 13 November 2025 (Part II s.3(i), No. 757, CG-DL-E-14112025-267647): G.S.R. 843(E), signed by Ajit Kumar, Jt. Secy.: (a) ss.1(2), 2, 18–26, 35, 38–43, 44(1) and (3) on publication; (b) ss.6(9) and 27(1)(d) one year after; (c) ss.3–5, 6(1)–(8) and (10), 7–17, 27 except (1)(d), 28–34, 36, 37 and 44(2) eighteen months after. The earlier unofficial one-page summary agrees with this text, but only the Gazette copy was relied on. |
| G-DPDPR (G.S.R. 846(E), Rules) | partly verified | **verified** | Checked against the Gazette of India Extraordinary, Part II, Section 3(i), No. 760, 13 November 2025 (CG-DL-E-14112025-267650), supplied by the maintainer. Rule 1(2)–(4) quoted exactly: Rules 1, 2 and 17–21 in force on publication; Rule 4 one year after; Rules 3, 5–16, 22 and 23 eighteen months after. This file does not contain G.S.R. 843(E). |

**Gazette copy supplied by the maintainer (2026-11-01):** Gazette of India Extraordinary, Part II, Section 2, No. 18,
3 August 2023 (CG-DL-E-04082023-247847). It prints the **DPDP Bill, 2023 (Bill No. 113 of 2023) as introduced in Lok
Sabha**, not the Act as passed, the commencement notification G.S.R. 843(E) or the Rules G.S.R. 846(E).

- **What it confirms:** the clauses G-DPDP cites. Clause 1(2) leaves commencement to notification, with different
  dates allowed for different provisions; clause 8(5)–(6) covers security safeguards and breach intimation; clause
  44(2)(a) omits IT Act s.43A. This is recorded in G-DPDP's note.
- **What it does not confirm:** the enacted text, or any commencement date. Both DPDP records stay partly verified.

**To finish, either:**
- download the PDF in your own browser and add it to this chat or the repository; or
- allow `*.lencr.org` as well, so the missing Let's Encrypt certificate can be fetched and the site's certificate checked in full.

Then confirm, for each notification:
- the notification date;
- the date each part comes into force, quoted exactly;
- the rule numbers in each phase.

## 1b. The 24 partly verified legal records

**10 records are now verified** and **14 stay partly verified**. Some were checked against official sites
after network access was widened; others against official copies the maintainer supplied (Gazette PDFs, the CERT-In
Directions and MeitY's signed advisory of 15 March 2024). Files without an official header or publisher were not
relied on. Every upgrade was made by the AI-assisted session and awaits the maintainer's confirmation.

| ID | Record | Before | After | What was checked, or what is still missing | Official source |
|---|---|---|---|---|---|
| G-ITA | Information Technology Act, 2000 | partly verified | partly verified (updated) | Partly checked on 2026-11-01. The s.43A end date is backed by G.S.R. 843(E) (Gazette, 13 November 2025, CG-DL-E-14112025-267647): DPDP Act s.44(2), which omits s.43A, comes into force eighteen months from publication. A consolidated text of the Act supplied by the maintainer ('it_act_2000_updated.pdf', Act No. 21 of 2000) contains every section listed (ss.43, 43A, 66, 66C, 66D, 66E, 67, 67A, 69A, 75, 79, 79A) and gives the commencement as '17th October, 2000, vide notification No. G.S.R. 788 (E)'. That copy has no publisher, letterhead or Gazette header, so it is not relied on as an official source. Still missing for 'yes': an official copy (India Code or the issuing ministry) at a link that can be cited. | |
| G-ITR21 | IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 | partly verified | partly verified (updated) | Partly checked on 2026-11-01. (1) Principal rules checked against the Gazette pages of G.S.R. 139(E), New Delhi, 25 February 2021, Part II s.3(i), F. No. 16(4)/2020-CLES, signed by Dr. Rajendra Kumar, Addl. Secy., digitally signed by the Government of India Press on 25 February 2021 (copy from mib.gov.in, supplied by the maintainer): rule 1(2) in force on publication; rule 3(1)(b), rule 3(1)(d) 'thirty-six hours', rule 3(2)(b) 'twenty-four hours'. (2) Amendment history checked against the note to G.S.R. 120(E) (Gazette, 10 February 2026): G.S.R. 794(E) of 28 October 2022, G.S.R. 275(E) of 6 April 2023 and G.S.R. 775(E) of 22 October 2025. Still missing for 'yes': the text of G.S.R. 794(E), to confirm that it replaced rule 3(1)(b), and an official link for the url (the current link is an unopened copy on thc.nic.in). | |
| G-ITR26 | IT (Intermediary Guidelines and Digital Media Ethics Code) Amendment Rules, 2026 | partly verified | **verified** | Checked on 2026-11-01 against the Gazette of India Extraordinary, Part II, Section 3(i), No. 114, 10 February 2026 (CG-DL-E-10022026-269993), supplied by the maintainer: G.S.R. 120(E), F. No. 2(5)/2025-CyberLaws, signed by Ajit Kumar, Jt. Secy.; 'They shall come into force on the 20th day of February, 2026'; clause (wa); rule 3(1)(d) 'thirty-six hours' to 'within three hours'; rule 3(2)(a)(i) 'fifteen days' to 'seven days'; rule 3(2)(b) 'twenty-four hours' to 'two hours'; new rule 3(3); new rule 4(1A). The url follows egazette.gov.in's file pattern from the Gazette ID and was not opened from the build session. The draft Second Amendment (2026) was not read. Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://egazette.gov.in/WriteReadData/2026/269993.pdf) |
| G-ADV-DEC23 | MeitY advisory to intermediaries on prohibited content and deepfakes (No. 2(4)/2023-CyberLaws-2, 26 Dec 2023) | partly verified | partly verified (updated) | Date corrected on 2026-11-01 from 23 to 26 December 2023: MeitY's signed advisory of 15 March 2024 (eNo.2(4)/2023-CyberLaws-3) refers to 'advisory No. 2(4)/2023-CyberLaws - 2 dated 26th December, 2023' and lists it as its Annexure A. The earlier date came from a JSA summary. Still missing for 'yes': the advisory's own text (Annexure A was not in the copy supplied); content still rests on secondary reporting. | |
| G-ADV-MAR24 | MeitY advisory on AI models and platforms (1 Mar 2024, revised 15 Mar 2024) | partly verified | partly verified (updated) | Text checked on 2026-11-01 against a signed copy supplied by the maintainer: MeitY, Cyber Law and Data Governance Group, eNo.2(4)/2023-CyberLaws-3, dated 15-03-2024, signed by Dr. Sandip Chatterjee, Scientist G and Group Coordinator (Cyber Law); 'issued in supersession of advisory eNo.2(4)/2023-CyberLaws-3, dated 1st March, 2024'; paras 2(a)-(d), 3, 4 and 5 read. The earlier summary said the revision 'dropped prior government permission'; that compares it with the 1 March text, which has not been read, so it has been removed. Still missing for 'yes': an official MeitY link for the url (the current link is a JSA summary). The 'binding effect disputed' label rests on JSA's commentary. | |
| G-CERTIN | CERT-In Directions under s.70B(6) IT Act (No. 20(3)/2022-CERT-In) | partly verified | **verified** | Checked on 2026-11-01 against the CERT-In PDF supplied by the maintainer, the same file name as the url: No. 20(3)/2022-CERT-In, MeitY / CERT-In, dated 28 April 2022, 'Directions under sub-section (6) of section 70B of the Information Technology Act, 2000'. Direction (ii): report Annexure I cyber incidents 'within 6 hours of noticing such incidents'; direction (iv): logs of all ICT systems kept 'for a rolling period of 180 days' within the Indian jurisdiction; 'This direction will become effective after 60 days from the date on which it is issued' (27 June 2022 is calculated). No AI-specific incident category in Annexure I. Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf) |
| G-DPDP | Digital Personal Data Protection Act, 2023 | partly verified | **verified** | Checked on 2026-11-01 against two Gazette copies supplied by the maintainer. (1) Gazette of India Extraordinary, Part II, Section 1, No. 25, 11 August 2023 (CG-DL-E-12082023-248045): 'The Digital Personal Data Protection Act, 2023 (No. 22 of 2023)', assent 11 August 2023; s.1(2), s.3, Chapter II (ss.4-10), s.8(5)-(6) and s.44(2)(a) 'section 43A shall be omitted' checked. (2) Gazette of India Extraordinary, Part II, Section 3(i), No. 757, 13 November 2025 (CG-DL-E-14112025-267647): MeitY notification G.S.R. 843(E), F. No. AA-11038/1/2025-CL&ES, signed by Ajit Kumar, Jt. Secy., appointing (a) the date of publication for ss.1(2), 2, 18-26, 35, 38-43 and 44(1) and (3); (b) one year from publication for s.6(9) and s.27(1)(d); (c) eighteen months from publication for ss.3-5, 6(1)-(8) and (10), 7-10, 11-17, 27 except (1)(d), 28-34, 36, 37 and 44(2). '13 May 2027' is calculated from the publication date, not stated in the notification. The url is India Code's copy of the Act, which could not be opened from the build session. Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://www.indiacode.nic.in/bitstream/123456789/22037/2/a2023-22.pdf) |
| G-DPDPR | Digital Personal Data Protection Rules, 2025 | partly verified | **verified** | Checked on 2026-11-01 against the Gazette of India Extraordinary, Part II, Section 3(i), No. 760, New Delhi, 13 November 2025 (CG-DL-E-14112025-267650), a copy supplied by the maintainer that matches the egazette.gov.in file at the url. MeitY notification G.S.R. 846(E) dated 13 November 2025 makes the Rules under s.40(1) and (2) of the Act (22 of 2023). Rule 1(2)-(4), quoted: 'Rules 1, 2 and 17 to 21 shall come into force on the date of their publication in the Official Gazette'; 'Rule 4 shall come into force one year after the date of publication of this Gazette'; 'Rules 3, 5 to 16, 22 and 23 shall come into force eighteen months after the date of publication of this Gazette'. Rule headings for the provisions listed were checked. This Gazette file does not contain G.S.R. 843(E). Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://egazette.gov.in/WriteReadData/2025/267650.pdf) |
| G-CPA | Consumer Protection Act, 2019 | partly verified | partly verified | indiacode.nic.in answered 504; egazette.gov.in certificate chain incomplete. Still missing: Act number, assent date, commencement and section numbers supplied by the project owner. Missing for 'yes': the bare Act and S.O. 2351(E) not opened; URL is the India Code home page, not the Act. | |
| G-CCPA-DP | Guidelines for Prevention and Regulation of Dark Patterns, 2023 | partly verified | partly verified | consumeraffairs.nic.in did not answer. Still missing: Date from Mondaq headline ('effective 30 November 2023'); text not opened. | |
| G-COPY | Copyright Act, 1957 | partly verified | partly verified | indiacode.nic.in answered 504. Still missing: Commencement date from researcher knowledge; s.52(1)(a) reading from iPleaders summary of ANI v OpenAI. | |
| G-DPIIT-WP | DPIIT Working Paper (Part 1) on generative AI and copyright | partly verified | partly verified | dpiit.gov.in builds its pages in the browser; the paper could not be located. Still missing: Secondary reporting; paper itself not opened. | |
| G-PSA-WP | PSA white paper: Strengthening AI Governance through Techno-Legal Framework | partly verified | **verified** | Checked on 2026-11-01 against the official PDF on psa.gov.in: title, 'January 2026' on the cover, Section IV 'National Database of AI Incidents' (record, classify and analyse safety failures, biased outcomes, security breaches and misuse; India-specific risk taxonomy), TPEC, and the voluntary practices listed. Date 2026-01-23 is the 'Published on' date on the PSA AI page. Earlier date (2026-01-24) was a news report date. Checked by the AI-assisted session; awaiting the maintainer's confirmation. Directly overlaps this observatory's purpose. | [source](https://psa.gov.in/CMS/web/sites/default/files/publication/AI-WP_TechnoLegal.pdf) |
| G-AISI | IndiaAI Safety Institute | partly verified | **verified** | Checked on 2026-11-01 against the IndiaAI article at the url (dated Jan 31, 2025): the Minister of Electronics and IT announced the setting up of the IndiaAI Safety Institute under the Safe and Trusted pillar of the IndiaAI Mission, on a hub-and-spoke model. The date is the article's publication date. The Guidelines' recommendation in the summary rests on G-AIGG. Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://indiaai.gov.in/article/india-takes-the-lead-establishing-the-indiaai-safety-institute-for-responsible-ai-innovation) |
| G-NITI2 | Responsible AI for All – Approach Document for India, Part 2: Operationalizing Principles for Responsible AI | partly verified | **verified** | Checked on 2026-11-01 against the official PDF on niti.gov.in: title and 'AUGUST 2021' on the cover; the document sets out the role of Government as policy maker, regulator and procurer (section 3) and actions for the private sector and research institutions (section 4). The cover gives the month only, so the earlier day (12 August, taken from the file name) has been removed. Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://niti.gov.in/sites/default/files/2021-08/Part2-Responsible-AI-12082021.pdf) |
| G-RBI | RBI FREE-AI Committee Report: Framework for Responsible and Ethical Enablement of Artificial Intelligence (Financial sector) | partly verified | **verified** | Checked on 2026-11-01 against the full report text on the RBI publication page at the url (dated 13 Aug 2025): 7 Sutras, 6 Pillars (Infrastructure, Policy, Capacity; Governance, Protection, Assurance) and 26 Recommendations, all 26 read, including 15-26 (data lifecycle governance, AI system governance, product approval, consumer protection, cybersecurity, red teaming, business continuity, AI incident reporting, AI inventory, audit, disclosures, AI toolkit). Summary items checked: AI Innovation Sandbox (Rec. 2), graded liability framework (Rec. 8), Standing Committee (Rec. 9, para 4.4.32), board-approved AI policy (Rec. 14). Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://www.rbi.org.in/Scripts/PublicationReportDetails.aspx?UrlPage=&ID=1306) |
| G-SEBI-CP | SEBI consultation paper on guidelines for responsible usage of AI/ML in securities markets | partly verified | partly verified | sebi.gov.in search refused the automated request (error 530). Still missing: Secondary summary; whether final guidelines issued not confirmed. | |
| G-ICMR | Ethical Guidelines for Application of Artificial Intelligence in Biomedical Research and Healthcare | partly verified | **verified** | Checked on 2026-11-01 against the official PDF on icmr.gov.in (78 pages): title, 'Prepared by DHR-ICMR Artificial Intelligence Cell', '© 2023, Indian Council of Medical Research'. Section 1 sets out ethical principles for AI in healthcare; Section 2 guiding principles for development, validation and deployment. Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://www.icmr.gov.in/icmrobject/custom_data/pdf/Ethical-guidelines/Ethical_Guidelines_AI_Healthcare_2023.pdf) |
| G-TEC | TEC Standard for Fairness Assessment and Rating of AI Systems | partly verified | partly verified | tec.gov.in did not answer. Still missing: Release date and standard number not stated in the source read. | |
| G-ECI-24 | ECI advisory on responsible use of social media (2024 general election) | partly verified | partly verified | eci.gov.in answered 406 Not Acceptable to automated requests. Still missing: Described in MediaNama’s Oct 2025 report; original advisory not opened. | |
| G-ECI-25 | ECI directive on AI-generated campaign content (Bihar 2025) | partly verified | partly verified | eci.gov.in answered 406 Not Acceptable to automated requests. Still missing: Exact issue date not stated in the source; reported 10 Oct 2025. | |
| G-J-ANIL | Anil Kapoor v. Simply Life India & Ors., CS(COMM) 652/2023 (Delhi High Court), personality-rights order | partly verified | **verified** | Checked on 2026-11-01 against the digitally signed order on the Delhi High Court portal (21 pages, dated 20.09.2023, Coram Justice Prathiba M. Singh): para 48 restrains Defendants 1-16 from using the plaintiff's name, likeness, image, voice or persona 'using technological tools such as Artificial Intelligence, Machine Learning, deep fakes, face morphing'; para 49 locks and suspends three domain names; para 50 directs ISPs to take down the listed links; para 51 directs DoT/MeitY to issue blocking orders. Judge's name corrected from 'Pratibha' to the spelling in the order. Checked by the AI-assisted session; awaiting the maintainer's confirmation. | [source](https://delhihighcourt.nic.in/app/downloadOrderbByDate/CS(COMM)/652/2023/20-09-2023) |
| G-J-ARIJIT | Arijit Singh v. Codible Ventures LLP (Bombay High Court) | partly verified | partly verified | bombayhighcourt.nic.in did not answer. Still missing: Order PDF available via Columbia Global Freedom of Expression; not read. | |
| G-J-ANI | ANI Media Pvt. Ltd. v. OpenAI OpCo LLC, CS(COMM) 1028/2024 (Delhi High Court) | partly verified | partly verified (updated) | Partly checked on 2026-11-01 against two official orders on the Delhi High Court portal. Order of 24.07.2026 (downloadOrderbByDate/CS(COMM)/1028/2024/24-07-2026): Justice Amit Bansal; I.A. 45300/2024 'decided' through a separate judgment pronounced that day; suit listed on 11 September 2026. Order of 27.07.2026: corrects a citation in paragraph 80 of that judgment. Still missing for 'yes': the judgment itself (holding on jurisdiction, fair dealing and outputs) and the neutral citation 2026:DHC:5900, which rest on the iPleaders summary at the url. | |

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

### Tests based on METR: checked against METR's own pages (2026-11-01)

| Card | Report | Result |
|---|---|---|
| MOD-01 GPT-5.6 Sol | TR-001, METR, 26 August 2026 | Supported. METR: "the vast majority or all of the agents involved in this attack were instances of HPIM (~95%) and GPT-5.6 Sol (~5%)"; about 1,200 agents on the message board, about 700 in the attack; "Roughly 7% of the transcripts we evaluated were successfully spoofed". |
| MOD-02 HPIM | TR-001 | Supported. "Agents realized this activity was out of scope and unethical, but joined"; of the 533 agents active on the board in the period, over 90% joined, which supports "usually joined anyway". |
| MOD-03 Claude Opus 4.6 | TR-002, METR, 19 May 2026 | Supported. The report discusses Opus 4.6 among the models it evaluated; its findings on internally deployed agents (means, motive and opportunity for a minimal "rogue deployment"; at least 16% of successful runs on 8h+ tasks illegitimate; 25 of 44 incidents combining overreach and deception) are not attributed to this model alone, as the card says. |
| MOD-04 o3, MOD-05 Claude Opus 4, MOD-06 DeepSeek-R1, MOD-07 Gemini 2.5 Pro (preview) | TR-003, METR, 14 October 2025 | Supported. MALT covers "21 models"; its model list includes o3, claude-opus-4-20250514, deepseek-r1 and gemini-2.5-pro-preview; "At a fixed 5% false positive rate, the best monitors catch 80%-90% of true positives"; METR says label frequency is not "a meaningful measure of the base rate". |

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

1. **DPDP:** done. Both records are verified.
2. **Official links still needed** for the 2021 IT Rules (the mib.gov.in Gazette copy), the March 2024 MeitY advisory and
   the IT Act copy, and the source of `it_act_2000_updated.pdf`. Their texts were checked, but a verified record must
   cite a link anyone can open.
2. **The other 17 partly verified records:** each needs a site that refused automated access or did not answer from the
   build session (India Code, MeitY, SEBI, ECI, CERT-In, Consumer Affairs, TEC, DPIIT, Bombay High Court). The fastest
   route is to download those official PDFs in your own browser and add them here; the table names what each one is.
3. **Confirm or reject the 6 upgrades** made in this pass (G-PSA-WP, G-AISI, G-NITI2, G-RBI, G-ICMR, G-J-ANIL).
4. **Model cards:** decide on the AML.CS0056 date and the MOD-10 release source, and confirm if any card should move
   from unreviewed after your own reading.
