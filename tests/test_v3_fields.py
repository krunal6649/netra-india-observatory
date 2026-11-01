"""Version 3 additive fields: the optional `assessment` block on incidents.
Run from the netra-india folder:  python3 -m unittest discover tests
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build  # noqa: E402

TRIAL = {"IN-INC-20": "confirmed", "IN-INC-09": "suspected", "IN-INC-14": "not AI"}


class V3Fields(unittest.TestCase):
    def setUp(self):
        self.tax, self.india, self.glob = build.load("taxonomy.json"), build.load("india.json"), build.load("global_evidence.json")

    def inc(self, d, iid):
        return next(i for i in d["incidents"] if i["id"] == iid)

    def rejects(self, d, text):
        with self.assertRaises(build.ValidationError) as c:
            build.validate(self.tax, d, self.glob)
        self.assertIn(text, str(c.exception))

    def test_only_the_three_trial_cases_carry_an_assessment(self):
        have = {i["id"]: i["assessment"]["ai_role"]["value"] for i in self.india["incidents"] if "assessment" in i}
        self.assertEqual(have, TRIAL)

    def test_trial_assessments_are_unreviewed_and_tag_nothing_yet(self):
        for iid in TRIAL:
            a = self.inc(self.india, iid)["assessment"]
            self.assertEqual(a["review"], "unreviewed")
            self.assertEqual(a["failure_modes"], build.NOT_ASSESSED)
            self.assertEqual(a["crosswalk"], build.NOT_ASSESSED)

    def test_records_without_an_assessment_still_pass(self):
        d = copy.deepcopy(self.india)
        for i in d["incidents"]:
            i.pop("assessment", None)
        self.assertIsNotNone(build.validate(self.tax, d, self.glob))

    def test_bad_ai_role_rejected(self):
        d = copy.deepcopy(self.india); self.inc(d, "IN-INC-20")["assessment"]["ai_role"]["value"] = "probably"
        self.rejects(d, "ai_role value must be one of")

    def test_ai_role_needs_basis(self):
        d = copy.deepcopy(self.india); self.inc(d, "IN-INC-20")["assessment"]["ai_role"].pop("basis")
        self.rejects(d, "ai_role needs a basis")

    def test_assessment_cannot_be_marked_reviewed_without_reviewer(self):
        d = copy.deepcopy(self.india); self.inc(d, "IN-INC-09")["assessment"]["review"] = "human_reviewed"
        self.rejects(d, "a reviewed assessment needs reviewed_by")

    def test_unknown_field_rejected(self):
        d = copy.deepcopy(self.india); self.inc(d, "IN-INC-09")["assessment"]["benchmark_score"] = 0.9
        self.rejects(d, "unknown field benchmark_score")

    def test_scale_must_cite_one_of_the_incidents_sources(self):
        d = copy.deepcopy(self.india)
        self.inc(d, "IN-INC-14")["assessment"]["impact"]["scale"]["source"] = "https://example.com/elsewhere"
        self.rejects(d, "impact.scale needs a value and a source")

    def test_failure_mode_must_be_a_real_item_of_its_edition(self):
        d = copy.deepcopy(self.india); i = self.inc(d, "IN-INC-20")
        # LLM08 is "Hidden Context Exposure" in 2026 but does not exist as LLM08:2026 in the 2025 list
        i["assessment"]["failure_modes"] = [{"framework": "OWASP-LLM-2025", "id": "LLM08:2026",
                                             "source": i["sources"][0]["url"], "basis": "test"}]
        self.rejects(d, "LLM08:2026 is not an item of OWASP-LLM-2025")

    def test_failure_mode_needs_a_cited_source(self):
        d = copy.deepcopy(self.india); i = self.inc(d, "IN-INC-20")
        i["assessment"]["failure_modes"] = [{"framework": "MITRE-ATLAS", "id": "AML.T0051",
                                             "source": "https://example.com/blog", "basis": "test"}]
        self.rejects(d, "needs a basis and a source that is one of this incident's sources")

    def test_valid_failure_mode_and_crosswalk_pass(self):
        d = copy.deepcopy(self.india); i = self.inc(d, "IN-INC-20")
        i["assessment"]["failure_modes"] = [{"framework": "OWASP-LLM-2026", "id": "LLM07:2026",
                                             "source": i["sources"][0]["url"], "basis": "test only"}]
        i["assessment"]["crosswalk"] = [{"framework": "NIST-AI-RMF", "label": "MANAGE", "why": "test only"}]
        self.assertIsNotNone(build.validate(self.tax, d, self.glob))

    def test_nist_crosswalk_label_is_a_function(self):
        d = copy.deepcopy(self.india)
        self.inc(d, "IN-INC-20")["assessment"]["crosswalk"] = [{"framework": "NIST-AI-RMF", "label": "MAP 9.9", "why": "x"}]
        self.rejects(d, "NIST AI RMF crosswalk label must be one of")

    def test_reference_lists_keep_editions_apart(self):
        ids = build.failure_mode_ids()
        self.assertEqual(len(ids["OWASP-LLM-2025"]), 10)
        self.assertEqual(len(ids["OWASP-LLM-2026"]), 10)
        self.assertIn("AML.T0024", ids["MITRE-ATLAS"])
        self.assertEqual(build.load("atlas_techniques.json")["meta"]["release"], "2026.10")


if __name__ == "__main__":
    unittest.main()
