# Using the two modes

We have two modes for the tutor. Confirmatory has two separate model setups so a
student with only G1 is not passed to a model trained on the G1/G2 average.

| Mode / available grades | Inputs used by the model | Model setup |
|---|---|---|
| Early-Warning, no grades needed | Attendance estimate, study hours, past failures | `early_warning` |
| Confirmatory, G1 only | Same three inputs, plus G1 scaled to 0-100 | `g1` |
| Confirmatory, G1 and G2 | Same three inputs, plus their average scaled to 0-100 | `g1_g2` |

G1 and G2 are entered on the UCI **0-20 scale**, including zero. G1 is required in
Confirmatory. G2 may be absent or blank. A supplied G2 that is text, infinite or
outside 0-20 is an error; it is not silently ignored. G2 alone is not enough.
G3 is only used to make the training label: below 10 is High Risk.

## Run the checks and model comparison

From the repository root, after the README setup:

```powershell
.venv\Scripts\python.exe -m unittest discover -s assignment/code -v
.venv\Scripts\python.exe assignment/code/train_models.py
```

The first command checks validation, grade handling and model routing. The second
prints six result rows: Logistic Regression and Decision Tree for each of the three
setups. Both use balanced class weights. Tree depth is fixed at 3 for this baseline.
We use the same stratified five folds (seed 42) for each comparison; scaling for
Logistic Regression is fitted inside each training fold. Precision, recall and F1
refer to High Risk. These are development comparisons, not a separate final test
of a chosen winner. They do not reuse the unverified numbers in PRs #44-46.

If Python already has the required packages, use `python` instead of the `.venv` path.

## A class list with some invalid students

From a script in `assignment/code/`:

```python
import pandas as pd
from data_processing import validate_students

students = pd.DataFrame({
    "attendance_pct": [80, 70, 150],  # Our absence-based estimate, not measured attendance.
    "study_hours": [4, 6, 5],
    "failures": [0, 1, 0],
    "G1": [12, 8, 10],
    "G2": [None, 10, None],
})
batch = validate_students(students, mode="confirmatory")
print(batch.message)  # 2 valid students; 1 skipped.
print(batch.errors)   # Row 3: attendance_pct must be 0 to 100.
print(batch.groups["g1"])     # Row 1, previous_score = 60.
print(batch.groups["g1_g2"])  # Row 2, previous_score = 45.
```

- Missing required columns, duplicate column names or an empty table stop the file.
- Invalid rows are skipped and listed with a reason. Other students continue.
- Row numbers start at 1 for the first student, excluding the CSV header. Keep the
  original table to look up the student's name/ID; IDs are not model inputs.
- Attendance estimate: 0-100. Study hours: **0-40 inclusive**. Past failures: whole
  numbers from 0 to 3. Required values cannot be blank, text or infinite.
- The 40-hour maximum is our team's input rule, not a limit proved by the dataset.
- If all rows fail, `batch.message` says **No valid students to process.**
- For an individual form, the same validation returns the student's error so the
  tutor can correct it. A dashboard/upload screen is still to be built.

For raw UCI columns (`absences`, `studytime`, `failures`, G1 and optional G2), pass
`raw_uci=True`. Raw absences and failures must be non-negative whole numbers;
absences are capped at 30 and failures at 3. Studytime must be 1, 2, 3 or 4.

## Train and try predictions

```python
from pathlib import Path
from train_models import train_models, predict_students

data_dir = Path(__file__).resolve().parents[1] / "data"
models = train_models(data_dir)
predictions, skipped = predict_students(students, models, mode="confirmatory")
print(predictions)  # Original row number, model setup and risk (1 = High Risk).
print(skipped)
```

This trains three separate balanced Logistic Regression models as a demo baseline.
It does not choose the best model automatically. An absent G2 uses the G1 model;
a valid G2 uses the G1/G2 model. For Early-Warning, set `mode="early_warning"`.
If every row is invalid, predictions is empty and skipped contains the reasons.
Training predictions must not be reported as test accuracy.

Training code can also call `build_training_xy(data_dir, mode="confirmatory",
grade_setup="g1")` or `grade_setup="g1_g2"`. Both use the same 395 Math students and
separate labels. The two-grade training setup requires both grades for every row.

`engineer_inputs()` and `prepare_model_inputs()` remain strict helpers for trusted
training/analysis inputs: they raise on invalid data. Use `validate_students()` or
`predict_students()` for forms and class lists. `prepare_model_inputs()` accepts
already-computed features, but does not determine which grade setup they came from.
`engineer_features()` keeps the existing G1/G2 EDA view for the complete Math dataset.

## What Early-Warning can show with this dataset

It estimates risk without assessment grades. It does **not** establish prediction
accuracy on day one or in a particular week. UCI has absence counts and study-time
categories, not weekly attendance histories or the total scheduled lessons needed
for a true attendance percentage. Our attendance value is a capped absence-based
proxy; study hours are category estimates (including an assumed 12 for the top group).
Real attendance percentages should not be substituted without reviewing this mismatch.

For the assignment we can compare grade-free predictions against final outcomes and
report weak results honestly. Example CSVs test the program's behaviour, not its
accuracy. Testing at a specific early point needs records collected up to that point;
this is future work. See the [UCI dataset description](https://archive.ics.uci.edu/dataset/320/student+performance).
