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
        # Same students skipped; the dashboard rewords the reasons in plain language (#69 part 3).
        self.assertEqual([s["student_id"] for s in skipped], [s["student_id"] for s in cli_skipped])


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
        self.assertIn("Model-estimated High-Risk probability", " ".join(m.value for m in at.markdown))
        at.number_input[0].set_value(50.0).run()  # change attendance
        self.assertNotIn("Model-estimated High-Risk probability", " ".join(m.value for m in at.markdown))
        at.button[0].click().run()
        at.radio[0].set_value("confirmatory").run()  # change mode
        self.assertNotIn("Model-estimated High-Risk probability", " ".join(m.value for m in at.markdown))

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
            self.assertNotIn("Model-estimated High-Risk probability", " ".join(m.value for m in at.markdown))

    def test_failures_only_offers_whole_numbers_0_to_3(self):
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        self.assertEqual(list(at.selectbox[0].options), ["0", "1", "2", "3"])

    def test_confirmatory_form_without_g1_shows_error(self):
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        at.radio[0].set_value("confirmatory").run()
        at.button[0].click().run()
        self.assertTrue(any("G1 is required" in e.value for e in at.error))


class AcceptedUsabilityChanges(unittest.TestCase):
    """#69: the four changes the team accepted after the 17 October usability check (#68).
    Exact wording agreed on 19 October 2026 is checked so it cannot drift."""

    def page(self):
        return AppTest.from_file(DASHBOARD, default_timeout=30).run()

    def test_human_review_notice_on_page_and_with_result(self):
        at = self.page()
        self.assertEqual(at.warning[0].value,
                         "Support tool only. Do not use this prediction alone to make decisions about a student.")
        at.button[0].click().run()
        self.assertEqual(sum(w.value == dashboard.HUMAN_REVIEW_NOTICE for w in at.warning), 2)

    def test_probability_is_a_percentage_with_the_agreed_caveat(self):
        self.assertEqual(dashboard.probability_text(0.818),
                         "Model-estimated High-Risk probability: **81.8%**. This estimate may be inaccurate "
                         "and should be considered alongside other information about the student.")
        at = self.page()
        at.number_input[0].set_value(40.0).run()
        at.number_input[1].set_value(4.0).run()
        at.button[0].click().run()
        shown = " ".join(m.value for m in at.markdown)
        self.assertIn("Model-estimated High-Risk probability: **85.9%**", shown)

    def test_mode_and_field_help_explain_grades_blank_zero_and_attendance(self):
        at = self.page()
        at.radio[0].set_value("confirmatory").run()
        text = " ".join(c.value for c in at.caption) + " " + " ".join(i.value for i in at.info)
        for phrase in ["first-period grade", "second-period grade", "Leave G2 blank",
                       "0 is a real grade", "Attendance is an estimate"]:
            self.assertIn(phrase, text)
        self.assertEqual([t.label for t in at.text_input],
                         ["G1 - first-period grade (0-20, required)",
                          "G2 - second-period grade (0-20, optional - leave blank if not available)"])

    def test_skipped_warning_counts_and_points_to_reasons(self):
        self.assertIsNone(dashboard.skipped_warning(0, 4))
        self.assertEqual(dashboard.skipped_warning(2, 4),
                         "2 of 4 students were skipped and got no prediction. "
                         "See **Skipped rows** below for the reason for each one.")
        self.assertTrue(dashboard.skipped_warning(1, 5).startswith("1 of 5 students was skipped"))

    def test_screen_shows_percentages_but_results_and_download_are_unchanged(self):
        results, skipped, total = dashboard.process_upload(dashboard.SAMPLE_CSV.read_text(), "confirmatory")
        shown = dashboard.display_results(results)
        self.assertEqual(list(shown["probability_high_risk"]),
                         [round(p * 100, 1) for p in results["probability_high_risk"]])
        self.assertEqual(len(shown), 2)                       # valid results are never hidden
        self.assertEqual(list(results["probability_high_risk"]),   # download keeps predict.py's 0-1 values
                         list(predict_roster(dashboard.SAMPLE_CSV, "confirmatory")[0]["probability_high_risk"]))


class ReadabilityChanges(unittest.TestCase):
    """#69 part 2: team readability proposals from the #57 record. Long suggestions and
    skipped reasons must be readable in full, and each suggestion's reason explained."""

    def test_full_suggestion_list_keeps_every_message_unchanged(self):
        from recommend import recommend
        text = ("student_id,attendance_pct,study_hours,failures\n"
                "A,40,1.5,2\nB,90,6,0\nC,150,4,0\n")
        results, skipped, _ = dashboard.process_upload(text, "early_warning", recommend)
        listed = dashboard.suggestions_by_student(results)
        self.assertEqual([(s, l) for s, l, _ in listed], list(zip(results["student_id"], results["risk_label"])))
        for (student, label, messages), key in zip(listed, ["A", "B"]):
            values = {"A": (40, 1.5, 2), "B": (90, 6, 0)}[key]
            expected = recommend(dashboard.build_student_fields("early_warning", *values), label)
            self.assertEqual(messages, expected)            # full text, same order, nothing cut
        self.assertEqual([s["student_id"] for s in skipped], ["C"])   # skipped rows not listed

    def test_no_recommendation_column_gives_empty_list(self):
        results, _, _ = dashboard.process_upload(dashboard.SAMPLE_CSV.read_text(), "confirmatory", None)
        self.assertEqual(dashboard.suggestions_by_student(results), [])

    def test_skipped_reasons_are_shown_in_full(self):
        _, skipped, _ = dashboard.process_upload(
            "student_id,attendance_pct,study_hours,failures,G1,G2\nA,60,4,1,12,14,99\n", "confirmatory")
        self.assertEqual(dashboard.skipped_html(skipped),
                         "<ul><li><strong>row 1</strong>: has 7 values but the header has 6 columns "
                         "(check for a missing or extra comma)</li></ul>")

    def test_uploaded_ids_and_reasons_are_shown_literally_not_as_links_or_markup(self):
        # Review of PR #87: an ID like [B](https://example.com) must not become a link.
        from recommend import recommend
        text = ("student_id,attendance_pct,study_hours,failures,G1,G2\n"
                "[B](https://example.com),40,1.5,2,8,\n*star*,90,6,0,15,15\n<b>bad</b>,60,4,1,12,*x*\n")
        results, skipped, _ = dashboard.process_upload(text, "confirmatory", recommend)
        shown = dashboard.suggestions_html(dashboard.suggestions_by_student(results))
        self.assertIn("<strong>[B](https://example.com)</strong> (High Risk)", shown)   # literal text
        self.assertIn("<strong>*star*</strong>", shown)
        self.assertNotIn("<a", shown)
        skipped_shown = dashboard.skipped_html(skipped)
        self.assertIn("<strong>&lt;b&gt;bad&lt;/b&gt;</strong>", skipped_shown)          # no HTML injected
        self.assertIn("*x*", skipped_shown)                                             # user value kept
        self.assertNotIn("<b>", skipped_shown)

    def test_single_result_explains_what_a_suggestion_means(self):
        at = AppTest.from_file(DASHBOARD, default_timeout=30).run()
        at.number_input[0].set_value(40.0).run()
        at.button[0].click().run()
        self.assertIn(dashboard.SUGGESTION_EXPLANATION, [c.value for c in at.caption])


class PlainSkippedReasons(unittest.TestCase):
    """#69 part 3 (agreed 20 October 2026): skipped-row reasons say which value was
    found and how to fix the row. Which rows are skipped must not change."""

    H = "student_id,attendance_pct,study_hours,failures,G1,G2\n"

    def reasons(self, text, mode="confirmatory"):
        _, skipped, _ = dashboard.process_upload(text, mode)
        return {s["student_id"]: s["reason"] for s in skipped}

    def test_sample_file_reasons_use_the_agreed_wording(self):
        self.assertEqual(self.reasons(dashboard.SAMPLE_CSV.read_text()), {
            "C": "Attendance is 150. Enter a value from 0 to 100.",
            "D": "G2 is 'NA'. Leave it blank if there is no second-period grade, or enter 0\u201320.",
        })

    def test_each_field_names_the_value_and_the_fix(self):
        reasons = self.reasons(self.H + "A,,4,0,12,\nB,80,many,0,12,\nC,80,4,1.5,12,\n"
                                        "D,80,4,0,,\nE,80,4,0,25,\nF,80,4,0,12,21\n")
        self.assertEqual(reasons, {
            "A": "Attendance is missing. Enter a value from 0 to 100.",
            "B": "Study hours is 'many'. Enter a value from 0 to 40.",
            "C": "Past class failures is 1.5. Enter a whole number from 0 to 3.",
            "D": "G1 is missing. Enter the first-period grade from 0 to 20.",
            "E": "G1 is 25. Enter the first-period grade from 0 to 20.",
            "F": "G2 is 21. Leave it blank if there is no second-period grade, or enter 0\u201320.",
        })

    def test_every_problem_in_a_row_is_listed(self):
        self.assertEqual(self.reasons(self.H + "A,150,4,0,12,NA\n")["A"],
                         "Attendance is 150. Enter a value from 0 to 100. "
                         "G2 is 'NA'. Leave it blank if there is no second-period grade, or enter 0\u201320.")

    def test_early_warning_ignores_grade_columns(self):
        reasons = self.reasons(self.H + "A,60,50,0,abc,NA\n", "early_warning")
        self.assertEqual(reasons, {"A": "Study hours is 50. Enter a value from 0 to 40."})

    def test_same_rows_skipped_as_the_command_line(self):
        text = self.H + "A,60,4,1,12,\nB,,4,0,12,\nC,80,4,1.5,12,\nD,80,4,0,12,NA\nE,90,6,0,15,15\n"
        results, skipped, total = dashboard.process_upload(text, "confirmatory")
        cli_results, cli_skipped = predict_roster(io.StringIO(text), "confirmatory")
        self.assertEqual(results.to_dict("records"), cli_results.to_dict("records"))
        self.assertEqual([s["student_id"] for s in skipped], [s["student_id"] for s in cli_skipped])
        self.assertEqual(len(results) + len(skipped), total)

    def test_table_leaves_out_recommendations_but_download_keeps_them(self):
        from recommend import recommend
        results, _, _ = dashboard.process_upload(dashboard.SAMPLE_CSV.read_text(), "confirmatory", recommend)
        self.assertNotIn("recommendations", dashboard.display_results(results).columns)  # shown once, below
        self.assertIn("recommendations", results.columns)                              # still downloaded
        self.assertEqual(len(dashboard.suggestions_by_student(results)), len(results))  # full list complete

    def test_original_reason_kept_when_no_plain_reason_applies(self):
        self.assertEqual(dashboard.plain_reason({"attendance_pct": "60", "study_hours": "4", "failures": "0"},
                                                "early_warning", "some other problem"),
                         "some other problem")
        self.assertIn("has 7 values but the header has 6",            # wrong-length rows unchanged
                      self.reasons(self.H + "A,60,4,1,12,14,99\n")["row 1"])


if __name__ == "__main__":
    unittest.main()
