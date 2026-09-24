"""
SARAH — Prediction (single student or a whole class roster)
----------------------------------------------------------------
Loads the trained model for the chosen setup (assignment/models/) and
predicts risk for one student (CLI flags) or a whole class (--csv).

Confirmatory mode has TWO separately trained models, not one shared model:
G1 is required, G2 is optional. A student with only G1 is routed to the
"confirmatory_g1" model (trained only on G1-only data); a student with
both a valid G1 and a valid G2 is routed to the "confirmatory_g1_g2"
model (trained only on G1+G2-average data). Each model only ever sees the
kind of input it was actually trained on.

A supplied G2 that is invalid (out of range, or not a number) is an ERROR
-- it is reported, not silently treated as "G2 absent". Only a genuinely
missing/blank G2 routes to the G1-only model.

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
import math
from pathlib import Path

import joblib
import pandas as pd

from data_processing import GRADE_SETUPS, VALID_MODES, prepare_model_inputs, previous_score_from_grades

ASSIGNMENT_ROOT = Path(__file__).resolve().parents[1]  # assignment/code -> assignment/
MODELS_DIR = ASSIGNMENT_ROOT / "models"


def load_model(mode: str, grade_setup: str = None):
    """grade_setup is required for mode="confirmatory" ("g1" or "g1_g2"),
    ignored for mode="early_warning"."""
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {VALID_MODES}, got {mode!r}")
    if mode == "confirmatory":
        if grade_setup not in GRADE_SETUPS:
            raise ValueError(f"grade_setup must be one of {GRADE_SETUPS}, got {grade_setup!r}")
        filename = f"confirmatory_{grade_setup}_model.joblib"
    else:
        filename = "early_warning_model.joblib"
    path = MODELS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"No trained model at {path} -- run train_models.py first")
    return joblib.load(path)


def _parse_g2(value) -> float:
    """Returns a valid float G2, or None if truly absent/blank. Raises
    ValueError if a G2 was supplied but is not a usable number (invalid
    G2 must be reported, never silently treated as "no G2")."""
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    try:
        grade = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"G2={value!r} is not a valid number")
    if not math.isfinite(grade) or not 0 <= grade <= 20:
        raise ValueError("G2 must be a finite number from 0 to 20")
    return grade


def predict_one(attendance_pct, study_hours, failures, mode="early_warning", g1=None, g2=None):
    """Predict risk for a single, already-known-good student. Returns (label, probability_high_risk)."""
    row = {"attendance_pct": attendance_pct, "study_hours": study_hours, "failures": failures}
    grade_setup = None
    if mode == "confirmatory":
        g2 = _parse_g2(g2)
        grade_setup = "g1_g2" if g2 is not None else "g1"
        row["previous_score"] = previous_score_from_grades(g1, g2)
    X = prepare_model_inputs(pd.DataFrame([row]), mode)
    model = load_model(mode, grade_setup)
    pred = int(model.predict(X)[0])
    proba = float(model.predict_proba(X)[0][1])  # P(High Risk)
    label = "High Risk" if pred == 1 else "Low Risk"
    return label, round(proba, 3)


def predict_roster(csv_path: Path, mode: str = "early_warning"):
    """Predict risk for a whole class from a CSV.

    Missing required columns or an empty file stop the whole file.
    A row with a missing/invalid value (bad range, non-numeric,
    or an unusable supplied G2) is SKIPPED -- with a
    printed reason -- rather than stopping the whole file; every other,
    valid row is still predicted. Confirmatory-mode rows are routed to
    the G1-only or G1+G2 model depending on whether a valid G2 was given.

    CSV columns expected:
      early_warning:  student_id (optional), attendance_pct, study_hours, failures
      confirmatory:   same, plus G1 (required), G2 (optional)

    Returns (results_df, skipped_list).
    """
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {VALID_MODES}, got {mode!r}")
    try:
        # Preserve supplied text such as NA/null/nan so it cannot become absent G2.
        raw = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV contains no students.") from None
    if raw.empty:
        raise ValueError("The CSV contains no students.")
    required = ["attendance_pct", "study_hours", "failures"]
    if mode == "confirmatory":
        required.append("G1")
    missing = [name for name in required if name not in raw.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    models = {}  # grade_setup -> loaded model, loaded lazily and cached
    results, skipped = [], []

    for i, row in raw.iterrows():
        student_id = row.get("student_id", "").strip() or f"row {i + 1}"
        try:
            fields = {
                "attendance_pct": row["attendance_pct"],
                "study_hours": row["study_hours"],
                "failures": row["failures"],
            }
            for name, value in fields.items():
                if not value.strip():
                    raise ValueError(f"{name} is required")
            grade_setup = None
            if mode == "confirmatory":
                g1 = row.get("G1")
                if not g1.strip():
                    raise ValueError("Confirmatory mode needs at least G1")
                try:
                    g1 = float(g1)
                except ValueError:
                    raise ValueError("G1 must be a number from 0 to 20") from None
                g2 = _parse_g2(row.get("G2") if "G2" in raw.columns else None)
                grade_setup = "g1_g2" if g2 is not None else "g1"
                fields["previous_score"] = previous_score_from_grades(float(g1), g2)

            X = prepare_model_inputs(pd.DataFrame([fields]), mode)
            if grade_setup not in models:
                models[grade_setup] = load_model(mode, grade_setup)
            model = models[grade_setup]
            pred = int(model.predict(X)[0])
            proba = float(model.predict_proba(X)[0][1])
            results.append({
                "student_id": student_id,
                "risk_label": "High Risk" if pred == 1 else "Low Risk",
                "probability_high_risk": round(proba, 3),
                **({"grade_setup": grade_setup} if mode == "confirmatory" else {}),
            })
        except (ValueError, KeyError, TypeError) as exc:
            skipped.append({"student_id": student_id, "reason": str(exc)})

    columns = ["student_id", "risk_label", "probability_high_risk"]
    if mode == "confirmatory":
        columns.append("grade_setup")
    return pd.DataFrame(results, columns=columns), skipped


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
        try:
            results, skipped = predict_roster(args.csv, args.mode)
        except (ValueError, OSError) as exc:
            parser.error(str(exc))
        if results.empty:
            print("No valid students to process.")
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            results.to_csv(args.out, index=False)
            print(f"Saved {len(results)} prediction(s) to {args.out}")
        elif not results.empty:
            print(results.to_string(index=False))
        if skipped:
            print(f"\nSkipped {len(skipped)} row(s); processed {len(results)} valid student(s):")
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
