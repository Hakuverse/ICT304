# Windows package results

Tester: Anna. Status: device checks completed 29 October 2026; awaiting team review.

Benjamin's separate [preliminary launch check](benjamin-preliminary/README.md)
records the SmartScreen warning and successful launch on 28 October 2026.
It does not fill or replace Anna's results below.

| Detail | Actual record |
|---|---|
| Date | 29 October 2026 |
| OS/build and processor | Windows 11 Home 25H2, OS Build 26200.9711 (x64); Intel Core Ultra 5 125H |
| Browser/version | Microsoft Edge 156.0.4314.50 (default browser) |
| Package filename / SHA-256 | `SARAH-0.1.0-preview-windows-x64-ab4a604.zip` / `8828121aa9b343c07138657f6d827df168d33211782204fd5b019bf2577f4bc2` (matches the included `.sha256` file). SARAH.exe SHA-256 `5b1a3beb97e8ed05b64cf6e882aad17dbac46fb5e5fb253051d10f32f7aa9d2f` matches `executable_sha256` in build-info.json |
| Source commit / Actions run | `ab4a604a71ecef9f0585a137a014e7dd6fb861e2` (build-info.json, built 2026-10-27 18:08 UTC, bundled Python 3.12.10) / [run 40556703379](https://github.com/Hakuverse/ICT304/actions/runs/40556703379), artifact `SARAH-windows-x64-4` |
| Python installed? Developer computer? | Yes, Python 3.14.7 is installed, but the package uses its bundled Python 3.12.10. Yes, developer computer: this laptop is used for the SARAH repository, so this is not a clean-machine check |
| Download route and security messages | Artifact downloaded from GitHub Actions in Edge; no download warning. Outer download and inner SARAH ZIP extracted to `C:\Users\<user>\SARAH package test` (path with spaces, outside the repository). First launch: Microsoft Defender SmartScreen "Windows protected your PC" (details in W02); Run anyway chosen |
| Startup times / browser already open? | Timed with a phone stopwatch from double-click until the Attendance field could be used. First downloaded launch after restart: 1 min 14.67 s, including about 15 s on the SmartScreen dialog; Edge not opened before launch. Later launches after Quit SARAH: 11.15 s, 6.46 s, 4.35 s; Edge already open; no SmartScreen |

Use the [package testing guide](../../../app-package-testing.md).

| Case | Actual result | Evidence / help needed |
|---|---|---|
| W01 Platform and extraction | Pass. Details above recorded. Source commit `ab4a604` confirmed in build-info.json; package and SARAH.exe hashes match. Folder contains SARAH.exe, `_internal`, `third-party-notices`, START-HERE.txt, build files and both sample CSVs | [W01-package-and-platform.png](screenshots/W01-package-and-platform.png) (email in About Windows hidden). No help needed |
| W02 Downloaded first launch | Pass with expected unsigned-app warning. Double-click showed "Windows protected your PC: Microsoft Defender SmartScreen prevented an unrecognized app from starting. Running this app might put your PC at risk." After More info: App: SARAH.exe, Publisher: Unknown publisher. Hashes had been checked, so Run anyway was chosen; SARAH launched. No security settings changed; normal (non-administrator) launch | [W02-smartscreen-first-launch.png](screenshots/W02-smartscreen-first-launch.png). No help needed |
| W03 Ready and startup timing | Functional launch passed; routine startup target not fully verified. Launcher showed "Ready. Your dashboard is available in the browser." The Starting status was not observed by the tester. Edge opened the dashboard automatically and the form was usable. First launch 1 min 14.67 s (about 15 s on SmartScreen); later launches 11.15 s, 6.46 s, 4.35 s | [W03-ready-dashboard.png](screenshots/W03-ready-dashboard.png) (local address hidden). Observation: Streamlit's "Deploy" button is visible at the top right of the dashboard |
| W04 Reopen browser / repeated launch | Pass. After closing the dashboard tab, Open dashboard brought the dashboard back. Double-clicking SARAH.exe again while it was running showed "SARAH is already open: Use Open dashboard in the existing SARAH window. Quit that window before starting another copy." No SmartScreen on this attempt. After OK, the original launcher remained and worked | [W04-already-open-message.png](screenshots/W04-already-open-message.png). No help needed |
| W05 Early-Warning prediction | Pass. Attendance 40, study hours 4, failures 0: High Risk, 85.9%, with the attendance support suggestion (attendance estimate 60% or below). Matches expected | [W05-early-warning-result.png](screenshots/W05-early-warning-result.png). No help needed |
| W06 Study-hours warning | Pass. Confirmatory, attendance 80, study hours 40, failures 0, G1 12, G2 blank: High Risk, 66.1%, model used G1 only, study-hours warning shown, general staff-review suggestion. Matches expected | [W06-study-hours-warning.png](screenshots/W06-study-hours-warning.png). No help needed |
| W07 CSV and downloaded results | Pass. Confirmatory CSV: `sample_roster.csv` gave 4 rows, 2 predicted (A Low Risk 15.5%, B Low Risk 0.4%), 2 skipped with fixes (C: attendance 150, enter 0–100; D: G2 'NA', leave blank or enter 0–20). `study_hours_warning_demo.csv` gave 2 rows, 2 predicted, 0 skipped; the count message and full warning appeared once; A High Risk 66.1% marked "Yes - see warning above"; B Low Risk 0.4%. Results downloaded to the browser's Downloads folder and opened in Excel: full warning in `input_warning` for A, recommendations for both rows | [W07-sample-roster-results.png](screenshots/W07-sample-roster-results.png), [W07-study-warning-results.png](screenshots/W07-study-warning-results.png), [W07-export-opened-in-excel.png](screenshots/W07-export-opened-in-excel.png), exported file [W07-study-warning-results.csv](exports/W07-study-warning-results.csv) (fictional students). No help needed |
| W08 Offline prediction | Pass. Wi-Fi turned off from Windows Quick Settings while SARAH was running; Early-Warning 40 / 4 / 0 still gave High Risk 85.9% with attendance support. Wi-Fi turned back on after the result | No screenshot used: the captured image does not show the Wi-Fi status. Method recorded here. No help needed |
| W09 Quit/restart as normal user | Pass. Quit SARAH closed the launcher. The old dashboard tab showed Streamlit's "Connection error: Streamlit server is not responding. Are you connected to the internet?" After F5, Edge showed "127.0.0.1 refused to connect" (ERR_CONNECTION_REFUSED). SARAH reopened by normal double-click (not Run as administrator), without SmartScreen; three relaunches timed as above | [W09-after-quit-connection-refused.png](screenshots/W09-after-quit-connection-refused.png), [W09-old-tab-connection-error.png](screenshots/W09-old-tab-connection-error.png). Observation: the Streamlit message mentions the internet, although SARAH does not need internet; this could confuse a user after Quit |

Reviewer/date: pending. Functional checks found no blocking problem, but the routine post-reboot startup measurement is still missing.
Observations for team review: the "Deploy" button is visible; after Quit, the old tab's
Streamlit message refers to the internet; the Starting status was not seen on first launch.
Limitations: one developer laptop with Python installed (not a clean machine); timings are
manual stopwatch readings.
Automated build results must be recorded separately from these manual outcomes.


## Startup target review

The first downloaded launch took **74.67 seconds**, including approximately
15 seconds spent on SmartScreen. Keep the full measured duration; subtracting
an estimated prompt time would not produce a valid routine-start measurement.
The three later starts (11.15, 6.46 and 4.35 seconds) met the 30-second target.

The [agreed method](../../../app-deployment-plan.md#startup-timing-method) also
requires a routine launch after reboot. Anna's first post-reboot measurement
was also the initial SmartScreen launch, so a separate post-approval reboot
check remains outstanding. Restart Windows, keep Edge closed, launch the same
package, and time from double-click until the Attendance field is usable.
Record the duration, date and any warning; do not replace the initial result.
If the routine start exceeds 30 seconds, investigate or disclose the miss for
the team's release decision.

## Evidence review

The 11 screenshots and fictional CSV were reviewed and copied without changing
their contents. Personal details and the local browser address were already
hidden in Anna's supplied images. Screenshot names now identify their test case.
The W09 images show the expected stopped-server state, not the successful
restart; restarting successfully is recorded in Anna's written account.
W08 is a reported offline check without a Wi-Fi screenshot.

The exported CSV matches A: High Risk, 0.661, G1 only with the study-hours
warning; B: Low Risk, 0.004, G1+G2 without a warning. The sample-roster screenshot
also shows both skipped-row reasons. Hash matches are reported by Anna; the
supplied platform screenshot identifies the same build and bundled Python.

Windows and macOS tests both refer to candidate ab4a604 and bundled Python
3.12.10. Neither developer-computer test establishes a clean-machine result.
The visible Deploy button and the internet wording after Quit are usability
observations for team review, not evidence that prediction requires internet.
No new package or repeat of all functional cases is needed for this
documentation update. Keep #114 open until the timing follow-up and peer review
are resolved; #116-#118 remain separate.
