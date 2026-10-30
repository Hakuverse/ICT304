# Issue 116 Windows results

Tester: Anna

Actual test date: 30 October 2026

OS/build/processor: Windows 11 Home 25H2, OS Build 26200.9711 (x64); Intel Core Ultra 5 125H (developer laptop, same device as #114)

Browser/version: Microsoft Edge (default browser), 156.0.4314.50 as recorded on 29 October; not rechecked on 30 October

Package filename / SHA-256 / source commit: `SARAH-0.1.0-preview-windows-x64-ab4a604.zip` / `8828121aa9b343c07138657f6d827df168d33211782204fd5b019bf2577f4bc2` / `ab4a604a71ecef9f0585a137a014e7dd6fb861e2`. Same extracted package as #114 (SARAH.exe SHA-256 matched build-info.json on 29 October); not redownloaded.

Expected candidate: ab4a604; matches.

Test input files: repository ZIP of branch `issue116-packaged-workflow` (commit 8619bfb), `project/data/app116/`, extracted to the Downloads folder.

Reviewer/date: pending

Checked against the [run sheet](../../../../app-workflow-testing.md). A01-A05 reuse the [existing platform record](../../windows/results.md); they are not new runs. SARAH uses bundled Python 3.12.10.

| Case | Actual outcome | Evidence / exact observations |
|---|---|---|
| A01 | Reused existing evidence (not re-run) | [Windows record](../../windows/results.md) W01-W04: package identity and hashes, SmartScreen "Unknown publisher" then Run anyway, Edge opened automatically, "SARAH is already open" on repeat launch |
| A02 | Reused existing evidence (not re-run) | W05: Early-Warning 40/4/0, High Risk 85.9%, attendance support. Also seen again during D01 on 30 October |
| A03 | Reused existing evidence (not re-run) | W06: Confirmatory 80/40/0/G1 12/G2 blank, High Risk 66.1%, G1 only, study-hours warning, general staff review |
| A04 | Reused existing evidence (not re-run) | W07: sample_roster.csv (2 predicted, 2 skipped with fixes, Low-Risk routine guidance, G1 and G1+G2 routing) and study_hours_warning_demo.csv export with the warning |
| A05 | Reused existing evidence (not re-run) | W08 offline prediction, W09 Quit/restart; routine startup 13.20 s after reboot (post-approval), then 11.15, 6.46 and 4.35 s. The first downloaded launch (74.67 s including SmartScreen) is recorded separately |
| B01 | Pass | G2 blank: Low Risk 9.2%, G1 only, routine guidance. G2 0: High Risk 99.6%, G1 + G2, assessment review. G2 14: Low Risk 0.3%, G1 + G2, routine guidance. Zero not treated as blank. [B01-g2-blank.png](screenshots/B01-g2-blank.png), [B01-g2-zero.png](screenshots/B01-g2-zero.png), [B01-g2-14.png](screenshots/B01-g2-14.png) |
| B02 | Pass | Six subcases below. [B02-g1-required.png](screenshots/B02-g1-required.png) (blank), [B02-g1-range.png](screenshots/B02-g1-range.png) (-1) |
| B03 | Pass | Four subcases below. [B03-g2-invalid.png](screenshots/B03-g2-invalid.png) (NA), extra [B03-g2-minus1.png](screenshots/B03-g2-minus1.png) (-1) |
| B04 | Pass | Four subcases below. [B04-attendance-invalid.png](screenshots/B04-attendance-invalid.png) (-1), extra [B04-attendance-101.png](screenshots/B04-attendance-101.png). Typing and the -/+ buttons both worked; typed values were not blocked or changed |
| B05 | Pass | Three subcases below. [B05-study-invalid.png](screenshots/B05-study-invalid.png) (-1). Restored to 4: Low Risk 9.2% G1 only, matching B01 |
| B06 | Pass | Dropdown offers only 0, 1, 2, 3 ([B06-failures-dropdown.png](screenshots/B06-failures-dropdown.png), captured with Win + PrtScn because the dropdown closes when Snipping Tool opens). Each accepted, see subcases |
| B07 | Pass | Study 12: Low Risk 16.3%, G1 only, no study warning, routine guidance ([B07-study-12.png](screenshots/B07-study-12.png)). Study 12.5 (box shows 12.50, not clipped): Low Risk 16.9%, G1 only, full study-hours warning shown despite Low Risk, routine guidance ([B07-study-12-5.png](screenshots/B07-study-12-5.png)). Support text and warning agree with the inputs |
| B08 | Pass | Before: Confirmatory 80/4/0/G1 12/G2 blank, Low Risk 9.2% ([B08-before.png](screenshots/B08-before.png)). Attendance changed to 79 and Tab, no Predict: the old risk, probability and suggestions disappeared ([B08-input-change.png](screenshots/B08-input-change.png); the area below Predict is outside the image, so this part is tester-confirmed). Predicted again with 79 and saw a new result, then switched to Early-Warning: the result disappeared and G1/G2 fields were hidden ([B08-mode-change.png](screenshots/B08-mode-change.png)) |
| B09 | Pass | Early-Warning 80/4/0: Low Risk 28.4%, no G1/G2 fields, routine guidance ([B09-early-warning-form.png](screenshots/B09-early-warning-form.png)). Switched back to Confirmatory: G1 and G2 reappeared empty; Predict gave "Please fix the input: G1 is required in Confirmatory mode" with no old result ([B09-back-to-confirmatory.png](screenshots/B09-back-to-confirmatory.png)) |
| C01 | Pass | `all-invalid.csv`: Rows 2, Predicted 0, Skipped 2. "No valid students to process. See the skipped rows below." A: "Attendance is 101. Enter a value from 0 to 100." B: "Study hours is 41. Enter a value from 0 to 40." No results table or download button. [C01-all-invalid.png](screenshots/C01-all-invalid.png) |
| C02 | Pass | `missing-g1-column.csv`: "This file cannot be processed: Missing required columns: G1". No results table or download. [C02-missing-column.png](screenshots/C02-missing-column.png) |
| C03 | Pass | `empty.csv` (0.0 B): the browser accepted the zero-byte upload. "This file cannot be processed: The CSV contains no students." No results or download. [C03-empty.png](screenshots/C03-empty.png) |
| C04 | Pass | `header-only.csv`: "This file cannot be processed: The CSV contains no students." No results or download. [C04-header-only.png](screenshots/C04-header-only.png) |
| C05 | Pass | `duplicate-ids.csv`: Rows 2, Predicted 2, Skipped 0. Both SAME rows kept in order: High Risk 88.9% g1 (attendance support and assessment review), then Low Risk 0.3% g1_g2 (routine guidance). Neither overwrote the other. Downloaded and opened: [C05-results.csv](exports/C05-results.csv) has the expected columns, decimals 0.889 and 0.003, and matches the source reference exactly. [C05-duplicate-ids.png](screenshots/C05-duplicate-ids.png) |
| C06 | Pass | `study-boundaries.csv`: Rows 4, Predicted 3, Skipped 1. Messages: "1 of 4 students was skipped", "2 predicted student(s) have study hours above 12"; full warning once above the table. H12 Low 16.3% no warning; H12_5 Low 16.9% "Yes - see warning above"; H40 High 66.1% "Yes - see warning above", general staff review; H41 skipped ("Study hours is 41. Enter a value from 0 to 40."). [C06-results.csv](exports/C06-results.csv): decimals 0.163/0.169/0.661, warning text only on H12_5 and H40, H41 not exported; matches the source reference exactly. [C06-study-boundaries.png](screenshots/C06-study-boundaries.png) |
| C07 | Pass | `invalid-failures.csv`: Rows 3, Predicted 0, Skipped 3. "No valid students to process." FNEG -1, FFRACTION 1.5 and F4 4 each "Enter a whole number from 0 to 3". No download. [C07-invalid-failures.png](screenshots/C07-invalid-failures.png) |
| C08 | Pass | With the C06 table and download showing, `missing-g1-column.csv` was uploaded next (tester-confirmed order), then `header-only.csv`. Each time the previous table and Download results button disappeared and only the current file's error was shown. Evidence: [C02-missing-column.png](screenshots/C02-missing-column.png), [C04-header-only.png](screenshots/C04-header-only.png) |
| D01 | Pass | `py -3.12 project\data\app116\hold_port.py` failed with "No suitable Python runtime found" (Python 3.12 not installed). Used `py project\data\app116\hold_port.py` (installed Python 3.14.7; used only for the helper): "Held localhost port: 8501". SARAH.exe was then double-clicked: launcher Ready, dashboard opened on 127.0.0.1:49337 (different port), Early-Warning 40/4/0 gave High Risk 85.9% with attendance support. Quit SARAH, then Enter in the helper returned to the prompt. Original D01 screenshot reviewed locally; not published because terminal paths contain a personal computer username. The result above is retained from Anna's written record and the reviewed image. A privacy-safe replacement can be added later. |

## Boundary subcases

Base input unless stated: Confirmatory, One student, attendance 80, study 4, failures 0, G1 12, G2 blank.

| Case | Input | Actual outcome |
|---|---|---|
| B02 | G1 blank | "Please fix the input: G1 is required in Confirmatory mode"; no prediction |
| B02 | G1 -1 | "Please fix the input: G1 must be 0 to 20"; no prediction |
| B02 | G1 21 | "Please fix the input: G1 must be 0 to 20"; no prediction |
| B02 | G1 NA | "Please fix the input: G1 must be a number from 0 to 20"; no prediction |
| B02 | G1 0 | Accepted: High Risk 100.0%, G1 only, assessment review |
| B02 | G1 20 | Accepted: Low Risk 0.0%, G1 only, routine guidance |
| B03 | G2 -1 | "Please fix the input: G2 must be a finite number from 0 to 20"; no prediction |
| B03 | G2 21 | "Please fix the input: G2 must be a finite number from 0 to 20"; no prediction |
| B03 | G2 NA | "Please fix the input: G2 must be a number from 0 to 20"; no prediction; not treated as blank |
| B03 | G2 20 | Accepted: Low Risk 0.0%, G1 + G2, routine guidance |
| B04 | attendance -1 | "Please fix the input: attendance_pct must be 0 to 100"; no prediction |
| B04 | attendance 101 | "Please fix the input: attendance_pct must be 0 to 100"; no prediction |
| B04 | attendance 0 | Accepted: Low Risk 24.1%, G1 only |
| B04 | attendance 100 | Accepted: Low Risk 7.1%, G1 only |
| B05 | study -1 | "Please fix the input: study_hours must be 0 to 40"; no prediction |
| B05 | study 41 | "Please fix the input: study_hours must be 0 to 40"; no prediction |
| B05 | study 0 | Accepted: Low Risk 6.8%, G1 only |
| B06 | failures 0 | Low Risk 9.2%, G1 only |
| B06 | failures 1 | Low Risk 12.1%, G1 only |
| B06 | failures 2 | Low Risk 15.8%, G1 only |
| B06 | failures 3 | Low Risk 20.3%, G1 only |

Accepted boundary values are recorded as observed; no expected probabilities were assumed for them.
B06 results were all Low Risk, so routine guidance was shown (failure-based suggestions are High-Risk only).

## Failures, assistance and retests
No application failures or application retests reported. The initial helper command was unavailable, as recorded below. The tester followed the run sheet with step-by-step guidance from an AI assistant (Claude) and performed every action on her own laptop; results are her own observations and screenshots.
Deviation: the run sheet's `py -3.12` command was unavailable, so the helper ran on installed Python 3.14.7 (D01).

Observations for team review (not failures):
- Single-student error messages use internal names (`attendance_pct`, `study_hours`) rather than the form labels.
- G1 and G2 range messages are worded differently ("G1 must be 0 to 20" versus "G2 must be a finite number from 0 to 20"); "finite" may be unclear to users.
- The empty file and header-only file give the same message ("The CSV contains no students.").
- Streamlit's "Deploy" button remains visible (also noted in #114).

## Completion
All B, C and D checks passed on this device; A01-A05 reuse #114 evidence. Pending review.
Developer laptop with Python installed; no clean-machine or tutor-device claim.

Evidence check, 30 October 2026: both exported CSVs were compared field by field with [source-reference.json](../source-reference.json), including row order, decimal probabilities, recommendations and warnings. Both matched. This comparison does not replace the device test or team approval.
