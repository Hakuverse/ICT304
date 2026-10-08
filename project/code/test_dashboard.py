"""Tests for the dashboard (Issues #54 and #55).

Run from the repository root:
    python -m unittest discover -s project/code -v
"""

import io
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

import dashboard
from predict import predict_one, predict_roster

DASHBOARD = str(Path(__file__).with_name("dashboard.py"))


class SingleStudentLogic(unittest.TestCase):
    """#54: the form gives the same answer as predict.py."""

    def test_early_warning_matches_predict_one(self):
        label, proba, setup = dashboard.predict_single("early_warning", 60, 4, 1)
        self.assertEqual((label, proba), predict_one(60, 4, 1, "early_warning"))
        self.assertIsNone(setup)

    def test_g1_only_routes_to_g1_model(self):
        label, proba, setup = dashboard.predict_single("confirmatory", 60, 4, 1, "12", "")
        self.assertEqual(setup, "g1")
        self.assertEqual((label, proba), predict_one(60, 4, 1, "confirmatory", 12, None))

    def test_g1_and_g2_routes_to_combined_model(self):
        _, _, setup = dashboard.predict_single("confirmatory", 60, 4, 1, "12", "14")
        self.assertEqual(setup, "g1_g2")

    def test_g2_zero_is_a_valid_grade(self):
        _, _, setup = dashboard.predict_single("confirmatory", 60, 4, 1, "12", "0")
        self.assertEqual(setup, "g1_g2")

    def test_missing_g1_rejected(self):
        with self.assertRaisesRegex(ValueError, "G1 is required"):
            dashboard.predict_single("confirmatory", 60, 4, 1, "", "14")

    def test_invalid_g2_text_rejected(self):
        with self.assertRaises(ValueError):
            dashboard.predict_single("confirmatory", 60, 4, 1, "12", "NA")

    def test_g1_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            dashboard.predict_single("confirmatory", 60, 4, 1, "21", "")

    def test_study_hours_boundaries(self):
        dashboard.predict_single("early_warning", 60, 0, 1)
        dashboard.predict_single("early_warning", 60, 40, 1)
        with self.assertRaises(ValueError):
            dashboard.predict_single("early_warning", 60, 41, 1)


class ClassUploadLogic(unittest.TestCase):
    """#55: an uploaded file (file-like object) is handled like a CSV path."""

    def upload(self, text, mode="confirmatory"):
        return predict_roster(io.BytesIO(text.encode("utf-8")), mode)

    def test_sample_file_keeps_valid_and_skips_invalid(self):
        results, skipped = predict_roster(io.BytesIO(dashboard.SAMPLE_CSV.read_bytes()), "confirmatory")
        self.assertEqual(list(results["student_id"]), ["A", "B"])
        self.assertEqual(list(results["grade_setup"]), ["g1", "g1_g2"])
        self.assertEqual([s["student_id"] for s in skipped], ["C", "D"])

    def test_missing_column_reported(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns: G1"):
            self.upload("student_id,attendance_pct,study_hours,failures\nA,60,4,1\n")

    def test_header_only_file_reported(self):
        with self.assertRaisesRegex(ValueError, "no students"):
            self.upload("student_id,attendance_pct,study_hours,failures,G1,G2\n")

    def test_empty_file_reported(self):
        with self.assertRaisesRegex(ValueError, "no students"):
            self.upload("")

    def test_all_invalid_file_returns_no_results(self):
        results, skipped = self.upload(
            "student_id,attendance_pct,study_hours,failures,G1,G2\nX,150,4,1,12,\nY,60,99,1,12,\n")
        self.assertTrue(results.empty)
        self.assertEqual(len(skipped), 2)


class DashboardScreen(unittest.TestCase):
    """The page itself loads and the form works in both modes."""

    def test_page_loads_without_errors(self):
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.title[0].value, "SARAH - Student Academic Risk Assistance Hub")

    def test_early_warning_form_shows_result(self):
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertTrue(any("Risk" in s.value for s in at.success) or any("Risk" in e.value for e in at.error))

    def test_old_result_clears_when_input_or_mode_changes(self):
        # Note: AppTest reruns on every set_value, so it cannot see the
        # browser-only st.form behaviour (no rerun until submit). The real-browser
        # check is the screenshot evidence in the PR; this guards the rerun logic.
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        at.button[0].click().run()
        self.assertIn("Estimated High-Risk probability", " ".join(m.value for m in at.markdown))
        at.number_input[0].set_value(50.0).run()  # change attendance
        self.assertNotIn("Estimated High-Risk probability", " ".join(m.value for m in at.markdown))
        at.button[0].click().run()
        at.radio[0].set_value("confirmatory").run()  # change mode
        self.assertNotIn("Estimated High-Risk probability", " ".join(m.value for m in at.markdown))

    def test_confirmatory_form_without_g1_shows_error(self):
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        at.radio[0].set_value("confirmatory").run()
        at.button[0].click().run()
        self.assertTrue(any("G1 is required" in e.value for e in at.error))


if __name__ == "__main__":
    unittest.main()
