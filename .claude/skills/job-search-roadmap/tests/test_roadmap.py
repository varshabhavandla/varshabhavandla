import sys, unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import make_roadmap as m

class Roadmap(unittest.TestCase):
    def test_week_count_and_dates(self):
        r = m.plan(15, 12, date(2026, 10, 12))
        self.assertEqual(len(r), 12)
        self.assertEqual(r[1]["start"], date(2026, 10, 19))
    def test_hours_sum_exactly(self):
        for hours in (7, 10, 12.5, 15, 20, 33):
            for wk in m.plan(hours, 12, date(2026, 1, 1)):
                self.assertAlmostEqual(sum(wk["hours"].values()), hours)
    def test_phase_order(self):
        names = [w["phase"] for w in m.plan(10, 12, date(2026, 1, 1))]
        self.assertEqual(names[0], "Foundation")
        self.assertEqual(names[-1], "Close")
        self.assertEqual(names, sorted(names, key=[p[0] for p in m.PHASES].index))
    def test_foundation_heavy_early(self):
        r = m.plan(20, 12, date(2026, 1, 1))
        self.assertGreater(r[0]["hours"]["foundation"], r[-1]["hours"]["foundation"])
    def test_bad_input(self):
        with self.assertRaises(ValueError): m.plan(0)
        with self.assertRaises(ValueError): m.plan(10, 2)
    def test_render_has_all_weeks(self):
        rows = [l for l in m.render(m.plan(10, 8, date(2026, 1, 1))).splitlines() if l.startswith("| ")]
        self.assertEqual(len(rows) - 1, 8)  # minus header row
if __name__ == "__main__":
    unittest.main()
