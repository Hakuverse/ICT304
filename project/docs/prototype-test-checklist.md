# Prototype test checklist - Issue #56

Owner: Benjamin. Run after the cleanup PR is reviewed and merged.
These are planned checks, not completed results. Earlier review checks are
recorded separately in [implementation checks](sprint5-implementation-checks.md).

## Record each run

- Date:
- Tester:
- Git commit (git rev-parse HEAD):
- OS and Python version:
- Package versions:
- Evidence folder or PR link:

From the repository root on Windows:

```powershell
git rev-parse HEAD
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m unittest discover -s project/code -v
.venv\Scripts\python.exe -m streamlit run project/code/dashboard.py
```

On macOS, replace .venv\Scripts\python.exe with .venv/bin/python.
Setup instructions are in the [project README](../README.md).
Expect 89 tests for the current version. Record the actual result and stop to
investigate any failure. Keep the terminal running while using the dashboard.

## Checks

Use fictional student IDs. For every row, replace Not run with Pass, Fail or
Blocked, add the actual result and link a screenshot or terminal output.

| ID | Check and expected result | Status | Actual result / evidence |
|---|---|---|---|
| P1 | Package check and full automated suite pass | Not run | |
| P2 | Early-Warning: attendance 40, study 4, failures 0; High Risk and attendance suggestion with baseline models | Not run | |
| P3 | Confirmatory: 80, 4, 0, G1 8, G2 blank; G1-only model, score 40 and assessment suggestion | Not run | |
| P4 | Confirmatory: 80, 4, 0, G1 12, G2 0; G1+G2 model, score 30; zero is accepted | Not run | |
| P5 | Early-Warning: 80, 5, 0; Low Risk and routine guidance only with baseline models | Not run | |
| P6 | Match form and command-line labels/probabilities for the same inputs and models | Not run | |
| P7 | Study hours 0 and 40 accepted; above 40 rejected; invalid attendance rejected | Not run | |
| P8 | Confirmatory missing G1 rejected; blank G2 accepted; invalid G2 such as NA rejected | Not run | |
| P9 | Upload sample_roster.csv in Confirmatory: A/B processed, C/D skipped with reasons | Not run | |
| P10 | Try dashboard_checks missing_g1_column.csv, empty.csv, header_only.csv and all_invalid.csv; clear messages and no invented results | Not run | |
| P11 | Try extra_comma.csv and no_student_ids.csv; correct row reasons and processed/skipped totals | Not run | |
| P12 | Upload duplicate IDs with different valid inputs and an invalid row; recommendations stay with the correct valid row | Not run | |
| P13 | Same student through form and CSV has matching messages; downloaded CSV includes them | Not run | |
| P14 | Changing mode or inputs clears the previous form result | Not run | |
| P15 | Verify rule boundary, order and fallback unit-test results, including Low Risk with matching thresholds | Not run | |
| P16 | Invalid failures in CSV (such as 1.5 or 4) are skipped; form offers only 0-3 | Not run | |

Files above are under project/data/ or project/data/dashboard_checks/.
Rule-only cases may supply a risk label directly in unit tests; do not claim a
manual model prediction should change simply because a rule threshold is crossed.

## Problems and platform coverage

| Problem / failed check | Owner | Fix PR | Retest result |
|---|---|---|---|
| None recorded yet; testing pending | | | |

Windows run: Not run in this checklist.
macOS run: Not run in this checklist; coordinate with Jackie.

Save terminal output and readable screenshots showing inputs and results.
A screenshot alone should not replace the actual result written in the table.
Do not commit real student records. Link the evidence from #56 and request
teammate review. Leave unresolved cases clearly marked.
