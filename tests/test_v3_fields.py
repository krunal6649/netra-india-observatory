"""Version 3 additive fields: the optional `assessment` block on incidents.
Run from the netra-india folder:  python3 -m unittest discover tests
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build  # noqa: E402

TRIAL = {"IN-INC-20": "confirmed", "IN-INC-09": "suspected", "IN-INC-14": "not established"}


class V3Fields(unittest.TestCase):
    def setUp(self):
        self.tax, self.india, self.glob = build.load("taxonomy.json"), build.load("india.json"), build.load("global_evidence.json")

    def inc(self, d, iid):
        return next(i for i in d["incidents"] if i["id"] == iid)

    def rejects(self, d, text):
        with self.assertRaises(build.ValidationError) as c:
            build.validate(self.tax, d, self.glob)
        self.assertIn(text, str(c.exception))

    def test_every_case_carries_an_assessment(self):
        have = {i["id"]: i["assessment"]["ai_role"]["value"] for i in self.india["incidents"] if "assessment" in i}
        self.assertEqual(len(have), len(self.india["incidents"]))
        for iid, role in TRIAL.items():
            self.assertEqual(have[iid], role)

    def test_maintainer_checked_ai_roles(self):
        want = {"IN-INC-01": "confirmed", "IN-INC-04": "confirmed", "IN-INC-06": "suspected", "IN-INC-15": "confirmed",
                "IN-INC-16": "confirmed", "IN-INC-17": "suspected", "IN-INC-18": "suspected"}
        for iid, role in want.items():
            r = self.inc(self.india, iid)["assessment"]["ai_role"]
            self.assertEqual(r["value"], role, iid)
            self.assertIn("Checked by the maintainer, Krunal Maheshwari, on 2026-11-01.", r["basis"])
        # The CERT-In advisory number came from the maintainer and is not yet checked against an official link
        self.assertIn("not yet been checked", self.inc(self.india, "IN-INC-15")["assessment"]["ai_role"]["basis"])

    def test_wotnot_kept_in_scope_as_not_established(self):
        basis = self.inc(self.india, "IN-INC-14")["assessment"]["ai_role"]["basis"]
        self.assertIn("Kept in scope by the maintainer on 2026-11-01", basis)

    def test_assessments_are_unreviewed_and_only_inc15_is_tagged(self):
        for i in self.india["incidents"]:
            a = i["assessment"]
            self.assertEqual(a["review"], "unreviewed")
            if i["id"] == "IN-INC-15":
                self.assertEqual([t["id"] for t in a["failure_modes"]], ["LLM06:2025", "LLM03:2026"])
                self.assertTrue(all("does not use OWASP terms" in t["basis"] for t in a["failure_modes"]))
                continue
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

    def test_failure_mode_name_must_match_its_edition(self):
        d = copy.deepcopy(self.india)
        self.inc(d, "IN-INC-15")["assessment"]["failure_modes"][1]["name"] = "Supply Chain"
        self.rejects(d, "LLM03:2026 is named 'Excessive Agency' in OWASP-LLM-2026")

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
