# Issue 117 macOS walkthrough results

Tester: Jackie, experienced SARAH teammate. Date: 30 October 2026. Observer: not recorded. Benjamin confirmed on 30 October that Jackie needed no help.

Environment listed in the supplied document: Apple M3, macOS Tahoe 26.6.2 (25G83), Chrome 152.0.7977.75 arm64. The original document marked these details provisional. Benjamin confirmed on 30 October that these were the environment details for this walkthrough.

Package identified in the document and screenshots: SARAH-macos-arm64-4 containing the ab4a604 Apple Silicon package. Full source listed: `ab4a604a71ecef9f0585a137a014e7dd6fb861e2`. Previously recorded inner ZIP SHA-256: `0996cc189a435d1e1a4509a7fd754cdcf7366a36fed8a5cdb8c173fa4fedf875`. New checksum verification was not recorded. Benjamin confirmed the same ab4a604 package and download through GitHub Actions, with no help needed. Whether Jackie was already signed in or signed in during the run was not separately recorded.

Jackie's Mac was previously used for development and app testing. This is a teammate walkthrough, not an independent first-time or clean-machine test.

## Actual observations

| Case | Outcome | Evidence and limitations |
|---|---|---|
| U01 | Completed; GitHub Actions route confirmed | Download/extraction reported. Inner package image shows SARAH, START-HERE, sample CSVs and build records. Outer-package image reviewed locally, but withheld because the Finder sidebar includes a personal account name. |
| U02 | Completed after security approval | Gatekeeper blocked opening; Privacy & Security > Open Anyway allowed it. Launcher Ready and browser dashboard are shown. 4.25 seconds was reported from security approval to automatic browser opening, not full startup to usable Attendance. |
| U03 | Pass | 40 attendance / 4 study / 0 failures; High Risk 85.9% with attendance support. Form and result screenshots supplied. |
| U04 | Pass | Confirmatory 80/40/0/G1 12/G2 blank; High Risk 66.1%, G1 only, full study warning and general staff-review guidance. |
| U05 | Pass | Built-in sample workflow reported completed. Screenshots show 4 rows, 2 predicted, 2 skipped: A Low Risk 15.5% g1 and B Low Risk 0.4% g1_g2; C attendance 150 and D G2 NA errors. |
| U06 | Pass | Supplied U06-results.csv contains A Low Risk 0.155/g1 and B Low Risk 0.004/g1_g2, blank warnings and routine guidance. Spreadsheet screenshot agrees. |
| U07 | Pass; routine timing confirmed approximately | Quit image shows the old page on port 56358 no longer responding. Reopened image shows a new dashboard on 58167. Benjamin subsequently reported approximately 2 seconds from double-click to usable Attendance; see timing below. |
| U08 | Feedback supplied | The original document's heading says pending, but it contains the responses below. Feedback is recorded; do not treat it as missing. |

## Feedback from Jackie's document

- Modes: "I used Early-Warning without grades and Confirmatory with G1. Leaving G2 blank selected the G1-only model. The page explained that G1 is required and G2 is optional in Confirmatory mode."
- Probability: "The result displayed a model-estimated High-Risk probability and stated that it may be inaccurate. The page also said the prediction should not be used alone to make decisions about a student."
- Study warning: "Entering 40 study hours still produced a prediction with a warning. The warning told me to review the result with other information and not change the input to 12."
- Quitting: "I used Quit SARAH in the launcher window. Closing a browser tab alone did not stop the application."
- Improvements: "I did not report a problem with the prediction tasks. The macOS security approval added an extra step; showing Privacy & Security > Open Anyway clearly in the launch instructions would help."
- Instructions: "I completed the download and extraction. On the first launch, macOS blocked SARAH; I used Privacy & Security > Open Anyway, after which SARAH opened and the dashboard appeared automatically in the browser. I did not separately compare every written instruction with each step I took."

## Timing and limitations

- Download/extraction duration: not recorded (the original timing field contains a filename).
- Full first launch including security: not measured.
- Security approval to browser opening: 4.25 seconds, tester-reported. This is not a measurement to usable Attendance and does not assess the routine 30-second target.
- Subsequent double-click to usable Attendance: approximately 2 seconds, confirmed by Benjamin on 30 October. This reported approximate result is below the 30-second routine target; no stopwatch log or repeated-run series was supplied.
- Environment, package, GitHub Actions route and no-help completion were confirmed by Benjamin on 30 October. Exact sign-in sequence was not recorded. No fresh checksum verification is claimed.
- No application problem beyond the expected security exception was reported. Anna approved PR #123 on 30 October; it is merged.

## Evidence

- [01-package-inner-files.png](screenshots/01-package-inner-files.png)
- [02-security-prompt-setting.png](screenshots/02-security-prompt-setting.png)
- [02-security-prompt.png](screenshots/02-security-prompt.png)
- [03-dashboard-ready.png](screenshots/03-dashboard-ready.png)
- [04-early-warning-form.png](screenshots/04-early-warning-form.png)
- [04-early-warning-result.png](screenshots/04-early-warning-result.png)
- [05-study-warning-form.png](screenshots/05-study-warning-form.png)
- [05-study-warning-result.png](screenshots/05-study-warning-result.png)
- [06-csv-results.png](screenshots/06-csv-results.png)
- [06b-skipped-row-result.png](screenshots/06b-skipped-row-result.png)
- [06b-skipped-rows.png](screenshots/06b-skipped-rows.png)
- [07-downloaded-results.png](screenshots/07-downloaded-results.png)
- [08-quit.png](screenshots/08-quit.png)
- [09-reopened.png](screenshots/09-reopened.png)

[Original downloaded results](exports/U06-results.csv). Screenshot contents and export bytes are unchanged. The raw Word document is retained locally; this Markdown record resolves its contradictory status heading and links its supplied evidence.

Reviewed by Anna on 30 October 2026; approved and merged in PR #123. Follow-up confirmations are recorded; the timing, checksum and experienced-teammate limitations remain part of the accepted record.
