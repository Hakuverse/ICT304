# #69 retest after PRs #86 and #87 (S6-21 to S6-24)

Earlier evidence: [17 October usability record](../../../usability-feedback.md)
(the before result) and the [issue68 evidence folder](../../issue68/README.md).

## Run details

| Item | Value |
|---|---|
| Date | 19 October 2026 |
| Run by | Anna |
| Tester (S6-21 to S6-23) | Tester A, non-team family member: the same person as the 17 October tester |
| Commit | `9dc7132` (main after PR #87), clean checkout |
| Computer / OS | Windows laptop |
| Python / Streamlit | Python 3.14.7 / Streamlit 1.65.0 |
| Browser / zoom | Microsoft Edge, 100% zoom; sizes set with DevTools device mode |
| Automated tests | 99 tests OK (output: `test-output.txt`) |
| Data | Fictional only: typed examples and `project/data/sample_roster.csv` |

## S6-24 Readability (checked by Anna)

Horizontal scrolling is allowed only inside the CSV results table.

| Subcase | What was checked | 1366 × 768 | 1920 × 1080 | Evidence |
|---|---|---|---|---|
| S6-24-notice | "Support tool only. Do not use this prediction alone to make decisions about a student." at top and with each result | Pass | Pass | `s624-*-form-top.png`, `s624-*-form-result.png`, `s624-*-csv-bottom.png` |
| S6-24-probability | Early-Warning 40/4/0 shows 85.9% (checked on screen); G1-only example shows "Model-estimated High-Risk probability: 81.8%. This estimate may be inaccurate and should be considered alongside other information about the student." | Pass | Pass | `s624-*-form-result.png` |
| S6-24-help | Mode help; G1/G2 as first/second-period grades; blank vs 0; attendance as an estimate | Pass | Pass | `s624-*-form-top.png`, `s624-*-form-result.png`, `s624-*-csv-top.png` |
| S6-24-skipped | sample_roster.csv (Confirmatory): 4 rows, 2 predicted, 2 skipped; "2 of 4 students were skipped…" shown near results; A (15.5%) and B (0.4%) still shown | Pass | Pass | `s624-*-csv-top.png` |
| S6-24-full-text | Every suggestion (full list) and both skipped reasons (C, D) readable in full | Pass | Pass | `s624-*-csv-bottom.png` |
| S6-24-controls | Form, buttons, warnings and notice fit; no horizontal page scrolling | Pass | Pass | all eight screenshots |

`*` = `1366` or `1920`. Eight screenshots in total: `form-top`, `form-result`, `csv-top` and `csv-bottom` at each size.

**How the screenshots were taken:** Edge DevTools device mode with DevTools undocked, DPR 1, and "Fit to window" for 1920 × 1080 (the laptop screen is narrower than 1920).
The viewport was confirmed with `innerWidth + " x " + innerHeight` in the Console before capturing, and every file is exactly 1366 × 768 or 1920 × 1080 pixels.
Streamlit scrolls inside its own container, so each screen needed two viewport captures instead of one full-page capture.
Earlier captures were discarded because device mode had silently fallen back to a narrower viewport (964–1591 px wide), even though the size bar still showed the target size.

## S6-21 to S6-23 Usability (tester)

Rules: first attempt without coaching; help only if asked or stuck about 1 minute; any help recorded.
A correct result with help is not an independent pass.

| Case / task | Input | Expected result | What happened | Outcome | Help given |
|---|---|---|---|---|---|
| S6-21 task 1 | Early-Warning: attendance 40, study 4, failures 0 | High Risk, 85.9%, attendance suggestion | Entered the values slowly and completed the prediction: High Risk, 85.9%. Looked at the observer to check if it was right. | Helped (non-verbal) | Observer nodded when the tester looked for confirmation. No verbal help. |
| S6-21 task 2 | Confirmatory: attendance 80, study 4, failures 0, G1 8, G2 blank | High Risk, 81.8%, G1-only model, assessment review suggestion | Completed. Understood G1 as the first grade and G2 as the second grade. | Independent | None |
| S6-23 task 3 | Confirmatory: upload `sample_roster.csv`, download valid results | 4 rows: A and B predicted, C and D skipped; download works | Uploaded and downloaded the results. Downloaded file contains A (Low Risk, 0.155, g1) and B (Low Risk, 0.004, g1_g2) only, with recommendations. | Independent | None |
| S6-23 task 4 | Explain why C and D were skipped and how to fix them | C: attendance over 100; D: G2 "NA" is not a number (leave blank or enter 0–20) | Saw the skipped-row warning but could not explain why C and D were skipped or how to fix them. | Not completed | After the attempt, Anna explained the reasons (C: attendance_pct must be 0 to 100; D: G2 must be a valid number). |

## Understanding questions (answers recorded before any explanation)

| Case | Question | Tester's answer | Understood? |
|---|---|---|---|
| S6-21 | What do G1 and G2 mean? Blank G2 vs 0? | "G1 = first grade, G2 = second grade. Blank G2 means did not take the second exam, so G2 is blank; 0 means scored 0 marks in G2." | Yes |
| S6-21 | What does the attendance number mean? | "Attendance to class, present or absent." | Partly: understood attendance, but did not mention that it is an estimate |
| S6-22 | What does "High Risk" mean? | "High risk needs the tutor to pay more attention." | Yes |
| S6-22 | What does "81.8%" mean? | "82 out of 100 means high risk; if less than 50% it is low risk." | Partly: read it as a percentage, but did not mention that it is a model estimate that may be wrong. Anna explained this after the answer was recorded. |
| S6-22 | Would you use this result alone to decide about a student? | "No, but overall performance matters." | Yes |

## Compared with 17 October

| Finding on 17 Oct | Change | Result now |
|---|---|---|
| Needed help with mode, attendance %, G1 and blank G2 | #86 mode + field help | Improved: task 2 independent and G1/G2, blank vs 0 explained correctly. Task 1 still needed reassurance (nod). Attendance not described as an estimate. |
| Probability 0.818 not understood | #86 percentage + caveat | Improved: now read as a percentage. Uncertainty ("may be inaccurate") not mentioned. |
| Would use SARAH alone | #86 human-review notice | Fixed: tester now says the result should not be used alone. |
| Did not notice skipped rows | #86 warning; #87 full skipped list | Partly fixed: the tester now noticed the warning (it was missed on 17 Oct), but still could not explain why C and D were skipped or how to correct them. |

## Against the agreed targets (system test plan)

| Target | Result |
|---|---|
| Complete all four tasks without verbal help | Not met: task 1 assisted (non-verbal), task 4 not completed. |
| Explain that the probability is an estimate, can be wrong and must not be used alone | Partly met: "not used alone" understood; "estimate / can be wrong" not mentioned. |
| Readability at 1366 × 768 and 1920 × 1080, 100% zoom | Met (S6-24 all Pass). |

## Remaining problems / follow-up

1. **Skipped-row reasons not understood (S6-23 task 4).** The tester saw the warning, so the problem is the reason text: it uses technical wording
   (`attendance_pct must be 0 to 100`, `G2='NA' is not a valid number`) and do not say how to fix the row.
   Proposed follow-up for team agreement: plain-language reasons with a fix, e.g. "Attendance is 150. Enter a value from 0 to 100."
   and "G2 is 'NA'. Leave it blank if there is no second-period grade, or enter 0–20." Owner: Anna (#69). Not implemented.
2. Attendance not understood as an estimate (minor).
3. Probability not described as an uncertain estimate (minor).

## Limits of this check

- One tester only, the same person as on 17 October, so the tasks were already familiar. This may make the retest look easier than it would be for a new user.
- The observer's nod in task 1 may have influenced the result; it is recorded as assistance.
- Readability checked on one computer and browser, using DevTools device sizes.
