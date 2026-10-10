import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lint_resume as l

GOOD = """# Jane Doe
jane@example.com

## Experience
- Reduced deployment time 40% by migrating 12 pipelines to GitHub Actions
- Automated Terraform provisioning for 30 AKS clusters

## Education
MS, Business

## Skills
Terraform, Kubernetes
"""
class Lint(unittest.TestCase):
    def test_clean(self):
        e, w = l.lint(GOOD); self.assertEqual((e, w), ([], []))
    def test_missing_sections_and_email(self):
        e, _ = l.lint("# X\n- Built 3 things\n")
        self.assertEqual(sum("missing section" in x for x in e), 3); self.assertIn("no email address", e)
    def test_todo_is_error(self):
        e, _ = l.lint(GOOD + "\n[TODO: metric]\n"); self.assertIn("unfilled [TODO] placeholder", e)
    def test_weak_verb_and_phrase(self):
        _, w = l.lint(GOOD + "- Responsible for deployments of 5 apps\n")
        self.assertTrue(any("action verb" in x for x in w)); self.assertTrue(any("weak phrase" in x for x in w))
    def test_no_metric_and_pronoun(self):
        _, w = l.lint(GOOD + "- Built things that I loved\n")
        self.assertTrue(any("no number" in x for x in w)); self.assertTrue(any("first-person" in x for x in w))
    def test_long_bullet(self):
        _, w = l.lint(GOOD + "- Built " + "x" * 230 + " 1\n"); self.assertTrue(any("over 220" in x for x in w))
    def test_too_many_bullets(self):
        _, w = l.lint(GOOD + "\n" + "".join(f"- Built {i} things\n" for i in range(8)))
        self.assertTrue(any("consecutive bullets" in x for x in w))
    def test_table_warning(self):
        _, w = l.lint(GOOD + "| a | b |\n"); self.assertTrue(any("table" in x for x in w))
    def test_contact_line_pipes_ok(self):
        _, w = l.lint(GOOD.replace("jane@example.com", "Dallas, TX | jane@example.com | 555-0100 | linkedin.com/in/j"))
        self.assertFalse(any("table" in x for x in w))
    def test_round_bullets_recognised(self):
        _, w = l.lint(GOOD + "\u25cf Responsible for 5 deploys\n"); self.assertTrue(any("action verb" in x for x in w))
    def test_valid_verb_forms_pass(self):
        for v in ("Troubleshot", "Administered", "Applied", "Lead", "Own", "Built", "Led", "Migrated"):
            self.assertTrue(l.is_action_verb(v.lower()), v)
    def test_non_verbs_fail(self):
        for v in ("responsible", "various", "experience", "the", "seed"):
            self.assertFalse(l.is_action_verb(v), v)

if __name__ == "__main__":
    unittest.main()
