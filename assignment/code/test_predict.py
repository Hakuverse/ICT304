"""Run from the repository root: python -m unittest discover -s assignment/code -v

Covers the behaviours added in this PR that the existing test_data_processing.py
suite does not touch: routing a Confirmatory prediction to the correct
separately-trained model (G1-only vs G1+G2), reporting an invalid supplied G2
instead of silently treating it as absent, and CSV roster skip-invalid-rows
behaviour (including the 0-40 study_hours rule).
"""

import tempfile
import unittest
import io
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from predict import _parse_g2, load_model, predict_one, predict_roster, main


class TestParseG2(unittest.TestCase):
    def test_none_and_blank_are_treated_as_absent(self):
        for value in (None, "", "   "):
            self.assertIsNone(_parse_g2(value))

    def test_valid_numbers_pass_through(self):
        self.assertEqual(_parse_g2(14), 14.0)
        self.assertEqual(_parse_g2("14"), 14.0)
        self.assertEqual(_parse_g2(0), 0.0)

    def test_invalid_supplied_g2_is_reported_not_ignored(self):
        for bad in ("not-a-number", "twelve", "1,2"):
            with self.assertRaisesRegex(ValueError, "not a valid number"):
                _parse_g2(bad)

    def test_nonfinite_and_out_of_range_g2_rejected(self):
        for value in ("NA", "N/A", "null", "nan", float("nan"), "inf", -1, 21):
            with self.subTest(value=value), self.assertRaises(ValueError):
                _parse_g2(value)


class TestModelRouting(unittest.TestCase):
    """Confirms a G1-only prediction and a G1+G2 prediction load their own,
    separately-trained models -- never the same model for both cases."""

    def test_predict_one_loads_g1_model_when_g2_absent(self):
        with patch("predict.load_model", wraps=load_model) as spy:
            predict_one(70, 5, 0, mode="confirmatory", g1=12, g2=None)
            spy.assert_called_once_with("confirmatory", "g1")

    def test_predict_one_loads_g1_g2_model_when_g2_present(self):
        with patch("predict.load_model", wraps=load_model) as spy:
            predict_one(70, 5, 0, mode="confirmatory", g1=12, g2=14)
            spy.assert_called_once_with("confirmatory", "g1_g2")

    def test_load_model_rejects_confirmatory_without_grade_setup(self):
        with self.assertRaisesRegex(ValueError, "grade_setup must be"):
            load_model("confirmatory", None)

    def test_early_warning_ignores_grade_setup(self):
        # Should not raise even though grade_setup is meaningless here
        load_model("early_warning", None)


class TestPredictRoster(unittest.TestCase):
    def _write_csv(self, rows):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "roster.csv"
        pd.DataFrame(rows).to_csv(path, index=False)
        return path

    def test_empty_files_and_headers_only_stop_before_loading_models(self):
        for csv in ("", "\n", "attendance_pct,study_hours,failures\n"):
            with self.subTest(csv=csv), patch("predict.load_model") as model:
                with self.assertRaisesRegex(ValueError, "contains no students"):
                    predict_roster(io.StringIO(csv))
                model.assert_not_called()

    def test_missing_columns_stop_file_in_both_modes(self):
        for mode, csv, field in (
            ("early_warning", "attendance_pct,failures\n80,0\n", "study_hours"),
            ("confirmatory", "attendance_pct,study_hours,failures\n80,5,0\n", "G1"),
        ):
            with self.subTest(mode=mode), patch("predict.load_model") as model:
                with self.assertRaisesRegex(ValueError, f"Missing required columns: {field}"):
                    predict_roster(io.StringIO(csv), mode)
                model.assert_not_called()

    def test_csv_preserves_invalid_grade_text(self):
        for value in ("NA", "N/A", "null", "nan", "inf", "-1", "21"):
            csv = f"attendance_pct,study_hours,failures,G1,G2\n80,5,0,12,{value}\n"
            with self.subTest(value=value), patch("predict.load_model") as model:
                result, skipped = predict_roster(io.StringIO(csv), "confirmatory")
                self.assertTrue(result.empty)
                self.assertIn("G2", skipped[0]["reason"])
                model.assert_not_called()

    def test_blank_required_cells_report_field(self):
        for field in ("attendance_pct", "study_hours", "failures", "G1"):
            row = {"attendance_pct": "80", "study_hours": "5", "failures": "0", "G1": "12"}
            row[field] = " "
            with self.subTest(field=field):
                result, skipped = predict_roster(self._write_csv([row]), "confirmatory")
                self.assertTrue(result.empty)
                self.assertIn(field, skipped[0]["reason"])

    def test_absent_blank_and_zero_g2_choose_correct_setup(self):
        for suffix, value, expected in (("", "", "g1"), (",G2", ",   ", "g1"),
                                         (",G2", ",0", "g1_g2")):
            csv = f"attendance_pct,study_hours,failures,G1{suffix}\n80,5,0,12{value}\n"
            result, skipped = predict_roster(io.StringIO(csv), "confirmatory")
            self.assertEqual(skipped, [])
            self.assertEqual(result.iloc[0]["grade_setup"], expected)
            self.assertEqual(result.iloc[0]["student_id"], "row 1")

    def test_all_invalid_keeps_output_headers_and_prints_message(self):
        path = self._write_csv([{"attendance_pct": 150, "study_hours": 5, "failures": 0}])
        result, skipped = predict_roster(path)
        self.assertTrue(result.empty)
        self.assertEqual(list(result), ["student_id", "risk_label", "probability_high_risk"])
        with patch("sys.argv", ["predict.py", "--csv", str(path)]), patch("sys.stdout", new_callable=io.StringIO) as output:
            main()
        self.assertIn("No valid students to process.", output.getvalue())
        self.assertIn("attendance_pct", output.getvalue())

    def test_cli_structure_error_has_clear_message(self):
        path = self._write_csv([{"attendance_pct": 80}])
        with patch("sys.argv", ["predict.py", "--csv", str(path)]), patch("sys.stderr", new_callable=io.StringIO) as output:
            with self.assertRaises(SystemExit) as exit_result:
                main()
        self.assertEqual(exit_result.exception.code, 2)
        self.assertIn("Missing required columns", output.getvalue())

    def test_early_warning_skips_invalid_rows_processes_rest(self):
        path = self._write_csv([
            {"student_id": "S1", "attendance_pct": 80, "study_hours": 5, "failures": 0},
            {"student_id": "S2", "attendance_pct": 150, "study_hours": 5, "failures": 0},  # invalid
            {"student_id": "S3", "attendance_pct": 60, "study_hours": 999, "failures": 1},  # invalid (>40)
            {"student_id": "S4", "attendance_pct": 90, "study_hours": 0, "failures": 0},  # valid (0 allowed)
            {"student_id": "S5", "attendance_pct": 70, "study_hours": 40, "failures": 3},  # valid (40 allowed)
        ])
        results, skipped = predict_roster(path, "early_warning")
        self.assertEqual(sorted(results["student_id"]), ["S1", "S4", "S5"])
        self.assertEqual(sorted(s["student_id"] for s in skipped), ["S2", "S3"])

    def test_confirmatory_routes_g1_only_and_g1_g2_rows_and_reports_invalid_g2(self):
        path = self._write_csv([
            {"student_id": "A", "attendance_pct": 80, "study_hours": 5, "failures": 0, "G1": 15, "G2": ""},
            {"student_id": "B", "attendance_pct": 80, "study_hours": 5, "failures": 0, "G1": 15, "G2": 16},
            {"student_id": "C", "attendance_pct": 80, "study_hours": 5, "failures": 0, "G1": 15, "G2": "bad"},
            {"student_id": "D", "attendance_pct": 80, "study_hours": 5, "failures": 0, "G1": "", "G2": 16},
        ])
        results, skipped = predict_roster(path, "confirmatory")
        by_id = results.set_index("student_id")
        self.assertEqual(by_id.loc["A", "grade_setup"], "g1")
        self.assertEqual(by_id.loc["B", "grade_setup"], "g1_g2")
        self.assertEqual(sorted(s["student_id"] for s in skipped), ["C", "D"])
        self.assertIn("G2", [s["reason"] for s in skipped if s["student_id"] == "C"][0])
        self.assertIn("G1", [s["reason"] for s in skipped if s["student_id"] == "D"][0])


if __name__ == "__main__":
    unittest.main()
