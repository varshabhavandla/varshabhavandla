import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import skillify_check as k

GOOD = "---\nname: demo\ndescription: Does x. USE WHEN a. NOT FOR b.\n---\nTier: J\n"
CASES = '{"should_trigger":["a","b","c"],"should_not_trigger":["d","e","f"]}'

def make(root, skill=GOOD, cases=CASES, reg="demo"):
    d = Path(root) / "demo"; (d / "evals").mkdir(parents=True)
    (d / "SKILL.md").write_text(skill)
    if cases is not None: (d / "evals" / "cases.json").write_text(cases)
    if reg: (Path(root) / "SKILLS.md").write_text(f"| {reg} | J |")
    return d

class Gate(unittest.TestCase):
    def test_good(self):
        with tempfile.TemporaryDirectory() as r:
            self.assertEqual(k.check_skill(make(r)), [])
    def test_name_mismatch(self):
        with tempfile.TemporaryDirectory() as r:
            self.assertTrue(any("name" in e for e in k.check_skill(make(r, GOOD.replace("name: demo", "name: other")))))
    def test_missing_not_for(self):
        with tempfile.TemporaryDirectory() as r:
            self.assertTrue(any("NOT FOR" in e for e in k.check_skill(make(r, GOOD.replace(" NOT FOR b.", "")))))
    def test_missing_tier(self):
        with tempfile.TemporaryDirectory() as r:
            self.assertTrue(any("Tier" in e for e in k.check_skill(make(r, GOOD.replace("Tier: J", "")))))
    def test_few_cases(self):
        with tempfile.TemporaryDirectory() as r:
            self.assertTrue(any(">=3" in e for e in k.check_skill(make(r, cases='{"should_trigger":["a"],"should_not_trigger":[]}'))))
    def test_unregistered(self):
        with tempfile.TemporaryDirectory() as r:
            self.assertTrue(any("registered" in e for e in k.check_skill(make(r, reg=None))))
    def test_tier_d_needs_scripts(self):
        with tempfile.TemporaryDirectory() as r:
            self.assertTrue(any("scripts" in e for e in k.check_skill(make(r, GOOD.replace("Tier: J", "Tier: D")))))
if __name__ == "__main__":
    unittest.main()
