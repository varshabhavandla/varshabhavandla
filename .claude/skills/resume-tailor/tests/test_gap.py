import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import keyword_gap as k

JD = "We need Terraform and Kubernetes experience. GitHub Actions CI/CD pipelines. Terraform modules, on-call, Datadog."
class Gap(unittest.TestCase):
    def test_phrases_found(self):
        kws = k.keywords(JD)
        for w in ("terraform", "kubernetes", "github actions", "ci/cd", "on-call", "datadog"):
            self.assertIn(w, kws)
    def test_repeat_words_found(self):
        self.assertIn("pipelines", k.keywords("pipelines pipelines pipelines"))
    def test_stopwords_excluded(self):
        self.assertNotIn("the", k.keywords("the the the the"))
    def test_gap(self):
        r = k.gap(JD, "Built Terraform modules on Kubernetes using GitHub Actions and CI/CD.")
        self.assertIn("datadog", r["missing"]); self.assertIn("on-call", r["missing"])
        self.assertIn("terraform", r["have"])
    def test_no_substring_false_positive(self):
        self.assertIn("go", k.gap("Go required", "mongodb algorithm")["missing"])
    def test_full_coverage(self):
        self.assertEqual(k.gap("Python Docker", "python and docker")["coverage_pct"], 100.0)
    def test_empty_jd(self):
        self.assertEqual(k.gap("", "anything")["coverage_pct"], 100.0)
if __name__ == "__main__":
    unittest.main()
