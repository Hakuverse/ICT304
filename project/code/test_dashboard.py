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


class UploadStructureChecks(unittest.TestCase):
    """Messy files a tutor might really upload. The dashboard must never give a
    student a prediction from the wrong numbers, and totals must always add up."""

    H = "student_id,attendance_pct,study_hours,failures,G1,G2\n"

    def process(self, text, mode="confirmatory"):
        results, skipped, total = dashboard.process_upload(text, mode)
        self.assertEqual(len(results) + len(skipped), total, "predicted + skipped must equal rows")
        return results, skipped

    def test_extra_comma_skips_that_row_instead_of_shifting_columns(self):
        results, skipped = self.process(self.H + "A,60,4,1,12,14,99\nB,80,5,0,12,14\n")
        self.assertEqual(list(results["student_id"]), ["B"])
        self.assertEqual(results["probability_high_risk"].iloc[0], predict_one(80, 5, 0, "confirmatory", 12, 14)[1])
        self.assertIn("has 7 values but the header has 6", skipped[0]["reason"])

    def test_missing_comma_skips_that_row(self):
        results, skipped = self.process(self.H + "A,60,4,1,12\nB,80,5,0,12,14\n")
        self.assertEqual(list(results["student_id"]), ["B"])
        self.assertIn("has 5 values", skipped[0]["reason"])

    def test_unmatched_quote_rejects_file_clearly(self):
        with self.assertRaisesRegex(ValueError, "unmatched quote"):
            self.process(self.H + 'A,"60,4,1,12,14\nB,80,5,0,12,14\n')

    def test_header_case_and_spaces_are_accepted(self):
        results, _ = self.process(" Student_ID ,Attendance_pct, study_hours ,FAILURES, g1, g2\nA,60,4,1,12,\n")
        self.assertEqual(list(results["grade_setup"]), ["g1"])

    def test_duplicate_column_rejected(self):
        with self.assertRaisesRegex(ValueError, "more than once: G1"):
            self.process("student_id,G1,attendance_pct,study_hours,failures,g1\nA,12,60,4,1,13\n")

    def test_rows_without_ids_keep_their_original_row_numbers(self):
        results, skipped = self.process("attendance_pct,study_hours,failures\n60,4,1\n150,4,1\n80,5,0\n",
                                        "early_warning")
        self.assertEqual(list(results["student_id"]), ["row 1", "row 3"])
        self.assertEqual(skipped[0]["student_id"], "row 2")

    def test_all_rows_wrong_length_gives_no_results_not_a_crash(self):
        results, skipped = self.process(self.H + "A,1\nB,2\n")
        self.assertTrue(results.empty)
        self.assertEqual(len(skipped), 2)

    def test_windows_line_endings_blank_lines_and_spaces(self):
        text = (self.H + "\nA, 60 , 4 , 1 , 12 ,\n\nB,80,5,0,12,14\n").replace("\n", "\r\n")
        results, skipped = self.process(text)
        self.assertEqual(list(results["student_id"]), ["A", "B"])
        self.assertEqual(skipped, [])

    def test_sample_file_matches_command_line(self):
        results, skipped = self.process(dashboard.SAMPLE_CSV.read_text())
        cli_results, cli_skipped = predict_roster(dashboard.SAMPLE_CSV, "confirmatory")
        self.assertEqual(results.to_dict("records"), cli_results.to_dict("records"))
        self.assertEqual(skipped, cli_skipped)


class RecommendationContract(unittest.TestCase):
    """The #52 contract: recommend(student_fields, prediction) -> list[str].
    A stand-in recommend() records what the dashboard passes, so these tests work
    before Jackie's real recommend.py exists."""

    KEYS = {"mode", "attendance_pct", "study_hours", "failures", "previous_score"}

    def setUp(self):
        self.calls = []

        def fake(student_fields, prediction):
            self.calls.append((student_fields, prediction))
            return [f"{prediction}: att={student_fields['attendance_pct']}", "second message"]
        self.fake = fake

    def test_form_fields_early_warning(self):
        fields = dashboard.form_student_fields("early_warning", 40, 4, 0)
        self.assertEqual(set(fields), self.KEYS)
        self.assertEqual(fields, {"mode": "early_warning", "attendance_pct": 40.0, "study_hours": 4.0,
                                  "failures": 0, "previous_score": None})

    def test_form_fields_confirmatory_scores(self):
        self.assertEqual(dashboard.form_student_fields("confirmatory", 80, 4, 0, "8", "")["previous_score"], 40.0)
        self.assertEqual(dashboard.form_student_fields("confirmatory", 80, 4, 0, "8", "12")["previous_score"], 50.0)
        self.assertEqual(dashboard.form_student_fields("confirmatory", 80, 4, 0, "12", "0")["previous_score"], 30.0)

    def test_prediction_is_passed_as_plain_label_text(self):
        messages, error = dashboard.get_recommendations(
            dashboard.form_student_fields("early_warning", 40, 4, 0), "High Risk", self.fake)
        self.assertIsNone(error)
        self.assertEqual(self.calls[0][1], "High Risk")
        self.assertIsInstance(messages, list)

    def test_bad_return_value_is_reported_not_crashed(self):
        _, error = dashboard.get_recommendations({}, "High Risk", lambda f, p: "not a list")
        self.assertIn("list", error)
        _, error = dashboard.get_recommendations({}, "High Risk", lambda f, p: 1 / 0)
        self.assertIn("ZeroDivisionError", error)

    def test_no_recommend_py_means_placeholder(self):
        saved, dashboard.recommend = dashboard.recommend, None
        try:
            self.assertEqual(dashboard.get_recommendations({}, "High Risk"), (None, None))
        finally:
            dashboard.recommend = saved

    def test_csv_each_valid_row_gets_its_own_fields_even_with_duplicate_ids(self):
        text = ("student_id,attendance_pct,study_hours,failures,G1,G2\n"
                "A,40,4,0,8,\nA,90,6,1,12,14\nC,150,4,0,12,\nD,80,5,0,12,0\n")
        results, skipped, total = dashboard.process_upload(text, "confirmatory", self.fake)
        self.assertEqual(len(results) + len(skipped), total)
        self.assertEqual(list(results["student_id"]), ["A", "A", "D"])       # file order kept
        self.assertEqual([s["student_id"] for s in skipped], ["C"])           # skipped row: no call
        self.assertEqual(len(self.calls), 3)
        fields = [c[0] for c in self.calls]
        self.assertTrue(all(set(f) == self.KEYS for f in fields))
        self.assertEqual([f["attendance_pct"] for f in fields], [40.0, 90.0, 80.0])
        self.assertEqual([f["previous_score"] for f in fields], [40.0, 65.0, 30.0])  # G2 = 0 is a grade
        self.assertEqual([c[1] for c in self.calls], list(results["risk_label"]))
        self.assertTrue(results["recommendations"].iloc[0].startswith(results["risk_label"].iloc[0]))
        self.assertIn("recommendations", results.to_csv(index=False).splitlines()[0])  # in the download

    def test_csv_early_warning_rows_have_no_previous_score(self):
        dashboard.process_upload(dashboard.SAMPLE_CSV.read_text(), "early_warning", self.fake)
        self.assertTrue(self.calls)
        self.assertTrue(all(c[0]["previous_score"] is None and c[0]["mode"] == "early_warning"
                            for c in self.calls))

    def test_same_student_same_fields_through_form_and_csv(self):
        dashboard.process_upload("student_id,attendance_pct,study_hours,failures,G1,G2\nS,60,1.5,2,9,11\n",
                                 "confirmatory", self.fake)
        form = dashboard.form_student_fields("confirmatory", 60, 1.5, 2, "9", "11")
        self.assertEqual(self.calls[0][0], form)

    def test_csv_without_recommend_has_no_recommendation_column(self):
        results, _, _ = dashboard.process_upload(dashboard.SAMPLE_CSV.read_text(), "confirmatory", None)
        self.assertNotIn("recommendations", results.columns)


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

    def test_out_of_range_typed_values_show_error_not_old_value(self):
        # Regression: with min/max on the boxes, typing 150 kept the old 80
        # and predicted silently. Now each out-of-range value must give an error.
        for box, value, message in [(0, 150.0, "attendance_pct must be 0 to 100"),
                                    (0, -1.0, "attendance_pct must be 0 to 100"),
                                    (1, 41.0, "study_hours must be 0 to 40"),
                                    (1, -0.5, "study_hours must be 0 to 40")]:
            at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
            at.number_input[box].set_value(value).run()
            at.button[0].click().run()
            self.assertTrue(any(message in e.value for e in at.error), f"{value}: no error shown")
            self.assertNotIn("Estimated High-Risk probability", " ".join(m.value for m in at.markdown))

    def test_failures_only_offers_whole_numbers_0_to_3(self):
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        self.assertEqual(list(at.selectbox[0].options), ["0", "1", "2", "3"])

    def test_confirmatory_form_without_g1_shows_error(self):
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        at.radio[0].set_value("confirmatory").run()
        at.button[0].click().run()
        self.assertTrue(any("G1 is required" in e.value for e in at.error))


if __name__ == "__main__":
    unittest.main()
