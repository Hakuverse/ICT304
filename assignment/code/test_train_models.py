"""Checks model routing and the complete prototype workflow."""
import unittest
from pathlib import Path

import pandas as pd

from train_models import predict_students, train_models, evaluate_models


class RecordingModel:
    def __init__(self, risk):
        self.risk = risk
        self.seen = None

    def predict(self, X):
        self.seen = X.copy()
        return [self.risk] * len(X)


class TestModelWorkflow(unittest.TestCase):
    def test_mixed_roster_uses_matching_models_and_keeps_order(self):
        rows = pd.DataFrame({"attendance_pct": [80, 80, 150, 80],
                             "study_hours": [4] * 4, "failures": [0] * 4,
                             "G1": [10] * 4, "G2": [12, None, 12, 0],
                             "G3": [20] * 4, "risk": [9] * 4})
        models = {"g1": RecordingModel(1), "g1_g2": RecordingModel(0)}
        predictions, errors = predict_students(rows, models)
        self.assertEqual(predictions.row_number.tolist(), [1, 2, 4])
        self.assertEqual(predictions.risk.tolist(), [0, 1, 0])
        self.assertEqual(errors.row_number.tolist(), [3])
        self.assertEqual(models["g1"].seen.previous_score.tolist(), [50])
        self.assertEqual(models["g1_g2"].seen.previous_score.tolist(), [55, 25])
        self.assertNotIn("G3", models["g1"].seen)
        self.assertNotIn("risk", models["g1"].seen)
        with self.assertRaisesRegex(ValueError, "No trained model"):
            predict_students(rows, {"g1": models["g1"]})

    def test_all_invalid_does_not_call_a_model(self):
        rows = pd.DataFrame({"attendance_pct": [80], "study_hours": [41], "failures": [0]})
        predictions, errors = predict_students(rows, {}, "early_warning")
        self.assertTrue(predictions.empty)
        self.assertEqual(len(errors), 1)

    def test_real_data_training_evaluation_and_prediction(self):
        data_dir = Path(__file__).resolve().parents[1] / "data"
        models = train_models(data_dir)
        raw = pd.read_csv(data_dir / "student-mat.csv", sep=";")
        for mode in ("early_warning", "confirmatory"):
            for rows in (raw, raw.drop(columns="G2")):
                predictions, errors = predict_students(rows, models, mode, raw_uci=True)
                self.assertEqual(len(predictions), 395)
                self.assertTrue(errors.empty)
                self.assertTrue(set(predictions.risk).issubset({0, 1}))
        results = evaluate_models(data_dir)
        self.assertEqual(len(results), 6)
        self.assertEqual(set(results.setup), {"early_warning", "g1", "g1_g2"})
        metrics = results[["accuracy", "precision", "recall", "f1"]]
        self.assertTrue(((metrics >= 0) & (metrics <= 1)).all().all())


if __name__ == "__main__":
    unittest.main()
