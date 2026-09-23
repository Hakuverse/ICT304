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
  previous_score    Average of G1 and G2 (first/second period grades),
                    rescaled from 0-20 to 0-100%. G3 is deliberately
                    excluded here -- it becomes the label instead, so using
                    it as a feature would leak the answer into the model.
  failures          Raw count of past class failures (0-3).
  risk (target)     1 = High Risk if G3 < PASS_MARK (10/20, the standard
                    pass mark), else 0 = Low Risk.
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


def engineer_inputs(df: pd.DataFrame, mode: str = "confirmatory") -> pd.DataFrame:
    """Convert raw UCI fields into X, without reading final grades or labels."""
    columns = get_feature_columns(mode)
    required = ["absences", "studytime", "failures"]
    if mode == "confirmatory":
        required += ["G1", "G2"]
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
        for name in ["G1", "G2"]:
            _check_range(raw[name], 0, 20)
        out["previous_score"] = (raw["G1"] + raw["G2"]) / 2 / 20 * 100
    return out[columns].round(1)


def prepare_model_inputs(df: pd.DataFrame, mode: str = "confirmatory") -> pd.DataFrame:
    """Validate already-engineered form/CSV fields and return X only.

    This does not predict risk. A later trained model will consume the result.
    Attendance must use the same absence-based estimate as the training data.
    """
    out = _numeric_columns(df, get_feature_columns(mode))
    _check_range(out["attendance_pct"], 0, 100)
    _check_range(out["study_hours"], 0)
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


def build_training_dataset(data_dir: Path, mode: str = "confirmatory") -> pd.DataFrame:
    """Return mode-specific features followed by risk and risk_label.

    Prefer build_training_xy() when passing data to a model, to keep labels separate.
    """
    get_feature_columns(mode)
    raw = load_raw_uci(data_dir)
    out = engineer_inputs(raw, mode)
    out[TARGET_COLUMN] = _risk_target(raw)
    out["risk_label"] = out[TARGET_COLUMN].map({1: "High Risk", 0: "Low Risk"})
    return out


def build_training_xy(data_dir: Path, mode: str = "confirmatory"):
    """Return (X, y): approved inputs and the separate training target."""
    dataset = build_training_dataset(data_dir, mode)
    return dataset[get_feature_columns(mode)].copy(), dataset[TARGET_COLUMN].copy()


if __name__ == "__main__":
    assignment_root = Path(__file__).resolve().parents[1]  # assignment/code -> assignment/
    for mode in VALID_MODES:
        X, y = build_training_xy(assignment_root / "data", mode)
        print(f"{mode}: {len(X)} rows; inputs = {list(X.columns)}")
        print(f"High Risk: {int(y.sum())}; Low Risk: {int((y == 0).sum())}")
