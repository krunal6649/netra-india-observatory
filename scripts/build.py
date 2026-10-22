#!/usr/bin/env python3
"""Validate the NETRA India data files and build the single-page site.

Usage (from the netra-india folder):
    python3 scripts/build.py           # check data, write dist/index.html
    python3 scripts/build.py --check   # check data only

Standard library only. Nothing to install.
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATE = ROOT / "web" / "template.html"
OUT = ROOT / "dist" / "index.html"
PLACEHOLDER = "/*__DATA__*/null"
STAGE_STATES = {"done", "secondary", "partial", "draft", "open", "contested", "possible", "n/a"}


class ValidationError(Exception):
    pass


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def validate(tax, india, glob):
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
    causal = tax["causal"]

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
        for a in n["authorities"]:
            if a not in auth:
                errors.append(f"{inc['id']}: unknown authority {a}")
        if not n.get("overclaim") or not n.get("unknowns"):
            errors.append(f"{inc['id']}: needs an overclaim check and a 'what we do not know' list")

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
    keep = {k: glob[k] for k in ("reports", "instruments", "mappings", "classifications", "sources")}
    return keep


def build(check_only=False):
    tax, india, glob = load("taxonomy.json"), load("india.json"), load("global_evidence.json")
    warnings = validate(tax, india, glob)
    print(f"Validation passed: {len(india['risks'])} risks, {len(india['incidents'])} incidents, "
          f"{len(india['instruments'])} instruments, {len(india['mitigations'])} mitigations, "
          f"{len(india['gaps'])} gaps; {len(warnings)} verification warnings.")
    if check_only:
        for w in warnings:
            print("  ! " + w)
        return
    payload = {"tax": tax, "india": india, "global": slim_global(glob), "warnings": warnings,
               "built": date.today().isoformat()}
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in html:
        raise SystemExit("Template placeholder missing")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html.replace(PLACEHOLDER, blob), encoding="utf-8")
    print(f"Built dist/index.html ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    try:
        build(check_only="--check" in sys.argv)
    except ValidationError as e:
        print("Validation FAILED:\n" + str(e))
        sys.exit(1)
