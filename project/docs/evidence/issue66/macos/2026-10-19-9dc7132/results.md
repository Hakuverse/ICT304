# Sprint 6 macOS checks

Tester/coordinator: Jackie. Date: 19 October 2026. Related issue: #66.  
Tested commit: `9dc7132dc0a1a735b508447b99f49b70afb84f6d` (PR #87 merged).  
S6-11 Early-Warning retest: 20 October 2026, at the same tested commit.
Test-run branch: `main` in a fresh dedicated clone, initially clean as recorded during the guided run.  
Evidence submission branch: `66NNest-s6-run-complete-workflow-checks-on-windows-and-macos`.  
The submission branch is not the tested commit. Saved models at the tested commit were used without retraining.

## Environment

- MacBook Air, Apple M3, 24 GB RAM; macOS 26.6.2, build 25G83.
- Python 3.13.9; scikit-learn 1.8.0; pandas 3.0.6; NumPy 2.5.4; joblib 1.6.0; Streamlit 1.66.0.
- Original package list and successful pip check: [S6-1.png](screenshots/S6-1.png).
- Browser name/version, full screen resolution, viewport and zoom: not recorded. Cropped screenshots do not establish these values.
- [Supplementary environment record](environment-verified.md) was collected during evidence review, not presented as original setup output.
- Tests were performed manually by Jackie with step-by-step guidance. This is functional evidence, not an independent usability test.

## Results

S6-01 to S6-18 passed based on retained screenshots, logs and Jackie's case-by-case confirmations on 19 October 2026. The S6-11 Early-Warning missing-attendance check was retested on 20 October 2026 at the same tested commit. Where a screenshot does not show the entire operation, this report identifies the tester confirmation rather than claiming independent visual proof. No timing or usability pass is claimed. The earlier assisted 89-test run is not used here.

| Case / subcase | Input or fixture | Actual result | Status | Evidence link | Fix / retest link |
|---|---|---|---|---|---|
| S6-01 | Fresh clone at `9dc7132`; package check and full unit-test run | Python 3.13.9; `pip check` succeeded; 99 tests passed in 11.709 s. | Pass | [Setup screenshot](screenshots/S6-1.png), [test screenshot](screenshots/Issue-Unittest.png), [99-test log](logs/issue66-unittest.log) | N/A |
| S6-02 | Early-Warning; attendance 40, study hours 4, failures 0 | No grade needed. High Risk, 85.9%, with attendance support suggestion. | Pass | [Inputs](screenshots/S6-02-early-warning.png), [result](screenshots/S6-02-early-warning-result.png) | N/A |
| S6-03 | Confirmatory; attendance 80, study hours 4, failures 0, G1=8, G2 blank | G1-only model. High Risk, 81.8%, with assessment support suggestion. | Pass | [Inputs](screenshots/S6-03-g1-only.png), [result](screenshots/S6-03-g1-only-result.png) | N/A |
| S6-04 | Confirmatory; attendance 80, study hours 4, failures 0, G1=12, G2=0 | G1+G2 model. Zero was accepted as a real grade. High Risk, 99.6%. | Pass | [Inputs](screenshots/S6-04-g2-zero.png), [result](screenshots/S6-04-g2-zero-result.png) | N/A |
| S6-05 | S6-02/03/04 inputs plus Confirmatory G1=12/G2=14; [Early-Warning CSV](fixtures/S6-05-early.csv) and [Confirmatory CSV](fixtures/S6-05-confirmatory.csv) | Form, CLI and CSV labels/probabilities agreed at displayed precision: High Risk 0.859, High Risk 0.818 (`g1`), High Risk 0.996 (`g1_g2`) and Low Risk 0.003 (`g1_g2`). Form/CSV recommendation text agreed. | Pass | [CLI](screenshots/S6-05-cli.png), [G1/G2 form result](screenshots/S6-05-g1-g2-14-result.png), [Early-Warning CSV result](screenshots/S6-05-csv-early-result.png), [Confirmatory CSV result](screenshots/S6-05-csv-confirmatory-result.png) | N/A |
| S6-06 | Attendance 0, 100, -1 and 101 in the form and [mixed CSV](fixtures/S6-06-attendance.csv) | Form accepted 0/100 and rejected -1/101. CSV had 4 rows: 2 predicted, 2 skipped. Valid probabilities displayed as 100.0% and 52.4%. | Pass | [0 result](screenshots/S6-06-attendance-0-2.png), [100 result](screenshots/S6-06-attendance-100-2.png), [-1 error](screenshots/S6-06-attendance-minus1.png), [101 error](screenshots/S6-06-attendance-101.png), [CSV results](screenshots/S6-06-csv-attendance-result.png), [skipped rows](screenshots/S6-06-csv-attendance-skipped.png) | N/A |
| S6-07 | Study hours 0, 40, -1 and 41 in the form and [mixed CSV](fixtures/S6-07-study-hours.csv) | Form accepted 0/40 (both Low Risk, 28.4%) and rejected -1/41. CSV had 4 rows: 2 predicted, 2 skipped with study-hours reasons. | Pass | [0 result](screenshots/S6-07-study-0-result.png), [40 result](screenshots/S6-07-study-40-result.png), [-1 error](screenshots/S6-07-study-minus1-2.png), [41 error](screenshots/S6-07-study-41-2.png), [CSV results](screenshots/S6-07-csv-study-result.png), [skipped rows](screenshots/S6-07-csv-study-skipped.png) | N/A |
| S6-08 | Form dropdown and [CSV](fixtures/S6-08-failures.csv) with failures 0, 1, 2, 3, -1, 4 and 1.5 | Dropdown offered only 0–3. CSV accepted the four valid integers and skipped the three invalid values with reasons; 7 rows total, 4 predicted, 3 skipped. | Pass | [Dropdown](screenshots/S6-08-failures-dropdown.png), [CSV counts](screenshots/S6-08-csv-failures-result.png), [CSV reasons](screenshots/S6-08-csv-failures-result-3.png) | N/A |
| S6-09 | Confirmatory form grade boundaries and [mixed grade CSV](fixtures/S6-09-grades.csv) | G1 blank/-1/21/NA rejected; G1 0/20 accepted. G2 blank/0/20 accepted; G2 -1/21/NA rejected. CSV had 12 rows: 5 predicted, 7 skipped. Blank G2 used `g1`; supplied G2 used `g1_g2`. | Pass | [Blank G1](screenshots/S6-09-g1-blank-2.png), [G1=0](screenshots/S6-09-g1-0-result.png), [G1=20](screenshots/S6-09-g1-20-result.png), [G2=20](screenshots/S6-09-g2-20-result.png), [CSV results](screenshots/S6-09-csv-grades-result.png), [skipped rows](screenshots/S6-09-csv-grades-skipped.png) | N/A |
| S6-10 | Confirmatory upload of [sample_roster.csv](fixtures/sample_roster.csv) | Four rows: A/B predicted; C/D skipped for attendance and `G2=NA` reasons. Skipped rows received no prediction or recommendation. | Pass | [Results](screenshots/S6-10-sample-roster-result.png), [skipped rows](screenshots/S6-10-sample-roster-skipped.png) | N/A |
| S6-11 | `missing_g1_column.csv` in Confirmatory; `empty.csv`, `header_only.csv`; [missing-attendance fixture](fixtures/attendance_pct.csv) in Early-Warning | Each file produced a clear file-level error without invented predictions. The Early-Warning missing-attendance case was retested on 20 October 2026 at the same tested commit (`9dc7132dc0a1a735b508447b99f49b70afb84f6d`). | Pass | [Missing G1](screenshots/S6-11-missing-g1-column.png), [empty file](screenshots/S6-11-empty.png), [header-only file](screenshots/S6-11-header-only.png), [missing Early-Warning attendance](screenshots/S6-11-missing-attendance-ew.png) | N/A |
| S6-12 | Confirmatory upload of `dashboard_checks/all_invalid.csv` | Four rows total, none predicted, all four skipped with individual reasons; no valid result was invented. | Pass | [Counts](screenshots/S6-12-all-invalid-result.png), [skipped rows](screenshots/S6-12-all-invalid-skipped.png) | N/A |
| S6-13 | Confirmatory uploads of `extra_comma.csv`, `no_student_ids.csv`, `messy_headers.csv` and `unmatched_quote.csv` | Extra comma: 2 total/1 predicted/1 skipped. No IDs: 3 total/2 predicted/1 skipped, with rows 1 and 3 predicted. Messy headers: 1 predicted. Unmatched quote: clear file error. | Pass | [Extra-comma result](screenshots/S6-13-extra-comma-result.png), [extra-comma skipped row](screenshots/S6-13-extra-comma-skipped.png), [no-ID result](screenshots/S6-13-no-student-ids-result.png), [no-ID skipped row](screenshots/S6-13-no-student-ids-skipped.png), [messy headers](screenshots/S6-13-messy-headers-result.png), [unmatched quote](screenshots/S6-13-unmatched-quote.png) | N/A |
| S6-14 | Confirmatory upload of `project/data/issue56-duplicate-and-invalid.csv` | Five rows total: 2 predicted, 3 skipped. First `DUP` was G1-only High Risk, 81.8%; second `DUP` was G1+G2 Low Risk, 0.3%. Full messages stayed with their respective rows. | Pass | [Results](screenshots/S6-14-duplicate-result.png), [skipped rows](screenshots/S6-14-duplicate-skipped.png) | N/A |
| S6-15 | Download S6-14 results and compare the [export](exports/S6-14-duplicate-export.csv) with the dashboard | Export retained exactly two `DUP` rows in order, with their labels, decimal probabilities, grade setup and complete recommendations. Invalid rows were excluded. | Pass | [Export check](screenshots/S6-14-duplicate-check.png), [actual export](exports/S6-14-duplicate-export.csv) | N/A |
| S6-16 | Predict in Confirmatory; change attendance 80 to 81 and leave the field without predicting; predict again; switch to Early-Warning | Jackie confirmed that the old prediction and recommendations disappeared after the edit and after the mode switch. Saved after-edit screenshots show the later fresh 81.6% prediction, not the cleared intermediate state; the edit-clear result relies on tester confirmation. | Pass | [Before edit](screenshots/S6-16-before-edit.png), [after re-predicting](screenshots/S6-16-after-edit.png), [additional result](screenshots/S6-16-after-edit-2.png), [after mode switch](screenshots/S6-16-after-mode-switch.png) | N/A |
| S6-17 | Recommendation boundaries: attendance 60/60.1, study 1.5/1.6, failures 0/1; separate supplied High Risk check with previous score 49/50 | Rules triggered only at the approved boundaries. Assessment review appeared at score 49; at 50 the no-match fallback appeared. | Pass | [Rule-test screenshot](screenshots/S6-17-18-recommend-tests.png), [49/50 screenshot](screenshots/S6-17-score-49-50.png), [rule-test log](logs/issue66-recommend-tests.log), [49/50 log](logs/issue66-score-boundary.log) | N/A |
| S6-18 | `test_recommend.py`: all thresholds, no matching High Risk rule, Low Risk with thresholds, Early-Warning without grade | Eleven recommendation tests passed. Messages were unique and ordered; High Risk received fallback when no rule matched; Low Risk received routine guidance only; Early-Warning used no assessment rule. These 11 tests are included in the 99-test total, not additional unique tests. | Pass | [Test screenshot](screenshots/S6-17-18-recommend-tests.png), [rule-test log](logs/issue66-recommend-tests.log) | N/A |

## Boundary subcases

Other fields stayed valid while one input changed. Attendance, study-hour and failure checks used Early-Warning. Grade checks used Confirmatory with attendance 80, study hours 4 and failures 0. G1 checks left G2 blank; G2 checks used G1=12. Blank G2 and G2=0 form evidence is shared with S6-03/S6-04. Jackie explicitly confirmed the manual grade and failure checks; screenshots and saved CSV outcomes supplement that confirmation.

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
| S6-08-failures-0 | 0 | Offered by dropdown | Predicted | Pass |
| S6-08-failures-1 | 1 | Offered by dropdown | Predicted | Pass |
| S6-08-failures-2 | 2 | Offered by dropdown | Predicted | Pass |
| S6-08-failures-3 | 3 | Offered by dropdown | Predicted | Pass |
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

## Retained fixtures and exports

- S6-05: [Early-Warning input](fixtures/S6-05-early.csv), [Confirmatory input](fixtures/S6-05-confirmatory.csv), [Early-Warning export](exports/S6-05-early-export.csv) and [Confirmatory export](exports/S6-05-confirmatory-export.csv).
- S6-06: [Attendance input](fixtures/S6-06-attendance.csv) and [export](exports/S6-06-csv-Result.csv); 4 total/2 predicted/2 skipped.
- S6-07: [Study-hours input](fixtures/S6-07-study-hours.csv) and [export](exports/S6-07-study-hours-Result.csv); 4/2/2.
- S6-08: [Failure input](fixtures/S6-08-failures.csv); 7/4/3.
- S6-09: [Grade input](fixtures/S6-09-grades.csv) and [export](exports/S6-09-csv-grad.csv); 12/5/7.
- S6-10: [Retained roster](fixtures/sample_roster.csv) and [export](exports/S6-10-sample-roster-data.csv); 4/2/2.
- S6-11: [Missing-attendance input](fixtures/attendance_pct.csv). Despite its filename, it intentionally omits the attendance column.
- S6-11/12/13: unchanged repository fixtures in [dashboard_checks](../../../../../data/dashboard_checks): `missing_g1_column.csv`, `empty.csv`, `header_only.csv`, `all_invalid.csv`, `extra_comma.csv`, `no_student_ids.csv`, `messy_headers.csv` and `unmatched_quote.csv`.
- S6-14/15: [Repository duplicate-ID input](../../../../../data/issue56-duplicate-and-invalid.csv) and [actual downloaded export](exports/S6-14-duplicate-export.csv). The export and spreadsheet screenshot retain their original S6-14 filenames but also establish S6-15.
- The [evidence inventory](evidence-inventory.md) lists retained artifacts with source filenames and SHA-256 hashes.

## Commands

These commands describe the original run. Logs are retained without modification. The working directory was the fresh `ICT304-issue66-check` clone.

```sh
.venv/bin/python --version
.venv/bin/python -m pip check
.venv/bin/python -m pip list
.venv/bin/python -m unittest discover -s project/code -v 2>&1 | tee issue66-unittest.log
.venv/bin/python -m streamlit run project/code/dashboard.py
.venv/bin/python project/code/predict.py --mode early_warning --attendance 40 --study-hours 4 --failures 0
.venv/bin/python project/code/predict.py --mode confirmatory --attendance 80 --study-hours 4 --failures 0 --g1 8
.venv/bin/python project/code/predict.py --mode confirmatory --attendance 80 --study-hours 4 --failures 0 --g1 12 --g2 0
.venv/bin/python project/code/predict.py --mode confirmatory --attendance 80 --study-hours 4 --failures 0 --g1 12 --g2 14
.venv/bin/python -m unittest discover -s project/code -p "test_recommend.py" -v 2>&1 | tee issue66-recommend-tests.log
```

CLI output is retained in [S6-05-cli.png](screenshots/S6-05-cli.png): High Risk 0.859, High Risk 0.818, High Risk 0.996 and Low Risk 0.003. CLI comparisons concern labels and probabilities, not recommendation text.

The additional score test directly called `recommend` with `High Risk`, mode `confirmatory`, attendance 80, study hours 4, failures 0 and `previous_score` 49 then 50. It asserted exactly one Assessment review message at 49 and `[NO_MATCH_MESSAGE]` at 50. [Its screenshot](screenshots/S6-17-score-49-50.png) contains the command and assertions; [its log](logs/issue66-score-boundary.log) ends `ALL CHECKS PASSED`.

## Record notes and follow-up

- No application failure was reported during the guided functional run. Invalid-input errors were expected outcomes, not defects.
- Initial CSV preparation accidentally used RTF. Jackie corrected the input to plain CSV before the recorded successful uploads. That preparation error was not a model or application failure.
- S6-11 was initially attempted in Confirmatory and reported missing attendance and G1. The original `S6-11-missing-attendance.png` preserves that attempt; `S6-11-missing-attendance-ew.png` is the corrected Early-Warning screenshot sent at 17:35:40 and recovered from the original attachment.
- S6-16: `S6-16-after-edit.png` and `S6-16-after-edit-2.png` show a fresh 81.6% prediction at attendance 81, not the empty state before re-predicting. Do not use them alone to prove stale-result clearance. During evidence review Jackie explicitly reconfirmed that the old result disappeared first and these screenshots were taken after pressing Predict again. The input-change pass relies on that confirmation; the mode-switch screenshot shows the Early-Warning form without a result.
- Original filenames and image bytes are retained. Duplicate or overlapping screenshots are kept for traceability. No screenshots were regenerated or edited.
- Original logs are the 99-test run (11.709 s), the separate 11-rule-test run and the exact 49/50 check. The 11 tests are already part of the 99.
- S6-19 to S6-24 remain outside this functional record. Missing browser or viewport metadata must not be turned into a readability or timing pass.
- Windows evidence remains separate and unchanged. Issue #66 closure and combined review are not performed by this evidence preparation.
