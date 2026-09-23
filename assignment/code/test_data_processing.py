"""Run from the repository root: python -m unittest discover -s assignment/code -v"""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from data_processing import (
    build_training_dataset, build_training_xy, engineer_features, engineer_inputs,
    load_raw_uci, prepare_model_inputs,
)


class TestModes(unittest.TestCase):
    def setUp(self):
        self.raw = pd.DataFrame({
            "absences": [0, 15, 30, 75], "studytime": [1, 2, 3, 4],
            "failures": [0, 1, 3, 5], "G1": [18, 10, 5, 2],
            "G2": [16, 10, 6, 0], "G3": [17, 10, 9, 0],
            "course": ["Math"] * 4,
        }, index=[10, 20, 30, 40])
        self.early = ["attendance_pct", "study_hours", "failures"]
        self.confirmatory = self.early + ["previous_score"]

    def test_early_warning_needs_no_grades(self):
        result = engineer_inputs(self.raw.drop(columns=["G1", "G2", "G3"]), "early_warning")
        self.assertEqual(list(result.columns), self.early)
        self.assertEqual(list(result.index), [10, 20, 30, 40])

    def test_confirmatory_needs_no_final_grade(self):
        result = engineer_inputs(self.raw.drop(columns="G3"), "confirmatory")
        self.assertEqual(list(result.columns), self.confirmatory)
        self.assertEqual(result["previous_score"].tolist(), [85, 50, 27.5, 5])

    def test_labels_and_extra_fields_cannot_enter_inputs(self):
        for mode in ["early_warning", "confirmatory"]:
            raw = self.raw.assign(risk=1, risk_label="High Risk", secret_extra=999)
            features = engineer_inputs(raw, mode)
            dirty = features.assign(G3=0, risk=1, risk_label="High Risk", course="Math", extra=999)
            pd.testing.assert_frame_equal(prepare_model_inputs(dirty, mode), features)

    def test_engineered_form_input_needs_no_raw_grades(self):
        form = pd.DataFrame({"attendance_pct": [100], "study_hours": [3.5], "failures": [0]})
        self.assertEqual(list(prepare_model_inputs(form, "early_warning").columns), self.early)
        form["previous_score"] = 50
        self.assertEqual(list(prepare_model_inputs(form, "confirmatory").columns), self.confirmatory)

    def test_invalid_mode_rejected_before_loading(self):
        for call in [lambda: engineer_inputs(self.raw, "wrong"),
                     lambda: prepare_model_inputs(self.raw, "wrong"),
                     lambda: build_training_dataset(Path("not-a-directory"), "wrong")]:
            with self.assertRaisesRegex(ValueError, "mode must"):
                call()

    def test_absence_cap_study_mapping_and_failure_cap(self):
        result = engineer_inputs(self.raw)
        self.assertEqual(result["attendance_pct"].tolist(), [100, 50, 0, 0])
        self.assertEqual(result["study_hours"].tolist(), [1.5, 3.5, 7.5, 12])
        self.assertEqual(result["failures"].tolist(), [0, 1, 3, 3])

    def test_g3_boundary_and_eda_compatibility(self):
        result = engineer_features(self.raw)
        self.assertEqual(result["risk"].tolist(), [0, 0, 1, 1])
        self.assertEqual(result["risk_label"].tolist(), ["Low Risk", "Low Risk", "High Risk", "High Risk"])
        self.assertIn("course", result)
        self.assertNotIn("G3", result)

    def test_changing_g3_changes_only_labels(self):
        changed = self.raw.assign(G3=0)
        for mode in ["early_warning", "confirmatory"]:
            pd.testing.assert_frame_equal(engineer_inputs(self.raw, mode), engineer_inputs(changed, mode))
        self.assertNotEqual(engineer_features(self.raw)["risk"].tolist(),
                            engineer_features(changed)["risk"].tolist())

    def test_missing_and_invalid_raw_inputs_raise(self):
        cases = [self.raw.drop(columns="absences"), self.raw.assign(studytime=0),
                 self.raw.assign(absences=-1), self.raw.assign(failures=0.5),
                 self.raw.assign(G1=21), self.raw.assign(studytime="not a number"),
                 self.raw.assign(G2=None), self.raw.assign(absences=float("inf"))]
        for raw in cases:
            with self.subTest(columns=list(raw.columns)):
                with self.assertRaises(ValueError):
                    engineer_inputs(raw)

    def test_invalid_engineered_inputs_raise(self):
        valid = engineer_inputs(self.raw)
        for name, value in [("attendance_pct", 150), ("study_hours", -1),
                            ("failures", 4), ("previous_score", None),
                            ("study_hours", "bad"), ("previous_score", 101)]:
            with self.subTest(field=name, value=value):
                with self.assertRaises(ValueError):
                    prepare_model_inputs(valid.assign(**{name: value}))

    def test_empty_or_duplicate_columns_raise(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            engineer_inputs(self.raw.iloc[:0])
        with self.assertRaisesRegex(ValueError, "duplicated"):
            engineer_inputs(pd.concat([self.raw, self.raw[["G1"]]], axis=1))

    def test_missing_g3_is_not_silently_labelled_low_risk(self):
        with self.assertRaises(ValueError):
            engineer_features(self.raw.assign(G3=None))

    def test_training_modes_and_math_only_loading(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            self.raw.to_csv(directory / "student-mat.csv", sep=";", index=False)
            self.raw.assign(G3=0).to_csv(directory / "student-por.csv", sep=";", index=False)
            loaded = load_raw_uci(directory)
            self.assertEqual(len(loaded), 4)
            self.assertEqual(set(loaded["course"]), {"Math"})
            for mode, columns in [("early_warning", self.early), ("confirmatory", self.confirmatory)]:
                dataset = build_training_dataset(directory, mode)
                self.assertEqual(list(dataset), columns + ["risk", "risk_label"])
                X, y = build_training_xy(directory, mode)
                self.assertEqual(list(X), columns)
                self.assertEqual(y.tolist(), [0, 0, 1, 1])
                self.assertTrue(X.index.equals(y.index))

    def test_real_math_dataset_both_modes(self):
        data_dir = Path(__file__).resolve().parents[1] / "data"
        for mode, columns in [("early_warning", self.early), ("confirmatory", self.confirmatory)]:
            X, y = build_training_xy(data_dir, mode)
            self.assertEqual(X.shape, (395, len(columns)))
            self.assertEqual(int(y.sum()), 130)
            self.assertEqual(int((y == 0).sum()), 265)
            self.assertFalse(X.isna().any().any())


if __name__ == "__main__":
    unittest.main()
