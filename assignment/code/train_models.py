"""Compare three input setups; keep G1 and G1+G2 models separate.

Run from the repository root: python assignment/code/train_models.py
The printed scores are development cross-validation results, not evidence of
day-one performance or a separate final evaluation of a selected model.
"""

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from data_processing import build_training_xy, validate_students

SETUPS = {
    "early_warning": ("early_warning", "g1_g2"),
    "g1": ("confirmatory", "g1"),
    "g1_g2": ("confirmatory", "g1_g2"),
}


def make_model(technique="logistic_regression"):
    if technique == "logistic_regression":
        return make_pipeline(StandardScaler(), LogisticRegression(
            class_weight="balanced", random_state=42, max_iter=1000))
    if technique == "decision_tree":
        # Fixed baseline depth, not chosen by trying depths on these test folds.
        return DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=42)
    raise ValueError(f"Unknown technique: {technique}")


def evaluate_models(data_dir):
    """Use identical student folds for all setups and scale inside each fold."""
    scoring = {
        "accuracy": "accuracy",
        "precision": make_scorer(precision_score, zero_division=0),
        "recall": make_scorer(recall_score, zero_division=0),
        "f1": make_scorer(f1_score, zero_division=0),
    }
    results = []
    for setup, (mode, grade_setup) in SETUPS.items():
        X, y = build_training_xy(data_dir, mode, grade_setup=grade_setup)
        for technique in ("logistic_regression", "decision_tree"):
            scores = cross_validate(make_model(technique), X, y,
                                    cv=StratifiedKFold(5, shuffle=True, random_state=42),
                                    scoring=scoring, error_score="raise")
            results.append({"setup": setup, "model": technique,
                            **{metric: scores[f"test_{metric}"].mean() for metric in scoring}})
    return pd.DataFrame(results)


def train_models(data_dir, technique="logistic_regression"):
    """Fit one model per setup for the prototype after evaluating separately.

    Balanced Logistic Regression is the default demo baseline, not an automatically
    selected winner. Do not report training predictions as evaluation results.
    """
    models = {}
    for setup, (mode, grade_setup) in SETUPS.items():
        X, y = build_training_xy(data_dir, mode, grade_setup=grade_setup)
        models[setup] = make_model(technique).fit(X, y)
    return models


def predict_students(students, models, mode="confirmatory", *, raw_uci=False):
    """Return (predictions, skipped_rows), identified by 1-based input row number."""
    batch = validate_students(students, mode, raw_uci=raw_uci)
    results = []
    for setup, X in batch.groups.items():
        if X.empty:
            continue
        if setup not in models:
            raise ValueError(f"No trained model for {setup}")
        prediction = models[setup].predict(X)
        results.append(pd.DataFrame({"row_number": X.index, "setup": setup,
                                     "risk": prediction}))
    output = (pd.concat(results, ignore_index=True).sort_values("row_number").reset_index(drop=True)
              if results else pd.DataFrame(columns=["row_number", "setup", "risk"]))
    return output, batch.errors


if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parents[1] / "data"
    print("Development results: stratified 5-fold CV, seed 42; High Risk is the positive class.")
    print("Both models use balanced class weights; Decision Tree depth is fixed at 3.")
    print(evaluate_models(data_dir).to_string(index=False, float_format=lambda value: f"{value:.3f}"))
    print("These results do not establish day-one or week-specific prediction performance.")
