#!/usr/bin/env python3
"""Validate the NETRA India data files and build the single-page site.

Usage (from the netra-india folder):
    python3 scripts/build.py           # check data, write dist/index.html
    python3 scripts/build.py --check   # check data only

Standard library only. Nothing to install.
"""
import difflib
import itertools
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATE = ROOT / "web" / "template.html"
OUT = ROOT / "dist" / "index.html"
PLACEHOLDER = "/*__DATA__*/null"
STAGE_STATES = {"done", "secondary", "partial", "draft", "open", "contested", "possible", "n/a"}
VERIFIED = {"yes", "partial", "no"}
ACT_NO = re.compile(r"^Act \d+ of (19|20)\d\d$")
NOTIFICATION_NO = re.compile(r"^(G\.S\.R\.|S\.O\.) \d+\(E\)$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TITLE_SIMILARITY = 0.75  # titles this alike are treated as the same case unless marked distinct
DOC_KINDS = {"order", "judgment", "petition", "notice"}
REVIEWED = {"human_reviewed", "published"}
EMAIL = re.compile(r"^[^@\s<>\"]+@[^@\s<>\"]+\.[A-Za-z]{2,}$")


def is_date(s):
    if not isinstance(s, str) or not ISO_DATE.match(s):
        return False
    try:
        date.fromisoformat(s)
    except ValueError:
        return False
    return True


def check_duplicates(incidents, errors):
    """Stop the same case from being added twice, for example by a later batch or the weekly feed.
    Two records clash if they cite the same source or court document, or have near-identical titles.
    A record can list ids in 'distinct_from' after a person has checked that the cases really differ."""
    def norm_url(u):
        return u.split("#")[0].rstrip("/").replace("://www.", "://").replace("/amp/", "/").lower()

    def norm_title(t):
        return " ".join(re.sub(r"[^\w₹]+", " ", t.lower()).split())

    def allowed(a, b):
        return b["id"] in a.get("distinct_from", []) or a["id"] in b.get("distinct_from", [])

    owner = {}
    for inc in incidents:
        urls = {norm_url(x["url"]) for x in inc["sources"]} | {norm_url(x["url"]) for x in inc.get("court_documents", [])}
        for u in urls:
            other = owner.setdefault(u, inc)
            if other is not inc and not allowed(inc, other):
                errors.append(f"{inc['id']}: possible duplicate of {other['id']} (both cite {u})")
    for a, b in itertools.combinations(incidents, 2):
        r = difflib.SequenceMatcher(None, norm_title(a["title"]), norm_title(b["title"])).ratio()
        if r >= TITLE_SIMILARITY and not allowed(a, b):
            errors.append(f"{b['id']}: possible duplicate of {a['id']} (titles {r:.0%} alike)")
    ids = {i["id"] for i in incidents}
    for inc in incidents:
        for x in inc.get("distinct_from", []):
            if x not in ids:
                errors.append(f"{inc['id']}: distinct_from names unknown incident {x}")


def check_documents(inc, errors):
    """Official court documents shown under Location & jurisdiction."""
    for doc in inc.get("court_documents", []):
        label = f"{inc['id']}: court document {doc.get('title', '?')}"
        for f in ("title", "court", "date", "kind", "url", "host", "opened", "note"):
            if not doc.get(f):
                errors.append(f"{label} missing {f}")
        if doc.get("kind") and doc["kind"] not in DOC_KINDS:
            errors.append(f"{label} kind must be one of {sorted(DOC_KINDS)}")
        if doc.get("date") and not is_date(doc["date"]):
            errors.append(f"{label} date must be an ISO date")
        if doc.get("url") and not doc["url"].startswith("https://"):
            errors.append(f"{label} url must be https")
        if doc.get("opened") and doc["opened"] not in ("yes", "no"):
            errors.append(f"{label} opened must be 'yes' or 'no'")
        # A document can only be shown as checked when someone says who opened it and when
        if doc.get("opened") == "yes" and (not doc.get("checked_by") or not is_date(doc.get("checked_on"))):
            errors.append(f"{label} opened 'yes' needs checked_by and an ISO checked_on date")
        # Only court websites count as official copies
        if doc.get("host") == "official" and doc.get("url") and not urlparse(doc["url"]).hostname.endswith((".nic.in", ".gov.in")):
            errors.append(f"{label} is marked official but is not on a .nic.in or .gov.in court site")


def check_instrument_detail(i, errors):
    """Optional structured fields added in v0.2: act number, Gazette notifications, cases."""
    iid = i["id"]
    if i["verified"] not in VERIFIED:
        errors.append(f"{iid}: verified must be one of {sorted(VERIFIED)}")
    # A record marked verified must point at a specific document, not a site's home page
    if i["verified"] == "yes" and urlparse(i["url"]).path.strip("/") == "":
        errors.append(f"{iid}: verified 'yes' needs a specific document URL, not a home page")
    if "act_no" in i and not ACT_NO.match(i["act_no"]):
        errors.append(f"{iid}: act_no must look like 'Act 45 of 2023'")
    if "checked" in i and not is_date(i["checked"]):
        errors.append(f"{iid}: checked must be an ISO date")
    if "gazette_url" in i and not i["gazette_url"].startswith("https://"):
        errors.append(f"{iid}: gazette_url must be https")
    for n in i.get("notifications", []):
        if not NOTIFICATION_NO.match(n.get("no", "")):
            errors.append(f"{iid}: notification number '{n.get('no')}' must look like 'G.S.R. 139(E)' or 'S.O. 2351(E)'")
        for k in ("date", "effective"):
            if k in n and not is_date(n[k]):
                errors.append(f"{iid}: notification {n.get('no')} {k} must be an ISO date")
        if not n.get("what"):
            errors.append(f"{iid}: notification {n.get('no')} needs a 'what' description")
    for c in i.get("cases", []):
        for f in ("name", "citation", "court", "date", "holding", "verified", "note"):
            if not c.get(f):
                errors.append(f"{iid}: case {c.get('name', '?')} missing {f}")
        if c.get("date") and not is_date(c["date"]):
            errors.append(f"{iid}: case {c.get('name')} date must be an ISO date")
        if c.get("verified") and c["verified"] not in VERIFIED:
            errors.append(f"{iid}: case {c.get('name')} verified must be one of {sorted(VERIFIED)}")
        for k in ("url", "report_url"):
            if k in c and not c[k].startswith("https://"):
                errors.append(f"{iid}: case {c.get('name')} {k} must be https")


class ValidationError(Exception):
    pass


# ---- Version 3: additive assessment fields (all optional; absent means "not yet assessed") ----
NOT_ASSESSED = "not yet assessed"
AI_ROLES = {"confirmed", "suspected", "not established", "not AI"}
CROSSWALK = {"NIST-AI-RMF", "ISO-42001", "OWASP-LLM-2025", "OWASP-LLM-2026"}
NIST_FUNCTIONS = {"GOVERN", "MAP", "MEASURE", "MANAGE"}


def failure_mode_ids():
    """Allowed failure-mode tags, read from the two reference lists in data/."""
    owasp, atlas = load("owasp_llm_top10.json"), load("atlas_techniques.json")
    ids = {ed: dict(e["items"]) for ed, e in owasp["editions"].items()}
    ids["MITRE-ATLAS"] = dict(atlas["techniques"])
    return ids


def check_v3_fields(inc, harms, errors, fm_ids=None):
    """Check an incident's optional `assessment` block. Records without one pass unchanged."""
    a = inc.get("assessment")
    if a is None:
        return
    iid = f"{inc['id']} assessment"
    if not isinstance(a, dict):
        errors.append(f"{iid}: must be an object")
        return
    known = {"review", "reviewed_by", "reviewed_on", "assessed_on", "ai_role", "ai_system", "impact",
             "evidence_provenance", "failure_modes", "crosswalk"}
    for k in sorted(set(a) - known):
        errors.append(f"{iid}: unknown field {k}")
    # The assessment has its own review status; a reviewed incident does not make its new fields reviewed
    if a.get("review") not in {"unreviewed", "source_checked", "human_reviewed", "published"}:
        errors.append(f"{iid}: review must be unreviewed, source_checked, human_reviewed or published")
    if a.get("review") in REVIEWED and (not a.get("reviewed_by") or not is_date(a.get("reviewed_on"))):
        errors.append(f"{iid}: a reviewed assessment needs reviewed_by and an ISO reviewed_on date")
    if a.get("review") not in REVIEWED and (a.get("reviewed_by") or a.get("reviewed_on")):
        errors.append(f"{iid}: reviewed_by / reviewed_on set on an assessment that is not reviewed")
    if "assessed_on" in a and not is_date(a["assessed_on"]):
        errors.append(f"{iid}: assessed_on must be an ISO date")
    cited = {s["url"] for s in inc.get("sources", [])} | {d.get("url") for d in inc.get("court_documents", [])}

    def text(v, label):
        if not isinstance(v, str) or not v.strip():
            errors.append(f"{iid}: {label} must be text (use '{NOT_ASSESSED}' if unknown)")

    role = a.get("ai_role", NOT_ASSESSED)
    if role != NOT_ASSESSED:
        if not isinstance(role, dict) or role.get("value") not in AI_ROLES:
            errors.append(f"{iid}: ai_role value must be one of {sorted(AI_ROLES)}")
        elif not role.get("basis"):
            errors.append(f"{iid}: ai_role needs a basis saying which source supports it")
    sysrec = a.get("ai_system", NOT_ASSESSED)
    if sysrec != NOT_ASSESSED:
        if not isinstance(sysrec, dict):
            errors.append(f"{iid}: ai_system must be an object")
        else:
            for f in ("name", "developer", "deployer", "version"):
                text(sysrec.get(f, NOT_ASSESSED), f"ai_system.{f}")
    imp = a.get("impact", NOT_ASSESSED)
    if imp != NOT_ASSESSED:
        if not isinstance(imp, dict):
            errors.append(f"{iid}: impact must be an object")
        else:
            text(imp.get("who", NOT_ASSESSED), "impact.who")
            for h in imp.get("harm_types", []):
                if h not in harms:
                    errors.append(f"{iid}: unknown harm type {h}")
            sc = imp.get("scale", NOT_ASSESSED)
            if sc not in (NOT_ASSESSED, "not stated in sources"):
                if not isinstance(sc, dict) or not sc.get("value") or sc.get("source") not in cited:
                    errors.append(f"{iid}: impact.scale needs a value and a source that is one of this incident's sources")
    prov = a.get("evidence_provenance", NOT_ASSESSED)
    if prov != NOT_ASSESSED:
        if not isinstance(prov, dict):
            errors.append(f"{iid}: evidence_provenance must be an object")
        else:
            for f in ("produced_by", "reported_by", "establishes", "does_not_establish"):
                text(prov.get(f, NOT_ASSESSED), f"evidence_provenance.{f}")
    fms = a.get("failure_modes", NOT_ASSESSED)
    if fms != NOT_ASSESSED:
        if not isinstance(fms, list):
            errors.append(f"{iid}: failure_modes must be a list or '{NOT_ASSESSED}'")
        else:
            fm_ids = fm_ids or failure_mode_ids()
            for t in fms:
                fw, tid = t.get("framework"), t.get("id")
                if fw not in fm_ids:
                    errors.append(f"{iid}: failure-mode framework must be one of {sorted(fm_ids)}")
                elif tid not in fm_ids[fw]:
                    errors.append(f"{iid}: {tid} is not an item of {fw}")
                elif t.get("name", fm_ids[fw][tid]) != fm_ids[fw][tid]:
                    errors.append(f"{iid}: {tid} is named '{fm_ids[fw][tid]}' in {fw}, not '{t.get('name')}'")
                # Only where a cited source supports it: the tag must point at one of the incident's own sources
                if t.get("source") not in cited or not t.get("basis"):
                    errors.append(f"{iid}: failure mode {tid} needs a basis and a source that is one of this incident's sources")
    cw = a.get("crosswalk", NOT_ASSESSED)
    if cw != NOT_ASSESSED:
        if not isinstance(cw, list):
            errors.append(f"{iid}: crosswalk must be a list or '{NOT_ASSESSED}'")
        else:
            for t in cw:
                if t.get("framework") not in CROSSWALK:
                    errors.append(f"{iid}: crosswalk framework must be one of {sorted(CROSSWALK)}")
                elif t["framework"] == "NIST-AI-RMF" and t.get("label") not in NIST_FUNCTIONS:
                    errors.append(f"{iid}: a NIST AI RMF crosswalk label must be one of {sorted(NIST_FUNCTIONS)}")
                elif not t.get("label"):
                    errors.append(f"{iid}: crosswalk needs a label")
                if not t.get("why"):
                    errors.append(f"{iid}: crosswalk {t.get('label')} needs a 'why' (it is NETRA's mapping, not a finding)")


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


ROLES = {"enforces", "adjudicates", "regulates", "supports"}


def check_directory(directory, india, errors):
    """data/authorities.json: the 'Who to approach' directory (Phase 3)."""
    meta, bodies = directory["meta"], directory["bodies"]
    ins = {i["id"] for i in india["instruments"]}
    places = set(india["states_uts"]["states"]) | set(india["states_uts"]["union_territories"])
    ids = set()
    for x in bodies:
        bid = x.get("id", "?")
        if bid in ids:
            errors.append(f"directory: duplicate id {bid}")
        ids.add(bid)
        for f in ("name", "level", "place", "group", "role", "can_do", "how_to_report", "verified", "source"):
            if not x.get(f):
                errors.append(f"directory {bid}: missing {f}")
        if x.get("role") not in ROLES:
            errors.append(f"directory {bid}: role must be one of {sorted(ROLES)}")
        if x.get("verified") not in VERIFIED:
            errors.append(f"directory {bid}: verified must be one of {sorted(VERIFIED)}")
        if x.get("level") == "union":
            if x.get("place") != "Union" or x.get("group") not in meta["union_groups"]:
                errors.append(f"directory {bid}: a Union body needs place 'Union' and a Union group")
        elif x.get("level") == "state":
            if x.get("place") not in places or x.get("group") not in meta["state_groups"]:
                errors.append(f"directory {bid}: a state body needs one of the 36 states or UTs and a state group")
        else:
            errors.append(f"directory {bid}: level must be 'union' or 'state'")
        if x.get("url") is not None and not str(x["url"]).startswith("https://"):
            errors.append(f"directory {bid}: url must be https or null")
        # A body shown as checked needs a link, a checker and a date
        if x.get("verified") == "yes" and (not x.get("url") or not x.get("checked_by") or not is_date(x.get("checked_on"))):
            errors.append(f"directory {bid}: verified 'yes' needs a url, checked_by and an ISO checked_on date")
        for law in x.get("laws", []):
            if law not in ins:
                errors.append(f"directory {bid}: unknown instrument {law}")
    for p in places:
        if not any(x.get("place") == p for x in bodies):
            errors.append(f"directory: no bodies listed for {p}")
    # Every incident's reporting route must lead to a body in the directory
    auth = {a["id"]: a for a in india["authorities"]}
    for a in auth.values():
        for t in a.get("directory", []):
            if t not in ids:
                errors.append(f"{a['id']}: directory link {t} does not exist")
        if not a.get("directory") and not a.get("directory_state"):
            errors.append(f"{a['id']}: needs a directory or directory_state link")
    by_place = {(x["place"], x["id"].rsplit("-", 1)[-1]) for x in bodies if x.get("level") == "state"}
    for inc in india["incidents"]:
        place = inc["state"].split(" (")[0]
        for a in inc["netra"]["authorities"]:
            kind = auth.get(a, {}).get("directory_state")
            if kind and place != "National" and (place, kind) not in by_place:
                errors.append(f"{inc['id']}: {a} points to {place}, which has no {kind} body in the directory")
    return ids


LAW_LABELS = {"possible", "interpretive", "gap"}


def check_models(models, india, glob, directory, errors):
    """data/models.json: the model register (Phase 5). What testers found and NETRA's analysis stay separate."""
    ins = {i["id"] for i in india["instruments"]}
    incs = {i["id"] for i in india["incidents"]}
    bodies = {b["id"] for b in directory["bodies"]}
    reports = {r["id"] for r in glob["reports"]}
    maps = {m["id"] for m in glob["mappings"]}
    gaps = {g["id"] for g in glob["gaps"]} | {g["id"] for g in india["gaps"]}
    seen = set()
    for m in models["models"]:
        mid = m.get("id", "?")
        if mid in seen:
            errors.append(f"models: duplicate id {mid}")
        seen.add(mid)
        for f in ("name", "developer", "release_note", "netra", "review"):
            if not m.get(f):
                errors.append(f"{mid}: missing {f}")
        if m.get("release_date") is not None and not (is_date(m["release_date"]) or re.match(r"^\d{4}-\d{2}$", str(m["release_date"]))):
            errors.append(f"{mid}: release_date must be an ISO date or null")
        if m.get("release_date") and not m.get("release_source"):
            errors.append(f"{mid}: a release date needs a release_source")
        for t in m.get("tests", []):
            for f in ("by", "what", "found", "licence", "date"):
                if not t.get(f):
                    errors.append(f"{mid}: test missing {f}")
            if t.get("report") and t["report"] not in reports:
                errors.append(f"{mid}: unknown report {t['report']}")
            if not t.get("report") and not str(t.get("url", "")).startswith("https://"):
                errors.append(f"{mid}: a test needs a METR report id or an https source url")
        n = m.get("netra", {})
        for f in ("risk_areas", "laws", "authorities", "unknowns", "overclaim"):
            if not n.get(f):
                errors.append(f"{mid}: NETRA analysis missing {f}")
        if m.get("tests") and "not evidence of real-world harm" not in n.get("overclaim", ""):
            errors.append(f"{mid}: overclaim must say a test result is not evidence of real-world harm")
        for l in n.get("laws", []):
            if l.get("instrument") not in ins:
                errors.append(f"{mid}: unknown instrument {l.get('instrument')}")
            if l.get("label") not in LAW_LABELS:
                errors.append(f"{mid}: law label must be one of {sorted(LAW_LABELS)}")
            if not l.get("why"):
                errors.append(f"{mid}: each law needs a 'why'")
        for a in n.get("authorities", []):
            if a not in bodies:
                errors.append(f"{mid}: unknown directory body {a}")
        for x in n.get("mappings", []):
            if x not in maps:
                errors.append(f"{mid}: unknown mapping {x}")
        for x in n.get("gaps", []):
            if x not in gaps:
                errors.append(f"{mid}: unknown gap {x}")
        for x in m.get("incidents", []):
            if x not in incs:
                errors.append(f"{mid}: unknown incident {x}")
        if m.get("review") not in india["review_statuses"]:
            errors.append(f"{mid}: bad review status")
        if m.get("review") in REVIEWED and (not m.get("reviewed_by") or not is_date(m.get("reviewed_on"))):
            errors.append(f"{mid}: a reviewed model needs reviewed_by and reviewed_on")


def check_drafts(errors):
    """data/drafts/*.json: AI-assisted drafts opened by the owner's workflow. They can never be marked reviewed."""
    for p in sorted((DATA / "drafts").glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("review") != "unreviewed" or not d.get("ai_generated"):
            errors.append(f"drafts/{p.name}: an AI draft must be ai_generated and 'unreviewed'")
        if any(q.get("verified") is not True for q in d.get("quotes", [])):
            errors.append(f"drafts/{p.name}: every kept quote must have been verified word for word")


def check_terms(terms, subs, india, errors):
    """data/check_terms.json: the keyword lists behind the in-browser NETRA check on an added report."""
    ins = {i["id"] for i in india["instruments"]}
    if not isinstance(terms.get("meta", {}).get("min_hits"), int) or terms["meta"]["min_hits"] < 1:
        errors.append("check_terms: meta.min_hits must be a whole number of at least 1")
    for kind, known in (("risk_areas", subs), ("instruments", ins)):
        block = terms.get(kind, {})
        for k, words in block.items():
            if k not in known:
                errors.append(f"check_terms: unknown {kind} id {k}")
            if not words or not all(isinstance(w, str) and w.strip() for w in words):
                errors.append(f"check_terms: {kind} {k} needs a list of non-empty terms")
        for k in sorted(known - set(block)):
            errors.append(f"check_terms: {kind} {k} has no terms")


def check_weekly(weekly, india, subs, errors):
    """data/weekly.json from scripts/weekly_top5.py: auto-selected, unreviewed, at most 5 AI items, cyber kept apart."""
    for w in weekly.get("weeks", []):
        wid = f"weekly {w.get('week_start')}"
        if not (is_date(w.get("week_start")) and is_date(w.get("week_end")) and w["week_start"] <= w["week_end"]):
            errors.append(f"{wid}: week_start and week_end must be ISO dates in order")
        if len(w.get("top", [])) > 5:
            errors.append(f"{wid}: at most 5 AI items")
        if len(w.get("cyber", [])) > 5:
            errors.append(f"{wid}: at most 5 cyber items")
        top_urls = {x["url"] for it in w.get("top", []) for x in it.get("sources", [])}
        for kind in ("top", "cyber"):
            for it in w.get(kind, []):
                iid = f"{wid} {it.get('id', '?')}"
                if it.get("auto_selected") is not True or it.get("review") != "unreviewed":
                    errors.append(f"{iid}: must be auto-selected and 'unreviewed'")
                if not it.get("summary") or len(it["summary"]) > 400:
                    errors.append(f"{iid}: needs NETRA's own summary of at most 400 characters")
                if not it.get("sources") or any(not str(x.get("url", "")).startswith(("https://", "http://")) for x in it["sources"]):
                    errors.append(f"{iid}: every item needs source links")
                if set(it) & {"text", "body", "content", "article"}:
                    errors.append(f"{iid}: article text must not be stored")
                if subs and any(r not in subs for r in it.get("risk_areas", [])):
                    errors.append(f"{iid}: unknown risk area")
                if kind == "cyber" and (it.get("risk_areas") or top_urls & {x["url"] for x in it["sources"]}):
                    errors.append(f"{iid}: cyber items stay out of AI counts (no risk areas, no shared sources)")
        for m in w.get("models", []):
            if m.get("review") != "unreviewed" or not str(m.get("url", "")).startswith("https://"):
                errors.append(f"{wid} model item {m.get('title', '?')[:40]}: must be unreviewed with an https link")


def validate(tax, india, glob, directory=None, models=None, terms=None, weekly=None):
    if directory is None:
        directory = load("authorities.json")
    if models is None:
        models = load("models.json")
    if terms is None:
        terms = load("check_terms.json")
    if weekly is None:
        weekly = load("weekly.json") if (DATA / "weekly.json").exists() else {"weeks": []}
    errors, warnings = [], []
    subs = {s["id"] for d in tax["domains"] for s in d["subs"]}
    msubs = {s["id"] for d in tax["mitigation"] for s in d["subs"]}
    stages = {s["id"] for s in tax["netra_stages"]}
    sectors = set(tax["sectors"])
    harms = set(tax["harm_types"])
    fw = {f["id"] for f in india["frameworks"]}
    ins = {i["id"]: i for i in india["instruments"]}
    auth = {a["id"] for a in india["authorities"]}
    incs = {i["id"] for i in india["incidents"]}
    statuses = set(india["review_statuses"])
    su = india["states_uts"]
    places = set(su["states"]) | set(su["union_territories"]) | {"National"}
    if len(su["states"]) != 28 or len(su["union_territories"]) != 8:
        errors.append("states_uts must list 28 states and 8 union territories")
    causal = tax["causal"]
    fm_ids = failure_mode_ids()

    # The home page shows this date beside the cases-tracked counter
    if not is_date(india["meta"].get("updated")):
        errors.append("meta.updated must be the ISO date the data was last changed")

    if "contact_email" in india["meta"] and not EMAIL.match(india["meta"]["contact_email"]):
        errors.append("meta.contact_email must be a plain email address")

    seen = set()
    for coll in ("risks", "instruments", "mitigations", "incidents", "gaps", "authorities", "frameworks"):
        for item in india[coll]:
            if item["id"] in seen:
                errors.append(f"duplicate id {item['id']}")
            seen.add(item["id"])

    for r in india["risks"]:
        if r["framework"] not in fw:
            errors.append(f"{r['id']}: unknown framework")
        if not r.get("quote") or not r.get("locator"):
            errors.append(f"{r['id']}: every risk needs a verbatim quote and a locator")
        for d in r["domain"]:
            if d not in subs:
                errors.append(f"{r['id']}: unknown subdomain {d}")
        for k in ("entity", "intent", "timing"):
            if r[k] not in causal[k]:
                errors.append(f"{r['id']}: bad {k} {r[k]}")

    for i in india["instruments"]:
        for f in ("title", "issuer", "type", "force", "date", "status", "url", "verified", "note"):
            if not i.get(f):
                errors.append(f"{i['id']}: missing {f}")
        if not i["url"].startswith("https://"):
            errors.append(f"{i['id']}: url must be https")
        check_instrument_detail(i, errors)
        for d in i["domains"]:
            if d not in subs:
                errors.append(f"{i['id']}: unknown subdomain {d}")
        for s in i["sectors"]:
            if s not in sectors:
                errors.append(f"{i['id']}: unknown sector {s}")
        if i["verified"] != "yes":
            warnings.append(f"{i['id']}: {i['verified']} verification – {i['note']}")

    for m in india["mitigations"]:
        if m["source"] not in ins:
            errors.append(f"{m['id']}: unknown source instrument")
        if m["category"] not in msubs:
            errors.append(f"{m['id']}: unknown mitigation category {m['category']}")
        if not m.get("quote"):
            errors.append(f"{m['id']}: needs a quote or marked summary")

    for inc in india["incidents"]:
        for f in ("title", "date", "harm", "response", "sources", "netra", "review"):
            if not inc.get(f):
                errors.append(f"{inc['id']}: missing {f}")
        if inc.get("review") not in statuses:
            errors.append(f"{inc['id']}: bad review status")
        if not 1 <= int(inc.get("severity", 0)) <= 5:
            errors.append(f"{inc['id']}: severity must be 1–5")
        for d in inc["domains"]:
            if d not in subs:
                errors.append(f"{inc['id']}: unknown subdomain {d}")
        for h in inc["harm_types"]:
            if h not in harms:
                errors.append(f"{inc['id']}: unknown harm type {h}")
        for s in inc["sectors"]:
            if s not in sectors:
                errors.append(f"{inc['id']}: unknown sector {s}")
        for k in ("entity", "intent", "timing"):
            if inc[k] not in causal[k]:
                errors.append(f"{inc['id']}: bad {k}")
        for iid in inc["instruments"]:
            if iid not in ins:
                errors.append(f"{inc['id']}: unknown instrument {iid}")
        for s in inc["sources"]:
            if not s["url"].startswith("https://"):
                errors.append(f"{inc['id']}: source url must be https")
        n = inc["netra"]
        if set(n["stages"]) != stages:
            errors.append(f"{inc['id']}: NETRA stages must list exactly {sorted(stages)}")
        for st, v in n["stages"].items():
            if v not in STAGE_STATES:
                errors.append(f"{inc['id']}: stage {st} has bad state {v}")
        # Safeguard: the human-review stage may never be marked done while the record is unreviewed
        if n["stages"]["S11"] == "done" and inc["review"] == "unreviewed":
            errors.append(f"{inc['id']}: S11 Human review cannot be 'done' on an unreviewed record")
        # A human review must say who did it and when, and must close stage S11
        if inc["review"] in REVIEWED:
            if not inc.get("reviewed_by") or not is_date(inc.get("reviewed_on")):
                errors.append(f"{inc['id']}: a reviewed record needs reviewed_by and an ISO reviewed_on date")
            if n["stages"]["S11"] != "done":
                errors.append(f"{inc['id']}: a reviewed record must have S11 Human review 'done'")
        elif inc.get("reviewed_by") or inc.get("reviewed_on"):
            errors.append(f"{inc['id']}: reviewed_by / reviewed_on set on a record that is not reviewed")
        # The state filter and the authorities treemap rely on the place starting with a known state or UT
        if inc["state"].split(" (")[0] not in places:
            errors.append(f"{inc['id']}: state must start with one of the 28 states, 8 UTs or 'National', not '{inc['state']}'")
        check_documents(inc, errors)
        check_v3_fields(inc, harms, errors, fm_ids)
        if "batch" in inc and not re.match(r"^B\d+$", str(inc["batch"])):
            errors.append(f"{inc['id']}: batch must look like 'B2'")
        for a in n["authorities"]:
            if a not in auth:
                errors.append(f"{inc['id']}: unknown authority {a}")
        if not n.get("overclaim") or not n.get("unknowns"):
            errors.append(f"{inc['id']}: needs an overclaim check and a 'what we do not know' list")

    for a in india["authorities"]:
        if a.get("verified") not in VERIFIED:
            errors.append(f"{a['id']}: verified must be one of {sorted(VERIFIED)}")
        if not a.get("url", "").startswith("https://"):
            errors.append(f"{a['id']}: url must be https")
        # A contact route shown as checked must say who checked it and when
        if a.get("verified") == "yes" and (not a.get("checked_by") or not is_date(a.get("checked_on"))):
            errors.append(f"{a['id']}: verified 'yes' needs checked_by and an ISO checked_on date")

    check_duplicates(india["incidents"], errors)
    check_directory(directory, india, errors)
    check_models(models, india, glob, directory, errors)
    check_drafts(errors)
    check_terms(terms, subs, india, errors)
    check_weekly(weekly, india, subs, errors)

    for g in india["gaps"]:
        for x in g["incidents"]:
            if x not in incs:
                errors.append(f"{g['id']}: unknown incident {x}")
        for x in g["instruments"]:
            if x not in ins:
                errors.append(f"{g['id']}: unknown instrument {x}")

    if not glob.get("reports"):
        errors.append("global_evidence.json has no reports")

    if errors:
        raise ValidationError("\n".join(errors))
    return warnings


def slim_global(glob):
    """Keep only what the site shows from the earlier METR pilot."""
    keep = {k: glob[k] for k in ("reports", "instruments", "mappings", "classifications", "sources", "gaps")}
    return keep


JSONLD = "<!--__JSONLD__-->"
SITE = "https://krunal6649.github.io/netra-india-observatory/"
REPO_URL = "https://github.com/krunal6649/netra-india-observatory"


def dataset_jsonld(india, directory, models):
    """schema.org/Dataset description for Google Dataset Search, built from the data so counts never go stale.
    Version, DOI and ORCID are read from CITATION.cff, the release's own citation file."""
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    pick = lambda key: (re.search(rf'^\s*{key}:\s*"?([^"\n]+)"?', cff, re.M) or [None, None])[1]
    version, doi, orcid = pick("version"), pick("doi"), pick("orcid")
    zen = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    inc, ins = india["incidents"], india["instruments"]
    verified = sum(i["verified"] == "yes" for i in ins)
    dates = sorted(str(i["date"])[:4] for i in inc if re.match(r"^\d{4}", str(i["date"])))
    author = {"@type": "Person", "name": "Krunal Maheshwari",
              "affiliation": {"@type": "Organization", "name": "Independent researcher; Advocate, Bar Council of Gujarat"}}
    if orcid:
        author["@id"] = author["sameAs"] = orcid
    data = {
        "@context": "https://schema.org", "@type": "Dataset",
        "name": "NETRA India AI Risk Observatory",
        "description": (f"Open record of AI-linked harms in India, the Indian laws that may apply and the authorities that can act. "
                        f"Holds {len(inc)} documented Indian AI incidents traced through a 14-stage method, {len(ins)} laws, rules, "
                        f"advisories and court orders ({verified} verified against official texts), {len(india['risks'])} risks "
                        f"quoted from Indian government frameworks, {len(india['mitigations'])} measures, {len(india['gaps'])} "
                        f"governance gaps, a directory of {len(directory['bodies'])} Union and state bodies and "
                        f"{len(models['models'])} AI model cards. Research material, not legal advice."),
        "url": SITE, "sameAs": REPO_URL, "version": version,
        "creator": author, "license": "https://creativecommons.org/licenses/by/4.0/",
        "isAccessibleForFree": True, "inLanguage": "en",
        "keywords": zen.get("keywords", []),
        "spatialCoverage": {"@type": "Place", "name": "India"},
        "temporalCoverage": f"{dates[0]}/{dates[-1]}" if dates else None,
        "dateModified": india["meta"].get("updated"),
        "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{SITE}data/{f}"}
                         for f in ("india.json", "authorities.json", "models.json")],
        "isBasedOn": "https://airisk.mit.edu/",
        "subjectOf": {"@type": "ScholarlyArticle", "name": "NETRA: An Open, Verification-First Observatory of AI Harms, Law and Accountability in India", "identifier": "https://doi.org/10.5281/zenodo.23865186",
                      "author": {"@type": "Person", "name": "Krunal Maheshwari"}, "datePublished": "2026-11-01"},
    }
    if doi:
        data["identifier"] = f"https://doi.org/{doi}"
        data["citation"] = f"Maheshwari, K. (2026). NETRA India AI Risk Observatory (version {version}) [Data set]. Zenodo. https://doi.org/{doi}"
    data = {k: v for k, v in data.items() if v is not None}
    blob = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{blob}\n</script>'


def build(check_only=False):
    tax, india, glob, directory, models, terms = (load("taxonomy.json"), load("india.json"), load("global_evidence.json"),
                                                  load("authorities.json"), load("models.json"), load("check_terms.json"))
    weekly = load("weekly.json") if (DATA / "weekly.json").exists() else {"meta": {}, "weeks": []}
    warnings = validate(tax, india, glob, directory, models, terms, weekly)
    print(f"Validation passed: {len(india['risks'])} risks, {len(india['incidents'])} incidents, "
          f"{len(india['instruments'])} instruments, {len(india['mitigations'])} mitigations, "
          f"{len(india['gaps'])} gaps, {len(directory['bodies'])} directory bodies, {len(models['models'])} models; {len(warnings)} verification warnings.")
    if check_only:
        for w in warnings:
            print("  ! " + w)
        return
    atlas = load("atlas_techniques.json")
    refs = {"owasp": load("owasp_llm_top10.json"),
            "atlas": {**atlas["meta"], "count": len(atlas["techniques"])}}
    payload = {"refs": refs, "tax": tax, "india": india, "global": slim_global(glob), "directory": directory, "models": models, "check": terms, "weekly": weekly, "warnings": warnings,
               "built": date.today().isoformat()}
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in html:
        raise SystemExit("Template placeholder missing")
    OUT.parent.mkdir(exist_ok=True)
    html = html.replace(JSONLD, dataset_jsonld(india, directory, models))
    OUT.write_text(html.replace(PLACEHOLDER, blob), encoding="utf-8")
    print(f"Built dist/index.html ({OUT.stat().st_size // 1024} KB)")
    write_pages(OUT.read_text(encoding="utf-8"))


def write_pages(page):
    """Write a complete HTML document for GitHub Pages (index.html at repo root).
    The Claude artifact wraps the page automatically; ordinary hosts and link-preview
    crawlers (LinkedIn, X) need a real <html><head> with the meta tags inside it."""
    cut = page.index("</style>") + len("</style>")
    head, body = page[:cut], page[cut:]
    doc = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
           "<style>:root{color-scheme:dark;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
           "body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>\n"
           + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")
    (ROOT / "index.html").write_text(doc, encoding="utf-8")
    print("Built index.html for GitHub Pages (full document)")


if __name__ == "__main__":
    try:
        build(check_only="--check" in sys.argv)
    except ValidationError as e:
        print("Validation FAILED:\n" + str(e))
        sys.exit(1)
