"""
SARAH — Data Processing
------------------------
Loads the UCI "Student Performance" dataset and turns its raw columns into
the four SARAH input features plus the Low/High Risk label.

Feature engineering decisions:
  attendance_pct   From `absences` (capped at 30, rescaled so 0 absences =
                    100% attendance, >=30 absences = 0%).
  study_hours       From `studytime` (1-4 ordinal bucket), converted to a
                    numeric hours/week estimate using each bucket's midpoint.
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
TARGET_COLUMN = "risk"


def load_raw_uci(data_dir: Path) -> pd.DataFrame:
    """Load student-mat.csv, and student-por.csv too if it's been added."""
    data_dir = Path(data_dir)
    mat = pd.read_csv(data_dir / "student-mat.csv", sep=";")
    mat["course"] = "Math"

    por_path = data_dir / "student-por.csv"
    if por_path.exists():
        por = pd.read_csv(por_path, sep=";")
        por["course"] = "Portuguese"
        return pd.concat([mat, por], ignore_index=True)

    print(f"Note: student-por.csv not found in {data_dir} -- using Math course "
          f"data only ({len(mat)} rows).")
    return mat


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)

    capped_absences = df["absences"].clip(upper=MAX_ABSENCES_FOR_SCALING)
    out["attendance_pct"] = (1 - capped_absences / MAX_ABSENCES_FOR_SCALING) * 100

    out["study_hours"] = df["studytime"].map(STUDYTIME_HOURS_MAP)
    out["previous_score"] = ((df["G1"] + df["G2"]) / 2) / 20 * 100
    out["failures"] = df["failures"].clip(upper=3)

    out[TARGET_COLUMN] = np.where(df["G3"] < PASS_MARK, 1, 0)
    out["risk_label"] = out[TARGET_COLUMN].map({1: "High Risk", 0: "Low Risk"})

    if "course" in df.columns:
        out["course"] = df["course"]

    return out.round({"attendance_pct": 1, "study_hours": 1, "previous_score": 1})


def build_training_dataset(data_dir: Path) -> pd.DataFrame:
    raw = load_raw_uci(data_dir)
    return engineer_features(raw)


if __name__ == "__main__":
    assignment_root = Path(__file__).resolve().parents[1]  # assignment/code -> assignment/
    dataset = build_training_dataset(assignment_root / "data")
    print(f"Built {len(dataset)} rows")
    print(dataset["risk_label"].value_counts(normalize=True).round(3))
