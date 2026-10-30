# Issue 116 macOS results

Tester: Jackie

Actual test dates: 29 October 2026 (B01-C08); 30 October 2026 (D01 follow-up)

OS/build/processor: macOS Tahoe 26.6.2, build 25G83, Apple M3 (arm64)

Browser: Google Chrome 152.0.7977.75 (arm64)

Package: `SARAH-0.1.0-preview-macos-arm64-ab4a604.zip`

ZIP SHA-256: `0996cc189a435d1e1a4509a7fd754cdcf7366a36fed8a5cdb8c173fa4fedf875`

Package source: `ab4a604a71ecef9f0585a137a014e7dd6fb861e2`

SARAH runtime: bundled Python 3.12.10; the Mac's installed Python is not used to run SARAH.

Reviewer/date: pending

This record summarises Jackie's supplied test document, screenshots and downloaded CSVs against the [run sheet](../../../../app-workflow-testing.md). Pass means Jackie reported the case passed. Screenshots support the states they show; they do not prove every action between captures. A01-A05 reuse the [earlier macOS package record](../../macos/results.md).

| Case | Outcome | Actual record / evidence |
|---|---|---|
| A01 | Reused | M01-M04: package identity, first-open security steps, ready dashboard and repeat launch. Not a new run. |
| A02 | Reused | M05: Early-Warning 40/4/0, High Risk 85.9%, attendance support. |
| A03 | Reused | M06: G1-only 80/40/0/G1=12, High Risk 66.1%, study warning and general review. |
| A04 | Reused | M07: mixed CSV, grade routing, Low-Risk guidance and study-warning export. |
| A05 | Reused | M08-M09: offline, Quit/restart. Routine startup 6.72/4.29/3.64/3.58 seconds; first security-prompt launch was not timed. |
| B01 | Pass | G2 blank: Low Risk 9.2%, g1. G2 0: High Risk 99.6%, g1_g2. G2 14: Low Risk 0.3%, g1_g2. Zero is not treated as blank. |
| B02 | Pass, tester-reported subcases | G1 blank, -1, 21 and NA rejected; 0 and 20 accepted. Selected images show blank, -1 and NA. The supplied image named B02-g1-21 actually shows -1, so it is renamed B02-g1-minus1. G1=21 remains tester-reported, not visually evidenced by that image. |
| B03 | Pass, tester-reported subcases | G2 -1, 21 and NA rejected; 20 accepted. Selected image shows -1 and the range error. |
| B04 | Pass, tester-reported subcases | Attendance -1 and 101 rejected; 0 and 100 accepted. Selected image shows -1 and the range error. |
| B05 | Pass, tester-reported subcases | Study hours -1 and 41 rejected; 0 accepted. Selected image shows -1 and the range error. |
| B06 | Pass | Dropdown offers 0, 1, 2 and 3. Jackie reports each accepted. |
| B07 | Pass | Study 12: Low Risk 16.3%, no study warning. Study 12.5: Low Risk 16.9%, warning shown. Jackie also reports 40 accepted with warning and 41 rejected; C06 export supports these two boundaries. |
| B08 | Pass | Before image shows Low Risk 9.2%. After attendance changed to 79, no previous result is shown below the form. Mode-change image shows Early-Warning fields without the previous result. Jackie reports the run-sheet sequence passed. |
| B09 | Pass | Early-Warning 80/4/0 shows Low Risk 28.4%. Returning to Confirmatory shows empty G1/G2 fields and no previous result. The required-G1 check is also covered by B02. |
| C01 | Pass | All-invalid file: 2 rows, 0 predicted, 2 skipped; attendance 101 and study 41 errors. |
| C02 | Pass | Missing-column file rejected: Missing required columns: G1. |
| C03 | Pass | Zero-byte file accepted for upload, then rejected: The CSV contains no students. |
| C04 | Pass | Header-only file rejected: The CSV contains no students. |
| C05 | Pass | Both SAME rows retained in order: High Risk 0.889/g1 with attendance and assessment support, then Low Risk 0.003/g1_g2 with routine guidance. Downloaded CSV matches the reference in every field. |
| C06 | Pass | 4 rows, 3 predicted, 1 skipped. Export: H12 Low 0.163 without warning; H12_5 Low 0.169 and H40 High 0.661 with full warning text. H41 rejected and absent from export. H40 has general review guidance. |
| C07 | Pass | 3 rows, 0 predicted, 3 skipped. Failures -1, 1.5 and 4 rejected with whole-number 0-to-3 messages. |
| C08 | Pass, tester-reported sequence | Jackie reports the replacement-file case passed. Selected image shows missing-G1 error without the previous result table/download; C04 shows the header-only error. The full replacement order is supported by the written case confirmation, not a continuous recording. |
| D01 | Pass, 30 October follow-up | Helper held localhost port 8501; SARAH opened on port 64211 and predicted Early-Warning 40/4/0 as High Risk 85.9%, with attendance support. Screenshots confirm the ports and prediction; Benjamin relayed Jackie's confirmation that D01 passed. See follow-up below. |

## Screenshots and exports

The focused screenshots below retain their original contents. Additional context and boundary captures remain in the supplied local folder. A separate screenshot is not required for each subcase when the written record states what was checked; those subcases remain clearly labelled as tester-reported.

- [B01-g2-14.png](screenshots/B01-g2-14.png)
- [B01-g2-blank.png](screenshots/B01-g2-blank.png)
- [B01-g2-zero.png](screenshots/B01-g2-zero.png)
- [B02-g1-minus1.png](screenshots/B02-g1-minus1.png)
- [B02-g1-na.png](screenshots/B02-g1-na.png)
- [B02-g1-required.png](screenshots/B02-g1-required.png)
- [B03-g2-invalid.png](screenshots/B03-g2-invalid.png)
- [B04-attendance-invalid.png](screenshots/B04-attendance-invalid.png)
- [B05-study-invalid.png](screenshots/B05-study-invalid.png)
- [B06-failures-dropdown.png](screenshots/B06-failures-dropdown.png)
- [B07-study-12-5.png](screenshots/B07-study-12-5.png)
- [B07-study-12.png](screenshots/B07-study-12.png)
- [B08-before.png](screenshots/B08-before.png)
- [B08-input-change.png](screenshots/B08-input-change.png)
- [B08-mode-change.png](screenshots/B08-mode-change.png)
- [B09-confirmatory-switch-cleared.png](screenshots/B09-confirmatory-switch-cleared.png)
- [B09-early-warning-result.png](screenshots/B09-early-warning-result.png)
- [C01-all-invalid.png](screenshots/C01-all-invalid.png)
- [C02-missing-column.png](screenshots/C02-missing-column.png)
- [C03-empty.png](screenshots/C03-empty.png)
- [C04-header-only.png](screenshots/C04-header-only.png)
- [C05-duplicate-ids-2.png](screenshots/C05-duplicate-ids-2.png)
- [C06-study-boundaries-result.png](screenshots/C06-study-boundaries-result.png)
- [C06-study-boundaries.png](screenshots/C06-study-boundaries.png)
- [C07-invalid-failures.png](screenshots/C07-invalid-failures.png)
- [C08-stale-results-cleared.png](screenshots/C08-stale-results-cleared.png)

Exports: [C05-results.csv](exports/C05-results.csv) and [C06-results.csv](exports/C06-results.csv).

Evidence check, 30 October 2026: both exports match [source-reference.json](../source-reference.json) field by field, including row order, decimal probabilities, grade setup, recommendations and warning text. All seven supplied input CSVs match the shared fixtures when parsed as CSV. The local missing-column filename had an extra space before `.csv`; its name was corrected without changing its contents. The C06 export was renamed from `C06-study-boundaries-result.csv` to `C06-results.csv`.

## Failures, assistance and retests

Jackie reported no failures for B01-C08 and no fix/retest. Assistance was not recorded in the supplied document. D01 was not tested in the original 29 October record; the 30 October follow-up below records its completion. This was a developer computer; no clean-machine or tutor-device claim is made.

## D01 follow-up - 30 October 2026

Jackie completed the previously outstanding occupied-port check. Benjamin supplied four screenshots and confirmed that Jackie's D01 passed.

- The terminal screenshot shows `python3 project/data/app116/hold_port.py` holding localhost port **8501**.
- The combined screenshot shows the helper still holding 8501 while SARAH's browser dashboard uses **64211**.
- Early-Warning inputs were attendance **40**, study hours **4**, failures **0**.
- The result is **High Risk, 85.9%**, with attendance support, matching the expected output.
- Completion of the full D01 procedure, including quitting SARAH and releasing the helper port, is recorded from the relayed pass confirmation. These final cleanup actions are not shown in the screenshots.

Public evidence: [form and app port](screenshots/D01-occupied-port-form.png) and [prediction and attendance support](screenshots/D01-occupied-port-result.png).

The original `D01-terminal-port.png` and `D01-occupied-port.png` were reviewed locally. They show the held port and simultaneous operation, but contain a personal computer username and path, so they remain in the supplied local folder rather than the public repository. No screenshot content was changed. The public images show a loopback-only session address from this test, not a hosted service address.

This is a follow-up to the same package test record, not a new build or a repeat of B01-C08. The helper uses installed Python; SARAH uses bundled Python 3.12.10.

## Completion

B01-C08 and the D01 follow-up are recorded as passed; A01-A05 reuse the earlier record. Ready for team review and approval in PR #122. Close #116 after the reviewed PR is merged.
