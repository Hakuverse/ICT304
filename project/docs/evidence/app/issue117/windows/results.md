# Issue 117 Windows walkthrough results

Participant: Ka Jun (public alias, agreed by participant). No prior SARAH involvement or knowledge.

Observer: Benjamin. Date: 30 October 2026.

Environment reported: Windows 11 Home, version 26H2; AMD Ryzen 7 260 with Radeon 780M Graphics; Opera GX, Chromium 154.0.8037.99. OS version is transcribed from the supplied record, not independently verified. OS build was not recorded.

Package reported: SARAH-windows-x64-4 / `SARAH-0.1.0-preview-windows-x64-ab4a604.zip`. Actual ZIP checksum verification was not recorded for this walkthrough. Development tools, Python and virtual-environment status are awaiting confirmation; do not call this a clean-machine test.

The participant used the shared walkthrough and user guide. GitHub downloading needed Benjamin's sign-in advice. Subsequent tasks were reported completed independently. This is an independent participant, but not a completely unassisted download-to-use run.

## Task mapping and observations

The supplied record uses an older U01-U10 list. Its screenshot filenames are retained for traceability. This table maps those tasks to the current shared U01-U08; numbering differences do not mean a retest was performed.

| Shared case | Original case | Outcome and actual observation | Evidence |
|---|---|---|---|
| U01 | U01, U02 | Completed with help at download. An unauthenticated download showed GitHub 404; Benjamin advised signing in and retrying. Extraction was completed independently, but the ZIP inside a ZIP and additional folders seemed unusual. App folder kept together. | U01-download-problem.png; U02-extracted-package.png; U02-extracted-package-b.png |
| U02 | U03, U04 | Completed independently. SmartScreen appeared on first opening and not on later openings. Default Opera browser opened automatically. First launch recorded as 23 seconds; whether this included the security decision and ended at usable Attendance is not specified. | U03-security-warning.png; U03-security-details.png; U04-ready-dashboard.png |
| U03 | U05 | Completed independently. Early-Warning 40/4/0 produced High Risk 85.9% with attendance support. | U05-early-warning-result.png |
| U04 | U06 | Prediction completed independently: study 40, failures 0, G1 12, G2 blank, High Risk 66.1%, G1 only and warning. Understanding needs clarification: the participant described predictions above 12 hours as inaccurate, rather than potentially unreliable. | U06-confirmatory-warning.png; feedback below |
| U05 | U07 | Completed independently. Mixed sample: 4 rows, 2 predicted, 2 skipped. A Low Risk 15.5% g1; B Low Risk 0.4% g1_g2. C attendance 150 and D G2 NA rejected with corrective messages. | U07-csv-results-and-skipped.png |
| U06 | U08 | Completed independently using the warning-demo CSV, not the shared plan's U05 sample export. Two rows retained: A High Risk 0.661/g1 with full warning and general review, B Low Risk 0.004/g1_g2 with blank warning and routine guidance. Participant found the download and noticed the warned student. This is a documented task variation. | U08-warning-csv-result.png; U08-export-opened.png; exported CSV below |
| U07 | U09, U10 | Completed independently as reported. Closing browser left SARAH running; Open dashboard reopened at default Early-Warning mode. Participant first used the window X out of habit, then reopened and tested Quit SARAH. Old page showed connection error; restarting opened a new browser page while the old tab stayed disconnected. Restart outcome is written evidence, not a separate restart screenshot. | U10-after-quit.png; observer's record |
| U08 | Feedback section | Responses recorded below. Human review and quitting understood; study-warning wording was overinterpreted. | Written feedback |

## Feedback recorded by Benjamin

These are the supplied participant responses; they are not corrected answers.

- Modes: "early warning no need grades, while confirmatory can input grade results."
- Required grades: "g1 and g2, but g2 is optional"
- Percentage: "how likely the student is going to not do well in the module"
- Use alone: "No, because training model can be inaccurate and the study warning limitation."
- Study warning: "the model needs human review if study hours past 12, model becomes inaccurate, i will use my own judgement to attend to the student without putting much trust in the system after 12 hours."
- Skipped CSV rows: "entry field are entered incorrectly."
- Closing: "closing the browser does not automatically closes sarah while clicking quit sarah closes sarah but the browser just shows connection error."
- Improvements: "all okay, every step is understandable."

Review finding: the participant recognised the need for human review, but interpreted the warning too strongly. Above 12 hours is outside the converted training values and may be unreliable; it does not prove every such result is wrong. Values at or below 12 are not guaranteed reliable either. Clarification and the participant's subsequent understanding have not yet been recorded. Keep the original response even after follow-up.

## Timing and limitations

- First launch: 23 seconds as reported, with measurement boundaries unspecified.
- Download/extraction: not measured in the supplied record.
- Subsequent launch to usable Attendance: not recorded. The routine 30-second target cannot be assessed from this walkthrough yet.
- Participant had no project involvement, but installed development tools/source environment are not recorded.
- Checksum verification is not recorded; package identity is supported by the reported name and extraction screenshots.
- No application failure was reported. Download assistance, folder confusion, habitual window-X use and warning misunderstanding are retained as findings.

## Evidence

- [U01-download-problem.png](screenshots/U01-download-problem.png)
- [U02-extracted-package-b.png](screenshots/U02-extracted-package-b.png)
- [U02-extracted-package.png](screenshots/U02-extracted-package.png)
- [U03-security-details.png](screenshots/U03-security-details.png)
- [U03-security-warning.png](screenshots/U03-security-warning.png)
- [U04-ready-dashboard.png](screenshots/U04-ready-dashboard.png)
- [U05-early-warning-result.png](screenshots/U05-early-warning-result.png)
- [U06-confirmatory-warning.png](screenshots/U06-confirmatory-warning.png)
- [U07-csv-results-and-skipped.png](screenshots/U07-csv-results-and-skipped.png)
- [U08-export-opened.png](screenshots/U08-export-opened.png)
- [U08-warning-csv-result.png](screenshots/U08-warning-csv-result.png)
- [U10-after-quit.png](screenshots/U10-after-quit.png)

[Original warning-demo export](exports/U06-warning-demo-results.csv), supplied as `U08-exported-results.csv`. Contents preserved; this is not the mixed-roster export.

Reviewer/date: pending. Confirm the environment and timing limitations, clarify the study warning and record the follow-up before treating #117 as fully complete.
