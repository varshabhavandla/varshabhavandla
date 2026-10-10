import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import compare_offers as c

class Offers(unittest.TestCase):
    def test_total(self):
        r = c.total({"name": "A", "base": 100000, "bonus_pct": 10, "equity_total": 80000, "vest_years": 4,
                     "signing": 5000, "match_pct": 4})
        self.assertEqual(r["steady"], 100000 + 10000 + 20000 + 4000)
        self.assertEqual(r["year1"], r["steady"] + 5000)
    def test_defaults(self):
        self.assertEqual(c.total({"name": "A", "base": 90000})["steady"], 90000)
    def test_sorted_by_steady(self):
        r = c.compare([{"name": "low", "base": 80000}, {"name": "high", "base": 120000}])
        self.assertEqual([x["name"] for x in r], ["high", "low"])
    def test_validation(self):
        for bad in ({"base": 1}, {"name": "x"}, {"name": "x", "base": 0}, {"name": "x", "base": 1, "vest_years": 0}):
            with self.assertRaises(ValueError): c.total(bad)
if __name__ == "__main__":
    unittest.main()
