"""
SARAH — Data Processing
------------------------
Loads the UCI Math dataset and prepares the approved three- or four-field inputs.
Training labels are created separately; prediction inputs do not need G3.

Feature engineering decisions:
  attendance_pct   From `absences` (capped at 30, rescaled so 0 absences =
                    100% attendance, >=30 absences = 0%).
  study_hours       From `studytime` (1-4 ordinal bucket), converted to a
                    numeric hours/week estimate (including an assumed top bucket).
  previous_score    Confirmatory mode has two grade setups (see GRADE_SETUPS
                    below): "g1_g2" averages G1 and G2 (first/second period
                    grades), "g1" uses G1 alone. Both are rescaled from 0-20
                    to 0-100%. G3 is deliberately excluded here -- it becomes
                    the label instead, so using it as a feature would leak
                    the answer into the model.
  failures          Raw count of past class failures (0-3).
  risk (target)     1 = High Risk if G3 < PASS_MARK (10/20, the standard
                    pass mark), else 0 = Low Risk.

Why two grade setups, trained separately: a tutor may only have G1 (partway
through term) or both G1 and G2 (later). Feeding a G1-only value into a model
that only ever saw G1+G2 averages during training means the model is being
asked to extrapolate to a pattern it never learned from. Training a separate
model on each grade setup keeps the training distribution honest for both
real-world cases.
"""

from pathlib import Path

import numpy as np
import pandas as pd

MAX_ABSENCES_FOR_SCALING = 30
STUDYTIME_HOURS_MAP = {1: 1.5, 2: 3.5, 3: 7.5, 4: 12.0}
PASS_MARK = 10  # out of 20

FEATURE_COLUMNS = ["attendance_pct", "study_hours", "previous_score", "failures"]
EARLY_WARNING_FEATURES = ["attendance_pct", "study_hours", "failures"]
CONFIRMATORY_FEATURES = EARLY_WARNING_FEATURES + ["previous_score"]
VALID_MODES = ("early_warning", "confirmatory")
GRADE_SETUPS = ("g1", "g1_g2")  # Confirmatory mode only
TARGET_COLUMN = "risk"


def load_raw_uci(data_dir: Path) -> pd.DataFrame:
    """Use Math only, even if another course file is in the same directory."""
    data_dir = Path(data_dir)
    mat = pd.read_csv(data_dir / "student-mat.csv", sep=";")
    mat["course"] = "Math"

    return mat


def get_feature_columns(mode: str) -> list[str]:
    """Return only the approved model columns, in a repeatable order."""
    if mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {VALID_MODES}, got {mode!r}")
    return list(EARLY_WARNING_FEATURES if mode == "early_warning" else CONFIRMATORY_FEATURES)


def _numeric_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    if not df.columns.is_unique:
        raise ValueError("Column names must not be duplicated")
    missing = [name for name in columns if name not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if df.empty:
        raise ValueError("Provide at least one student")
    result = df[columns].apply(pd.to_numeric, errors="coerce")
    if not np.isfinite(result.to_numpy(dtype=float)).all():
        raise ValueError("Required values must be numbers, without blanks or infinity")
    return result


def _check_range(values: pd.Series, minimum: float, maximum=None, *, whole=False):
    invalid = values < minimum
    if maximum is not None:
        invalid |= values > maximum
    if whole:
        invalid |= values % 1 != 0
    if invalid.any():
        limit = f"{minimum} to {maximum}" if maximum is not None else f"at least {minimum}"
        suffix = " (whole numbers)" if whole else ""
        raise ValueError(f"{values.name} must be {limit}{suffix}")


def engineer_inputs(df: pd.DataFrame, mode: str = "confirmatory", grade_setup: str = "g1_g2") -> pd.DataFrame:
    """Convert raw UCI fields into X, without reading final grades or labels.

    grade_setup only matters for mode="confirmatory": "g1_g2" (default) uses
    the average of G1 and G2; "g1" uses G1 alone. Ignored for early_warning.
    """
    if mode == "confirmatory" and grade_setup not in GRADE_SETUPS:
        raise ValueError(f"grade_setup must be one of {GRADE_SETUPS}, got {grade_setup!r}")
    columns = get_feature_columns(mode)
    required = ["absences", "studytime", "failures"]
    if mode == "confirmatory":
        required += ["G1", "G2"] if grade_setup == "g1_g2" else ["G1"]
    raw = _numeric_columns(df, required)
    _check_range(raw["absences"], 0, whole=True)
    _check_range(raw["studytime"], 1, 4, whole=True)
    _check_range(raw["failures"], 0, whole=True)
    out = pd.DataFrame(index=df.index)
    capped_absences = raw["absences"].clip(upper=MAX_ABSENCES_FOR_SCALING)
    out["attendance_pct"] = (1 - capped_absences / MAX_ABSENCES_FOR_SCALING) * 100
    out["study_hours"] = raw["studytime"].map(STUDYTIME_HOURS_MAP)
    out["failures"] = raw["failures"].clip(upper=3)
    if mode == "confirmatory":
        if grade_setup == "g1_g2":
            for name in ["G1", "G2"]:
                _check_range(raw[name], 0, 20)
            out["previous_score"] = (raw["G1"] + raw["G2"]) / 2 / 20 * 100
        else:  # "g1"
            _check_range(raw["G1"], 0, 20)
            out["previous_score"] = raw["G1"] / 20 * 100
    return out[columns].round(1)


def prepare_model_inputs(df: pd.DataFrame, mode: str = "confirmatory") -> pd.DataFrame:
    """Validate already-engineered form/CSV fields and return X only.

    This does not predict risk. A later trained model will consume the result.
    Attendance must use the same absence-based estimate as the training data.
    Works the same for both Confirmatory grade setups: by this point
    previous_score is already a single 0-100 number (see previous_score_from_grades).
    """
    out = _numeric_columns(df, get_feature_columns(mode))
    _check_range(out["attendance_pct"], 0, 100)
    _check_range(out["study_hours"], 0, 40)
    _check_range(out["failures"], 0, 3, whole=True)
    if mode == "confirmatory":
        _check_range(out["previous_score"], 0, 100)
    return out.copy()


def _risk_target(df: pd.DataFrame) -> pd.Series:
    grades = _numeric_columns(df, ["G3"])["G3"]
    _check_range(grades, 0, 20)
    return (grades < PASS_MARK).astype(int).rename(TARGET_COLUMN)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Keep the existing four-feature labelled view used by eda.py."""
    out = engineer_inputs(df)[FEATURE_COLUMNS]
    out[TARGET_COLUMN] = _risk_target(df)
    out["risk_label"] = out[TARGET_COLUMN].map({1: "High Risk", 0: "Low Risk"})

    if "course" in df.columns:
        out["course"] = df["course"]

    return out


def build_training_dataset(data_dir: Path, mode: str = "confirmatory", grade_setup: str = "g1_g2") -> pd.DataFrame:
    """Return mode-specific features followed by risk and risk_label.

    Prefer build_training_xy() when passing data to a model, to keep labels separate.
    """
    get_feature_columns(mode)
    raw = load_raw_uci(data_dir)
    out = engineer_inputs(raw, mode, grade_setup)
    out[TARGET_COLUMN] = _risk_target(raw)
    out["risk_label"] = out[TARGET_COLUMN].map({1: "High Risk", 0: "Low Risk"})
    return out


def build_training_xy(data_dir: Path, mode: str = "confirmatory", grade_setup: str = "g1_g2"):
    """Return (X, y): approved inputs and the separate training target."""
    dataset = build_training_dataset(data_dir, mode, grade_setup)
    return dataset[get_feature_columns(mode)].copy(), dataset[TARGET_COLUMN].copy()


def previous_score_from_grades(g1: float, g2: float = None) -> float:
    """Team rule (Confirmatory mode, live tutor input): G1 is required, G2 is
    optional. With both grades, previous_score is their average -- matching
    how the "g1_g2" model was trained. With G1 alone, previous_score is G1 by
    itself, rescaled the same way -- matching how the "g1" model was trained.
    This covers the two real-world points a tutor can be at: only the first
    assessment period is in yet, or both are. Which trained model gets used
    is decided by the caller based on whether g2 was given (see predict.py).

    Both grades are out of 20 and the result is rescaled to 0-100%, matching
    engineer_inputs()'s previous_score calculation exactly for each grade_setup.
    """
    if g1 is None:
        raise ValueError("previous_score needs at least G1")
    if not (0 <= g1 <= 20):
        raise ValueError("G1 must be 0 to 20")
    if g2 is None:
        return round(g1 / 20 * 100, 1)
    if not (0 <= g2 <= 20):
        raise ValueError("G2 must be 0 to 20")
    return round((g1 + g2) / 2 / 20 * 100, 1)


if __name__ == "__main__":
    assignment_root = Path(__file__).resolve().parents[1]  # assignment/code -> assignment/
    for mode in VALID_MODES:
        setups = GRADE_SETUPS if mode == "confirmatory" else ("g1_g2",)  # placeholder, ignored
        for grade_setup in setups:
            X, y = build_training_xy(assignment_root / "data", mode, grade_setup)
            label = f"{mode} ({grade_setup})" if mode == "confirmatory" else mode
            print(f"{label}: {len(X)} rows; inputs = {list(X.columns)}")
            print(f"High Risk: {int(y.sum())}; Low Risk: {int((y == 0).sum())}")
