import sys, tempfile, zipfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import scaffold_workshop as s, check_draft as c

class Scaffold(unittest.TestCase):
    def test_creates_workshops(self):
        with tempfile.TemporaryDirectory() as r:
            s.scaffold(r, 1, 5)
            for k in range(1, 6):
                self.assertTrue((Path(r) / "GPT-1" / f"Workshop-{k}" / ".gitkeep").exists())
    def test_unzip_routes_by_item_number(self):
        with tempfile.TemporaryDirectory() as r:
            s.scaffold(r, 1, 5)
            z = Path(r) / "1.2 Discussion  Alignment.html.zip"
            with zipfile.ZipFile(z, "w") as f: f.writestr("a.html", "<p>x</p>")
            d = s.unzip(z, r, 1)
            self.assertEqual(d, Path(r) / "GPT-1" / "Workshop-1" / "1.2")
            self.assertTrue((d / "a.html").exists())
            self.assertFalse((d.parent / ".gitkeep").exists())
    def test_rejects_zip_slip(self):
        with tempfile.TemporaryDirectory() as r:
            z = Path(r) / "1.1 x.zip"
            with zipfile.ZipFile(z, "w") as f: f.writestr("../evil", "x")
            with self.assertRaises(ValueError): s.unzip(z, r, 1)
    def test_no_item_number(self):
        with self.assertRaises(ValueError): s.target_for("notes.zip", ".", 1)

class Words(unittest.TestCase):
    def test_count(self):
        self.assertEqual(c.count_words("It's a well-known fact, 2026."), 5)
    def test_range_parse(self):
        self.assertEqual(c.parse_limit("150-200 word written reflection"), (150, 200))
        self.assertEqual(c.parse_limit("between 300 to 500 words"), (300, 500))
        self.assertEqual(c.parse_limit("at least 250 words"), (250, None))
        self.assertEqual(c.parse_limit("no more than 100 words"), (None, 100))
        self.assertEqual(c.parse_limit("write something"), (None, None))
    def test_check(self):
        self.assertTrue(c.check("word " * 160, "150-200 word")[3])
        self.assertFalse(c.check("word " * 120, "150-200 word")[3])
        self.assertFalse(c.check("word " * 250, "150-200 word")[3])
        self.assertTrue(c.check("anything", "")[3])

if __name__ == "__main__":
    unittest.main()
