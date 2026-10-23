# Demonstration video notes (#81)

Owner: Anna. Peer check: Benjamin and Jackie, 22 October 2026.

## Requirements from the brief

No video-specific rules (length, format, presenters or submission method) were found in the
project brief (checked by Anna on 23 October 2026). The five-minute meeting limit was not assumed
to apply to the video. If the LMS or tutor later gives video rules, check this video against them
before submission.

## Version shown and recording setup

- Commit: `ddedc0f` (main after PR #106). The dashboard, data and models are unchanged since `fe9685a`,
  the version used in the user guide screenshots.
- Computer: Windows laptop, Microsoft Edge in full screen (F11), 100% zoom.
- Recorded with a Microsoft Teams meeting recording (camera off, narration, screen shared).
- Screens shown: the SARAH dashboard; a PowerShell window showing the automated test run
  (`Ran 106 tests … OK`); the [user guide](user-guide.md) section 6 on GitHub; the downloaded results CSV.
- Data: fictional students only (typed examples and `project/data/sample_roster.csv`).
  No real student data, private messages or declarations are shown.

## Outline and script

The narration was revised after team review so that it does not claim proven early accuracy,
keeps the model prediction separate from the recommendation rules, explains that the displayed
percentage is the estimated probability of High Risk, and states the limitations.

| # | Show on screen | Say |
|---|---|---|
| 1 | Start screen with the support notice | "This is SARAH, the Student Academic Risk Assistance Hub. It estimates academic risk and provides support suggestions for a tutor to review. It supports predictions without grades and predictions using available grades. It does not make decisions about students." |
| 2 | **Early-Warning**: attendance 40, study hours 4, failures 0 → Predict | "Early-Warning mode uses an attendance estimate, study hours and past failures, without G1 or G2. It is intended to support earlier review, but our dataset does not establish how accurately it works at the beginning of a course. Here, we use fictional example inputs. For this fictional student, we enter an attendance estimate of 40%, four study hours per week and no previous failures. SARAH predicts High Risk, with an estimated High-Risk probability of 85.9%. Separately, because the attendance estimate is 60% or below, the attendance-support rule is triggered, so SARAH suggests attendance support for the tutor to review." |
| 3 | **Confirmatory, G1 only**: 80, 4, 0, G1 8, G2 blank → Predict | "Now the first grades are available, so we switch to Confirmatory mode. For this fictional student, we enter an attendance estimate of 80%, four study hours per week, no previous failures, and a G1 of 8 out of 20. There's no second grade yet, so we leave G2 blank, and SARAH uses the G1-only model. Using these inputs, the G1-only model predicts High Risk, with an estimated High-Risk probability of 81.8%. Separately, the assessment-review rule is triggered because G1 is below 10 out of 20. This suggestion is a prompt for discussion, not proof of what caused the prediction. Remember, this is only an estimate. It can be wrong, so the tutor should check other information too." |
| 4 | **Confirmatory, G1 + G2, High Risk**: 55, 1.5, 1, G1 9, G2 8 → Predict | "Here's a fictional student who already has both grades. We enter an attendance estimate of 55%, 1.5 study hours per week, one previous failure, and 9 and 8 out of 20 for G1 and G2. With both grades entered, SARAH uses the G1 plus G2 model and predicts High Risk, with an estimated High-Risk probability of 84.2%. Separately, all four agreed recommendation rules are triggered: the attendance estimate is 60% or below, study time is 1.5 hours or less, there is a previous failure, and the average grade is below 10 out of 20. So SARAH shows four targeted suggestions. These are prompts for a conversation, not proof of the cause." |
| 5 | **Confirmatory, G1 + G2, Low Risk**: 80, 4, 0, G1 12, G2 8 → Predict | "This fictional student has an attendance estimate of 80%, four study hours per week, no previous failures, and 12 and 8 out of 20 for G1 and G2. SARAH predicts Low Risk. The displayed 30% is the model's estimated probability of High Risk; it is not a 30% probability of Low Risk. The student receives routine guidance rather than targeted recommendations." |
| 6 | **Class CSV** in Confirmatory: upload `sample_roster.csv`; counts 4 / 2 / 2; C and D skipped messages; full support suggestions; click **Download results as CSV**; open the downloaded file showing A and B with recommendations | "For a whole class, the tutor uploads a CSV file. This file has four rows. The two valid rows are processed, while the two invalid rows are skipped with explanations: C's attendance estimate is 150, and D's G2 is 'NA'. Each message says how to fix the row. The full support suggestions are listed for each student. Finally, the tutor can download the results. The downloaded file contains students A and B with their recommendations. In the file, the probability is written as a decimal, so 0.155 means 15.5%." |
| 7 | PowerShell test run (`Ran 106 tests … OK`), then the user guide section 6 | "Our recorded verification reports 106 passing automated tests. These check software behaviour, not prediction accuracy. The models were developed using 395 students from one mathematics-course dataset. On the 79 reserved test students, Early-Warning identified 11 of the 26 High-Risk students, so it missed some students and also raised false alarms. Attendance and study inputs are approximate, and support suggestions are not proven interventions. SARAH should therefore support, rather than replace, a tutor's judgement." |
| 8 | Start screen | "Thank you." |

Expected values were checked against the dashboard at `ddedc0f`.

## Record of the actual video

| Item | Value |
|---|---|
| Date recorded | 22 October 2026 |
| Commit shown | `ddedc0f` |
| Length | 6 min 25 s |
| Filename | `SARAH_demonstration.mp4` |
| Stored at (agreed location / link) | The team's Microsoft Teams workspace (link shared with the team; not public) |
| Peer check (who, date, plays fully, matches version) | Benjamin and Jackie watched the video on 22 October 2026 |

The video file itself is not stored in Git unless the team decides otherwise.
