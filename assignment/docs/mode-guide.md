# Using the two modes

This covers issue #26. The code prepares inputs for a model; it does not train a model
or predict a student's risk yet.

## Run it

From the repository root, use the environment described in the README:

```powershell
.venv\Scripts\python.exe assignment/code/data_processing.py
.venv\Scripts\python.exe -m unittest discover -s assignment/code -v
```

The first command prints 395 students for each mode: 130 High Risk and 265 Low Risk.
The second runs the small checks in `test_data_processing.py`. If Python already has
the required packages, `python` can replace `.venv\Scripts\python.exe`.

## For training later

From a script saved in `assignment/code/`:

```python
from pathlib import Path
from data_processing import build_training_xy

data_dir = Path(__file__).resolve().parents[1] / "data"
X, y = build_training_xy(data_dir, mode="early_warning")
# X: attendance_pct, study_hours, failures
# y: 1 for High Risk, 0 for Low Risk

X, y = build_training_xy(data_dir, mode="confirmatory")
# X also includes previous_score, calculated from G1 and G2.
```

The code reads `student-mat.csv` only. It never adds another course automatically.
Pass X to the later model, not the complete labelled dataset. G3 is used only to make y.

## For a form or CSV later

If the input already contains the prepared fields, use `prepare_model_inputs()`:

```python
import pandas as pd
from data_processing import prepare_model_inputs

students = pd.DataFrame({
    "attendance_pct": [50.0],  # Our absence estimate: 15 absences -> 50.
    "study_hours": [3.5],
    "failures": [1],
})
X = prepare_model_inputs(students, mode="early_warning")

students["previous_score"] = [60.0]
X = prepare_model_inputs(students, mode="confirmatory")
```

Neither call needs a final grade. Early-Warning does not need any prior grade.
The function returns only the chosen input columns and keeps the original row index.
Extra columns such as student IDs and labels are not passed to the model; keep IDs
separately when displaying the results.

For raw UCI fields, `engineer_inputs(raw, mode)` makes the attendance/study estimates
first. Early-Warning needs only `absences`, `studytime` and `failures`; Confirmatory
also needs G1 and G2. `engineer_features(raw)` is the existing EDA helper and still
requires G3 because it adds the labels for charts.

## Input checks

- Missing fields, blank cells, non-numeric or infinite values raise a clear error.
- Raw absences and failures must be non-negative whole numbers; absences are capped
  at 30 for the estimate, and failures are capped at 3. Studytime must be 1, 2, 3 or 4.
- Prepared attendance and previous score must be between 0 and 100. Prepared failures
  must be a whole number from 0 to 3. Study hours must be non-negative.
- An empty table or an unknown mode is rejected. Invalid rows are not silently filled in.

The helper currently rejects invalid input as a whole. A future dashboard can catch
the error and ask the teacher to correct it. Per-row CSV skipping is not implemented.
Actual attendance percentages from another system should not be treated as equivalent
to our absence-based estimate without reviewing the data meaning first.

## Before closing #26

Ask Anna or Jackie to run the commands above on their machine and review the PR.
These checks confirm input preparation; model accuracy is separate Sprint 4 work.
