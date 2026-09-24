"""
SARAH — Prediction (single student or a whole class roster)
----------------------------------------------------------------
Loads the trained model for the chosen mode (assignment/models/) and
predicts risk for one student (CLI flags) or a whole class (--csv).

Confirmatory mode's previous_score is built from the grades a tutor
actually has: G1 is required, G2 is optional. With both, previous_score is
their average (matching how the model was trained); with G1 only,
previous_score is G1 alone, rescaled the same way (0-20 -> 0-100%). This
gives Confirmatory mode two real-world variants -- "G1 only" (partway
through term) and "G1 and G2" (later in term) -- both going through the
same trained model.

study_hours is capped at 40 (a hard week has 168 hours; 40 is a generous
ceiling for study time and rejects obvious data-entry mistakes like 999).

For a CSV of a whole class: a row with a missing or invalid value is
SKIPPED, with the reason printed, while every valid row is still
processed and predicted -- one bad row in a roster of 30 should not block
the other 29.

Run with (from the repository root):
  python assignment/code/predict.py --attendance 62 --study-hours 4 --failures 1
  python assignment/code/predict.py --mode confirmatory --attendance 62 \
      --study-hours 4 --failures 1 --g1 12
  python assignment/code/predict.py --mode confirmatory --attendance 62 \
      --study-hours 4 --failures 1 --g1 12 --g2 14
  python assignment/code/predict.py --csv assignment/data/sample_roster.csv \
      --out assignment/reports/roster_predictions.csv
"""

import argparse
from pathlib import Path

import joblib
import pandas as pd

from data_processing import VALID_MODES, prepare_model_inputs, previous_score_from_grades

ASSIGNMENT_ROOT = Path(__file__).resolve().parents[1]  # assignment/code -> assignment/
MODELS_DIR = ASSIGNMENT_ROOT / "models"


def load_model(mode: str):
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {VALID_MODES}, got {mode!r}")
    path = MODELS_DIR / f"{mode}_model.joblib"
    if not path.exists():
        raise FileNotFoundError(f"No trained model at {path} -- run train_models.py first")
    return joblib.load(path)


def predict_one(attendance_pct, study_hours, failures, mode="early_warning", g1=None, g2=None):
    """Predict risk for a single, already-known-good student. Returns (label, probability_high_risk)."""
    row = {"attendance_pct": attendance_pct, "study_hours": study_hours, "failures": failures}
    if mode == "confirmatory":
        row["previous_score"] = previous_score_from_grades(g1, g2)
    X = prepare_model_inputs(pd.DataFrame([row]), mode)
    model = load_model(mode)
    pred = int(model.predict(X)[0])
    proba = float(model.predict_proba(X)[0][1])  # P(High Risk)
    label = "High Risk" if pred == 1 else "Low Risk"
    return label, round(proba, 3)


def predict_roster(csv_path: Path, mode: str = "early_warning"):
    """Predict risk for a whole class from a CSV.

    A row with a missing/invalid value (bad range, non-numeric, missing
    required column) is SKIPPED -- with a printed reason -- rather than
    stopping the whole file; every other, valid row is still predicted.

    CSV columns expected:
      early_warning:  student_id (optional), attendance_pct, study_hours, failures
      confirmatory:   same, plus G1 (required), G2 (optional)

    Returns (results_df, skipped_list).
    """
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {VALID_MODES}, got {mode!r}")
    raw = pd.read_csv(csv_path)
    model = load_model(mode)
    results, skipped = [], []

    for i, row in raw.iterrows():
        student_id = row["student_id"] if "student_id" in raw.columns and pd.notna(row.get("student_id")) else i
        try:
            fields = {
                "attendance_pct": row["attendance_pct"],
                "study_hours": row["study_hours"],
                "failures": row["failures"],
            }
            if mode == "confirmatory":
                g1 = row.get("G1")
                if pd.isna(g1):
                    raise ValueError("Confirmatory mode needs at least G1")
                g2 = row.get("G2")
                g2 = float(g2) if ("G2" in raw.columns and pd.notna(g2)) else None
                fields["previous_score"] = previous_score_from_grades(float(g1), g2)

            X = prepare_model_inputs(pd.DataFrame([fields]), mode)
            pred = int(model.predict(X)[0])
            proba = float(model.predict_proba(X)[0][1])
            results.append({
                "student_id": student_id,
                "risk_label": "High Risk" if pred == 1 else "Low Risk",
                "probability_high_risk": round(proba, 3),
            })
        except (ValueError, KeyError, TypeError) as exc:
            skipped.append({"student_id": student_id, "reason": str(exc)})

    return pd.DataFrame(results), skipped


def main():
    parser = argparse.ArgumentParser(description="SARAH risk prediction")
    parser.add_argument("--mode", choices=VALID_MODES, default="early_warning")
    parser.add_argument("--attendance", type=float, help="Attendance %% (0-100)")
    parser.add_argument("--study-hours", type=float, help="Study hours/week (0-40)")
    parser.add_argument("--failures", type=float, help="Past class failures (0-3)")
    parser.add_argument("--g1", type=float, help="Confirmatory mode: first assessment grade (0-20)")
    parser.add_argument("--g2", type=float, help="Confirmatory mode: second assessment grade (0-20), optional")
    parser.add_argument("--csv", type=Path, help="Predict a whole class from a CSV roster instead")
    parser.add_argument("--out", type=Path, help="Where to save --csv results")
    args = parser.parse_args()

    if args.csv:
        results, skipped = predict_roster(args.csv, args.mode)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            results.to_csv(args.out, index=False)
            print(f"Saved {len(results)} prediction(s) to {args.out}")
        else:
            print(results.to_string(index=False))
        if skipped:
            print(f"\nSkipped {len(skipped)} row(s) (rest of the class was still processed):")
            for s in skipped:
                print(f"  student_id={s['student_id']}: {s['reason']}")
        return

    if args.attendance is None or args.study_hours is None or args.failures is None:
        parser.error("--attendance, --study-hours and --failures are required (or use --csv)")
    if args.mode == "confirmatory" and args.g1 is None:
        parser.error("Confirmatory mode needs --g1 (--g2 is optional)")

    try:
        label, proba = predict_one(
            args.attendance, args.study_hours, args.failures, args.mode, args.g1, args.g2
        )
    except (ValueError, KeyError) as exc:
        parser.error(str(exc))
        return
    print(f"Risk: {label} (probability High Risk: {proba})")


if __name__ == "__main__":
    main()
