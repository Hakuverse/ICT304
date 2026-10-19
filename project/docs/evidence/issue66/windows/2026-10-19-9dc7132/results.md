# Sprint 6 Windows checks

Tester: Benjamin. Date: 19 October 2026. Related issue: #66.
Branch: `sprint6-windows-evidence`.
Tested commit: `9dc7132dc0a1a735b508447b99f49b70afb84f6d` (PR #87 merged).
Started from a fresh, clean clone. Saved models from this commit were used without retraining.

## Environment

- Windows: NT 10.0.26200.0, as recorded by the PowerShell transcript.
- Python 3.12.10; scikit-learn 1.8.0; pandas 3.0.6; NumPy 2.5.4; joblib 1.6.0; Streamlit 1.66.0.
- Browser/version, full screen resolution and browser zoom: not recorded. Cropped screenshots do not establish a viewport or zoom.
- The original [environment transcript](environment.txt) missed command output. The [supplementary environment check](environment-verified.txt) records the same virtual environment during evidence review; it is not presented as the original transcript output.

## Results

All S6-01 to S6-18 Windows cases passed based on the retained screenshots/logs and Benjamin's confirmation of the form boundary subcases on 19 October. Screenshots are representative; they do not independently show every manual input. macOS, timing and usability outcomes are recorded separately under their own runs.

| Test | Actual result | Status | Evidence |
|---|---|---|---|
| S6-01 | Fresh clone at 9dc7132, initially clean. 99 tests passed in 16.178 s. Supplementary package check found no broken requirements. | Pass | [01-S6-01-clean-checkout](01-S6-01-clean-checkout.png), [02-S6-01-automated-tests](02-S6-01-automated-tests.png), [automated-tests.txt](automated-tests.txt), [environment-verified.txt](environment-verified.txt) |
| S6-02 | Early-Warning 40/4/0: High Risk, 85.9%, attendance support; no grades. | Pass | [03-S6-02-05-early-warning](03-S6-02-05-early-warning.png) |
| S6-03 | Confirmatory 80/4/0, G1 8, G2 blank: High Risk, 81.8%, G1 only, assessment support. | Pass | [04-S6-03-05-g1-only](04-S6-03-05-g1-only.png) |
| S6-04 | Confirmatory 80/4/0, G1 12, G2 0: High Risk, 99.6%, G1+G2; zero accepted. | Pass | [05-S6-04-05-g2-zero](05-S6-04-05-g2-zero.png) |
| S6-05 | All four form/CLI/CSV examples match: High Risk 0.859, High Risk 0.818 (g1), High Risk 0.996 (g1_g2), Low Risk 0.003 (g1_g2). Form and CSV messages agree. Percentages are the same probabilities displayed as percent. | Pass | [03-S6-02-05-early-warning](03-S6-02-05-early-warning.png), [04-S6-03-05-g1-only](04-S6-03-05-g1-only.png), [05-S6-04-05-g2-zero](05-S6-04-05-g2-zero.png), [06-S6-05-g1-g2](06-S6-05-g1-g2.png), [07-S6-05-csv-early-warning](07-S6-05-csv-early-warning.png), [08-S6-05-csv-confirmatory](08-S6-05-csv-confirmatory.png), [S6-05-cli-comparison.txt](S6-05-cli-comparison.txt) |
| S6-06 | Attendance 0 and 100 accepted; -1 and 101 rejected in form and skipped in mixed CSV. | Pass | [09-S6-06-attendance-invalid](09-S6-06-attendance-invalid.png), [15-S6-06-09-csv-boundary-results-a](15-S6-06-09-csv-boundary-results-a.png), [15-S6-06-09-csv-boundary-results-b](15-S6-06-09-csv-boundary-results-b.png), [15-S6-06-09-csv-boundary-results-c](15-S6-06-09-csv-boundary-results-c.png), [16-S6-06-09-csv-boundary-errors](16-S6-06-09-csv-boundary-errors.png); form confirmation below |
| S6-07 | Study hours 0 and 40 accepted; -1 and 41 rejected in form and skipped in mixed CSV. | Pass | [10-S6-07-study-40-accepted](10-S6-07-study-40-accepted.png), [11-S6-07-study-41-rejected](11-S6-07-study-41-rejected.png), [15-S6-06-09-csv-boundary-results-a](15-S6-06-09-csv-boundary-results-a.png), [15-S6-06-09-csv-boundary-results-b](15-S6-06-09-csv-boundary-results-b.png), [15-S6-06-09-csv-boundary-results-c](15-S6-06-09-csv-boundary-results-c.png), [16-S6-06-09-csv-boundary-errors](16-S6-06-09-csv-boundary-errors.png); form confirmation below |
| S6-08 | Form dropdown offers 0, 1, 2, 3. CSV accepts these four values; -1, 4 and 1.5 are skipped. | Pass | [12-S6-08-failure-options](12-S6-08-failure-options.png), [15-S6-06-09-csv-boundary-results-a](15-S6-06-09-csv-boundary-results-a.png), [15-S6-06-09-csv-boundary-results-b](15-S6-06-09-csv-boundary-results-b.png), [15-S6-06-09-csv-boundary-results-c](15-S6-06-09-csv-boundary-results-c.png), [16-S6-06-09-csv-boundary-errors](16-S6-06-09-csv-boundary-errors.png) |
| S6-09 | G1 blank/-1/21/NA rejected; G1 0/20 accepted. G2 blank/0/20 accepted, -1/21/NA rejected. Blank G2 uses g1; supplied G2 uses g1_g2. Form subcases confirmed by Benjamin; CSV outcomes recorded. | Pass | [04-S6-03-05-g1-only](04-S6-03-05-g1-only.png), [05-S6-04-05-g2-zero](05-S6-04-05-g2-zero.png), [13-S6-09-g1-invalid-text](13-S6-09-g1-invalid-text.png), [14-S6-09-invalid-grade](14-S6-09-invalid-grade.png), [15-S6-06-09-csv-boundary-results-a](15-S6-06-09-csv-boundary-results-a.png), [15-S6-06-09-csv-boundary-results-b](15-S6-06-09-csv-boundary-results-b.png), [15-S6-06-09-csv-boundary-results-c](15-S6-06-09-csv-boundary-results-c.png), [16-S6-06-09-csv-boundary-errors](16-S6-06-09-csv-boundary-errors.png) |
| S6-10 | sample_roster.csv: 4 rows, A/B predicted, C/D skipped for attendance and G2=NA. | Pass | [17-S6-10-mixed-roster](17-S6-10-mixed-roster.png) |
| S6-11 | Missing G1 and missing Early-Warning attendance column rejected; empty and header-only files report no students. No predictions shown. | Pass | [18-S6-11-missing-g1-column](18-S6-11-missing-g1-column.png), [19-S6-11-empty-file](19-S6-11-empty-file.png), [20-S6-11-header-only](20-S6-11-header-only.png), [27-S6-11-missing-ew-column](27-S6-11-missing-ew-column.png) |
| S6-12 | All-invalid fixture: 4 rows, 0 predicted, 4 skipped, with attendance/study/failures/missing-G1 reasons. | Pass | [21-S6-12-all-invalid](21-S6-12-all-invalid.png) |
| S6-13 | Extra comma: 2/1/1. No IDs: 3/2/1, row 1 and row 3 predicted. Messy headers: 1/1/0. Unmatched quote rejected clearly. Counts are total/predicted/skipped. | Pass | [22-S6-13-extra-comma](22-S6-13-extra-comma.png), [23-S6-13-no-student-ids](23-S6-13-no-student-ids.png), [24-S6-13-messy-headers](24-S6-13-messy-headers.png), [25-S6-13-unmatched-quote](25-S6-13-unmatched-quote.png) |
| S6-14 | Duplicate fixture: 5/2/3. First DUP High Risk 81.8% g1, second DUP Low Risk 0.3% g1_g2. Each keeps its own message. | Pass | [26-S6-14-15-duplicate-ids](26-S6-14-15-duplicate-ids.png) |
| S6-15 | Downloaded file retains exactly the two DUP results in order, full messages, decimal probabilities and setups. Invalid rows excluded. Retained export verified against the saved models and rules. | Pass | [26-S6-14-15-duplicate-ids](26-S6-14-15-duplicate-ids.png), [28-S6-15-downloaded-results](28-S6-15-downloaded-results.png), [S6-15-duplicate-results.csv](S6-15-duplicate-results.csv), [evidence-verification.txt](evidence-verification.txt) |
| S6-16 | Result and suggestions disappear when attendance changes from 40 to 50, and after a new prediction followed by switching to Confirmatory. | Pass | [29-S6-16-before-change](29-S6-16-before-change.png), [30-S6-16-after-input-change](30-S6-16-after-input-change.png), [31-S6-16-after-mode-change](31-S6-16-after-mode-change.png) |
| S6-17 | Recommendation boundary tests passed; separate supplied High-Risk checks confirm score 49 triggers assessment review and score 50 returns fallback with other thresholds inactive. | Pass | [32-S6-17-18-recommendation-tests](32-S6-17-18-recommendation-tests.png), [S6-17-18-recommendation-tests.txt](S6-17-18-recommendation-tests.txt), [S6-17-score-49-50.txt](S6-17-score-49-50.txt) |
| S6-18 | 11 rule tests passed, including message order/no duplicates, High-Risk fallback, Low-Risk routine guidance and no Early-Warning assessment rule. These tests are included in the 99, not additional. | Pass | [32-S6-17-18-recommendation-tests](32-S6-17-18-recommendation-tests.png), [S6-17-18-recommendation-tests.txt](S6-17-18-recommendation-tests.txt) |

## Boundary subcases

Benjamin confirmed on 19 October that every listed form boundary subcase passed. The table distinguishes that confirmation from the saved CSV screenshots. Other fields stayed valid while one input changed. Screenshot 13 shows G1=NA, not a blank-G1 form submission; its filename was corrected. Blank G1 is visible as rejected in the CSV evidence, and its form result is supported by Benjamin's confirmation.

The [boundary fixture](fixtures/boundary-checks.csv) contains 28 rows: 14 predicted and 14 skipped. Screenshots 15a-c and 16 show the accepted students and rejected reasons. A supplementary file check also reproduced these totals; it does not replace the manual form run.

| Subcase | Value | Form actual result | CSV actual result | Status |
|---|---|---|---|---|
| S6-06-attendance-0 | 0 | Accepted | Predicted | Pass |
| S6-06-attendance-100 | 100 | Accepted | Predicted | Pass |
| S6-06-attendance--1 | -1 | Rejected | Skipped with reason | Pass |
| S6-06-attendance-101 | 101 | Rejected | Skipped with reason | Pass |
| S6-07-study-0 | 0 | Accepted | Predicted | Pass |
| S6-07-study-40 | 40 | Accepted | Predicted | Pass |
| S6-07-study--1 | -1 | Rejected | Skipped with reason | Pass |
| S6-07-study-41 | 41 | Rejected | Skipped with reason | Pass |
| S6-08-failures-0 | 0 | Accepted | Predicted | Pass |
| S6-08-failures-1 | 1 | Accepted | Predicted | Pass |
| S6-08-failures-2 | 2 | Accepted | Predicted | Pass |
| S6-08-failures-3 | 3 | Accepted | Predicted | Pass |
| S6-08-failures--1 | -1 | Not offered by dropdown | Skipped with reason | Pass |
| S6-08-failures-4 | 4 | Not offered by dropdown | Skipped with reason | Pass |
| S6-08-failures-1.5 | 1.5 | Not offered by dropdown | Skipped with reason | Pass |
| S6-09-G1-blank | blank | Rejected | Skipped with reason | Pass |
| S6-09-G1-0 | 0 | Accepted | Predicted | Pass |
| S6-09-G1-20 | 20 | Accepted | Predicted | Pass |
| S6-09-G1--1 | -1 | Rejected | Skipped with reason | Pass |
| S6-09-G1-21 | 21 | Rejected | Skipped with reason | Pass |
| S6-09-G1-NA | NA | Rejected | Skipped with reason | Pass |
| S6-09-G2-blank | blank | Accepted | Predicted | Pass |
| S6-09-G2-0 | 0 | Accepted | Predicted | Pass |
| S6-09-G2-20 | 20 | Accepted | Predicted | Pass |
| S6-09-G2--1 | -1 | Rejected | Skipped with reason | Pass |
| S6-09-G2-21 | 21 | Rejected | Skipped with reason | Pass |
| S6-09-G2-NA | NA | Rejected | Skipped with reason | Pass |

## Record notes and follow-up

- No functional failures were reported in this Windows run. The red PowerShell `NativeCommandError` wrapper in unittest output is how this shell displayed the test runner's stderr; the retained suite ends with 99 tests and OK, and the rule-only run ends with 11 tests and OK.
- The actual downloaded CSV was retained from Downloads. Its original local name had a doubled `.csv.csv` extension; only the evidence filename was shortened.
- No boundary-results download was retained. The boundary input, screenshots and supplementary check preserve the outcomes; the required duplicate-results export is included for S6-15.
- S6-19 to S6-24 are not marked passed by this functional run. Browser viewport/zoom are needed for Anna's separate readability checks.
- Issue #66 remains open until Jackie's macOS evidence and the combined platform review are complete. Benjamin consolidates results in #70.

## Screenshot index

- [01-S6-01-clean-checkout.png](01-S6-01-clean-checkout.png)
- [02-S6-01-automated-tests.png](02-S6-01-automated-tests.png)
- [03-S6-02-05-early-warning.png](03-S6-02-05-early-warning.png)
- [04-S6-03-05-g1-only.png](04-S6-03-05-g1-only.png)
- [05-S6-04-05-g2-zero.png](05-S6-04-05-g2-zero.png)
- [06-S6-05-g1-g2.png](06-S6-05-g1-g2.png)
- [07-S6-05-csv-early-warning.png](07-S6-05-csv-early-warning.png)
- [08-S6-05-csv-confirmatory.png](08-S6-05-csv-confirmatory.png)
- [09-S6-06-attendance-invalid.png](09-S6-06-attendance-invalid.png)
- [10-S6-07-study-40-accepted.png](10-S6-07-study-40-accepted.png)
- [11-S6-07-study-41-rejected.png](11-S6-07-study-41-rejected.png)
- [12-S6-08-failure-options.png](12-S6-08-failure-options.png)
- [13-S6-09-g1-invalid-text.png](13-S6-09-g1-invalid-text.png)
- [14-S6-09-invalid-grade.png](14-S6-09-invalid-grade.png)
- [15-S6-06-09-csv-boundary-results-a.png](15-S6-06-09-csv-boundary-results-a.png)
- [15-S6-06-09-csv-boundary-results-b.png](15-S6-06-09-csv-boundary-results-b.png)
- [15-S6-06-09-csv-boundary-results-c.png](15-S6-06-09-csv-boundary-results-c.png)
- [16-S6-06-09-csv-boundary-errors.png](16-S6-06-09-csv-boundary-errors.png)
- [17-S6-10-mixed-roster.png](17-S6-10-mixed-roster.png)
- [18-S6-11-missing-g1-column.png](18-S6-11-missing-g1-column.png)
- [19-S6-11-empty-file.png](19-S6-11-empty-file.png)
- [20-S6-11-header-only.png](20-S6-11-header-only.png)
- [21-S6-12-all-invalid.png](21-S6-12-all-invalid.png)
- [22-S6-13-extra-comma.png](22-S6-13-extra-comma.png)
- [23-S6-13-no-student-ids.png](23-S6-13-no-student-ids.png)
- [24-S6-13-messy-headers.png](24-S6-13-messy-headers.png)
- [25-S6-13-unmatched-quote.png](25-S6-13-unmatched-quote.png)
- [26-S6-14-15-duplicate-ids.png](26-S6-14-15-duplicate-ids.png)
- [27-S6-11-missing-ew-column.png](27-S6-11-missing-ew-column.png)
- [28-S6-15-downloaded-results.png](28-S6-15-downloaded-results.png)
- [29-S6-16-before-change.png](29-S6-16-before-change.png)
- [30-S6-16-after-input-change.png](30-S6-16-after-input-change.png)
- [31-S6-16-after-mode-change.png](31-S6-16-after-mode-change.png)
- [32-S6-17-18-recommendation-tests.png](32-S6-17-18-recommendation-tests.png)
