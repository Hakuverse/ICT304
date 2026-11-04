# Sprint 6 evidence and handover

Prepared by Benjamin on 20 October 2026 for issue #70.
Repository checked at `6bc1c18` after PRs #101 and #102 merged. This is an
evidence summary, not a new test run or a claim that every usability target passed.

## Completed work

| Issue | Owner | Outcome and merged PRs |
|---|---|---|
| [#65](https://github.com/Hakuverse/ICT304/issues/65) | Benjamin | Test plan and team-agreed targets: [#85](https://github.com/Hakuverse/ICT304/pull/85) |
| [#66](https://github.com/Hakuverse/ICT304/issues/66) | Jackie; Windows run by Benjamin | Functional evidence: [#88](https://github.com/Hakuverse/ICT304/pull/88), [#90](https://github.com/Hakuverse/ICT304/pull/90) |
| [#67](https://github.com/Hakuverse/ICT304/issues/67) | Jackie | Reference-device response times: [#101](https://github.com/Hakuverse/ICT304/pull/101) |
| [#68](https://github.com/Hakuverse/ICT304/issues/68) | Anna | Initial user feedback and agreed changes: [#84](https://github.com/Hakuverse/ICT304/pull/84) and [feedback record](usability-feedback.md) |
| [#69](https://github.com/Hakuverse/ICT304/issues/69) | Anna | Fixes #86, #87, #92 and #100; evidence/status updates #89, #91 and [#102](https://github.com/Hakuverse/ICT304/pull/102). Remaining limitations below. |
| [#70](https://github.com/Hakuverse/ICT304/issues/70) | Benjamin | Summary and handover reviewed and merged in PR #103; #70 is closed. |

The PRs and their review histories record the team's implementation and review
work. Target agreement was recorded on 19 October in #85. Benjamin confirmed the
Sprint 7 allocation on 20 October. This document does not claim another meeting
or additional testing took place.

## Requirements and evidence

Use the [system test plan](system-test-plan.md) for every case and subcase.

| Requirement | Evidence | Recorded outcome and scope |
|---|---|---|
| Setup, validation, three model setups, form/CSV results and downloads | S6-01–S6-16: [Windows](evidence/issue66/windows/2026-10-19-9dc7132/results.md), [macOS](evidence/issue66/macos/2026-10-19-9dc7132/results.md) | Passed at `9dc7132` on 19 October; macOS S6-11 missing-attendance retest on 20 October at the same commit. Each run records 99 automated tests. |
| Fixed recommendation rules, boundaries and High-Risk-only targeted support | S6-17–S6-18 in those platform records; [rules](recommendation-rules.md), [rule tests](../code/test_recommend.py) | Passed. Low-Risk results remain visible with routine guidance. The separate 11 recommendation tests are included in the 99, not added to them. |
| Form and CSV response time | S6-19–S6-20: [results](evidence/issue67/2026-10-20-6395d82/results.md), [individual timings](evidence/issue67/2026-10-20-6395d82/timings.md) | All 11 scenarios met targets on Jackie's reference Mac at `6395d82`, 20 October. Windows timing was not required by the agreed reference-device target. |
| Find modes and understand inputs | S6-21: [19 October retest](evidence/issue69/2026-10-19-9dc7132/results.md) | Target not met: first task assisted; attendance not described as an estimate. No later pass is claimed. |
| Understand probability and human review | S6-22: [20 October retest](evidence/issue69/2026-10-20-e246495/results.md) | Partly met at `e246495`: human review understood; probability as an uncertain model estimate not explained. Follow-up #79, Anna. |
| Explain and correct skipped rows | S6-23: [20 October retest](evidence/issue69/2026-10-20-e246495/results.md) | Met without help after #92. Same tester had received explanations in the earlier session; improvement cannot be attributed to wording alone. |
| Read complete messages and use controls | S6-24: [20 October retest](evidence/issue69/2026-10-20-e246495/results.md) | Changed CSV view passed at 1366 × 768 and 1920 × 1080, 100% zoom. Unchanged form evidence remains from 19 October. |

Anna's [20 October test log](evidence/issue69/2026-10-20-e246495/test-output.txt)
records 106 tests passing at `e246495`. Earlier 99-test logs remain correct for
their versions. The timing run predates #92/#100; do not relabel it as a timing
run of the final UI. Run affected checks if later changes alter the workflow.

## Response-time summary

Jackie used a standalone stopwatch and restarted the Streamlit process for each
cold run, followed by five warm runs. Timing covered visible dashboard results;
server startup, file choosing and saving downloads were excluded.

| Scenario group | Cold target | Each warm target | Highest recorded cold / warm |
|---|---|---|---|
| Three single-student setups | 10 s | 3 s | 1.53 / 0.39 s |
| 30-row valid/mixed CSV, both modes | 10 s | 5 s | 1.97 / 1.00 s |
| 395-row valid/mixed CSV, both modes | 20 s | 10 s | 2.81 / 1.95 s |

These are manual measurements on one reference computer. They are not accuracy
results, multi-user load tests, or a performance guarantee on other computers.

## Model results remain the baseline

The [evaluation report](evaluation_report.md) compares Logistic Regression and
Decision Tree across three input setups and two class-weight settings (12
comparisons). Five-fold validation on 316 development students guided selection;
79 reserved students were used for the separate test results.

| Setup | Selected model | Reserved-test High-Risk recall |
|---|---|---|
| Early-Warning | Balanced Decision Tree, depth 4 | 0.423 |
| Confirmatory, G1 only | Balanced Logistic Regression | 0.769 |
| Confirmatory, G1 and G2 | Balanced Logistic Regression | 0.885 |

These are retained model results, not new Sprint 6 validation. See the
[comparison and limitations](issue33_report.md) for false alarms, missed students,
feature importance and confusion matrices. The small dataset, proxy attendance
and study inputs, uncalibrated probabilities and absence of week-by-week records
limit interpretation. No day-one accuracy, causal effect or intervention benefit
has been established. Software tests do not remove those limitations.

## Remaining limitations and next actions

| Item | Owner / next action |
|---|---|
| S6-21 assisted task and attendance-estimate explanation | Anna: make the steps and proxy inputs clear in #79; Benjamin: record any help needed during the #80 walkthrough. Keep the original unmet result. |
| S6-22 probability understanding partly met | Anna: explain model uncertainty and human review in #79, as recorded in #102. Benjamin checks the guide in #80; a teammate walkthrough is not a new independent-user study. |
| One repeat usability tester, prior coaching and one browser | Retain these limits in the report under #70/#93. Do not claim all users can use the system independently. |
| Timing on one device and an earlier UI version | Retain original commit and method. Benjamin flags any affected checks during #80/#82 if later changes affect performance. |
| macOS S6-16 input-change clearance partly confirmed by tester | Preserve the limitation in the macOS results; do not describe its screenshots alone as proof of the cleared state. |

## Sprint 7 and final-stage handover

Benjamin confirmed this Sprint 7 split on 20 October 2026:

| Owner | Issues | Output by the 27 October review |
|---|---|---|
| Jackie | #77, #78 | Local deployment instructions and maintenance/recovery plan |
| Anna | #79, #81 | User guide including the usability follow-up, and reviewed demo video |
| Benjamin | #80, #82 | Teammate guide walkthrough and Phase E review/handover |

See [Sprint 7](sprint7-planning.md) for dependencies. Sprint 8 (27 October–3
November) covers report/forms, slides/rehearsal and package/readiness checks in
[#93–#98](sprint8-planning.md). The updated Sprint 8 allocation gives Benjamin the report and final checking/
submission, and Anna the slides, with review by the other two. Practical
sessions, speaking parts and the backup uploader are separate decisions. Keep 4–7 November
for final corrections and submission, and confirm the exact LMS cutoff.

## Closure

Issues #65–#70 are closed with merged evidence, including PR #103 for #70.
Milestone 6 was closed on 23 October. Closing the sprint
accepts the documented handover; it does not turn S6-21 or S6-22 into passes.
