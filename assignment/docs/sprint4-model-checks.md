# Sprint 4 model checks

> Historical development record. Tasks and results below describe the position at the time.
> See the [submission verification summary](submission-verification.md) for the later report checks.

Tester: Benjamin
Date: 29 September 2026
Issues: #30, #31 and #32
Platform: Windows

## Environment

- Python 3.12.10
- scikit-learn 1.8.0
- pandas 3.0.6
- NumPy 2.5.3
- joblib 1.6.0
- Package check: no broken requirements found.

## #30: Training setup

I checked the Math dataset and ran the data preparation code.
There were 395 students: 130 High Risk and 265 Low Risk.

Early-Warning used attendance_pct, study_hours and failures.
Both Confirmatory setups also used previous_score, calculated
from G1 alone or from G1 and G2. G3 was not a model input.

The code reserves 79 students for final testing and uses the
other 316 for development. The comparisons use five-fold
stratified validation, with shuffling and random_state=42.

Logistic Regression currently runs without StandardScaler.
This is a limitation to discuss, not a feature already implemented.

## #31: Logistic Regression

I ran the training script and checked all six Logistic Regression
comparisons: three input setups, each with class_weight=None
and class_weight="balanced".

The code uses max_iter=1000 and random_state=42.
The results matched the existing evaluation report.

Balanced weights increased High-Risk recall in all three setups,
but reduced precision. This means more High-Risk students were
found, with more false alarms.

## #32: Decision Tree

I checked all six Decision Tree comparisons.

The script tried depths 2, 3, 4, 5, 6 and no depth limit using
balanced Early-Warning development results. Depth 4 had the
highest recall, 0.482, and was then used for all tree comparisons.
The trees use random_state=42.

The results matched the existing evaluation report.
Depth was selected using development data, not the reserved test set.

## Model selection and final results

The code selects the highest development recall and uses F1
to break a tie.

| Setup | Selected model | Final test recall |
|---|---|---:|
| Early-Warning | Balanced Decision Tree, depth 4 | 0.423 |
| Confirmatory: G1 | Balanced Logistic Regression | 0.769 |
| Confirmatory: G1 and G2 | Balanced Logistic Regression | 0.885 |

These final results use the 79 reserved students. They are
separate from the development comparison scores.

Full comparison: [evaluation report](evaluation_report.md).

## Commands and checks

Run from the repository root:

```powershell
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe assignment/code/verify_dataset.py
.venv\Scripts\python.exe assignment/code/data_processing.py
.venv\Scripts\python.exe assignment/code/train_models.py
.venv\Scripts\python.exe -m unittest discover -s assignment/code -v
.venv\Scripts\python.exe assignment/code/predict.py --mode confirmatory --csv assignment/data/sample_roster.csv
```

All 38 automated tests passed before and after training.

The sample CSV produced:
- A: Low Risk, probability 0.155, G1-only model.
- B: Low Risk, probability 0.004, G1+G2 model.
- C: skipped because attendance was outside 0-100.
- D: skipped because G2 contained invalid text.

Retraining changed the three saved model files. Git reported
no changes to the evaluation report or figures. The reason
for the binary model differences has not yet been checked.

## Remaining review

- [ ] Anna or Jackie reviews this note and the linked results.
- [ ] Review the regenerated model files before deciding whether to include them.
- [ ] Add the review/PR link to #30, #31 and #32.

These checks reproduce the existing experiment. They do not
provide new independent evidence of real-world accuracy.