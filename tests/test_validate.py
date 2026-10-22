"""Checks the validator accepts the seed data and rejects unsafe edits.
Run from the netra-india folder:  python3 -m unittest discover tests
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build  # noqa: E402


class Tests(unittest.TestCase):
    def setUp(self):
        self.tax, self.india, self.glob = build.load("taxonomy.json"), build.load("india.json"), build.load("global_evidence.json")

    def rejects(self, india, text):
        with self.assertRaises(build.ValidationError) as c:
            build.validate(self.tax, india, self.glob)
        self.assertIn(text, str(c.exception))

    def test_seed_passes(self):
        self.assertTrue(build.validate(self.tax, self.india, self.glob))

    def test_human_review_cannot_be_faked(self):
        d = copy.deepcopy(self.india); d["incidents"][0]["netra"]["stages"]["S11"] = "done"
        self.rejects(d, "S11 Human review")

    def test_risk_needs_quote(self):
        d = copy.deepcopy(self.india); d["risks"][0]["quote"] = ""
        self.rejects(d, "verbatim quote")

    def test_unknown_subdomain(self):
        d = copy.deepcopy(self.india); d["incidents"][0]["domains"] = ["9.9"]
        self.rejects(d, "unknown subdomain 9.9")

    def test_incident_needs_overclaim_check(self):
        d = copy.deepcopy(self.india); d["incidents"][0]["netra"]["overclaim"] = ""
        self.rejects(d, "overclaim")

    def test_severity_range(self):
        d = copy.deepcopy(self.india); d["incidents"][0]["severity"] = 7
        self.rejects(d, "severity must be 1–5")


if __name__ == "__main__":
    unittest.main()
