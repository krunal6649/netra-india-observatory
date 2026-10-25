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
        d = copy.deepcopy(self.india); inc = d["incidents"][0]
        inc["review"], inc["netra"]["stages"]["S11"] = "unreviewed", "done"
        for k in ("reviewed_by", "reviewed_on"):
            inc.pop(k, None)
        self.rejects(d, "S11 Human review")

    def test_review_needs_reviewer_and_date(self):
        d = copy.deepcopy(self.india); inc = d["incidents"][0]
        inc["review"] = "human_reviewed"; inc.pop("reviewed_by", None)
        self.rejects(d, "needs reviewed_by")

    def test_review_must_close_s11(self):
        d = copy.deepcopy(self.india); inc = d["incidents"][0]
        inc["review"], inc["reviewed_by"], inc["reviewed_on"] = "human_reviewed", "X", "2026-10-25"
        inc["netra"]["stages"]["S11"] = "open"
        self.rejects(d, "must have S11")

    def test_official_document_must_be_on_court_site(self):
        d = copy.deepcopy(self.india)
        d["incidents"][0]["court_documents"] = [{"title": "Order", "court": "Delhi High Court", "date": "2023-09-20", "kind": "order",
            "url": "https://example.com/order.pdf", "host": "official", "opened": "no", "note": "x"}]
        self.rejects(d, "not on a .nic.in or .gov.in court site")

    def test_checked_document_needs_checker(self):
        d = copy.deepcopy(self.india)
        doc = next(i for i in d["incidents"] if i.get("court_documents"))["court_documents"][0]
        doc.pop("checked_by")
        self.rejects(d, "needs checked_by")

    def test_new_batch_arrives_unreviewed(self):
        b2 = [i for i in self.india["incidents"] if i.get("batch") == "B2"]
        self.assertEqual(len(b2), 10)
        for i in b2:
            self.assertEqual((i["review"], i["netra"]["stages"]["S11"]), ("unreviewed", "open"), i["id"])
            self.assertNotIn("reviewed_by", i)
            self.assertTrue(i["sources"] and all(s["url"].startswith("https://") for s in i["sources"]))
        # Batch 2 was chosen to cover every risk domain
        self.assertEqual({d.split(".")[0] for i in b2 for d in i["domains"]}, {"1", "2", "3", "4", "5", "6", "7"})

    def test_document_kind(self):
        d = copy.deepcopy(self.india)
        d["incidents"][0]["court_documents"] = [{"title": "Order", "court": "Delhi High Court", "date": "2023-09-20", "kind": "memo",
            "url": "https://delhihighcourt.nic.in/x.pdf", "host": "official", "opened": "no", "note": "x"}]
        self.rejects(d, "kind must be one of")

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

    def test_v02_verification_records(self):
        bns, bsa = self.ins(self.india, "G-BNS"), self.ins(self.india, "G-BSA")
        self.assertEqual((bns["verified"], bns["act_no"]), ("yes", "Act 45 of 2023"))
        for s in ("s.77 ", "s.308 ", "s.318 ", "s.319 ", "s.335 ", "s.336 ", "s.340 ", "s.351 ", "s.353 ", "s.356 "):
            self.assertIn(s, bns["provisions"])
        self.assertEqual((bsa["verified"], bsa["act_no"]), ("yes", "Act 47 of 2023"))
        # The case was read only through a report, so it must not be marked verified
        self.assertEqual(bsa["cases"][0]["verified"], "partial")
        nos = lambda iid: [n["no"] for n in self.ins(self.india, iid)["notifications"]]
        self.assertEqual(nos("G-ITR21"), ["G.S.R. 139(E)", "G.S.R. 794(E)"])
        self.assertEqual(nos("G-ITR26"), ["G.S.R. 120(E)"])
        self.assertEqual(nos("G-DPDP"), ["G.S.R. 843(E)"])
        self.assertEqual(nos("G-DPDPR"), ["G.S.R. 846(E)"])
        for iid in ("G-ITR21", "G-ITA", "G-CPA", "G-ITR26", "G-DPDP", "G-DPDPR"):
            self.assertEqual(self.ins(self.india, iid)["verified"], "partial", iid)
        self.assertEqual(len(build.validate(self.tax, self.india, self.glob)), 24)

    def test_meta_updated_date(self):
        d = copy.deepcopy(self.india); d["meta"]["updated"] = "last week"
        self.rejects(d, "meta.updated")

    def test_contact_email_format(self):
        d = copy.deepcopy(self.india); d["meta"]["contact_email"] = "krunal at gmail"
        self.rejects(d, "contact_email")

    def test_case_needs_fields(self):
        d = copy.deepcopy(self.india); self.ins(d, "G-BSA")["cases"] = [{"name": "X v. Y"}]
        self.rejects(d, "case X v. Y missing citation")


if __name__ == "__main__":
    unittest.main()
