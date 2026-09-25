# Using the two modes

The command-line prototype now trains models and predicts risk. The tutor dashboard
and recommendations are still planned work.

## Set up and check

Run these from the repository root (see the README for creating `.venv`):

```powershell
.venv\Scripts\python.exe -m pip install -r assignment/code/requirements.txt
.venv\Scripts\python.exe -m unittest discover -s assignment/code -v
```

Use `python` instead of the `.venv` path if your environment already has the packages.
The saved models use scikit-learn 1.8.0, which is pinned in the requirements.

**macOS:** from Terminal in the repository root, with Python 3.11 or newer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r assignment/code/requirements.txt
.venv/bin/python -m unittest discover -s assignment/code -v
.venv/bin/python assignment/code/predict.py --mode confirmatory --csv assignment/data/sample_roster.csv
```

If `.venv` is already set up, start at the install command. No activation is needed.
Expect `OK` from the tests (currently 38) and predictions for A/B with C/D skipped.
For all examples below, replace `.venv\Scripts\python.exe` with `.venv/bin/python`
on macOS. This also applies to the training command.

## Predict one student

```powershell
.venv\Scripts\python.exe assignment/code/predict.py --attendance 60 --study-hours 4 --failures 1
.venv\Scripts\python.exe assignment/code/predict.py --mode confirmatory --attendance 60 --study-hours 4 --failures 1 --g1 12
.venv\Scripts\python.exe assignment/code/predict.py --mode confirmatory --attendance 60 --study-hours 4 --failures 1 --g1 12 --g2 14
```

| Mode / grades supplied | Model used | Previous score inside the model |
|---|---|---|
| Early-Warning | Early-Warning | Not used |
| Confirmatory, G1 only | G1-only | G1 multiplied by 5 |
| Confirmatory, G1 and G2 | G1+G2 | Their average multiplied by 5 |

Enter G1 and G2 on the **0-20 scale**, not as percentages. G1 is required for
Confirmatory; G2 may be absent or blank. Each setup has its own trained model.
Neither prediction mode needs G3. Output includes a risk label and the model's
estimated probability of High Risk; it is not a guarantee about the student.

## Predict a class list

```powershell
.venv\Scripts\python.exe assignment/code/predict.py --mode confirmatory --csv assignment/data/sample_roster.csv
```

The included sample is invented for software checks, not accuracy measurement.
Students A and B are valid (G1-only and G1+G2); C has invalid attendance and D has
invalid G2 text. The last two should be skipped with explanations.
Add `--out assignment/reports/roster_predictions.csv` to save valid results.

- Required columns: `attendance_pct`, `study_hours`, `failures`; add `G1` for Confirmatory.
- `student_id` and `G2` are optional. Without an ID, errors/results use a data-row number.
- Attendance estimate: 0-100. Study hours: **0-40 inclusive**. Failures: whole numbers 0-3.
- An absent/empty/space-only G2 uses the G1-only model. Zero is a valid G2.
- Supplied G2 text such as `NA`, `N/A`, `null` or `nan`, infinity, or a number outside
  0-20 is invalid. That student is skipped; G2 is not silently ignored.
- Missing required columns stop the file with one message. Empty files and files
  containing only headers show "The CSV contains no students."
- Invalid rows are skipped with reasons while valid students continue. If every row
  is invalid, the command shows "No valid students to process" and the reasons.
- The 40-hour maximum is our input rule, not a maximum established by the dataset.

## Repeat training and evaluation

```powershell
.venv\Scripts\python.exe assignment/code/train_models.py
```

This rewrites the three saved models, evaluation report and confusion figures.
It compares 3 setups x 2 techniques x 2 class-weight settings = 12 combinations.
The same 79 students are reserved first for testing. Selection uses five-fold
cross-validation on the other 316 students. Read final performance from the reserved
[test results](evaluation_report.md), not the development comparison scores.

For code using raw UCI data, `build_training_xy(data_dir, "confirmatory", "g1")`
and `build_training_xy(data_dir, "confirmatory", "g1_g2")` return the matching inputs
and separate labels. `engineer_inputs()` defaults to `g1_g2` for compatibility with
EDA. `prepare_model_inputs()` validates already-prepared features as a whole;
use `predict_roster()` for row skipping and automatic model routing.

## Early-Warning limitations

Early-Warning predicts **without assessment grades**. The dataset does not establish
accuracy on day one or in a particular week. Its absence count becomes a capped
attendance proxy, not a measured attendance percentage; study hours are estimates
from categories. Do not substitute actual attendance percentages without reviewing
this mismatch. Testing at an early point needs records collected up to that point.

## Teammate check for #26 and #28

Anna or Jackie should install the requirements, run the tests, try the three single
student commands and the sample roster. Record their name, date, Python version and
outcome in the report checklist. The automated checks do not replace this team review.
