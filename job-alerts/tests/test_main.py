import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jobalerts import main  # noqa: E402
from jobalerts.sources import Job  # noqa: E402

CFG = str(Path(__file__).resolve().parents[1] / "config.yaml")


def mk(i, **kw):
    d = dict(uid=f"j{i}", company="acme", title="Cloud Platform Engineer", location="Remote, US", url="http://x",
             description="Azure Kubernetes Terraform GitOps ArgoCD Helm", posted=datetime.now(timezone.utc) - timedelta(minutes=2))
    d.update(kw)
    return Job(**d)


class T(unittest.TestCase):
    def test_seed_then_alert_dedupe(self):
        with tempfile.TemporaryDirectory() as d:
            st = str(Path(d) / "seen.json")
            with mock.patch.object(main.sources, "fetch_all", return_value=[mk(1)]), \
                 mock.patch.object(main.notify, "send") as send:
                self.assertEqual(main.run(CFG, st, False), 0)  # first run seeds silently
                send.assert_not_called()
            with mock.patch.object(main.sources, "fetch_all", return_value=[mk(1), mk(2), mk(3, description="US citizen only")]), \
                 mock.patch.object(main.notify, "send") as send, mock.patch.object(main.tailor, "draft", return_value="d"):
                self.assertEqual(main.run(CFG, st, False), 1)
                self.assertEqual(send.call_count, 1)
                self.assertEqual(main.run(CFG, st, False), 0)  # nothing new second time
            self.assertEqual(len(json.loads(Path(st).read_text())), 3)


if __name__ == "__main__":
    unittest.main()
