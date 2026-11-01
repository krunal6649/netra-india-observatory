"""The page carries a schema.org/Dataset description for Google Dataset Search, built from the data."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402


class DatasetJsonLd(unittest.TestCase):
    def setUp(self):
        self.india, self.dir, self.models = build.load("india.json"), build.load("authorities.json"), build.load("models.json")
        html = build.dataset_jsonld(self.india, self.dir, self.models)
        self.data = json.loads(re.search(r"<script type=\"application/ld\+json\">\n(.*)\n</script>", html, re.S).group(1).replace("<\\/", "</"))

    def test_is_a_dataset_with_licence_and_creator(self):
        d = self.data
        self.assertEqual((d["@context"], d["@type"]), ("https://schema.org", "Dataset"))
        self.assertEqual(d["license"], "https://creativecommons.org/licenses/by/4.0/")
        self.assertEqual(d["creator"]["name"], "Krunal Maheshwari")
        self.assertTrue(d["creator"]["@id"].startswith("https://orcid.org/"))

    def test_counts_and_release_come_from_the_data(self):
        d = self.data
        self.assertIn(f"{len(self.india['incidents'])} documented Indian AI incidents", d["description"])
        self.assertIn(f"{len(self.dir['bodies'])} Union and state bodies", d["description"])
        cff = (ROOT / "CITATION.cff").read_text()
        self.assertIn(f'version: "{d["version"]}"', cff)
        self.assertIn(d["identifier"].replace("https://doi.org/", ""), cff)

    def test_downloads_exist_in_the_repository(self):
        for dist in self.data["distribution"]:
            name = dist["contentUrl"].rsplit("/", 1)[1]
            self.assertTrue((ROOT / "data" / name).exists(), name)

    def test_built_page_has_it_in_head(self):
        page = (ROOT / "index.html").read_text()
        self.assertLess(page.index("application/ld+json"), page.index("</head>"))
        self.assertNotIn(build.JSONLD, page)


if __name__ == "__main__":
    unittest.main()
