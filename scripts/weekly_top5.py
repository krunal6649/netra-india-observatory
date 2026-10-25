#!/usr/bin/env python3
"""Weekly "This week in India" (Phase 6).

Finds up to five AI incidents in India from the past 7 days, a separate Cyber watch (kept out of AI counts) and a
Model watch (new MITRE ATLAS case studies and METR publications), and writes them to data/weekly.json.
Everything it adds is auto-selected and unreviewed. It stores NETRA's own short summary and the source links;
headlines are kept only as link titles, like a citation, and no article text is copied.

Sources (official feeds and APIs only, listed in scripts/weekly_sources.json): GDELT DOC 2.0 API, PIB RSS,
METR RSS and the MITRE ATLAS data on GitHub. A source that fails is reported and skipped; the run still completes.
No AI is used and no key is needed. Standard library only.

Usage (from the repo root):  python3 scripts/weekly_top5.py [--date YYYY-MM-DD]
The GitHub workflow .github/workflows/weekly.yml runs it every Saturday at 00:00 IST and opens a pull request.
"""
import argparse
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONFIG = json.loads((ROOT / "scripts" / "weekly_sources.json").read_text(encoding="utf-8"))
UA = "NETRA-India-Observatory-weekly/1.0 (+https://github.com/krunal6649/netra-india-observatory)"

AI_TERMS = ["artificial intelligence", "deepfake", "deep fake", "deepfakes", "ai-generated", "ai generated", "chatbot",
            "voice clone", "voice cloning", "cloned voice", "generative ai", "genai", "chatgpt", "gemini", "grok", "copilot",
            "ai tool", "ai app", "ai model", "ai-based", "ai based", "algorithm", "facial recognition", "morphed", "ai"]
HARM_TERMS = ["fraud", "scam", "scammed", "cheat", "cheated", "duped", "arrest", "arrested", "fir", "booked", "deepfake",
              "morphed", "fake", "leak", "leaked", "breach", "extortion", "extort", "sextortion", "harass", "harassment",
              "misuse", "lawsuit", "sued", "suit", "court", "ban", "banned", "blocked", "notice", "probe", "complaint",
              "victim", "victims", "lost", "loses", "duping", "impersonat", "misinformation", "wrong", "error", "bias",
              "discriminat", "suicide", "death", "injur", "obscene", "abuse", "threat", "hoax", "manipulat", "stolen"]
CYBER_TERMS = ["ransomware", "data breach", "breach", "cyber attack", "cyberattack", "cyber-attack", "phishing", "cert-in",
               "hacked", "hack", "hackers", "malware", "data leak", "ddos", "vulnerability", "spyware", "cyber fraud"]
INDIA_TERMS = ["india", "indian", "delhi", "mumbai", "bengaluru", "bangalore", "hyderabad", "chennai", "kolkata", "pune",
               "ahmedabad", "lucknow", "jaipur", "noida", "gurugram", "gurgaon", "high court", "supreme court", "police",
               "meity", "rbi", "sebi", "cert-in", "i4c", "cybercrime", "₹", "rs", "lakh", "crore", "pib", "union minister",
               "jammu", "kashmir", "ladakh", "arunachal"]
STOP = set("a an the of to in on for and or with by from at as is are was were be has have had its it this that new over after "
           "says said say amid into via up out about against how why what who will can could may".split())


class SourceError(Exception):
    pass


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception as e:  # network errors are reported per source, never fatal
        raise SourceError(f"{type(e).__name__}: {str(e)[:160]}") from None


def has(text, terms):
    """Terms found in text, matched on word starts (so 'impersonat' finds 'impersonation')."""
    t = text.lower()
    return [w for w in terms if re.search(r"(?<![\w])" + re.escape(w) + (r"" if w.endswith(("at", "injur", "discriminat", "manipulat", "hack")) else r"(?![\w])"), t)]


def tokens(title):
    return {w for w in re.findall(r"[a-z0-9₹]+", title.lower()) if w not in STOP and len(w) > 2}


def same_story(a, b):
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return False
    jac = len(ta & tb) / len(ta | tb)
    return jac >= 0.4 or difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() >= 0.75


def gdelt_date(s):
    try:
        return datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).date().isoformat()
    except (TypeError, ValueError):
        return ""


def gdelt(query, get, start, end, sleep=time.sleep):
    """GDELT asks for one request every few seconds and answers 429 when busy; wait and try again a few times."""
    g = CONFIG["gdelt"]
    q = urllib.parse.urlencode({"query": query, "mode": "ArtList", "format": "json", "maxrecords": g["maxrecords"], "sort": "DateDesc",
                                "startdatetime": start.strftime("%Y%m%d") + "000000", "enddatetime": end.strftime("%Y%m%d") + "235959"})
    waits = list(g.get("retry_waits", []))
    while True:
        try:
            raw = get(g["url"] + "?" + q)
            break
        except SourceError as e:
            if "429" not in str(e) or not waits:
                raise
            sleep(waits.pop(0))
    try:
        data = json.loads(raw.decode("utf-8", "replace") or "{}")
    except json.JSONDecodeError:
        raise SourceError("GDELT did not return JSON: " + raw[:120].decode("utf-8", "replace")) from None
    return [{"title": a.get("title", "").strip(), "url": a.get("url", ""), "domain": a.get("domain", ""),
             "date": gdelt_date(a.get("seendate")), "via": "GDELT"} for a in data.get("articles", []) if a.get("url", "").startswith("http")]


def feed_items(raw):
    """RSS 2.0 or Atom: [{title, url, date}]. Undated items get date ''."""
    root = ElementTree.fromstring(raw)
    out = []
    for it in root.iter():
        tag = it.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        get = lambda name: next((c for c in it if c.tag.split("}")[-1] == name), None)
        title = (get("title").text or "").strip() if get("title") is not None else ""
        link = get("link")
        url = (link.text or "").strip() if link is not None and (link.text or "").strip() else (link.get("href", "") if link is not None else "")
        d = get("pubDate") if get("pubDate") is not None else (get("updated") if get("updated") is not None else get("published"))
        when = ""
        if d is not None and d.text:
            try:
                when = parsedate_to_datetime(d.text.strip()).date().isoformat()
            except (TypeError, ValueError, IndexError):
                try:
                    when = datetime.fromisoformat(d.text.strip().replace("Z", "+00:00")).date().isoformat()
                except ValueError:
                    when = ""
        if title and url:
            out.append({"title": re.sub(r"\s+", " ", title), "url": url.strip(), "date": when})
    return out


def atlas_studies(get):
    a = CONFIG["atlas"]
    raw = get(a["pointer"]).decode("utf-8", "replace")
    if len(raw) < 200 and raw.strip().endswith(".yaml"):  # the 'latest' file names the dated release
        raw = get(a["base"] + raw.strip()).decode("utf-8", "replace")
    version = (re.search(r"^  version: '?([^'\n]+)'?", raw, re.M) or [None, ""])[1]
    m = re.search(r"^case-studies:\n(.*?)(?=^\S)", raw, re.S | re.M)
    studies = []
    for block in re.split(r"^  (?=AML\.CS\d+:)", m.group(1) if m else "", flags=re.M):
        sid = re.match(r"(AML\.CS\d+):", block)
        if not sid:
            continue
        f = lambda k: (re.search(r"^    " + k + r": '?(.*?)'?$", block, re.M) or [None, ""])[1]
        studies.append({"id": sid[1], "name": f("name"), "created": f("created-date"), "target": f("target")})
    return version, studies


def india_nexus(title, states):
    return has(title, INDIA_TERMS) + [s for s in states if s.lower() in title.lower()]


def cluster(items):
    groups = []
    for it in items:
        for g in groups:
            if any(same_story(it["title"], x["title"]) for x in g):
                g.append(it)
                break
        else:
            groups.append([it])
    return groups


def risk_areas(text, terms):
    hits = []
    for sid, words in terms["risk_areas"].items():
        n = sum(1 for w in words if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", text, 0 if (w.isupper() and len(w) > 1) else re.I))
        if n:
            hits.append((n, sid))
    return [s for _, s in sorted(hits, key=lambda x: (-x[0], x[1]))[:2]]


def summarise(group, areas, sub_names, kind):
    doms = sorted({x["domain"] or urllib.parse.urlparse(x["url"]).hostname or "" for x in group})
    dates = sorted(x["date"] for x in group if x["date"])
    span = (f"on {dates[0]}" if dates[0] == dates[-1] else f"between {dates[0]} and {dates[-1]}") if dates else "this week"
    n = len(group)
    s = f"{n} report{'s' if n != 1 else ''} from {', '.join(doms[:4])}{' and others' if len(doms) > 4 else ''} {span}."
    if kind == "ai":
        s += (f" NETRA's keyword match suggests risk area {areas[0]} ({sub_names[areas[0]]})." if areas else " No NETRA risk area matched the headlines.")
        s += " Auto-selected and not yet checked by a person: open the sources for the facts."
    else:
        s += " Cyber security item, listed separately and not counted as an AI incident. Not checked by a person."
    return s


def select(articles, kind, existing, seen_urls, states, terms, sub_names, limit=5):
    """Rank candidate stories. kind 'ai' needs an AI term, a harm term and an India link; 'cyber' needs a cyber term,
    an India link and no AI term (so it never inflates AI counts)."""
    cands, skipped = [], []
    for a in articles:
        if not a["title"] or a["url"] in seen_urls:
            continue
        t = a["title"]
        ai, harm, cyber, ind = has(t, AI_TERMS), has(t, HARM_TERMS), has(t, CYBER_TERMS), india_nexus(t, states)
        ok = (ai and harm and ind) if kind == "ai" else (cyber and ind and not ai)
        if ok:
            cands.append({**a, "_score": len(set(harm)) + len(set(ai)) + (2 if a.get("official") else 0) if kind == "ai" else len(set(cyber)) + (2 if a.get("official") else 0)})
    picked = []
    for g in cluster(sorted(cands, key=lambda x: -x["_score"])):
        lead = g[0]
        dup = next((i for i in existing if same_story(lead["title"], i["title"]) or any(s["url"] == x["url"] for s in i["sources"] for x in g)), None)
        if dup:
            skipped.append(f"{lead['title'][:80]}: matches NETRA record {dup['id']}")
            continue
        doms = {x["domain"] for x in g}
        score = max(x["_score"] for x in g) + 2 * (len(doms) - 1)
        if score < (3 if kind == "ai" else 1):
            continue
        areas = risk_areas(" ".join(x["title"] for x in g), terms) if kind == "ai" else []
        picked.append({"title": lead["title"], "summary": summarise(g, areas, sub_names, kind), "risk_areas": areas,
                       "sources": [{"title": x["title"][:200], "url": x["url"], "domain": x["domain"], "date": x["date"], "via": x["via"]} for x in g[:6]],
                       "score": score, "auto_selected": True, "review": "unreviewed"})
    picked.sort(key=lambda x: -x["score"])
    return picked[:limit], skipped


def run(today, get=fetch, sleep=time.sleep):
    end = today - timedelta(days=1)
    start = today - timedelta(days=CONFIG["window_days"])
    india = json.loads((DATA / "india.json").read_text(encoding="utf-8"))
    terms = json.loads((DATA / "check_terms.json").read_text(encoding="utf-8"))
    tax = json.loads((DATA / "taxonomy.json").read_text(encoding="utf-8"))
    models = json.loads((DATA / "models.json").read_text(encoding="utf-8"))
    sub_names = {s["id"]: s["name"] for d in tax["domains"] for s in d["subs"]}
    states = india["states_uts"]["states"] + india["states_uts"].get("uts", [])
    path = DATA / "weekly.json"
    store = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"meta": {}, "weeks": []}
    seen = {s["url"] for w in store["weeks"] if w["week_start"] != start.isoformat() for k in ("top", "cyber") for it in w[k] for s in it["sources"]}
    report, ai_items, cyber_items, model_items, notes = [], [], [], [], []

    g = CONFIG["gdelt"]
    for label, q, bucket in (("GDELT: AI news", g["ai_query"], ai_items), ("GDELT: cyber news", g["cyber_query"], cyber_items)):
        try:
            arts = gdelt(q, get, start, end, sleep)
            bucket.extend(arts)
            report.append({"name": label, "url": g["url"], "status": "ok", "items": len(arts)})
        except SourceError as e:
            report.append({"name": label, "url": g["url"], "status": "failed", "items": 0, "error": str(e)})
        sleep(g["pause_seconds"])

    for f in CONFIG["feeds"]:
        if not f["enabled"]:
            report.append({"name": f["name"], "url": f["url"], "status": "off", "items": 0, "error": f["checked"]})
            continue
        try:
            items = [x for x in feed_items(get(f["url"])) if not x["date"] or start.isoformat() <= x["date"] <= end.isoformat()]
            undated = sum(1 for x in items if not x["date"])
            report.append({"name": f["name"], "url": f["url"], "status": "ok", "items": len(items), **({"error": f"{undated} undated items kept"} if undated else {})})
        except (SourceError, ElementTree.ParseError) as e:
            report.append({"name": f["name"], "url": f["url"], "status": "failed", "items": 0, "error": str(e)[:200]})
            continue
        for x in items:
            if f["kind"] == "india_official":
                dom = urllib.parse.urlparse(x["url"]).hostname or "pib.gov.in"
                rec = {**x, "domain": dom, "via": f["name"], "official": True}
                ai_items.append(rec)
                cyber_items.append(rec)
            elif f["kind"] == "model_tests" and x["url"] not in seen:
                model_items.append({"kind": "METR publication", "title": x["title"][:200], "url": x["url"], "date": x["date"],
                                    "note": "New METR publication. Cite and summarise only; NETRA has not read or mapped it yet.", "review": "unreviewed"})

    try:
        version, studies = atlas_studies(get)
        used = {t.get("atlas") for m in models["models"] for t in m["tests"]}
        new = [s for s in studies if s["created"] and start.isoformat() <= s["created"] <= end.isoformat() and s["id"] not in used]
        for s in new:
            model_items.append({"kind": "MITRE ATLAS case study", "title": f"{s['id']} {s['name']}"[:200], "url": CONFIG["atlas"]["study_url"] + s["id"],
                                "date": s["created"], "note": f"New ATLAS case study{(' (target: ' + s['target'] + ')') if s['target'] else ''}. Apache 2.0, © MITRE. Not yet in NETRA's register.", "review": "unreviewed"})
        report.append({"name": f"{CONFIG['atlas']['name']} (release {version or 'unknown'})", "url": CONFIG["atlas"]["pointer"], "status": "ok", "items": len(new)})
        notes.append(f"MITRE ATLAS release {version}: {len(studies)} case studies in total, {sum(1 for s in studies if s['id'] not in used)} not yet in NETRA's model register.")
    except SourceError as e:
        report.append({"name": CONFIG["atlas"]["name"], "url": CONFIG["atlas"]["pointer"], "status": "failed", "items": 0, "error": str(e)})

    pool = ai_items + [x for x in cyber_items if x not in ai_items]   # each pool's own rules decide what is AI and what is cyber
    top, skipped_ai = select(pool, "ai", india["incidents"], seen, states, terms, sub_names)
    cyber, skipped_cy = select(pool, "cyber", india["incidents"], seen | {s["url"] for t in top for s in t["sources"]}, states, terms, sub_names)
    for k, it in enumerate(top, 1):
        it["id"] = f"W-{start.isoformat()}-{k}"
    for k, it in enumerate(cyber, 1):
        it["id"] = f"C-{start.isoformat()}-{k}"
    if len(top) < 5:
        notes.append(f"Only {len(top)} AI item{'s' if len(top) != 1 else ''} met the selection rules this week; NETRA does not pad the list.")
    notes += [f"Not listed (already a NETRA record): {s}" for s in skipped_ai + skipped_cy]
    week = {"week_start": start.isoformat(), "week_end": end.isoformat(), "generated": today.isoformat(), "sources": report,
            "top": top, "cyber": cyber, "models": model_items[:10], "notes": notes, "review": "unreviewed"}
    store["meta"] = {"title": "This week in India", "method": "docs/weekly-method.md",
                     "note": "Auto-selected from official feeds and APIs; unreviewed. NETRA's own summaries; headlines only as link titles.",
                     "credit": CONFIG["gdelt"]["credit"]}
    store["weeks"] = [week] + [w for w in store["weeks"] if w["week_start"] != week["week_start"]]
    store["weeks"] = store["weeks"][:CONFIG["keep_weeks"]]
    return store, week


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--date", help="run as if today were this date (YYYY-MM-DD); default today in IST")
    a = ap.parse_args(argv)
    today = date.fromisoformat(a.date) if a.date else datetime.now(timezone(timedelta(hours=5, minutes=30))).date()
    store, week = run(today)
    (DATA / "weekly.json").write_text(json.dumps(store, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Week {week['week_start']} to {week['week_end']}: {len(week['top'])} AI items, {len(week['cyber'])} cyber items, {len(week['models'])} model items.")
    for s in week["sources"]:
        print(f"  [{s['status']}] {s['name']}: {s['items']} items" + (f" ({s['error']})" if s.get("error") else ""))
    for n in week["notes"]:
        print("  note: " + n)
    if all(s["status"] != "ok" for s in week["sources"]):
        print("Every source failed; nothing to review.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
