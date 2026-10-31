# Sprint 7 review and Phase F handover

Prepared by Benjamin on 27 October 2026 for issue #82.
Status: Anna approved PR #111 on 27 October 2026 and it was merged. Issue #82 is closed; milestone 7 was closed on 30 October.
This is a repository handover record, not a claim that a team meeting took place.

## Version and completed outputs

Reviewed main: `914f808f5e6cf0df7a17331c088859e3f46607b5`, after PR #107.
The final video uses `847d460`; #107 adds notes without changing code or models.

| Issue | Output | Merged record |
|---|---|---|
| #77 | [Local deployment guide](deployment-guide.md) | [#104](https://github.com/Hakuverse/ICT304/pull/104); later setup clarification in #108 |
| #78 | [Maintenance and recovery plan](maintenance-plan.md) | [#105](https://github.com/Hakuverse/ICT304/pull/105) |
| #79 | [User guide](user-guide.md) | [#106](https://github.com/Hakuverse/ICT304/pull/106), [#109](https://github.com/Hakuverse/ICT304/pull/109) |
| #80 | [Teammate walkthrough](guide-walkthrough.md), Python fallback and [study-hours limitation](study-hours-limitation.md) | [#108](https://github.com/Hakuverse/ICT304/pull/108); CSV display follow-up [#110](https://github.com/Hakuverse/ICT304/pull/110) |
| #81 | [Video notes](demo-video-notes.md) and final video file | [#107](https://github.com/Hakuverse/ICT304/pull/107) |
| #82 | This review, linked outputs and [Phase F plan](sprint8-planning.md) | Reviewed by Anna; merged [#111](https://github.com/Hakuverse/ICT304/pull/111) |

Issues #77–#82 are closed. The project README links these outputs. The guides,
[current workflow](system-workflow.md) and warning descriptions have been aligned
with the reviewed implementation. The submission package will receive its own
clean-copy check under #97; this review does not claim that check has happened.

## Walkthrough and video findings

Benjamin's Windows walkthrough on 23 October at `ddedc0f` passed the reported
workflow steps with 106 automated tests. The initial Python command needed the
`py -3.12` fallback, now documented. These screenshots predate the warning.
The 24 October warning follow-up records 109 passing tests; the final video notes
report Anna's 110-test run at `847d460`. Keep these separate dated records.

The 40-hour example exposed extrapolation beyond converted training values.
Inputs remain valid from 0–40. Values above 12 receive a warning in the form and
CSV workflow. The screen uses `study_hours_warning` markers and the download
keeps full `input_warning` text. The warning applies to either risk label and
does not change predictions or High-Risk-only targeted support rules.

Anna's final video is `SARAH_demonstration_v2.mp4`, recorded 25 October, length
6 minutes 11 seconds. The merged notes record Benjamin and Jackie's full review
on 25 October. Benjamin confirmed on 27 October that it plays completely and
matches the screen. The file is stored in the team's Teams workspace. Submit the
video file as required by the brief; an optional viewing link does not replace it.

## Limits retained for the final report

- [Sprint 6 review](sprint6-review.md): S6-21 remains not met and S6-22 partly met.
  #79/#80 provide explanations and teammate feedback, not an independent user study
  or new passes for those original cases. Retain the findings from #68/#69.
- Windows/macOS functional evidence at `9dc7132` and timing evidence at `6395d82`
  are historical. They are not new platform/timing runs on this handover commit.
- Maintenance includes a recovery plan, not an executed recovery drill. No ongoing
  hosted service or post-project support commitment has been established.
- The model evaluation is the retained assignment baseline. Early-Warning missed
  15 of 26 High-Risk test students. Inputs are approximate, probabilities are not
  established as calibrated, and recommendations are not proven interventions.
- The study-hours warning explains uncertainty; it does not improve accuracy.
  Twelve is not a proven reliability boundary. Do not replace higher inputs with 12.
- Historical user-guide screenshots retain their version labels. The final video
  demonstrates the later warning behaviour. The local application trial is separate.

## Phase F work and remaining decisions

The reviewed handover records shared work by Benjamin, Anna and Jackie on
#93–#98 rather than exclusive pairs. The [Sprint 8 plan](sprint8-planning.md)
sets out proposed intermediate dates, the 3 November readiness review and
4–7 November correction/submission period. All three members are included as
contributors; record actual editors, testers, presenters and reviewers as work happens.

| Next action | Responsible people / existing issue | Target |
|---|---|---|
| Agree practical editing/session schedule when work resumes | Benjamin coordinates with Anna and Jackie; #93–#98 | Paused on 31 October |
| Review report and private declarations | Team; #93/#94 | By 3 November |
| Prepare slides, agree presenters and rehearse | Team; #95/#96 | Draft by 30 October; rehearsal by 2 November (proposed) |
| Choose submission commit and check extracted package | Team; #97 | By 3 November |
| Confirm LMS cutoff/formats, uploader, backup and support limits | Team; #94/#98 | By the 3 November readiness review |
| Final corrections and actual upload | Uploader and backup to be agreed; #98 | 4–7 November, before confirmed LMS cutoff |

Keep personal details, signed forms and upload receipts private. Do not mark
rehearsal, package checks, signatures or submission complete before they happen.

## Peer review and closure

- [x] Link the merged Phase E outputs and record the current version.
- [x] Consolidate walkthrough/video findings and preserve historical limits.
- [x] Prepare the Phase F checklist and proposed shared work.
- [x] Anna reviewed and approved the handover in PR #111 on 27 October.
- [x] PR #111 merged and #82 closed; milestone 7 closed on 30 October.

Shared Sprint 8 work is the reviewed handover approach. Specific session dates,
presenters and submission roles are separate decisions, not implied by PR approval.

Sprint 7 is closed. The later 31 October allocation makes Benjamin the report
lead and Anna the slide lead, with review by the other two. Benjamin leads final
checking/submission. See the updated Sprint 8 plan; planned actions above are not completed results.
