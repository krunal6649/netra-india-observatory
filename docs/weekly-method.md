# This week in India: method

The weekly update finds **up to five AI incidents in India from the past seven days**, a separate **Cyber watch** and a
**Model watch**. It is produced by `scripts/weekly_top5.py` (standard-library Python, no AI, no API key) and shown on
the Home page. Every item is labelled **Auto-selected, unreviewed**.

## When it runs

`.github/workflows/weekly.yml` runs **every morning at 07:00 IST** (cron `30 1 * * *`, 01:30 UTC). A NETRA week runs
Saturday to Friday: each morning's run covers the current week up to yesterday, and Saturday's run completes the week
just ended.

Each week has **one pull request**:
- it is opened the first morning something turns up;
- on later mornings, if anything new appears, the run updates the pull request and adds a comment listing only the new
  items, so GitHub notifies the owner only when there is something to look at;
- if the owner has already edited the pull request (for example deleted a wrong item), the run does not overwrite it;
  it only comments with the new items;
- quiet mornings change nothing.

It can also be started by hand from *Actions › Daily check (unreviewed) › Run workflow*. To redo an earlier week, enter a
date in that week in the *run_date* box (for example `2026-11-14` for the week of 7 to 13 November); the redone week
replaces the old one. GitHub sometimes starts scheduled runs a few minutes late, and pauses scheduled workflows after 60
days without repository activity (re-enable them from the Actions tab).

GDELT limits requests per address, and GitHub's runners are shared, so GDELT sometimes answers "too many requests". The
script retries after 20, 45 and 90 seconds. If either GDELT search still fails, the workflow waits 10 minutes and runs
once more. If news still cannot be fetched, the run notes say which search did not answer, not that nothing happened.

Nothing is merged automatically, and nothing becomes a NETRA incident record by itself. The owner checks each item
against its sources and deletes any that are wrong before merging. Promoting an item to a full incident record is a
separate, manual step that follows the normal review rules.

## Sources

Only official feeds and APIs are used, with no scraping. The addresses are in `scripts/weekly_sources.json`, and each
run reports whether each source answered.

| Source | What it gives | Status |
|---|---|---|
| GDELT Project DOC 2.0 API | News articles from Indian outlets (English), past 7 days | Reached on the first run (2026-10-25) but answered "too many requests"; the script now waits and retries (20, 45, 90 s) |
| PIB press-release RSS | Official Government of India releases | **Off.** Answered 403 (forbidden) to GitHub's servers on the first run; NETRA does not work around a refusal |
| CERT-In | Advisories and guidelines whose own text mentions AI (*Official watch*) | **On** since 2026-11-15, by the owner's decision. CERT-In has no feed, so the run reads its two public lists and the newest six advisories |
| METR RSS | New METR publications (Model watch) | Working: 2 items on the first run (2026-10-25) |
| MITRE ATLAS data (GitHub) | New case studies (Model watch) | Confirmed on 2026-10-25: release 2026.09, 73 case studies |

## Selection rules

The rules work on headlines only, so they are simple and can be checked.

1. **AI item:** the headline has an AI term (for example *deepfake*, *chatbot*, *voice clone*, *AI*), a harm term (for
   example *fraud*, *arrested*, *FIR*, *leak*, *court*) and a link to India. A link to India means one of these:
   - an Indian state, union territory, city or institution named in the headline, or ₹, lakh or crore;
   - an official Indian source;
   - a headline from an Indian outlet that names no other country, no global tech company (Google, OpenAI,
     Anthropic, Meta, Microsoft and others) and is not business or product news.

   An outlet's own name at the end of a headline ("… – Trak.in – Indian Business of Tech") is removed first. Business
   and product news is never an item: an IPO, a valuation, shares, or a product launch or unveiling. "Launches a
   probe" still counts.
2. **Cyber item:** the headline has a cyber term (for example *ransomware*, *data breach*, *phishing*), a link to India,
   **no** AI term (OpenAI and GPT count as AI terms), and is not a product launch. The word *cybersecurity* alone does
   not count: it names a topic, not an incident. Violence such as "hacked to death" is not counted. Cyber items are never counted as AI incidents
   and carry no risk area.
3. Headlines about the same story are grouped together. They are grouped when they share most of their key words,
   including names and figures such as "3.75 lakh", or a specific three-word phrase such as "SBI data breach". A
   phrase made only of topic words, such as "AI voice clone", does not count. A story reported by more outlets ranks
   higher. GDELT's spaced-out punctuation ("AI - generated") is put back before matching.
4. Stories that match an existing NETRA incident, by headline similarity or a shared source link, are left out and
   listed in the run notes. Stories that appeared in an earlier week are also left out.
5. At most five AI items and five cyber items are kept. **When fewer qualify, fewer are shown**: the list is never
   padded.
6. The suggested risk area comes from the same keyword lists as the NETRA check (`data/check_terms.json`).

## What is stored

For each item, NETRA stores:

- **its own short summary**: how many outlets reported it, when, and the suggested risk area;
- the **source links**, with each headline kept only as the link title, like a citation;
- the dates.

No article text is copied. The build (`scripts/build.py`) rejects a weekly file that has:

- more than five items;
- an item marked reviewed;
- a summary over 400 characters;
- stored article text;
- a cyber item that shares a source with an AI item.

The last 12 weeks are kept.

## Limits

- Headlines can mislead, and keyword rules miss stories that use other words. A person must read the sources.
- GDELT covers what it indexes; regional-language reporting is under-represented because only English is queried.
- An auto-selected item is not a finding that anything happened or that anyone did anything wrong.

## Credits

News discovery by the GDELT Project (gdeltproject.org). PIB releases © Government of India. MITRE ATLAS data is used
under the Apache License 2.0, © MITRE. METR publications are linked and cited only.
