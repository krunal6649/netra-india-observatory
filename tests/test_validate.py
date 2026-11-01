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
        self.dir = build.load("authorities.json")
        self.models = build.load("models.json")

    def rejects(self, india, text, directory=None):
        with self.assertRaises(build.ValidationError) as c:
            build.validate(self.tax, india, self.glob, directory or self.dir, getattr(self, "_models", None) or self.models)
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

    def test_batch_two_reviewed_by_owner(self):
        b2 = [i for i in self.india["incidents"] if i.get("batch") == "B2"]
        self.assertEqual(len(b2), 10)
        for i in b2:
            # Reviewed by the project owner on 2026-10-25; the validator separately requires reviewer, date and S11
            self.assertEqual((i["review"], i["reviewed_by"], i["netra"]["stages"]["S11"]), ("human_reviewed", "Krunal Maheshwari (project owner)", "done"), i["id"])
            self.assertTrue(i["sources"] and all(s["url"].startswith("https://") for s in i["sources"]))
        # Batch 2 was chosen to cover every risk domain
        self.assertEqual({d.split(".")[0] for i in b2 for d in i["domains"]}, {"1", "2", "3", "4", "5", "6", "7"})

    def test_duplicate_source_rejected(self):
        d = copy.deepcopy(self.india); new = copy.deepcopy(d["incidents"][0])
        new["id"], new["title"] = "IN-INC-99", "A differently worded headline about something"
        d["incidents"].append(new)
        self.rejects(d, "IN-INC-99: possible duplicate of IN-INC-01 (both cite")

    def test_duplicate_source_ignores_www_and_amp(self):
        d = copy.deepcopy(self.india); new = copy.deepcopy(d["incidents"][0])
        new["id"], new["title"] = "IN-INC-99", "A differently worded headline about something"
        u = new["sources"][0]["url"]
        new["sources"] = [{"title": "x", "url": u.replace("://", "://www.", 1) if "://www." not in u else u.replace("://www.", "://"), "date": "2026"}]
        d["incidents"].append(new)
        self.rejects(d, "possible duplicate of IN-INC-01")

    def test_near_identical_title_rejected(self):
        d = copy.deepcopy(self.india); new = copy.deepcopy(d["incidents"][2])
        new["id"] = "IN-INC-99"; new["title"] = new["title"].replace("Kozhikode man", "Kozhikode resident")
        new["sources"] = [{"title": "x", "url": "https://example.org/other-report", "date": "2026"}]
        d["incidents"].append(new)
        self.rejects(d, "IN-INC-99: possible duplicate of IN-INC-03 (titles")

    def test_distinct_from_allows_checked_lookalikes(self):
        d = copy.deepcopy(self.india); new = copy.deepcopy(d["incidents"][2])
        new["id"] = "IN-INC-99"; new["title"] = new["title"].replace("Kozhikode man", "Kozhikode resident")
        new["sources"] = [{"title": "x", "url": "https://example.org/other-report", "date": "2026"}]
        new["distinct_from"] = ["IN-INC-03"]
        d["incidents"].append(new)
        build.validate(self.tax, d, self.glob)

    def test_incident_state_must_be_known(self):
        d = copy.deepcopy(self.india); d["incidents"][0]["state"] = "Bombay"
        self.rejects(d, "state must start with one of")

    def test_all_states_and_uts_listed(self):
        su = self.india["states_uts"]
        self.assertEqual((len(su["states"]), len(su["union_territories"])), (28, 8))

    def test_verified_authority_needs_checker(self):
        d = copy.deepcopy(self.india)
        a = next(x for x in d["authorities"] if x["verified"] == "yes"); a.pop("checked_by")
        self.rejects(d, "needs checked_by")

    def test_owner_checked_authorities(self):
        yes = {a["id"] for a in self.india["authorities"] if a["verified"] == "yes"}
        self.assertEqual(yes, {"A-NCRP", "A-GAC", "A-CERTIN", "A-ECI", "A-SC"})

    def test_directory_covers_union_and_all_places(self):
        b = self.dir["bodies"]
        self.assertGreaterEqual(sum(1 for x in b if x["level"] == "union"), 30)
        places = set(self.india["states_uts"]["states"]) | set(self.india["states_uts"]["union_territories"])
        self.assertEqual({x["place"] for x in b if x["level"] == "state"}, places)

    def test_directory_role(self):
        d = copy.deepcopy(self.dir); d["bodies"][0]["role"] = "helps"
        self.rejects(self.india, "role must be one of", d)

    def test_directory_verified_needs_checker(self):
        d = copy.deepcopy(self.dir); x = next(b for b in d["bodies"] if b["verified"] == "yes"); x.pop("checked_on")
        self.rejects(self.india, "needs a url, checked_by", d)

    def test_directory_unknown_law(self):
        d = copy.deepcopy(self.dir); d["bodies"][0]["laws"] = ["G-NOPE"]
        self.rejects(self.india, "unknown instrument G-NOPE", d)

    def test_incident_route_must_resolve(self):
        d = copy.deepcopy(self.dir); d["bodies"] = [x for x in d["bodies"] if x["id"] != "S-kerala-POLICE"]
        self.rejects(self.india, "points to Kerala, which has no POLICE body", d)

    def test_authority_directory_link_must_exist(self):
        d = copy.deepcopy(self.india); next(a for a in d["authorities"] if a["id"] == "A-NCRP")["directory"] = ["U-NOPE"]
        self.rejects(d, "directory link U-NOPE does not exist")

    def test_only_owner_checked_bodies_are_verified(self):
        yes = {x["id"] for x in self.dir["bodies"] if x["verified"] == "yes"}
        # Every body with a link has been opened and confirmed by the owner
        self.assertEqual(len(yes), 32)
        self.assertTrue(all(x["verified"] == "yes" for x in self.dir["bodies"] if x["url"]))

    def rejects_models(self, models, text):
        self._models = models
        try:
            self.rejects(self.india, text)
        finally:
            self._models = None

    def check_terms_rejects(self, terms, text):
        with self.assertRaises(build.ValidationError) as c:
            build.validate(self.tax, self.india, self.glob, self.dir, self.models, terms)
        self.assertIn(text, str(c.exception))

    def test_check_terms_cover_every_risk_area_and_law(self):
        t = build.load("check_terms.json")
        del t["risk_areas"]["7.6"]
        self.check_terms_rejects(t, "check_terms: risk_areas 7.6 has no terms")

    def test_check_terms_unknown_id_and_empty_term(self):
        t = build.load("check_terms.json")
        t["instruments"]["G-NOPE"] = ["x"]
        t["risk_areas"]["4.3"] = ["fraud", " "]
        self.check_terms_rejects(t, "unknown instruments id G-NOPE")
        self.check_terms_rejects(t, "risk_areas 4.3 needs a list of non-empty terms")

    def test_models_first_set(self):
        m = self.models["models"]
        self.assertTrue(10 <= len(m) <= 15)
        self.assertTrue(all(x["review"] == "unreviewed" for x in m))
        # The three METR reports from global evidence are all used
        self.assertEqual({t["report"] for x in m for t in x["tests"] if t.get("report")}, {"TR-001", "TR-002", "TR-003"})

    def test_model_overclaim_required(self):
        d = copy.deepcopy(self.models); d["models"][0]["netra"]["overclaim"] = "Looks bad."
        self.rejects_models(d, "not evidence of real-world harm")

    def test_model_unknown_body(self):
        d = copy.deepcopy(self.models); d["models"][0]["netra"]["authorities"] = ["U-NOPE"]
        self.rejects_models(d, "unknown directory body U-NOPE")

    def test_model_law_label(self):
        d = copy.deepcopy(self.models); d["models"][0]["netra"]["laws"][0]["label"] = "certain"
        self.rejects_models(d, "law label must be one of")

    def test_model_release_needs_source(self):
        d = copy.deepcopy(self.models); m = next(x for x in d["models"] if x.get("release_date")); m.pop("release_source")
        self.rejects_models(d, "needs a release_source")

    def test_model_cannot_be_reviewed_without_reviewer(self):
        d = copy.deepcopy(self.models); d["models"][0]["review"] = "human_reviewed"
        self.rejects_models(d, "a reviewed model needs reviewed_by")

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
        # Version 3: amendment history from the note to G.S.R. 120(E), Gazette of 10 February 2026
        self.assertEqual(nos("G-ITR21"), ["G.S.R. 139(E)", "G.S.R. 794(E)", "G.S.R. 275(E)", "G.S.R. 775(E)"])
        self.assertEqual(nos("G-ITR26"), ["G.S.R. 120(E)"])
        self.assertEqual(nos("G-DPDP"), ["G.S.R. 843(E)"])
        self.assertEqual(nos("G-DPDPR"), ["G.S.R. 846(E)"])
        for iid in ("G-ITR21", "G-ITA", "G-CPA"):
            self.assertEqual(self.ins(self.india, iid)["verified"], "partial", iid)
        self.assertEqual(self.ins(self.india, "G-ITR26")["verified"], "yes")
        # Version 3: the DPDP Act and its commencement were checked against the Gazettes of 11 Aug 2023 and 13 Nov 2025
        self.assertEqual(self.ins(self.india, "G-DPDP")["verified"], "yes")
        self.assertNotIn("gazette_url", self.ins(self.india, "G-DPDP"))
        # Version 3: the DPDP Rules were checked against the Gazette of 13 November 2025 (G.S.R. 846(E))
        rules = self.ins(self.india, "G-DPDPR")
        self.assertEqual((rules["verified"], rules["url"]), ("yes", "https://egazette.gov.in/WriteReadData/2025/267650.pdf"))
        # one warning per law record that is not fully verified
        self.assertEqual(len(build.validate(self.tax, self.india, self.glob)), sum(1 for i in self.india["instruments"] if i["verified"] != "yes"))

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
