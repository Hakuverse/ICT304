# Packaged application workflow checks (#116)

Anna tests Windows; Jackie tests macOS. Benjamin collects the records.
Current results are in the [evidence summary](evidence/app/issue116/README.md).
Windows and macOS B01-B09, C01-C08 and D01 are recorded as passed.
The macOS D01 follow-up was completed on 30 October; Anna approved PR #122 on 30 October; it is merged and #116 is closed.

The Windows port helper uses an installed Python 3 via `py`; it does not require
a separately installed Python 3.12. SARAH itself uses its bundled runtime.

This is the retained run sheet for the completed #116 checks. Normal app users
can follow the [user guide](user-guide.md) directly. The steps below are for
reproducing a test, not unfinished acceptance work.

## 1. Get ready

Use the same ab4a604 package tested in #114/#115, from Actions run 40556703379.
Keep its ZIP, checksum and build-info.json. Do not download another binary just
because it is newer. Both applications use bundled Python 3.12.10.

The test fixtures were merged in PR #122. Download the repository source ZIP
through **Code > Download ZIP**, or update your checkout. The input files are
in `project/data/app116/`. They are uploaded into the existing app; they do not
replace anything in the app folder. Do not download a GitHub HTML preview as CSV.

Open SARAH normally. Record any follow-up run separately in the platform record at
`project/docs/evidence/app/issue116/windows/results.md` or `macos/results.md`.
Retain the existing results; add the actual follow-up date and package details. Use only fictional students.

## 2. Reuse completed evidence

| Case | Coverage | Windows | macOS |
|---|---|---|---|
| A01 | Package identity, launch/security, browser opening, repeat launch | W01-W04 | M01-M04 |
| A02 | Early-Warning 40/4/0: High Risk 85.9%, attendance support | W05 | M05 |
| A03 | G1-only 80/40/0/G1=12: High Risk 66.1%, warning, general review | W06 | M06 |
| A04 | Mixed roster, Low-Risk guidance, grade routing and warning export | W07 | M07 |
| A05 | Offline, Quit/restart and routine startup timings | W08-W09 and timing follow-up | M08-M09 and timings |

Link the [Windows record](evidence/app/windows/results.md) and
[Mac record](evidence/app/macos/results.md). These are existing results, not new runs.
Windows routine times are 13.20/11.15/6.46/4.35 seconds; Mac times are
6.72/4.29/3.64/3.58. Retain initial security-prompt launches separately.
Anna approved PR #121, which merged as b7218af on 29 October.

## 3. Form checks

For B01-B09 start in **Confirmatory > One student** with attendance **80**,
study hours **4**, failures **0**, G1 **12**, G2 **blank**.
Change only the specified field, press **Predict**, record the outcome, then
restore that field before the next subcase. Finish typing and press Tab to apply
a field change before checking whether old results disappeared.

| Case | Action | Expected result | Screenshot name |
|---|---|---|---|
| B01 | G2 blank, then G2 0, then G2 14; predict each time | Blank: Low Risk 9.2%, G1 only. Zero: High Risk 99.6%, G1+G2, assessment-review support. 14: Low Risk 0.3%, G1+G2, routine guidance. Zero must not be treated as blank. | B01-g2-blank.png, B01-g2-zero.png, B01-g2-14.png |
| B02 | G1 blank, -1, 21, NA, then valid 0 and 20 (G2 blank) | First four rejected with a useful G1 error and no current prediction. 0 and 20 accepted with G1-only routing. | B02-g1-required.png and B02-g1-range.png; record all six subcases in text |
| B03 | Keep G1 12; G2 -1, 21, NA, then 20 | First three rejected, not silently changed to blank. 20 accepted as G1+G2. Blank/0 already covered in B01. | B03-g2-invalid.png; record each subcase |
| B04 | Attendance -1, 101, then 0 and 100 | Invalid values rejected; endpoints accepted. Restore 80. | B04-attendance-invalid.png; record all four |
| B05 | Study hours -1, 41, then 0 | Negative and 41 rejected, 0 accepted. Restore 4. | B05-study-invalid.png; record all three |
| B06 | Open failures dropdown; select 0, 1, 2, 3 and predict each | Only whole numbers 0-3 offered; each accepted. Invalid CSV values tested below. | B06-failures-dropdown.png |
| B07 | Study hours 12, then 12.5; predict both | 12: Low Risk 16.3%, no study warning. 12.5: Low Risk 16.9%, full warning despite Low Risk. No clipping to 12. | B07-study-12.png, B07-study-12-5.png |
| B08 | Produce B01 blank result, then change attendance to 79 without Predict | Old risk, probability and suggestions disappear. Predict again, then switch to Early-Warning: old results disappear again. | B08-before.png, B08-input-change.png, B08-mode-change.png |
| B09 | In Early-Warning use 80/4/0 and predict; check no G1/G2 fields | Prediction works without grades. Switch back to Confirmatory and confirm G1 required. Do not count an old result as a new prediction. | B09-early-warning-form.png |

For accepted boundary values, record acceptance and routing; do not invent expected
probabilities. Exact checked comparisons are B01/B07 and the source reference.
For B01/B07 record whether support text and the study warning agree with the inputs.
The warning is a caution, not a change to the input or a reason to clip it.

## 4. CSV checks

Choose **Confirmatory > Class CSV** for every case below. Upload each file from
`project/data/app116/`. Remove/replace the previous upload each time.

| Case | File | Expected result | Evidence |
|---|---|---|---|
| C01 | all-invalid.csv | 2 rows, 0 predicted, 2 skipped; no valid students message, attendance and study errors; no results download | C01-all-invalid.png |
| C02 | missing-g1-column.csv | Missing required G1 column error; no current results/download | C02-missing-column.png |
| C03 | empty.csv | No students/file-empty error; no result/download. If the browser refuses a zero-byte upload, record that actual behaviour rather than Pass for the dashboard check. | C03-empty.png |
| C04 | header-only.csv | No students error; no result/download | C04-header-only.png |
| C05 | duplicate-ids.csv | 2 predicted, 0 skipped. Both SAME rows retained in order: High Risk 88.9% G1, then Low Risk 0.3% G1+G2. First has attendance and assessment support; second routine guidance. Neither row overwrites the other. | C05-duplicate-ids.png plus C05-results.csv |
| C06 | study-boundaries.csv | 4 total, 3 predicted, 1 skipped. H12: 16.3% no warning; H12_5: 16.9% warning; H40: 66.1% warning; H41 rejected. Two affected rows marked and one full warning above the table. | C06-study-boundaries.png plus C06-results.csv |
| C07 | invalid-failures.csv | 3 total, 0 predicted, 3 skipped: -1, 1.5 and 4 are invalid failures | C07-invalid-failures.png |
| C08 | After C05/C06, replace with C02 then C04 | Previous successful table and download disappear; the current file's error is shown | Can reuse C02/C04 screenshots if captured in this order |

For C05/C06, click Download results as CSV and open the saved file.
Check `student_id, risk_label, probability_high_risk, grade_setup, input_warning,
recommendations`. Probabilities are decimals (0.163, not 16.3); only valid rows
are exported. C06 warning text must stay on H12_5/H40 only. Keep CSV files.
The [source reference](evidence/app/issue116/source-reference.json) contains the
full expected rows and recommendations, generated from matching source code.
It is not evidence that either packaged application passed.

## 5. Occupied-port check (D01)

This is a technical check on each tester's developer computer. Installed Python
is used only to occupy a port, not to run SARAH.

1. Quit SARAH. Open a terminal in the downloaded repository folder.
2. Windows: `py project/data/app116/hold_port.py`.
   Mac: `python3 project/data/app116/hold_port.py`.
3. Keep that terminal open. It reports the occupied localhost port (normally
   8501; if already occupied it reserves another available port).
4. Double-click the packaged SARAH application. Confirm Ready and a working
   prediction while the other port remains occupied.
5. Record both the held port and SARAH browser port. They should differ.
   Capture D01-occupied-port.png with the helper message and Ready/dashboard
   visible; hide unrelated personal details.
6. Quit SARAH; return to the helper and press Enter to release its port.

The launcher requests an available port rather than assuming 8501. This check
covers starting alongside an occupied port, not every possible port race.
If the helper cannot start, record the error and ask Benjamin; do not change
firewall settings. The existing automated port-selection test is supporting
source evidence, not a substitute for both platform results.

## 6. Finish the evidence

Save screenshots and CSVs in your platform folder under
`project/docs/evidence/app/issue116/`. Each platform already has a results.md.
Record each boundary subcase, not only the pictured example. One image can cover
multiple cases only if their outcomes are visible. Text is sufficient for
unpictured subcases if it states what was tested and what happened.

Do not tick Pass in advance. Record failures and any assistance honestly.
Send the folder to Benjamin or add it in a follow-up evidence PR.
Both platform records were reviewed by Anna and merged in PR #122 on 30 October;
#116 is closed. The later #117 walkthrough was reviewed in PR #123. Publication
is recorded under #118; none of these updates changes the original test results.
