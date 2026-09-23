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
  previous_score    G1 alone, or average of G1 and G2 when G2 is available,
                    rescaled from 0-20 to 0-100%. G3 is deliberately
                    excluded here -- it becomes the label instead, so using
                    it as a feature would leak the answer into the model.
  failures          Raw count of past class failures (0-3).
  risk (target)     1 = High Risk if G3 < PASS_MARK (10/20, the standard
                    pass mark), else 0 = Low Risk.
"""

from pathlib import Path
from dataclasses import dataclass

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
GRADE_SETUPS = ("g1", "g1_g2")
FEATURE_VALID_RANGES = {
    "attendance_pct": (0, 100), "study_hours": (0, 40),
    "failures": (0, 3), "previous_score": (0, 100),
}


def _has_grade(value) -> bool:
    return not (pd.isna(value) or (isinstance(value, str) and not value.strip()))


def _previous_score(df: pd.DataFrame) -> pd.Series:
    """G1 is required; blank/absent G2 means G1 only. Invalid G2 is an error."""
    g1 = _numeric_columns(df, ["G1"])["G1"]
    _check_range(g1, 0, 20)
    score = g1.astype(float).copy()
    if "G2" in df:
        supplied = df["G2"].map(_has_grade)
        if supplied.any():
            g2 = _numeric_columns(df.loc[supplied], ["G2"])["G2"]
            _check_range(g2, 0, 20)
            score.loc[supplied] = (g1.loc[supplied] + g2) / 2
    return score * 5


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
    for name in columns:
        if not np.isfinite(result[name].to_numpy(dtype=float)).all():
            raise ValueError(f"{name} must contain numbers, without blanks or infinity")
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
        required += ["G1"]
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
        out["previous_score"] = _previous_score(df)
    return out[columns].round(1)


def prepare_model_inputs(df: pd.DataFrame, mode: str = "confirmatory") -> pd.DataFrame:
    """Validate already-engineered form/CSV fields and return X only.

    This does not predict risk. A later trained model will consume the result.
    Attendance must use the same absence-based estimate as the training data.
    """
    out = _numeric_columns(df, get_feature_columns(mode))
    _check_range(out["attendance_pct"], 0, 100)
    _check_range(out["study_hours"], *FEATURE_VALID_RANGES["study_hours"])
    _check_range(out["failures"], 0, 3, whole=True)
    if mode == "confirmatory":
        _check_range(out["previous_score"], 0, 100)
    return out.copy()


@dataclass
class StudentBatch:
    """Inputs grouped by model, plus errors. Row numbers are 1-based data rows."""
    groups: dict[str, pd.DataFrame]
    errors: pd.DataFrame

    @property
    def message(self):
        count = sum(len(frame) for frame in self.groups.values())
        return (f"{count} valid students; {len(self.errors)} skipped."
                if count else "No valid students to process.")


def validate_students(df: pd.DataFrame, mode: str = "confirmatory", *,
                      raw_uci: bool = False) -> StudentBatch:
    """Public form/CSV entry point: skip bad rows and report their reasons.

    Forms supply attendance_pct, study_hours, failures and (Confirmatory) G1/G2.
    Grades use 0-20. Do not accept previous_score in place of G1: we need to know
    which model to use. Raw UCI files can use raw_uci=True.
    Missing required columns stop the whole file; optional G2 may be absent/blank.
    """
    columns = get_feature_columns(mode)
    required = (["absences", "studytime", "failures"] if raw_uci
                else EARLY_WARNING_FEATURES.copy())
    if mode == "confirmatory":
        required += ["G1"]
    if not df.columns.is_unique:
        raise ValueError("Column names must not be duplicated")
    missing = [name for name in required if name not in df]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if df.empty:
        raise ValueError("Provide at least one student")
    keys = ["early_warning"] if mode == "early_warning" else ["g1", "g1_g2"]
    groups = {key: [] for key in keys}
    errors = []
    # Use positions, not index labels: imported CSVs may contain duplicate IDs.
    for position in range(len(df)):
        row_number = position + 1
        row = df.iloc[[position]].copy()
        row.index = pd.Index([row_number], name="row_number")
        key = "early_warning" if mode == "early_warning" else (
            "g1_g2" if "G2" in row and _has_grade(row["G2"].iloc[0]) else "g1")
        try:
            if raw_uci:
                prepared = engineer_inputs(row, mode)
            else:
                prepared = row.copy()
                if mode == "confirmatory":
                    prepared["previous_score"] = _previous_score(row)
            groups[key].append(prepare_model_inputs(prepared, mode))
        except ValueError as error:
            errors.append({"row_number": row_number, "reason": str(error)})
    return StudentBatch(
        {key: pd.concat(rows) if rows else pd.DataFrame(columns=columns).rename_axis("row_number")
         for key, rows in groups.items()},
        pd.DataFrame(errors, columns=["row_number", "reason"]),
    )


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


def build_training_dataset(data_dir: Path, mode: str = "confirmatory", *,
                           grade_setup: str = "g1_g2") -> pd.DataFrame:
    """Return mode-specific features followed by risk and risk_label.

    Prefer build_training_xy() when passing data to a model, to keep labels separate.
    """
    get_feature_columns(mode)
    if grade_setup not in GRADE_SETUPS:
        raise ValueError(f"grade_setup must be one of {GRADE_SETUPS}")
    raw = load_raw_uci(data_dir)
    if mode == "confirmatory":
        if grade_setup == "g1":
            raw = raw.drop(columns="G2", errors="ignore")
        else:
            # A two-grade training set must never silently contain G1-only rows.
            _numeric_columns(raw, ["G1", "G2"])
    out = engineer_inputs(raw, mode)
    out[TARGET_COLUMN] = _risk_target(raw)
    out["risk_label"] = out[TARGET_COLUMN].map({1: "High Risk", 0: "Low Risk"})
    return out


def build_training_xy(data_dir: Path, mode: str = "confirmatory", *,
                      grade_setup: str = "g1_g2"):
    """Return (X, y): approved inputs and the separate training target."""
    dataset = build_training_dataset(data_dir, mode, grade_setup=grade_setup)
    return dataset[get_feature_columns(mode)].copy(), dataset[TARGET_COLUMN].copy()


if __name__ == "__main__":
    assignment_root = Path(__file__).resolve().parents[1]  # assignment/code -> assignment/
    for mode in VALID_MODES:
        X, y = build_training_xy(assignment_root / "data", mode)
        print(f"{mode}: {len(X)} rows; inputs = {list(X.columns)}")
        print(f"High Risk: {int(y.sum())}; Low Risk: {int((y == 0).sum())}")
