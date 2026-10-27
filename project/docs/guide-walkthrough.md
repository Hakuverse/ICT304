# Guide walkthrough - Issue 80

Benjamin followed Jackie's deployment guide and Anna's user guide on Windows on
23 October 2026 at commit `ddedc0fbce7c33d50deb7cd94a22f82322fd6f89` (PR106).
The clean-checkout screenshot shows no code/model difference from `fe9685a`.
This was a teammate walkthrough, not independent-user usability research.

Browser: Opera GX, Chromium 153.0.8010.55; browser identification reports
OPR/137.0.0.0 and Chrome/153.0.0.0. Zoom was not recorded. Python in the new
environment was 3.12.10. The transcript timestamps span 18:02:40–23:49:01;
these are log boundaries, not measured task time. Benjamin did not record a start
time separately. Evidence is in [the Windows folder](evidence/issue80/windows/).

## Actual outcomes

| Check | Result and evidence |
|---|---|
| Version and clean checkout | [01](evidence/issue80/windows/01-version-and-clean-checkout.png) |
| Installation | `python` produced the Store/alias message; Benjamin reported `py --version` returned 3.14.0. After setup clarification, `py -3.12 -m venv .venv` created the 3.12.10 environment. [02](evidence/issue80/windows/02-installation.checks.png) shows pip check passed. |
| Automated tests | 106 passed in 23.597 seconds at the original commit: [02a](evidence/issue80/windows/02a-automated-tests.png). |
| Dataset and sample CLI | 395 students, 130 High Risk, 265 Low Risk; A/B predicted and C/D skipped: [02b](evidence/issue80/windows/02b-dataset-and-sample-checks.png). |
| Dashboard startup | [03](evidence/issue80/windows/03-dashboard-start.png). |
| Early-Warning | Attendance 40, study 4, failures 0: High Risk 85.9%, attendance support: [04](evidence/issue80/windows/04-early-warning.png). |
| G1 only | Attendance 80, study 4, failures 0, G1 8, G2 blank: High Risk 81.8%: [05](evidence/issue80/windows/05-confirmatory-g1.png). |
| G1+G2 | Attendance 80, study 4, failures 0, G1 12, G2 0: High Risk 99.6%: [06](evidence/issue80/windows/06-confirmatory-g1-g2.png). |
| Mixed CSV | Four rows, two predicted, two skipped: [07](evidence/issue80/windows/07-csv-results.png); explanations: [08](evidence/issue80/windows/08-csv-messages.png). |
| Download | [09](evidence/issue80/windows/09-downloaded-results.png) shows A/B, decimal probabilities and recommendations in Excel. The actual downloaded CSV was not supplied in this evidence folder. |
| Correct and re-upload | [Corrected fixture](evidence/issue80/windows/10-corrected-roster.csv), [10](evidence/issue80/windows/10-corrected-csv.png): four predicted, zero skipped. |
| Clear previous results | Benjamin confirmed the input-change and mode-change checks passed; no separate screenshot was supplied. |
| Stop dashboard | [11](evidence/issue80/windows/11-dashboard-stopped.png) shows the returned prompt. |

Benjamin reported the remaining steps were clear and passed. No verbatim answers
to the understanding questions were recorded, so this record does not claim a
new pass for S6-21/S6-22. Existing platform coverage and limits remain in the
[Sprint 6 review](sprint6-review.md); this is not a new macOS run.

The [transcript](evidence/issue80/windows/setup-log.txt) has local account and
computer identifiers redacted in this public copy. Some command outputs are
absent from the transcript; screenshots and Benjamin's confirmation supplement it.
Original local files were preserved.

## Corrections and review

The deployment guide and project README now include the Windows `py -3.12`
fallback actually used. The additional 40-hour example exposed a model limitation:
see [study-hours finding](study-hours-limitation.md). The 24 October warning change
has separate automated evidence; the screenshots above predate it.

Issue #80 is closed following merged PR #108. PR #110 refined the CSV warning
display, and #109 updated the user guide. Anna recorded the final demonstration
at `847d460`; Benjamin confirmed on 27 October that it plays completely and matches
the screen. See the [video record](demo-video-notes.md) and [Sprint 7 review](sprint7-review.md).
Keep the earlier evidence dates and model results. The local Windows application
trial is separate and is not the deployment tested here.

[24 October automated warning checks](evidence/issue80/warning-followup/README.md): 109 tests passed.
