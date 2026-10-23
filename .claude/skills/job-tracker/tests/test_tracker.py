import sys, tempfile, unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tracker as t

class Tracker(unittest.TestCase):
    def test_add_ids_increment(self):
        rows = []
        a = t.add(rows, "Acme", "SRE"); b = t.add(rows, "Beta", "DevOps")
        self.assertEqual((a["id"], b["id"]), ("1", "2"))
    def test_wishlist_has_no_applied_date(self):
        self.assertEqual(t.add([], "A", "R", status="wishlist")["date_applied"], "")
    def test_bad_status(self):
        with self.assertRaises(ValueError): t.add([], "A", "R", status="ghosted")
        rows = []; t.add(rows, "A", "R")
        with self.assertRaises(ValueError): t.update(rows, 1, status="nope")
    def test_update_and_missing(self):
        rows = []; t.add(rows, "A", "R")
        self.assertEqual(t.update(rows, 1, status="interview", notes="x")["status"], "interview")
        with self.assertRaises(KeyError): t.update(rows, 9, status="offer")
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sub" / "t.csv"; rows = []
            t.add(rows, "A, Inc", 'Role "x"'); t.save(p, rows)
            self.assertEqual(t.load(p), rows)
        self.assertEqual(t.load("/nonexistent/x.csv"), [])
    def test_due_only_open_and_sorted(self):
        rows = []
        for c, s, nd in [("A", "applied", "2026-10-05"), ("B", "rejected", "2026-10-01"),
                         ("C", "screen", "2026-10-02"), ("D", "applied", "2026-12-01")]:
            r = t.add(rows, c, "R", status=s); r["next_action_date"] = nd; r["next_action"] = "x"
        self.assertEqual([r["company"] for r in t.due(rows, date(2026, 10, 10))], ["C", "A"])
    def test_stats(self):
        rows = []
        for s in ("applied", "applied", "screen", "interview", "rejected", "wishlist"):
            t.add(rows, "X", "R", status=s)
        st = t.stats(rows)
        self.assertEqual(st["applied_total"], 5)
        self.assertEqual(st["interview_rate"], 40.0)
        self.assertEqual(st["response_rate"], 60.0)
    def test_empty_stats(self):
        self.assertEqual(t.stats([])["response_rate"], 0.0)
if __name__ == "__main__":
    unittest.main()
