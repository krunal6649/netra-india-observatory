"""Checks the AI draft safeguards without calling any AI provider.
Run from the repo root:  python3 -m unittest discover tests
"""
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import ai_draft  # noqa: E402
import build  # noqa: E402

DOC = "[Page 1]\nThe agents used credentials found exposed online.\n[Page 2]\nAbout 7% of reviewed transcripts contained spoofed tool calls."


def fake_ask(extract, triage, draft):
    """Stands in for the model: returns the given replies in order."""
    replies = iter([extract, triage, draft])
    return lambda system, user, schema: next(replies)


class Tests(unittest.TestCase):
    def run_with(self, extract=None, triage=None, draft="## What the source found\nok"):
        extract = extract or {"summary": "s", "findings": ["f"], "quotes": []}
        triage = triage or {"risk_areas": [], "possible_laws": [], "authorities": [], "gaps": []}
        return ai_draft.run(DOC, {"title": "t"}, fake_ask(extract, triage, draft))

    def test_real_quote_kept_invented_quote_removed(self):
        out = self.run_with(extract={"summary": "s", "findings": [], "quotes": [
            {"text": "About 7% of reviewed transcripts contained spoofed tool calls.", "page": 2},
            {"text": "The developer admitted full responsibility.", "page": 1}]})
        self.assertEqual([q["text"] for q in out["quotes"]], ["About 7% of reviewed transcripts contained spoofed tool calls."])
        self.assertEqual(out["quotes_removed"][0]["text"], "The developer admitted full responsibility.")

    def test_quote_on_wrong_page_removed(self):
        out = self.run_with(extract={"summary": "s", "findings": [], "quotes": [
            {"text": "The agents used credentials found exposed online.", "page": 2}]})
        self.assertEqual(out["quotes"], [])

    def test_quote_matching_ignores_whitespace_and_curly_quotes(self):
        kept, _ = ai_draft.verify_quotes([{"text": "The  agents used\ncredentials", "page": 1}], DOC)
        self.assertEqual(len(kept), 1)

    def test_legal_conclusion_redacted(self):
        out = self.run_with(draft="Intro line.\nThe developer is liable under s.43. Other text.")
        self.assertNotIn("is liable", out["draft_markdown"])
        self.assertIn("Removed by NETRA safeguard", out["draft_markdown"])
        self.assertTrue(out["safeguard_flags"])

    def test_redaction_keeps_section_numbers_whole(self):
        md, flags = ai_draft.redact_blocked("Background. The firm is liable under s.43. Next point.")
        self.assertEqual(md, "Background. [Removed by NETRA safeguard: possible legal conclusion or accusation.] Next point.")
        self.assertEqual(flags, ["The firm is liable under s.43."])

    def test_accusation_redacted(self):
        md, flags = ai_draft.redact_blocked("Mr X has committed fraud. The report describes the event.")
        self.assertNotIn("committed", md)
        self.assertIn("The report describes the event.", md)

    def test_unknown_ids_dropped(self):
        out = self.run_with(triage={"risk_areas": ["4.3", "9.9"], "authorities": ["U-CERTIN", "U-NOPE"], "gaps": [],
                                    "possible_laws": [{"instrument_id": "G-ITA", "label": "possible", "why": "w"},
                                                      {"instrument_id": "G-FAKE", "label": "possible", "why": "w"},
                                                      {"instrument_id": "G-BNS", "label": "guilty", "why": "w"}]})
        self.assertEqual(out["triage"]["risk_areas"], ["4.3"])
        self.assertEqual(out["triage"]["authorities"], ["U-CERTIN"])
        self.assertEqual([l["instrument_id"] for l in out["triage"]["possible_laws"]], ["G-ITA"])
        self.assertIn("G-FAKE", out["unknown_ids_dropped"])

    def test_draft_is_always_unreviewed(self):
        out = self.run_with()
        self.assertEqual((out["review"], out["ai_generated"]), ("unreviewed", True))

    def test_too_long_document_refused(self):
        with self.assertRaises(ai_draft.DraftError):
            ai_draft.run("x" * (ai_draft.PROMPTS["max_chars"] + 1), {}, fake_ask({}, {}, ""))

    def test_reads_word_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "r.docx"
            xml = ('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
                   '<w:p><w:r><w:t>First para</w:t></w:r></w:p><w:p><w:r><w:t>Second </w:t></w:r><w:r><w:t>para</w:t></w:r></w:p></w:body></w:document>')
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("word/document.xml", xml)
            self.assertEqual(ai_draft.read_document(p), "First para\nSecond para")

    def test_pdf_refused_by_script(self):
        with self.assertRaises(ai_draft.DraftError):
            ai_draft.read_document("x.pdf")

    def test_metadata_checked(self):
        a = type("A", (), {"title": "", "source": "http://x", "date": "1 Oct", "licence": "Whatever"})
        self.assertEqual(len(ai_draft.check_meta(a)), 4)

    def test_build_rejects_a_draft_marked_reviewed(self):
        drafts = build.DATA / "drafts"
        created = not drafts.exists()
        drafts.mkdir(exist_ok=True)
        p = drafts / "zz-test-draft.json"
        try:
            p.write_text(json.dumps({"ai_generated": True, "review": "human_reviewed", "quotes": []}), encoding="utf-8")
            errors = []
            build.check_drafts(errors)
            self.assertTrue(any("must be ai_generated and 'unreviewed'" in e for e in errors))
        finally:
            p.unlink()
            if created:
                drafts.rmdir()


if __name__ == "__main__":
    unittest.main()
