# Prototype checks: 28 September 2026

Environment: Windows, Python 3.12.10, scikit-learn 1.8.0, pandas 3.0.6, NumPy 2.5.3 and Matplotlib 3.11.2.

| Check | Result |
|---|---|
| Automated input, routing and CSV tests | 38 tests passed. |
| Confirmatory sample roster | A used G1-only; B used G1+G2. Both predicted Low Risk. |
| Invalid sample rows | C skipped for attendance outside 0-100; D skipped for invalid G2 text (`NA`). |
| Repeat model training | All 12 development comparison rows and all three reserved-test results matched the recorded results. |
| Repeat EDA | Generated findings matched the recorded findings. |
| Confusion-matrix figures | Titles fit; counts match the recorded results. |

Commands from the repository root:

```powershell
.venv\Scripts\python.exe -m unittest discover -s assignment/code -v
.venv\Scripts\python.exe assignment/code/predict.py --mode confirmatory --csv assignment/data/sample_roster.csv
.venv\Scripts\python.exe assignment/code/train_models.py
.venv\Scripts\python.exe assignment/code/eda.py
```

Training and EDA were repeated with output redirected to a temporary folder for comparison. The saved models in the repository were not replaced. The clearer confusion figures and corrected report wording were brought across after checking the numerical results.

These are software and reproducibility checks, not new evidence of real-world accuracy. The dashboard and recommendations are not yet implemented. Add the team's final submission-folder check, tester name, date and macOS result before submission; do not infer a macOS pass from the Windows run.
