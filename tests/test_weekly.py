"""Checks the weekly selection with fixture feeds; no network is used.
Run from the repo root:  python3 -m unittest discover tests
"""
import json
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build  # noqa: E402
import weekly_top5 as wk  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "weekly"


def fake_get(url):
    """Serves the fixture that stands in for each source (the headlines are invented test data)."""
    if "gdeltproject" in url:
        return (FIX / ("gdelt_ai.json" if "deepfake" in url.lower() else "gdelt_cyber.json")).read_bytes()
    if "pib.gov.in" in url:
        if "Lang=1" in url:
            raise wk.SourceError("HTTPError: 404")
        return (FIX / "pib.xml").read_bytes()
    if "metr.org" in url:
        return (FIX / "metr.xml").read_bytes()
    if url.endswith("ATLAS-latest.yaml"):
        return (FIX / "atlas_latest.txt").read_bytes()
    if url.endswith("ATLAS-2026.10.yaml"):
        return (FIX / "atlas.yaml").read_bytes()
    raise wk.SourceError("unexpected url " + url)


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        real = wk.DATA / "weekly.json"
        cls.had = real.read_text(encoding="utf-8") if real.exists() else None
        if real.exists():
            real.unlink()   # start from an empty store so earlier weeks do not hide fixture items
        # PIB is switched off in production (it refuses GitHub's servers); switch it on here so feed reading stays tested
        saved = [f["enabled"] for f in wk.CONFIG["feeds"]]
        for f in wk.CONFIG["feeds"]:
            f["enabled"] = f["enabled"] or f["id"].startswith("pib")
        try:
            cls.store, cls.week = wk.run(date(2026, 10, 24), get=fake_get, sleep=lambda s: None)
        finally:
            for f, e in zip(wk.CONFIG["feeds"], saved):
                f["enabled"] = e
            if cls.had is not None:
                real.write_text(cls.had, encoding="utf-8")

    def test_week_window_is_the_past_seven_days(self):
        self.assertEqual((self.week["week_start"], self.week["week_end"]), ("2026-10-17", "2026-10-23"))

    def test_selects_india_ai_harms_and_clusters_the_same_story(self):
        titles = [t["title"] for t in self.week["top"]]
        self.assertTrue(any("voice clone" in t for t in titles))
        self.assertTrue(any("Kerala minister" in t for t in titles))
        clone = next(t for t in self.week["top"] if "voice clone" in t["title"])
        self.assertEqual(len(clone["sources"]), 2)
        self.assertIn("4.3", clone["risk_areas"])

    def test_no_harm_or_no_india_link_is_left_out(self):
        titles = " ".join(t["title"] for t in self.week["top"])
        self.assertNotIn("farmers", titles)
        self.assertNotIn("US court", titles)

    def test_existing_netra_record_is_not_repeated(self):
        self.assertFalse(any("Rashmika" in t["title"] for t in self.week["top"]))
        self.assertTrue(any("IN-INC-01" in n for n in self.week["notes"]))

    def test_cyber_watch_is_separate_and_has_no_ai_items(self):
        cy = [c["title"] for c in self.week["cyber"]]
        self.assertTrue(any("Ransomware" in t for t in cy))
        self.assertTrue(any("CERT-In" in t for t in cy))
        self.assertFalse(any("chatbot" in t.lower() for t in cy))
        top_urls = {s["url"] for t in self.week["top"] for s in t["sources"]}
        self.assertFalse(top_urls & {s["url"] for c in self.week["cyber"] for s in c["sources"]})

    def test_every_item_is_auto_selected_and_unreviewed_with_netras_own_summary(self):
        for it in self.week["top"] + self.week["cyber"]:
            self.assertEqual((it["auto_selected"], it["review"]), (True, "unreviewed"))
            self.assertTrue(it["summary"].startswith(("1 report", "2 reports", "3 reports")))
            self.assertNotIn(it["title"], it["summary"])
        self.assertLessEqual(len(self.week["top"]), 5)

    def test_fewer_than_five_is_reported_not_padded(self):
        self.assertLess(len(self.week["top"]), 5)
        self.assertTrue(any("does not pad" in n for n in self.week["notes"]))

    def test_model_watch_lists_new_atlas_and_metr_items_only(self):
        kinds = {(m["kind"], m["url"]) for m in self.week["models"]}
        self.assertIn(("MITRE ATLAS case study", "https://atlas.mitre.org/studies/AML.CS0099"), kinds)
        self.assertIn(("METR publication", "https://metr.example/test-pub"), kinds)
        self.assertFalse(any("CS0021" in m["title"] for m in self.week["models"]))

    def test_pib_is_off_in_production_after_the_403(self):
        self.assertFalse(any(f["enabled"] for f in wk.CONFIG["feeds"] if f["id"].startswith("pib")))

    def test_failed_and_switched_off_sources_are_reported(self):
        status = {s["name"]: s["status"] for s in self.week["sources"]}
        self.assertEqual(status["Press Information Bureau: press releases (RSS, Lang=1)"], "failed")
        self.assertEqual(status["CERT-In advisories"], "off")
        self.assertEqual(status["GDELT: AI news"], "ok")

    def test_gdelt_busy_is_retried_then_reported(self):
        calls, waits = [], []
        def busy_then_ok(url):
            calls.append(url)
            if len(calls) < 3:
                raise wk.SourceError("HTTPError: HTTP Error 429: Too Many Requests")
            return fake_get(url)
        arts = wk.gdelt(wk.CONFIG["gdelt"]["ai_query"], busy_then_ok, date(2026, 10, 17), date(2026, 10, 23), sleep=waits.append)
        self.assertTrue(arts)
        self.assertEqual(waits, wk.CONFIG["gdelt"]["retry_waits"][:2])
        always_busy = lambda url: (_ for _ in ()).throw(wk.SourceError("HTTPError: HTTP Error 429: Too Many Requests"))
        with self.assertRaises(wk.SourceError):
            wk.gdelt("x", always_busy, date(2026, 10, 17), date(2026, 10, 23), sleep=lambda s: None)

    def test_gdelt_spacing_is_cleaned(self):
        self.assertEqual(wk.clean_title("SBI data breach claim : Hackers access 3 . 75 lakh accounts"), "SBI data breach claim: Hackers access 3.75 lakh accounts")
        self.assertEqual(wk.clean_title("ID card made with AI - generated photo , police say"), "ID card made with AI-generated photo, police say")

    def test_violence_is_not_cyber_and_same_story_is_grouped(self):
        arts = [{"title": t, "url": f"https://x.example/{k}", "domain": d, "date": "2026-10-21", "via": "GDELT"} for k, (t, d) in enumerate([
            ("Bank data breach claim: hackers access 3.75 lakh accounts", "a.example"),
            ("Bank data exposure: what the dark-web breach means for 3.75 lakh accounts", "b.example"),
            ("Elderly man hacked to death in village over land dispute", "c.example")])]
        cyber, _ = wk.select(arts, "cyber", [], set(), [], {"risk_areas": {}}, {})
        self.assertEqual(len(cyber), 1)
        self.assertEqual(len(cyber[0]["sources"]), 2)

    def test_two_different_scams_with_the_same_topic_words_stay_apart(self):
        self.assertFalse(wk.same_story("Gang uses AI voice clone to cheat Surat trader", "AI voice clone used to cheat retired teacher in Nagpur"))
        self.assertTrue(wk.same_story("Bank data breach: hackers access 3.75 lakh accounts", "MP seeks probe into bank data breach affecting customers"))

    def test_indian_outlet_headline_without_a_place_counts_unless_it_names_another_country(self):
        self.assertTrue(wk.india_nexus("Deepfake scam: fraudsters fool us with cloned voice", [], indian_outlet=True))
        self.assertFalse(wk.india_nexus("US court fines chatbot maker over fake citations", [], indian_outlet=True))
        self.assertFalse(wk.india_nexus("Deepfake scam hits elderly", [], indian_outlet=False))

    def test_old_feed_items_are_outside_the_window(self):
        urls = {s["url"] for c in self.week["cyber"] + self.week["top"] for s in c["sources"]}
        self.assertNotIn("https://pib.gov.in/PressReleasePage.aspx?PRID=2", urls)

    def test_build_accepts_the_output_and_rejects_a_reviewed_or_overfull_week(self):
        errors = []
        build.check_weekly(self.store, build.load("india.json"), {s["id"] for d in build.load("taxonomy.json")["domains"] for s in d["subs"]}, errors)
        self.assertEqual(errors, [])
        bad = json.loads(json.dumps(self.store))
        bad["weeks"][0]["top"][0]["review"] = "human_reviewed"
        bad["weeks"][0]["top"] += [dict(bad["weeks"][0]["top"][1], id=f"W-x-{k}") for k in range(5)]
        errors = []
        build.check_weekly(bad, build.load("india.json"), set(), errors)
        self.assertTrue(any("at most 5" in e for e in errors))
        self.assertTrue(any("auto-selected and 'unreviewed'" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
