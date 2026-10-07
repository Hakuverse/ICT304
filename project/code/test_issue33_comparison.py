"""Check the comparison script's output paths without touching repository evidence."""

import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestComparisonOutputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.repo = Path(cls.temp.name)
        source = Path(__file__).resolve().parents[2]
        cls.script = source / "project/code/issue33_comparison.py"
        cls.inputs = ["project/code/data_processing.py", "project/code/train_models.py",
                      "project/docs/evaluation_report.md", "project/data/student-mat.csv"]
        for setup in ("early_warning", "confirmatory_g1", "confirmatory_g1_g2"):
            cls.inputs.extend([f"project/models/{setup}_model.joblib",
                               f"project/docs/figures/confusion_{setup}.png"])
        for name in cls.inputs:
            target = cls.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, target)
        cls.before = cls.hash_inputs()
        cls.command = [sys.executable, str(cls.script), "--repo", str(cls.repo)]
        subprocess.run(cls.command, capture_output=True, text=True, check=True)

    @classmethod
    def hash_inputs(cls):
        return {name: hashlib.sha256((cls.repo / name).read_bytes()).hexdigest()
                for name in cls.inputs}

    def test_outputs_and_links_preserve_existing_evidence(self):
        docs = self.repo / "project/docs"
        expected = {"issue33_report.md", "run_details.txt", "development_comparison.csv",
                    "final_test_results.csv", "feature_importance.csv",
                    "figures/early_warning_feature_importance.png"}
        existing = {Path(p).relative_to("project/docs").as_posix()
                    for p in self.inputs if p.startswith("project/docs/")}
        actual = {p.relative_to(docs).as_posix() for p in docs.rglob("*") if p.is_file()}
        self.assertEqual(actual, expected | existing)
        self.assertFalse((docs / "issue33").exists())
        for link in re.findall(r"!\[[^]]*\]\(([^)]+)\)",
                               (docs / "issue33_report.md").read_text(encoding="utf-8")):
            self.assertTrue((docs / link).is_file(), link)
        self.assertEqual(self.before, self.hash_inputs())

    def test_repeat_requires_explicit_overwrite(self):
        report = self.repo / "project/docs/issue33_report.md"
        original = report.read_bytes()
        result = subprocess.run(self.command, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--overwrite", result.stderr)
        self.assertEqual(original, report.read_bytes())
        subprocess.run(self.command + ["--overwrite"], capture_output=True, text=True, check=True)
        self.assertEqual(original, report.read_bytes())
        self.assertEqual(self.before, self.hash_inputs())

    def test_missing_confusion_matrix_stops_before_writes(self):
        image = self.repo / "project/docs/figures/confusion_early_warning.png"
        saved = image.read_bytes()
        report = self.repo / "project/docs/issue33_report.md"
        original = report.read_bytes()
        image.unlink()
        try:
            result = subprocess.run(self.command + ["--overwrite"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Missing existing confusion matrices", result.stderr)
            self.assertEqual(original, report.read_bytes())
        finally:
            image.write_bytes(saved)


if __name__ == "__main__":
    unittest.main()
