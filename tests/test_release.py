"""Checks the release files agree with each other and with the data.
Run from the repo root:  python3 -m unittest discover tests
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def cff(key):
    m = re.search(r'^' + key + r':\s*"?([^"\n]+)"?', (ROOT / "CITATION.cff").read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else None


class Tests(unittest.TestCase):
    def setUp(self):
        self.zen = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.india = json.loads((ROOT / "data" / "india.json").read_text(encoding="utf-8"))
        self.dir = json.loads((ROOT / "data" / "authorities.json").read_text(encoding="utf-8"))
        self.models = json.loads((ROOT / "data" / "models.json").read_text(encoding="utf-8"))

    def test_citation_and_zenodo_agree(self):
        self.assertEqual(cff("version"), self.zen["version"])
        self.assertEqual(cff("license"), "CC-BY-4.0")
        self.assertEqual(self.zen["license"], "cc-by-4.0")
        self.assertEqual(cff("title").strip('"'), self.zen["title"])
        self.assertRegex(cff("date-released"), r"^\d{4}-\d{2}-\d{2}$")

    def test_frozen_pilot_tag_is_not_reused(self):
        self.assertNotEqual(cff("version"), "0.1.0-pilot")

    def test_readme_figures_match_the_data(self):
        i = self.india
        unverified = sum(1 for x in i["instruments"] if x["verified"] != "yes")
        for text in (f"| Indian AI incidents | {len(i['incidents'])} |", f"| {len(i['instruments'])} |",
                     f"{len(i['instruments']) - unverified} verified against official texts; {unverified} partly verified",
                     f"| {len(i['risks'])} |", f"| Governance gaps | {len(i['gaps'])} |",
                     f"{len(self.dir['bodies'])} bodies", f"| AI model cards | {len(self.models['models'])} |",
                     f"data updated {i['meta']['updated']}"):
            self.assertIn(text, self.readme)
        if all(x["review"] == "human_reviewed" for x in i["incidents"]):
            self.assertIn("All reviewed by the maintainer", self.readme)

    def test_citation_abstract_matches_the_data(self):
        abstract = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        for n, what in ((len(self.india["incidents"]), "documented Indian incidents"), (len(self.dir["bodies"]), "Union and state bodies"),
                        (len(self.models["models"]), "AI model cards")):
            self.assertRegex(abstract.replace("\n  ", " "), rf"{n} {what}")

    def test_every_document_linked_from_the_readme_exists(self):
        for target in re.findall(r"\]\(((?:docs/|[A-Z-]+\.md)[^)#]*)\)", self.readme):
            self.assertTrue((ROOT / target).exists(), target)

    def test_roadmap_names_the_three_planned_areas(self):
        road = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
        for heading in ("## Live reporting", "## MIT AI Risk Repository import", "## Further sources"):
            self.assertIn(heading, road)


if __name__ == "__main__":
    unittest.main()
