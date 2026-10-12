import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jobalerts.filtering import evaluate  # noqa: E402
from jobalerts.sources import Job  # noqa: E402

CFG = yaml.safe_load((Path(__file__).resolve().parents[1] / "config.yaml").read_text())
NOW = datetime(2026, 10, 12, tzinfo=timezone.utc)


def job(**kw):
    d = dict(uid="x", company="c", title="Senior Platform Engineer", location="Remote - US",
             url="u", description="Azure Kubernetes Terraform GitOps ArgoCD Helm Prometheus",
             posted=NOW - timedelta(minutes=3))
    d.update(kw)
    return Job(**d)


class T(unittest.TestCase):
    def test_match(self):
        keep, sc, hits, _ = evaluate(job(), CFG, NOW)
        self.assertTrue(keep)
        self.assertIn("terraform", hits)

    def test_citizenship_blocked(self):
        keep, *_, r = evaluate(job(description="Azure Kubernetes Terraform. Must be a U.S. citizen."), CFG, NOW)
        self.assertFalse(keep)
        self.assertTrue(r.startswith("blocked"))

    def test_clearance_blocked(self):
        self.assertFalse(evaluate(job(description="Azure Terraform; active Secret clearance required"), CFG, NOW)[0])

    def test_title_and_location_and_stale(self):
        self.assertFalse(evaluate(job(title="Account Executive"), CFG, NOW)[0])
        self.assertFalse(evaluate(job(location="London, UK"), CFG, NOW)[0])
        self.assertFalse(evaluate(job(posted=NOW - timedelta(days=5)), CFG, NOW)[0])
        self.assertFalse(evaluate(job(title="DevOps Intern"), CFG, NOW)[0])


if __name__ == "__main__":
    unittest.main()
