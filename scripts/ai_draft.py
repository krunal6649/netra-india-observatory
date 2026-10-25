#!/usr/bin/env python3
"""Owner-only AI-assisted draft of a report (Phase 5, option B).

Reads a text, Markdown or Word file, asks an AI provider to Extract, Triage and Draft, applies NETRA's
safeguards, and writes data/drafts/<slug>.json as an unreviewed draft. The GitHub workflow
.github/workflows/ai-draft.yml runs this and opens a pull request; nothing is merged automatically.

Usage (from the repo root):
    NETRA_AI_KEY=... python3 scripts/ai_draft.py --file uploads/report.md --title "..." \\
        --source https://example.org/report --date 2026-10-01 --licence "CC BY 4.0"

Environment:
    NETRA_AI_KEY       API key (required; never written anywhere)
    NETRA_AI_PROVIDER  anthropic (default) or openai (any OpenAI-compatible chat completions endpoint)
    NETRA_AI_MODEL     model id (default from scripts/ai_prompts.json)
    NETRA_AI_BASE      base URL for openai-compatible providers

Standard library only. PDF is not supported here; convert it to text first, or use the in-browser tool.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = json.loads((ROOT / "scripts" / "ai_prompts.json").read_text(encoding="utf-8"))
LICENCES = {"CC BY 4.0", "CC BY-SA 4.0", "Apache 2.0", "MIT", "Public domain", "Cite and summarise only", "Unknown"}


class DraftError(Exception):
    pass


def read_document(path):
    """Return the document text. Word files are read from word/document.xml, one paragraph per line."""
    p = Path(path)
    ext = p.suffix.lower()
    if ext in (".txt", ".md", ".markdown"):
        return p.read_text(encoding="utf-8", errors="replace")
    if ext == ".docx":
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml")
        ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        root = ElementTree.fromstring(xml)
        paras = ["".join(t.text or "" for t in para.iter(ns + "t")) for para in root.iter(ns + "p")]
        return "\n".join(x for x in paras if x.strip())
    raise DraftError(f"{ext or 'this file type'} is not supported by the script; use .txt, .md or .docx (convert PDFs to text first)")


def norm(s):
    """Compare quotes ignoring whitespace runs, curly quotes and dash styles."""
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("­", "")
    return re.sub(r"\s+", " ", s).strip()


def pages_of(text):
    """Split on [Page N] markers. Returns {page: text}; empty when the text has no markers."""
    parts = re.split(r"\[Page (\d+)\]", text)
    return {int(parts[k]): parts[k + 1] for k in range(1, len(parts) - 1, 2)}


def verify_quotes(quotes, text):
    """Keep only quotes that appear word for word in the text (and on the stated page, when pages are known)."""
    whole, pages = norm(text), {k: norm(v) for k, v in pages_of(text).items()}
    kept, removed = [], []
    for q in quotes:
        t = norm(q.get("text", ""))
        page = q.get("page")
        ok = bool(t) and t in whole and (not pages or page is None or t in pages.get(page, ""))
        (kept if ok else removed).append({"text": q.get("text", ""), "page": page, "verified": ok})
    return kept, removed


def redact_blocked(md):
    """Remove sentences that state a legal conclusion, accuse someone or claim a review. Returns (text, flags)."""
    flags = []
    out = md
    part = r"(?:[^.\n]|\.(?=\d))*"  # a sentence ends at a full stop that is not part of a section number such as s.43
    for pat in PROMPTS["blocked_patterns"]:
        rx = re.compile(r"(^|\s*)(" + part + pat + part + r"(?:\.(?!\d))?)", re.I | re.M)
        flags += [m.group(2).strip() for m in rx.finditer(out)]
        out = rx.sub(lambda m: m.group(1) + "[Removed by NETRA safeguard: possible legal conclusion or accusation.]", out)
    return out, flags


def context_lists():
    """The ids the AI may use, taken from NETRA's own data."""
    tax = json.loads((ROOT / "data" / "taxonomy.json").read_text(encoding="utf-8"))
    india = json.loads((ROOT / "data" / "india.json").read_text(encoding="utf-8"))
    directory = json.loads((ROOT / "data" / "authorities.json").read_text(encoding="utf-8"))
    subs = {s["id"]: s["name"] for d in tax["domains"] for s in d["subs"]}
    ins = {i["id"]: i["title"] for i in india["instruments"]}
    bodies = {b["id"]: b["name"] for b in directory["bodies"] if b["level"] == "union"}
    return subs, ins, bodies


def lists_text(subs, ins, bodies):
    f = lambda d: "\n".join(f"- {k}: {v}" for k, v in d.items())
    return f"Risk areas:\n{f(subs)}\n\nIndian instruments:\n{f(ins)}\n\nDirectory bodies (Union):\n{f(bodies)}"


def call_model(system, user, schema, provider, key, model, base):
    """One request. Returns the model's text, or parsed JSON when a schema is given."""
    if provider == "anthropic":
        cfg = PROMPTS["anthropic"]
        body = {"model": model or cfg["default_model"], "max_tokens": cfg["max_tokens"], "system": system,
                "messages": [{"role": "user", "content": user}], "output_config": {"effort": cfg["effort"]},
                "fallbacks": "default"}
        if schema:
            body["output_config"]["format"] = {"type": "json_schema", "schema": schema}
        req = urllib.request.Request(cfg["url"], data=json.dumps(body).encode("utf-8"), method="POST", headers={
            "content-type": "application/json", "x-api-key": key, "anthropic-version": cfg["version"],
            "anthropic-beta": cfg["fallback_beta"]})
    elif provider == "openai":
        cfg = PROMPTS["openai_compatible"]
        msgs = [{"role": "system", "content": system + ("\nReply with one JSON object only." if schema else "")}, {"role": "user", "content": user}]
        body = {"model": model, "messages": msgs, "max_tokens": cfg["max_tokens"]}
        if schema:
            body["response_format"] = {"type": "json_object"}
        req = urllib.request.Request((base or cfg["default_base"]).rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"),
                                     method="POST", headers={"content-type": "application/json", "authorization": f"Bearer {key}"})
    else:
        raise DraftError("NETRA_AI_PROVIDER must be anthropic or openai")
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise DraftError(f"provider returned HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from None
    if provider == "anthropic":
        if data.get("stop_reason") == "refusal":
            raise DraftError("the model declined this request")
        if data.get("stop_reason") == "max_tokens":
            raise DraftError("the reply was cut off (max_tokens); try a shorter document")
        text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    else:
        text = data["choices"][0]["message"]["content"] or ""
    if not schema:
        return text
    try:
        return json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip()))
    except json.JSONDecodeError:
        raise DraftError("the model did not return valid JSON") from None


def run(text, meta, ask):
    """Run Extract, Triage and Draft with safeguards. `ask(system, user, schema)` calls the model."""
    if len(text) > PROMPTS["max_chars"]:
        raise DraftError(f"document is {len(text):,} characters; the limit is {PROMPTS['max_chars']:,}. Split it or trim it first.")
    subs, ins, bodies = context_lists()
    system = PROMPTS["system"] + "\n\n" + lists_text(subs, ins, bodies)
    doc = f"<document>\n{text}\n</document>"
    st = PROMPTS["steps"]
    ex = ask(system, f"{doc}\n\n{st['extract']['instruction']}", st["extract"]["schema"])
    kept, removed = verify_quotes(ex.get("quotes", []), text)
    tr = ask(system, f"Extraction:\n{json.dumps({**ex, 'quotes': kept}, ensure_ascii=False)}\n\n{st['triage']['instruction']}", st["triage"]["schema"])
    dropped = []
    triage = {
        "risk_areas": [x for x in tr.get("risk_areas", []) if x in subs or dropped.append(x)],
        "possible_laws": [l for l in tr.get("possible_laws", []) if (l.get("instrument_id") in ins and l.get("label") in ("possible", "interpretive", "gap")) or dropped.append(l.get("instrument_id"))],
        "authorities": [x for x in tr.get("authorities", []) if x in bodies or dropped.append(x)],
        "gaps": tr.get("gaps", [])}
    md = ask(system, f"Extraction:\n{json.dumps({**ex, 'quotes': kept}, ensure_ascii=False)}\n\nTriage:\n{json.dumps(triage, ensure_ascii=False)}\n\n{st['draft']['instruction']}", None)
    md, flags = redact_blocked(md)
    summary, f1 = redact_blocked(ex.get("summary", ""))
    return {**meta, "ai_generated": True, "review": "unreviewed", "created": date.today().isoformat(),
            "summary": summary, "findings": [redact_blocked(x)[0] for x in ex.get("findings", [])],
            "quotes": kept, "quotes_removed": removed, "triage": triage, "unknown_ids_dropped": [x for x in dropped if x],
            "draft_markdown": md, "safeguard_flags": flags + f1,
            "notice": "AI-assisted draft. Unreviewed. Not legal advice. Quotes were checked word for word against the source; any that did not match were removed."}


def check_meta(a):
    errs = []
    if not a.title.strip():
        errs.append("title is required")
    if not (a.source.startswith("https://") or (a.source.strip() and "://" not in a.source)):
        errs.append("source must be an https link or a plain name")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", a.date):
        errs.append("date must be YYYY-MM-DD")
    if a.licence not in LICENCES:
        errs.append(f"licence must be one of: {', '.join(sorted(LICENCES))}")
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for k in ("file", "title", "source", "date", "licence"):
        ap.add_argument("--" + k, required=True)
    a = ap.parse_args(argv)
    errs = check_meta(a)
    if errs:
        raise DraftError("; ".join(errs))
    key = os.environ.get("NETRA_AI_KEY", "")
    if not key:
        raise DraftError("set NETRA_AI_KEY (in GitHub: a repository secret); it is never written to the repo")
    provider = os.environ.get("NETRA_AI_PROVIDER", "anthropic")
    model, base = os.environ.get("NETRA_AI_MODEL", ""), os.environ.get("NETRA_AI_BASE", "")
    text = read_document(a.file)
    meta = {"title": a.title.strip(), "source": a.source.strip(), "date": a.date, "licence": a.licence,
            "provider": provider, "model": model or (PROMPTS["anthropic"]["default_model"] if provider == "anthropic" else "")}
    out = run(text, meta, lambda s, u, sc: call_model(s, u, sc, provider, key, model, base))
    slug = re.sub(r"[^a-z0-9]+", "-", a.title.lower()).strip("-")[:60] or "draft"
    dest = ROOT / "data" / "drafts" / f"{a.date}-{slug}.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {dest.relative_to(ROOT)}: {len(out['quotes'])} quotes kept, {len(out['quotes_removed'])} removed, {len(out['safeguard_flags'])} sentences redacted.")


if __name__ == "__main__":
    try:
        main()
    except DraftError as e:
        print("Draft FAILED: " + str(e))
        sys.exit(1)
