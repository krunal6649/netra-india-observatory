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

    def ins(self, d, iid):
        return next(i for i in d["instruments"] if i["id"] == iid)

    def test_verified_value(self):
        d = copy.deepcopy(self.india); self.ins(d, "G-BNS")["verified"] = "probably"
        self.rejects(d, "verified must be one of")

    def test_verified_needs_specific_url(self):
        d = copy.deepcopy(self.india); b = self.ins(d, "G-BNS")
        b["verified"], b["url"] = "yes", "https://www.indiacode.nic.in/"
        self.rejects(d, "not a home page")

    def test_act_number_format(self):
        d = copy.deepcopy(self.india); self.ins(d, "G-BNS")["act_no"] = "No. 45/2023"
        self.rejects(d, "act_no must look like")

    def test_notification_number_format(self):
        d = copy.deepcopy(self.india); self.ins(d, "G-ITR21")["notifications"] = [{"no": "GSR 139", "what": "x"}]
        self.rejects(d, "must look like 'G.S.R. 139(E)'")

    def test_notification_date_format(self):
        d = copy.deepcopy(self.india)
        self.ins(d, "G-ITR21")["notifications"] = [{"no": "G.S.R. 139(E)", "date": "25 Feb 2021", "what": "x"}]
        self.rejects(d, "date must be an ISO date")

    def test_case_needs_fields(self):
        d = copy.deepcopy(self.india); self.ins(d, "G-BSA")["cases"] = [{"name": "X v. Y"}]
        self.rejects(d, "case X v. Y missing citation")


if __name__ == "__main__":
    unittest.main()
