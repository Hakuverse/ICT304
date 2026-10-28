# macOS package results

Tester: Jackie. Test date: 28 October 2026. Recorded from Jackie's supplied notes,
screenshots and fictional CSV exports. Peer review is pending.

## Environment and package

| Detail | Actual record |
|---|---|
| OS / processor | macOS Tahoe 26.6.2 (25G83), Apple M3, as reported by Jackie |
| Browser | Google Chrome 152.0.7977.75 (Official Build, arm64) |
| Outer download | SARAH-macos-arm64-4.zip |
| Inner package | SARAH-0.1.0-preview-macos-arm64-ab4a604.zip |
| Inner ZIP SHA-256 | `0996cc189a435d1e1a4509a7fd754cdcf7366a36fed8a5cdb8c173fa4fedf875` |
| Source | `ab4a604a71ecef9f0585a137a014e7dd6fb861e2` |
| Build | [Actions run 40556703379](https://github.com/Hakuverse/ICT304/actions/runs/40556703379) |
| Installation location | Desktop folder named SARAH package test, outside the repository, with spaces in the path |
| Python installed / developer computer | Yes: Python 3.13.3 / yes. Benjamin confirmed the installed version on 28 October 2026 to resolve the conflicting versions in the notes. This is not the bundled runtime version. |
| Download security | Gatekeeper initially blocked SARAH; Jackie used the app-specific Open Anyway option, then the launcher and browser opened. |

Jackie reported a matching package checksum. The archive and build-info/checksum
files were not included in this evidence submission, so this record does not
claim a separate verification of his downloaded archive. Retain those files
with the original test package.

## Results

Use the [package testing guide](../../../app-package-testing.md).

| Case | Actual result | Evidence / help needed |
|---|---|---|
| M01 Platform and extraction | Pass, reported. Extracted outside the repository into a path with spaces; package files present. | [Test folder](screenshots/M01-test-folder.png), [outer files](screenshots/M01-extracted-download.png), [app contents](screenshots/M01-package-contents.png). |
| M02 Downloaded Finder launch | Launch successful after a security exception; needs peer review as an unsigned-app limitation. Initial launch was blocked, not warning-free. | [Gatekeeper block](screenshots/M02-gatekeeper-block.png), [Open Anyway confirmation](screenshots/M02-open-anyway-confirmation.png), then M03. |
| M03 Ready and startup timing | Pass, reported. Launcher Ready, browser opened and form usable. All four measured routine starts were below 30 seconds. | [Ready and dashboard](screenshots/M03-ready-dashboard.png); timing table below. |
| M04 Reopen browser / repeated launch | Pass, reported. Open dashboard reopened the closed tab. Double-clicking the running app brought the existing Ready window forward; browser unchanged. No separate already-open message appeared. | Jackie's written account. Original M04 screenshot retained locally because a personal folder name is visible. No process-count measurement was supplied. |
| M05 Early-Warning prediction | Pass. Attendance 40, study hours 4, failures 0 returned High Risk 85.9% and attendance support. | [Inputs](screenshots/M05-early-warning-input.png), [result](screenshots/M05-early-warning-result.png). |
| M06 Study-hours warning | Pass. Attendance 80, study hours 40, failures 0, G1 12, G2 blank returned High Risk 66.1%, G1-only setup and the study-hours warning. | [Inputs](screenshots/M06-study-hours-input.png), [warning and result](screenshots/M06-study-hours-warning-result.png). |
| M07 CSV and downloaded results | Pass. Sample roster: four rows, two valid, two skipped. Jackie reported checking the reasons. Warning sample: two valid rows, one warning. Both exports opened and matched. | [Sample upload](screenshots/M07-sample-roster-upload.png), [sample result](screenshots/M07-sample-roster-result.png), [warning upload](screenshots/M07-study-warning-upload.png), [warning result](screenshots/M07-study-warning-result.png); exports below. Skipped-row reasons are reported in the notes rather than visible in these screenshots. |
| M08 Offline prediction | Pass, reported and pictured. Wi-Fi was turned off, then Early-Warning 40/4/0 returned High Risk 85.9%. Network reconnected afterwards. | [Wi-Fi off](screenshots/M08-wifi-off.png), [offline prediction](screenshots/M08-offline-prediction.png). |
| M09 Quit/restart as normal user | Pass, reported. Quit stopped the old page after refresh; reopening from Finder returned a working dashboard under the normal account. | [Old page after Quit](screenshots/M09-after-quit-connection-error.png), [restarted dashboard](screenshots/M09-restarted-dashboard.png). The connection error here is the expected shutdown evidence. |

## Startup times

Times below are Jackie's recorded measurements, not measurements extracted from
the screenshots. The browser was initially closed for the post-reboot start.
Subsequent starts followed a full Quit.

| Start | Time to usable dashboard |
|---|---:|
| First routine launch after reboot | 6.72 seconds |
| Subsequent launch 1 | 4.29 seconds |
| Subsequent launch 2 | 3.64 seconds |
| Subsequent launch 3 | 3.58 seconds |

The first downloaded launch was interrupted by Gatekeeper and was not timed.
It is separate from the routine startup target; no security-prompt time has been
subtracted from these measurements.

## Exported results

- [Sample roster export](exports/M07-sample-roster-results.csv): A, Low Risk,
  0.155, G1; B, Low Risk, 0.004, G1+G2. Neither has an input warning.
- [Study-hours warning export](exports/M07-study-warning-results.csv): A,
  High Risk, 0.661, G1, with a study-hours warning; B, Low Risk, 0.004,
  G1+G2, without the warning.

Only fictional students A and B appear in the exported results.

## Evidence notes and remaining work

The supplied notes originally labelled Gatekeeper "Not tested", but their M02
account and screenshots show the actual warning and Open Anyway sequence. This
record follows that observed sequence.

The [checksum-file message](screenshots/M01-checksum-file-open-message.png)
appeared when opening the .sha256 document without an associated app. It is not
a SARAH launch failure; this file contains a checksum and is not an application.

Screenshots and CSV contents were retained unchanged; filenames were clarified.
The original Word notes and the M04 screenshot remain in Benjamin's local supplied
folder. See the [evidence index](evidence-index.md).

Reviewer/date: pending. Review the
unsigned-app exception before closing #115. Anna's Windows results are separate.
This developer-computer check does not establish use on a clean machine or on the
tutor's Mac. Full packaged workflow checks (#116), another-person download-to-use
checks (#117) and release review (#118) remain separate.
