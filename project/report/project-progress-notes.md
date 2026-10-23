# Project progress notes - updated 20 October 2026

SARAH currently supports single-student and class CSV predictions using
Early-Warning, G1-only Confirmatory and G1+G2 Confirmatory models. Invalid CSV
rows are skipped with reasons while valid rows are processed. Targeted support
suggestions apply to High-Risk predictions; Low-Risk results receive routine
guidance. Suggestions require human review and do not establish causes.

Benjamin completed the Windows integration checks on 12 October 2026. The
[evidence record](../docs/prototype-test-checklist.md) identifies the tested
commit, P1-P16 results and screenshots, including 89 passing automated tests.
These software checks do not measure predictive accuracy. The existing model
results remain the [baseline evaluation](../docs/evaluation_report.md).

At the 13 October meeting, attended by Benjamin, Anna, Jackie and Tutor, the
tutor found the modes, results, support messages and skipped-row explanations
clear. No specific changes were requested, and the tutor indicated that the
prototype could proceed to the next steps. This is demonstration feedback,
not evidence of independent user testing or real-world prediction performance.
The prediction examples were briefly covered using the issue #56 work. Invalid
CSV handling was discussed, not demonstrated live. The exact meeting checkout
commit was not recorded. See the [meeting record](../docs/prototype-demo-notes.md)
for the confirmed decisions. The team accepted #56 CSV evidence for this review.
Benjamin confirmed that estimated probabilities, possible prediction errors and
human review were explained during the meeting.

The Sprint 6 fixes added clearer field help, human-review notices, readable
support messages and plain-language skipped-row corrections. PR #100 removed
repeated recommendations from the CSV table while keeping the full suggestions
below it and in the download. The [current workflow](../docs/system-workflow.md)
shows how the implemented parts fit together.

## Sprint 6 results

The [Sprint 6 evidence summary](../docs/sprint6-review.md) links the requirements,
subsystem checks, full-system results, review history and handover. The
[system test plan](../docs/system-test-plan.md) retains each actual case outcome.

- Benjamin's Windows run and Jackie's macOS run passed S6-01–S6-18 at `9dc7132`
  with 99 automated tests each. The macOS missing-attendance retest was recorded
  on 20 October at the same commit. PRs #88 and #90 are merged.
- Jackie's reference-device timings at `6395d82` met the agreed S6-19/S6-20
  targets for all three form setups and all eight CSV scenarios. PR #101 is
  merged. These manual measurements describe that device/version, before the
  latest UI changes; they do not establish performance on every computer.
- Anna's 20 October retest at `e246495` records 106 automated tests passing.
  S6-23 was met without help, and the changed CSV view passed S6-24 readability
  checks at both agreed sizes. PR #102 is merged. The same tester had previously
  received explanations, so improved results may partly reflect familiarity.
- S6-21 remains not met from the earlier assisted task. S6-22 remains partly
  met: the tester understood human review but did not explain probability as
  an estimate that can be wrong. Anna carries the explanation work into #79;
  Benjamin checks the guide in #80. Closing #69 does not mean every target passed.

## Model evaluation and limitations

The existing [evaluation](../docs/evaluation_report.md) compares Logistic
Regression and Decision Tree across 12 development combinations. Model selection
uses 316 development students; the separate results use 79 reserved students.
Selected models are the balanced depth-4 Decision Tree for Early-Warning and
balanced Logistic Regression for each Confirmatory setup. Reserved-test
High-Risk recalls are 0.423, 0.769 and 0.885 respectively. These are the retained
baseline results, not new Sprint 6 model validation.

The [comparison discussion](../docs/issue33_report.md) explains missed students,
false alarms, feature importance and data limitations. Attendance and study
hours are proxy estimates, probabilities are not established as calibrated,
and the dataset does not demonstrate day-one accuracy. Fixed recommendations
suggest discussion topics, not causes or proven interventions. Functional test
passes and fast responses do not remove those limits.

## Remaining stages

| Period | Work and owners | Plan |
|---|---|---|
| Sprint 6 closeout | Benjamin: merge the reviewed #70 evidence/handover PR, then close milestone 6 | [Review](../docs/sprint6-review.md) |
| 20–27 October | Jackie #77/#78; Anna #79/#81; Benjamin #80/#82 | [Sprint 7](../docs/sprint7-planning.md) |
| 27 October–3 November | Report/forms, slides/rehearsal, package/readiness checks #93–#98; Benjamin coordinates owner agreement under #82 | [Sprint 8](../docs/sprint8-planning.md) |
| 4–7 November | Final corrections and actual submission before the confirmed LMS cutoff | Handover under #98 |

Benjamin confirmed the Sprint 7 split on 20 October. Sprint 8 individual owners
remain to be agreed. These dates describe planned work, not completed guides,
rehearsals or submission.


## Study-hours input warning and limitation

The accepted range remains 0–40. Values above 12 receive an input warning because
training categories were converted to 1.5, 3.5, 7.5 and 12 hours. Twelve is an
assumed conversion value, not a real maximum or a proven reliability boundary.
Values at or below 12 are not guaranteed reliable either. Do not substitute 12
for a higher value to avoid the warning. Valid rows remain processed.
Warnings apply to either risk label in both modes, separately from support rules.
The `input_warning` column stays with each CSV result and export; it is blank
when no warning applies. See the [finding and critical discussion](../docs/study-hours-limitation.md).


## 24 October status clarification

The earlier Phase E paragraph describes the plan as recorded on 20 October.
Deployment, maintenance and user guides are now merged (#104–#106). The #80
walkthrough and input warning are under review in #108; #81's final recording
update and #82 handover are still outstanding. Current warning-branch checks
passed 109 tests; original 106-test evidence keeps its original date and commit.
