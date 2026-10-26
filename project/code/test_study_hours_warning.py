"""Warning coverage added after Benjamin's issue 80 walkthrough."""
import io
from pathlib import Path
import unittest
import pandas as pd
from streamlit.testing.v1 import AppTest
from predict import predict_one, predict_roster, study_hours_warning, STUDY_HOURS_WARNING
from dashboard import process_upload
from recommend import recommend


class StudyHoursWarning(unittest.TestCase):
    def test_boundaries_all_setups_keep_prediction_and_validation(self):
        for mode, g1, g2 in [('early_warning', None, None), ('confirmatory', 12, None), ('confirmatory', 12, 14)]:
            for hours, warned in [(0, False), (12, False), (12.1, True), (40, True)]:
                with self.subTest(mode=mode, g2=g2, hours=hours):
                    predict_one(80, hours, 0, mode, g1, g2)
                    self.assertEqual(bool(study_hours_warning(hours)), warned)
            with self.assertRaises(ValueError):
                predict_one(80, 41, 0, mode, g1, g2)
        self.assertEqual(predict_one(80, 40, 0, 'confirmatory', 12, None), ('High Risk', .661))

    def test_csv_alignment_invalid_rows_and_export(self):
        text = ('student_id,attendance_pct,study_hours,failures,G1,G2\n'
                'same,80,40,0,12,\nsame,80,41,0,12,\n'
                'same,80,12,0,12,\nlow,100,40,0,20,20\n')
        for mode in ('early_warning', 'confirmatory'):
            with self.subTest(mode=mode):
                rows, skipped, total = process_upload(text, mode, recommend)
                self.assertEqual((len(rows), len(skipped), total), (3, 1, 4))
                self.assertEqual(rows.input_warning.tolist(), [STUDY_HOURS_WARNING, '', STUDY_HOURS_WARNING])
                exported = pd.read_csv(io.StringIO(rows.to_csv(index=False)), keep_default_na=False)
                self.assertEqual(exported.input_warning.tolist(), rows.input_warning.tolist())
                self.assertIn('recommendations', exported.columns)
        self.assertEqual(rows.iloc[-1].risk_label, 'Low Risk')

    def test_form_warning_and_clearance(self):
        at = AppTest.from_file(str(Path(__file__).with_name('dashboard.py')), default_timeout=30).run()
        at.number_input[1].set_value(40.0).run()
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertIn(STUDY_HOURS_WARNING, [w.value for w in at.warning])
        at.number_input[1].set_value(12.0).run()
        self.assertNotIn(STUDY_HOURS_WARNING, [w.value for w in at.warning])
        at.button[0].click().run()
        self.assertNotIn(STUDY_HOURS_WARNING, [w.value for w in at.warning])
        self.assertFalse(at.exception)

    def test_csv_screen_shows_full_warning_once_and_marks_students(self):
        import dashboard
        text = ('student_id,attendance_pct,study_hours,failures,G1,G2\n'
                'A,80,40,0,12,\nB,80,6,0,12,14\n')
        rows, _, _ = process_upload(text, 'confirmatory', recommend)
        shown = dashboard.display_results(rows)
        self.assertNotIn('input_warning', shown.columns)
        self.assertEqual(shown['study_hours_warning'].tolist(), [dashboard.WARNING_MARK, ''])
        self.assertEqual(rows.input_warning.tolist(), [STUDY_HOURS_WARNING, ''])  # download unchanged
        summary = dashboard.study_hours_summary(rows)
        self.assertTrue(summary.startswith('1 predicted student(s) have study hours above 12.'))
        self.assertNotIn(STUDY_HOURS_WARNING, summary)
        self.assertIsNone(dashboard.study_hours_summary(rows.iloc[[1]]))


if __name__ == '__main__':
    unittest.main()
