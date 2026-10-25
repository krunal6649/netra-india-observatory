# This week in India: method

The weekly update finds **up to five AI incidents in India from the past seven days**, a separate **Cyber watch** and a
**Model watch**. It is produced by `scripts/weekly_top5.py` (standard-library Python, no AI, no API key) and shown on
the Home page. Every item is labelled **Auto-selected, unreviewed**.

## When it runs

`.github/workflows/weekly.yml` runs every **Saturday at 00:00 IST** (cron `30 18 * * 5`, which is 18:30 UTC on
Friday). It can also be started by hand from *Actions › Weekly update (unreviewed) › Run workflow*. GitHub sometimes
starts scheduled runs a few minutes late. If the repository has no activity for 60 days, GitHub pauses scheduled
workflows. Re-enable it from the Actions tab.

Each run opens a **pull request**. Nothing is merged automatically, and nothing becomes a NETRA incident record by
itself. The owner checks each item against its sources and deletes any that are wrong before merging. Promoting an
item to a full incident record is a separate, manual step that follows the normal review rules.

## Sources

Only official feeds and APIs are used, with no scraping. The addresses are in `scripts/weekly_sources.json`, and each
run reports whether each source answered.

| Source | What it gives | Status |
|---|---|---|
| GDELT Project DOC 2.0 API | News articles from Indian outlets (English), past 7 days | Reached on the first run (2026-10-25) but answered "too many requests"; the script now waits and retries (20, 45, 90 s) |
| PIB press-release RSS | Official Government of India releases | **Off.** Answered 403 (forbidden) to GitHub's servers on the first run; NETRA does not work around a refusal |
| CERT-In | Advisories | **Off.** No official feed address could be confirmed |
| METR RSS | New METR publications (Model watch) | Working: 2 items on the first run (2026-10-25) |
| MITRE ATLAS data (GitHub) | New case studies (Model watch) | Confirmed on 2026-10-25: release 2026.09, 73 case studies |

## Selection rules

The rules work on headlines only, so they are simple and can be checked.

1. **AI item:** the headline has an AI term (for example *deepfake*, *chatbot*, *voice clone*, *AI*), a harm term (for
   example *fraud*, *arrested*, *FIR*, *leak*, *court*) and a link to India (an Indian state, union territory or city;
   Indian institutions; ₹, lakh or crore).
2. **Cyber item:** the headline has a cyber term (for example *ransomware*, *data breach*, *phishing*), a link to India,
   and **no** AI term. Cyber items are never counted as AI incidents and carry no risk area.
3. Headlines about the same story are grouped together. A story reported by more outlets ranks higher, and PIB
   releases get a small boost.
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
