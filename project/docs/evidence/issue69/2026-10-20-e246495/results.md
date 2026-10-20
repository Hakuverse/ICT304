# #69 retest after PRs #92 and #100 (S6-22, S6-23, S6-24)

Earlier evidence (kept unchanged as the historical record):
[19 October retest](../2026-10-19-9dc7132/results.md) and the
[17 October usability record](../../../usability-feedback.md).

## What changed since 19 October

| PR | Change |
|---|---|
| #92 | Skipped-row reasons on the dashboard name the value found and how to fix it, e.g. "Attendance is 150. Enter a value from 0 to 100." Same rows are skipped as before. |
| #100 | The results table no longer repeats the recommendations; they are shown once under "Full support suggestions for each student". The downloaded CSV still includes them. |

The probability wording was not changed. For S6-22 the team chose on 20 October to
record the earlier difficulty as an unresolved limitation instead of changing the
wording (see below).

## Run details

| Item | Value |
|---|---|
| Date | 20 October 2026 |
| Run by | Anna |
| Tester (S6-22, S6-23) | Tester A, the same non-team family member as on 17 and 19 October |
| Commit | `e246495` (main after PRs #92, #99 and #100) |
| Computer / OS | Windows laptop |
| Python / Streamlit | Python 3.14.7 / Streamlit 1.65.0 |
| Browser / zoom | Microsoft Edge, 100% zoom; sizes set with DevTools device mode (DPR 1, viewport confirmed with `innerWidth + " x " + innerHeight`) |
| Automated tests | 106 tests OK (output: `test-output.txt`) |
| Data | Fictional only: `project/data/sample_roster.csv` and `s624_multi_error_roster.csv` (in this folder) |

## S6-23 Notice and correct CSV problems (tester)

Rules as before: no coaching; help only if asked or stuck about 1 minute; any help recorded.

| Task | Input | Expected | Tester's words / what happened | Outcome | Help given |
|---|---|---|---|---|---|
| Task 3 | Upload `sample_roster.csv` in Confirmatory | A and B predicted, C and D skipped | Uploaded the file themselves. | Independent | None |
| Task 4 | "Some students were skipped. Why, and how would you fix them?" | C: attendance 150, enter 0 to 100. D: G2 "NA", leave blank or enter 0–20. | C: "C were skipped because the number must between 0 to 100". D: "D were skipped because G2 is NA, must be a grade like number, but number must between 0 to 20. G2 can leave it blank if there is no second exam grade." | Independent: reason and fix given for both rows (for C the tester gave the allowed range but did not name the attendance field) | None |

On 19 October the same tester saw the warning but could not explain C or D (task 4
not completed). After #92 they explained both rows and how to correct them.

## S6-22 Understand results and limitations (tester)

Answers recorded before any explanation.

| Question | Tester's words | Understood? |
|---|---|---|
| What does the 81.8% mean? | "can understand because there got "High Risk" shown on the dashboard" | Partly: linked the number to the High Risk label, but did not describe it as a model estimate that can be wrong |
| Would you use this result alone to decide about the student? | "can understand because the words "support tool", so this is just for tutor to see student performance but tutor should look at other student information as well." | Yes |

**Team decision, 20 October 2026:** the probability wording is not changed in #69.
Understanding the probability as an estimate that can be wrong is recorded as an
**unresolved limitation**. Follow-up: explain it in the user guide (#79).
Follow-up owner: Anna.

## S6-24 Readability after #92 and #100 (checked by Anna)

Fixture `s624_multi_error_roster.csv` (Confirmatory): 6 rows, 2 predicted (A, B), 4 skipped:
C (attendance 150), D (G2 "NA"), E (five problems in one row, the longest message),
F (attendance and G1 missing). Horizontal scrolling is allowed only inside the results table.

| Subcase | What was checked | 1366 × 768 | 1920 × 1080 | Evidence |
|---|---|---|---|---|
| S6-24-skipped | Counts 6 / 2 / 4; "4 of 6 students were skipped…" near the results; A and B still shown | Pass | Pass | `s624-*-csv-top.png` |
| S6-24-long-message | E's five-part reason and F's two-part reason readable in full and wrapped, nothing cut off | Pass | Pass | `s624-*-csv-bottom.png` |
| S6-24-table | Results table shows no recommendations column; full suggestions still listed below | Pass | Pass | `s624-*-csv-top.png`, `s624-*-csv-bottom.png` |
| S6-24-controls | No horizontal page scrolling; buttons, warnings and notice fit | Pass | Pass | all four screenshots |

All four screenshots are exactly 1366 × 768 or 1920 × 1080 pixels. The single-student form did not change after
19 October, so its screenshots are not repeated.

## Against the agreed targets

| Target | Result |
|---|---|
| Correct CSV problems without help (S6-23) | Met in this retest: both skipped rows explained with a fix, no help. |
| Explain that the probability is an estimate, can be wrong and must not be used alone (S6-22) | Partly met: "not used alone" understood; "estimate / can be wrong" not shown. Recorded as an unresolved limitation (team decision), follow-up in #79, owner Anna. |
| Readability at 1366 × 768 and 1920 × 1080, 100% zoom (S6-24) | Met for the changed CSV view (all four subcases Pass at both sizes). |

## Limits of this check

- One tester only, the same person as on 17 and 19 October. After the 19 October session
  Anna explained the C/D reasons and the probability to this tester, so the improved S6-23
  result may partly reflect memory rather than the new wording alone.
- Only the affected cases were repeated (S6-22, S6-23 task 3–4, S6-24 CSV view). Tasks 1 and 2
  and the form screenshots were not repeated because the form did not change.
- Readability checked on one computer and browser, using DevTools device sizes.
