import sys
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from lint_config import lint  # noqa: E402

GOOD = {"profile": {}, "search": {"title_include": ["devops"], "skills": {"azure": 1}, "min_score": 20},
        "exclude_patterns": ["clearance"], "sources": {"greenhouse": ["stripe"], "lever": []}}


class T(unittest.TestCase):
    def test_good(self):
        self.assertEqual(lint(GOOD), [])

    def test_bad_regex(self):
        c = dict(GOOD, exclude_patterns=["(unclosed"])
        self.assertTrue(any("bad regex" in e for e in lint(c)))

    def test_bad_slug_and_type_and_dupes(self):
        c = dict(GOOD, sources={"greenhouse": ["ok", "ok", "has space"], "workday": ["x"]})
        e = " ".join(lint(c))
        self.assertIn("malformed slug", e)
        self.assertIn("duplicate", e)
        self.assertIn("unknown source type", e)

    def test_missing_and_score_range(self):
        self.assertTrue(lint({}))
        c = dict(GOOD, search={"title_include": ["x"], "skills": {"a": 1}, "min_score": 150})
        self.assertTrue(any("min_score" in e for e in lint(c)))

    def test_repo_config_passes(self):
        cfg = HERE.parents[3] / "job-alerts" / "config.yaml"
        if cfg.exists():
            self.assertEqual(lint(yaml.safe_load(cfg.read_text())), [])


if __name__ == "__main__":
    unittest.main()
