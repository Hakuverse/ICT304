# Packaged app walkthrough (#117)

Prepared 30 October 2026 after PR #122 merged as `9fd287c`. Results from 30 October are now recorded in the [evidence review](evidence/app/issue117/README.md); follow-up confirmations are recorded and Anna approved PR #123 on 30 October; it is merged and #117 is closed. This checks the download-to-use experience. It does not repeat every #116 boundary test.

For current downloads and normal app use, go directly to the [app user guide](user-guide.md).
The procedure below records the **30 October Actions-based walkthrough**; the
public release uses direct app ZIPs and does not require that older download route.

## People and version

- Windows: a classmate who has not worked on SARAH. Use a public alias such as Windows tester A. Benjamin or Anna observes and records help actually given.
- macOS: Jackie follows the same tasks on Apple M3 / Tahoe 26.6.2. Record this as a teammate walkthrough, not an independent first-time user study.
- Use the same tested **ab4a604** packages, with bundled Python 3.12.10. No rebuild is needed. Do not install Python or clone the repository to run the app.
- Prefer a normal account/device without the SARAH repository or virtual environment. Record installed development tools and previous app/security approval. Jackie's existing computer cannot be described as a clean machine. A fresh extraction alone does not make a clean machine.

## Download and open

Historical distribution route used on 30 October: [Actions run 40556703379](https://github.com/Hakuverse/ICT304/actions/runs/40556703379).

| Platform | Download | Inner package |
|---|---|---|
| Windows x64 | [SARAH-windows-x64-4](https://github.com/Hakuverse/ICT304/actions/runs/40556703379/artifacts/12757642322) | SARAH-0.1.0-preview-windows-x64-ab4a604.zip |
| Apple Silicon Mac | [SARAH-macos-arm64-4](https://github.com/Hakuverse/ICT304/actions/runs/40556703379/artifacts/12758175843) | SARAH-0.1.0-preview-macos-arm64-ab4a604.zip |

These artifacts were available when checked on 30 October and expire on **10 November 2026**. GitHub may require sign-in. In the Windows walkthrough, the download showed 404 while signed out; signing in and retrying resolved it with observer advice. The [public release](https://github.com/Hakuverse/ICT304/releases/tag/v0.1.0-preview) was published on 31 October; these observations describe the earlier Actions route. Do not use GitHub's source-code ZIP as the application download.

1. Give the tester this page and the [user guide](user-guide.md); let them attempt the steps themselves.
2. Download the matching artifact. Extract the outer ZIP to find the versioned inner ZIP, checksum and JSON build records. Retain all of them.
3. Extract the inner ZIP. On Mac use Archive Utility. On Windows keep SARAH.exe and its complete `_internal` folder together.
4. Read START-HERE.txt. Record the package name and build-info source. The observer checks the inner ZIP checksum against the [existing platform record](app-package-testing.md); this is setup assistance if the tester needed it.
5. Open SARAH.exe on Windows or SARAH.app on Mac. Record any security prompt and decision. Follow the [unsigned-app opening guidance](app-package-testing.md#unsigned-app-first-launch) only for the verified team package and where device policy allows it. Do not disable protection. Stop and record a block if no permitted option is available.
6. Record whether the launcher and browser open automatically and the Attendance field becomes usable.

If a tester cannot access Actions, record the sign-in/download barrier. The team can transfer the unchanged inner ZIP and matching build records, but mark that run as a **team-provided package**: it does not prove independent GitHub downloading. Public downloads were subsequently integrity-checked under #118; no new device walkthrough was performed after publication.

## Tasks and evidence

Use only fictional inputs. Capture screenshots after the relevant outcome; do not interrupt every click. The observer may capture them. Exclude personal names, paths, browser profiles and unrelated windows. Record Pass, Fail, Blocked or Not tested honestly.

| ID | Task | Suggested evidence |
|---|---|---|
| U01 | Download, extract and locate START-HERE and the app. Record any help, wrong ZIP or sign-in barrier. | `01-package-files.png`; package/build details in results.md |
| U02 | Open the app. Record security prompts and time from double-click to usable Attendance. | `02-security-prompt.png` only if shown; `03-dashboard-ready.png` |
| U03 | Early-Warning: attendance 40, study 4, failures 0. Predict and read the result. | `04-early-warning.png`: High Risk 85.9%, attendance support |
| U04 | Confirmatory: attendance 80, study 40, failures 0, G1 12, G2 blank. Predict and explain the warning in the tester's own words. | `05-study-warning.png`: High Risk 66.1%, G1 only, warning and general review; a second detail image is fine if needed |
| U05 | In Confirmatory/Class CSV, click Download sample CSV (fictional students), upload that file and read totals/skipped reasons. | `06-csv-results.png`: 4 rows, 2 predicted, 2 skipped; use `06b-skipped-rows.png` if not visible together |
| U06 | Download results as CSV and open it in a spreadsheet or text viewer. Locate the two valid rows, probability, grade setup and recommendations. | `07-downloaded-results.png` and original `U06-results.csv` |
| U07 | Use Quit SARAH in the launcher. Refresh the old dashboard to confirm it stops responding, then reopen the app normally. | `08-quit.png` and `09-reopened.png`; record actual observation |
| U08 | Answer the questions below. | Written responses in results.md; no screenshot needed |

A single image may cover more than one item only if each outcome is visible. The images support the written observations, not an invented continuous recording. No screenshot of a security prompt is needed when it does not appear.

## Timing, help and feedback

Record download/extraction time separately from app startup. For the first launch, record the total time including security decisions; if the security-only time was not measured, do not subtract an estimate. Time a subsequent launch separately. The existing **30-second routine startup target** applies to the subsequent launch; retain any miss. This is not a new prediction-time benchmark or a claim about all machines.

Allow the tester to try with the written instructions first. If stuck, help as needed and record the exact help and step. Successful assisted completion is still useful evidence, but is not unassisted completion. Do not supply answers to these questions before recording them:

1. What is the difference between the two modes, and when are G1/G2 needed?
2. What does the percentage mean? Would you use it alone to decide what happens to a student?
3. What does the study-hours warning mean? Should you change 40 to 12 just to remove it?
4. How do you stop SARAH? Is closing the browser tab enough?
5. Which step or wording was confusing, and what would you improve?

Record the person's actual response before adding any clarification. Use a public alias, not their legal name. Get their agreement to record anonymous feedback and screenshots.

## Recorded runs

Ka Jun completed the Windows tasks with sign-in help; Jackie supplied the macOS teammate walkthrough. Both show working predictions, exports and quit/reopen. See the [evidence review and confirmed follow-ups](evidence/app/issue117/README.md). The Windows evidence uses older U01-U10 filenames and a warning-demo export; its record maps these differences without pretending the run followed an identical script.

## Records and completion

- [Windows record](evidence/app/issue117/windows/results.md)
- [macOS record](evidence/app/issue117/macos/results.md)

Actual outcomes and feedback were reviewed by Anna and merged in PR #123 on
30 October; #117 is closed. The original assistance and distribution limitations
remain in the evidence. Benjamin chose to reuse these device results for the
unchanged published app. Future application changes need affected checks; this
documentation correction does not claim or require another walkthrough.
