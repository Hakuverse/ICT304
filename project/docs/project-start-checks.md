# Project starting checks - Issue #51

Historical record from 6 October. For current implementation and remaining
checks, see [Sprint 5 implementation checks](sprint5-implementation-checks.md).

Date: 6 October 2026. Baseline: reviewed main commit `a97a9b0` (PR #64).
This records checks of the project copy, not a new model evaluation or dashboard test.

## Environment

Windows, Python 3.12.10, scikit-learn 1.8.0, pandas 3.0.6,
NumPy 2.5.3 and joblib 1.6.0. These checks used the existing local environment.
A fresh installation and the new macOS project commands still need a teammate check.

## Commands and results

Run from the repository root:

```powershell
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m unittest discover -s project/code -v
.venv\Scripts\python.exe project/code/verify_dataset.py
.venv\Scripts\python.exe project/code/predict.py --mode confirmatory --csv project/data/sample_roster.csv
```

| Check | Result |
|---|---|
| Package check | No broken requirements found |
| Copied automated suite | 41 tests passed |
| Dataset | 395 students; 130 High Risk and 265 Low Risk; 33 columns |
| Sample A, G1 only | Low Risk; estimated High-Risk probability 0.155 |
| Sample B, G1 and G2 | Low Risk; estimated High-Risk probability 0.004 |
| Sample C | Skipped: attendance_pct must be 0 to 100 |
| Sample D | Skipped: G2='NA' is not a valid number |

Single-student checks used attendance 60, study hours 4 and failures 1:

```powershell
.venv\Scripts\python.exe project/code/predict.py --attendance 60 --study-hours 4 --failures 1
.venv\Scripts\python.exe project/code/predict.py --mode confirmatory --attendance 60 --study-hours 4 --failures 1 --g1 12
.venv\Scripts\python.exe project/code/predict.py --mode confirmatory --attendance 60 --study-hours 4 --failures 1 --g1 12 --g2 14
```

All three returned Low Risk, with estimated High-Risk probabilities 0.456,
0.155 and 0.005 respectively. These are software examples, not accuracy results.

## Folder independence

The project folder was also copied into a temporary directory without assignment/.
All 41 tests passed there. Training and comparison were run in that isolated copy:

```powershell
.venv\Scripts\python.exe project/code/train_models.py
.venv\Scripts\python.exe project/code/issue33_comparison.py --overwrite
```

The commands above show the script arguments; the isolated run used the original
environment's absolute Python path. Both scripts finished successfully and wrote
only inside the temporary project folder. This caught and fixed a Windows console
encoding problem with the training report's arrow; the saved report retains it.
The comparison tests also checked overwrite protection and missing figures.

The actual assignment files, prompt files and baseline project models were checked
for changes and remained unchanged. Temporary training outputs were not committed.

## Later review and follow-up

Issue #51 was reviewed through merged PR #71 and is closed. The 41-test results
above remain the original project-start checks. Later Windows/macOS functional
runs and the app checks have their own versions and evidence; see the
[Sprint 6 review](sprint6-review.md) and [app release record](app-release-notes.md).
Dashboard/recommendation integration and the tutor demonstration were reviewed
under #56/#57. They are not unfinished project-start tasks.

The prepared assignment code ZIP used `a97a9b0`. The exact file actually uploaded
to LMS is not established by this record; it remains a private submission-history
fact, not something inferred from a merged PR.
