# Prototype test checklist - Issue #56

Owner and tester: Benjamin. Windows checks completed on 12 October 2026.
Benjamin reported that P1-P16 passed. The screenshots below record the run;
P7 and P10 have the evidence gaps noted below. Earlier review checks remain
separate in [implementation checks](sprint5-implementation-checks.md).

## Record each run

- Date: 12 October 2026
- Tester: Benjamin
- Git commit: `2bbb083074e265bb8931b053bd262bbf47d29b19` (after PR #75)
- Branch: `sprint5-integration-checks`
- OS and Python version: Windows, Python 3.12.10
- Packages: scikit-learn 1.8.0, pandas 3.0.6, NumPy 2.5.3, joblib 1.6.0, Streamlit 1.64.0
- Evidence: [Windows screenshots and notes](evidence/issue56/windows/README.md)

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

Fictional student IDs were used. Pass records Benjamin's completed checks.
Pass (reported) identifies a case whose screenshots do not cover every part.

| ID | Check and expected result | Status | Actual result / evidence |
|---|---|---|---|
| P1 | Package check and full automated suite pass | Pass | Package check found no broken requirements; 89 tests passed in 17.427 seconds. [p1-environment00](evidence/issue56/windows/p1-environment00.png); [p1-environment01](evidence/issue56/windows/p1-environment01.png); [p1-tests](evidence/issue56/windows/p1-tests.png) |
| P2 | Early-Warning: attendance 40, study 4, failures 0; High Risk and attendance suggestion with baseline models | Pass | High Risk, probability 0.859, attendance suggestion. [p2-early-warning](evidence/issue56/windows/p2-early-warning.png) |
| P3 | Confirmatory: 80, 4, 0, G1 8, G2 blank; G1-only model, score 40 and assessment suggestion | Pass | G1-only model: High Risk, 0.818, assessment suggestion; G1 8 gives score 40. [p3-g1-only](evidence/issue56/windows/p3-g1-only.png) |
| P4 | Confirmatory: 80, 4, 0, G1 12, G2 0; G1+G2 model, score 30; zero is accepted | Pass | G1+G2 model: High Risk, 0.996, assessment suggestion; G2 0 accepted (score 30). [p4-g2-zero](evidence/issue56/windows/p4-g2-zero.png) |
| P5 | Early-Warning: 80, 5, 0; Low Risk and routine guidance only with baseline models | Pass | Low Risk, 0.284, routine guidance only. [p5-low-risk](evidence/issue56/windows/p5-low-risk.png) |
| P6 | Match form and command-line labels/probabilities for the same inputs and models | Pass | CLI and form agree: Early-Warning 0.859, G1-only 0.818, G1+G2 with zero 0.996; all High Risk. [p6-cli-comparison](evidence/issue56/windows/p6-cli-comparison.png) |
| P7 | Study hours 0 and 40 accepted; above 40 rejected; invalid attendance rejected | Pass (reported) | Benjamin reports both 0 and 40 accepted; 41 and attendance 150 rejected. The file named p7-study-40.png duplicates the 0 screenshot, so 40 needs a replacement screenshot. [p7-study-0](evidence/issue56/windows/p7-study-0.png); [p7-study-41-error](evidence/issue56/windows/p7-study-41-error.png); [p7-attendance-150-error](evidence/issue56/windows/p7-attendance-150-error.png) |
| P8 | Confirmatory missing G1 rejected; blank G2 accepted; invalid G2 such as NA rejected | Pass | Missing G1 and G2 NA rejected. Blank G2 accepted in P3; zero accepted in P4. [p8-missing-g1](evidence/issue56/windows/p8-missing-g1.png); [p8-g2-NA-error](evidence/issue56/windows/p8-g2-NA-error.png) |
| P9 | Upload sample_roster.csv in Confirmatory: A/B processed, C/D skipped with reasons | Pass | 4 rows: A/B predicted, C/D skipped with attendance and G2 reasons; valid rows show routine guidance. [p9-results](evidence/issue56/windows/p9-results.png); [p9-skipped](evidence/issue56/windows/p9-skipped.png) |
| P10 | Try dashboard_checks missing_g1_column.csv, empty.csv, header_only.csv and all_invalid.csv; clear messages and no invented results | Pass (reported) | Missing G1 column, empty and header-only files rejected with clear messages. Benjamin also reports the all-invalid check passed; its screenshot was not supplied. [p10-missing-column](evidence/issue56/windows/p10-missing-column.png); [p10-empty](evidence/issue56/windows/p10-empty.png); [p10-header-only](evidence/issue56/windows/p10-header-only.png) |
| P11 | Try extra_comma.csv and no_student_ids.csv; correct row reasons and processed/skipped totals | Pass | Extra-comma file: 2 rows, 1 predicted, 1 skipped. No-ID file: 3 rows, row 1 and row 3 predicted, row 2 skipped for attendance. [p11-extra-comma](evidence/issue56/windows/p11-extra-comma.png); [p11-no-ids](evidence/issue56/windows/p11-no-ids.png) |
| P12 | Upload duplicate IDs with different valid inputs and an invalid row; recommendations stay with the correct valid row | Pass | Duplicate-ID file: 5 rows, 2 predicted, 3 skipped. First DUP: G1-only High Risk 0.818 with assessment suggestion; second DUP: G1+G2 Low Risk 0.003 with routine guidance. [p12-duplicate-results](evidence/issue56/windows/p12-duplicate-results.png); [p16-invalid-failures](evidence/issue56/windows/p16-invalid-failures.png) |
| P13 | Same student through form and CSV has matching messages; downloaded CSV includes them | Pass | First DUP matches the G1-only form example in P3. Downloaded CSV opened in Excel with two valid results and their recommendation messages. Export screenshot retained; CSV download itself is not included. [p13-export](evidence/issue56/windows/p13-export.png); [p12-duplicate-results](evidence/issue56/windows/p12-duplicate-results.png); [p3-g1-only](evidence/issue56/windows/p3-g1-only.png) |
| P14 | Changing mode or inputs clears the previous form result | Pass | Old prediction and recommendation cleared after attendance changed and after switching modes, without another prediction. [p14-before-change](evidence/issue56/windows/p14-before-change.png); [p14-after-input-change](evidence/issue56/windows/p14-after-input-change.png); [p14-after-mode-change](evidence/issue56/windows/p14-after-mode-change.png) |
| P15 | Verify rule boundary, order and fallback unit-test results, including Low Risk with matching thresholds | Pass | All 11 recommendation tests passed, including boundaries, order, fallback and Low-Risk guidance. These tests supply risk labels directly. [p15-rule-tests](evidence/issue56/windows/p15-rule-tests.png) |
| P16 | Invalid failures in CSV (such as 1.5 or 4) are skipped; form offers only 0-3 | Pass | Form offers only 0-3. CSV failures 1.5 and 4 skipped with whole-number/range messages. [p16-failures-options](evidence/issue56/windows/p16-failures-options.png); [p16-invalid-failures](evidence/issue56/windows/p16-invalid-failures.png) |

Files above are under project/data/ or project/data/dashboard_checks/.
Rule-only cases may supply a risk label directly in unit tests; do not claim a
manual model prediction should change simply because a rule threshold is crossed.

## Problems and platform coverage

| Problem / failed check | Owner | Fix PR | Retest result |
|---|---|---|---|
| No software failures reported in this Windows run | Benjamin | Not needed | P1-P16 reported passed |
| P7: study-hours 40 screenshot duplicates the 0 capture | Benjamin | Evidence follow-up | Replace with a capture showing 40 and its result |
| P10: all-invalid screenshot missing | Benjamin | Evidence follow-up | Add capture showing 0 predicted, 4 skipped |

Windows run: Completed by Benjamin on 12 October 2026; evidence review gaps above.
macOS run: Not included in this record. Separate platform testing is planned in
[Sprint 6, issue #66](https://github.com/Hakuverse/ICT304/issues/66).
Peer review of this evidence is through the accompanying PR. This record does
not claim that a teammate has repeated the run or that the #57 demo has happened.

Save terminal output and readable screenshots showing inputs and results.
A screenshot alone should not replace the actual result written in the table.
Do not commit real student records. Link the evidence from #56 and request
teammate review. Leave unresolved cases clearly marked.
