# Demonstration video notes (#81)

Owner: Anna. Peer check: Benjamin and Jackie, 25 October 2026.

## Requirements from the brief

The brief requires a demonstration video file but does not specify a separate duration for
the demo (checked by Anna on 23 October 2026). The 10-minute limit in the brief applies to
the presentation, not to this video.

## Version shown and recording setup

- Commit: `847d460` (main after PRs #108, #110 and #109). #108 added the study-hours warning and #110 shows it
  once in the CSV view; #109 changed the user guide only.
- Automated tests at that commit: `Ran 110 tests … OK` (Anna's run before recording).
- Computer: Windows laptop, Microsoft Edge in full screen (F11), 100% zoom.
- Recorded with a Microsoft Teams meeting recording (camera off, narration, whole screen shared).
- Screens shown: the SARAH dashboard; a downloaded results CSV; a PowerShell window showing the
  automated test result; the [user guide](user-guide.md) section 6 on GitHub.
- Data: fictional students only (typed examples, `project/data/sample_roster.csv` and a separate
  fictional `study_hours_warning_demo.csv` with one 40-hour row). No real student data, private
  messages or declarations are shown.

### Previous recording

A first video (`SARAH_demonstration.mp4`, 6 min 25 s, recorded 22 October 2026 at `ddedc0f`) was
replaced because it predates the study-hours warning added in #108 and refined in #110.

## Outline and script

The narration keeps the model prediction separate from the recommendation rules, explains that
the displayed percentage is the estimated probability of High Risk, demonstrates the study-hours
warning, and states the limitations.

| # | Show on screen | Say |
|---|---|---|
| 1 | Start screen with the support notice | "This is SARAH, the Student Academic Risk Assistance Hub. It estimates academic risk and provides support suggestions for a tutor to review. It supports predictions without grades and predictions using available grades. It does not make decisions about students." |
| 2 | **Early-Warning**: attendance 40, study hours 4, failures 0 → Predict | "Early-Warning mode uses an attendance estimate, study hours and past failures, without G1 or G2. It is intended to support earlier review, but our dataset does not establish how accurately it works at the beginning of a course. Here, we use fictional example inputs. For this fictional student, we enter an attendance estimate of 40%, four study hours per week and no previous failures. SARAH predicts High Risk, with an estimated High-Risk probability of 85.9%. Separately, because the attendance estimate is 60% or below, the attendance-support rule is triggered, so SARAH suggests attendance support for the tutor to review." |
| 3 | **Confirmatory, G1 only**: 80, 4, 0, G1 8, G2 blank → Predict | "Now the first grades are available, so we switch to Confirmatory mode. For this fictional student, we enter an attendance estimate of 80%, four study hours per week, no previous failures, and a G1 of 8 out of 20. There's no second grade yet, so we leave G2 blank, and SARAH uses the G1-only model. Using these inputs, the G1-only model predicts High Risk, with an estimated High-Risk probability of 81.8%. Separately, the assessment-review rule is triggered because G1 is below 10 out of 20. This suggestion is a prompt for discussion, not proof of what caused the prediction. Remember, this is only an estimate. It can be wrong, so the tutor should check other information too." |
| 4 | **Confirmatory, G1 + G2, High Risk**: 55, 1.5, 1, G1 9, G2 8 → Predict | "Here's a fictional student who already has both grades. We enter an attendance estimate of 55%, 1.5 study hours per week, one previous failure, and 9 and 8 out of 20 for G1 and G2. With both grades entered, SARAH uses the G1 plus G2 model and predicts High Risk, with an estimated High-Risk probability of 84.2%. Separately, all four agreed recommendation rules are triggered: the attendance estimate is 60% or below, study time is 1.5 hours or less, there is a previous failure, and the average grade is below 10 out of 20. So SARAH shows four targeted suggestions. These are prompts for a conversation, not proof of the cause." |
| 5 | **Confirmatory, G1 + G2, Low Risk**: 80, 4, 0, G1 12, G2 8 → Predict | "This fictional student has an attendance estimate of 80%, four study hours per week, no previous failures, and 12 and 8 out of 20 for G1 and G2. SARAH predicts Low Risk. The displayed 30% is the model's estimated probability of High Risk; it is not a 30% probability of Low Risk. The student receives routine guidance rather than targeted recommendations." |
| 6 | **Study-hours warning**, Confirmatory: 80, **40**, 0, G1 12, G2 blank → Predict; show the note under the study-hours box, the result and the yellow warning | "SARAH accepts study-hour estimates from zero to forty. However, our training-data conversion only used values up to twelve. Higher inputs receive a warning because the prediction extends beyond those training values and may be unreliable. Here, with 40 study hours, SARAH predicts High Risk at 66.1%, and the warning is shown with the result. Twelve is not a proven reliability boundary, and values below it are not guaranteed reliable either." |
| 7 | **Class CSV, invalid rows** (Confirmatory): upload `sample_roster.csv`; counts 4 / 2 / 2; C and D messages; full support suggestions | "For a whole class, the tutor uploads a CSV file. This file has four rows. The two valid rows are processed, while the two invalid rows are skipped with explanations: C's attendance estimate is 150, and D's G2 is 'NA'. Each message says how to fix the row. The full support suggestions are listed for each student." |
| 8 | **CSV with a 40-hour row and download**: remove the file (✕), upload `study_hours_warning_demo.csv`; counts 2 / 2 / 0; the summary line and full warning shown once; the table marks A with "Yes - see warning above"; click **Download results as CSV**; open the file and show the `input_warning` column (filled for A, blank for B) and the recommendations | "This second fictional file has a valid row with 40 study hours. The row is still processed, not skipped. On screen, the full warning is shown once, and the table marks student A. When the tutor downloads the results, the warning stays with that student in the input_warning column, next to the recommendations. Student B has no warning. In the file, the probability is a decimal, so 0.661 means 66.1%." |
| 9 | PowerShell test result (`Ran 110 tests … OK`), then user guide section 6 ("11 of the 26") | "Our recorded verification reports 110 passing automated tests. These check software behaviour, not prediction accuracy. The models were developed using 395 students from one mathematics-course dataset. On the 79 reserved test students, Early-Warning identified 11 of the 26 High-Risk students, so it missed some students and also raised false alarms. Attendance and study inputs are approximate, study hours above twelve receive a warning, and support suggestions are not proven interventions. SARAH should therefore support, rather than replace, a tutor's judgement." |
| 10 | Start screen | "Thank you." |

Expected values were checked against the dashboard after #108 (`2481be9`); predictions are
unchanged by #110, which only changes how the CSV warning is displayed.

## Record of the actual video

| Item | Value |
|---|---|
| Date recorded | 25 October 2026 |
| Commit shown | `847d460` |
| Length | 6 min 11 s |
| Filename | `SARAH_demonstration_v2.mp4` |
| Stored at (agreed location) | The team's Microsoft Teams workspace (link shared with the team; not public) |
| Peer check (who, date, plays fully, matches version) | Benjamin and Jackie watched the full video on 25 October 2026 and agreed it matches the demonstrated version |

The video file itself is not stored in Git unless the team decides otherwise.
