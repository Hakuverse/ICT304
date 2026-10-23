# Sprint 7: Deployment, User Guide and Demo Video

Working period: 20-27 October 2026. Phase E.
Milestone: [Sprint 7](https://github.com/Hakuverse/ICT304/milestone/7).
Prepared: 20 October 2026. Allocation confirmed by Benjamin on 20 October.

## Goal

Help someone else set up and use the tested SARAH prototype. Prepare the local
deployment instructions, maintenance plan, user guide and demonstration video.
This is local Streamlit deployment; public hosting is not an agreed deliverable.

## Tasks

| Issue | Work | Start after | Planned output |
|---|---|---|---|
| [#77](https://github.com/Hakuverse/ICT304/issues/77) | Local deployment and handover instructions | #66 platform evidence and #69 fixes; draft early | `project/docs/deployment-guide.md` |
| [#78](https://github.com/Hakuverse/ICT304/issues/78) | Maintenance and recovery plan | Deployment draft and test findings | `project/docs/maintenance-plan.md` |
| [#79](https://github.com/Hakuverse/ICT304/issues/79) | Beginner-friendly user guide | Reviewed dashboard behaviour and user feedback | `project/docs/user-guide.md` |
| [#80](https://github.com/Hakuverse/ICT304/issues/80) | Teammate walkthrough of the guides | #77 and #79 drafts | `project/docs/guide-walkthrough.md` |
| [#81](https://github.com/Hakuverse/ICT304/issues/81) | Record and check the demonstration video | Stable reviewed version and guide | `project/docs/demo-video-notes.md` and video in the agreed location |
| [#82](https://github.com/Hakuverse/ICT304/issues/82) | Review Phase E and hand over to Phase F | #70 and the Phase E outputs | `project/docs/sprint7-review.md` |

These paths are planned outputs, not claims that the files or work are complete.
Use the existing [project setup instructions](../README.md) and
[mode guide](mode-guide.md) so commands and input rules stay consistent.

## Agreed allocation

| Owner | Issues | Responsibility |
|---|---|---|
| Jackie | #77 and #78 | Local setup, maintenance and recovery plans |
| Anna | #79 and #81 | User guide, outstanding usability explanations and demo video |
| Benjamin | #80 and #82 | Teammate walkthrough, Phase E review and next-stage handover |

The guide walkthrough is done by someone other than its author. All members
help with reviews. This allocation was confirmed by Benjamin on 20 October.

## Work carried forward

[Sprint 6 evidence](sprint6-review.md) is consolidated under #70. Issues #65–#69
are closed with merged records. After #70 merges, close milestone 6 and use this
plan for Phase E.

Anna's #79 guide must explain attendance as an estimate, the prediction steps,
and probability as a model estimate that can be wrong. S6-21 was not met and
S6-22 was partly met; those results remain unchanged. Benjamin records any help
needed while following the guide in #80. This is a teammate walkthrough, not
proof of independent-user success. Record later findings as a new dated check.

Use the reviewed version for final screenshots and video. Earlier platform and
timing records keep their original tested commits. Retest affected cases after
code changes; do not describe historical evidence as a fresh run.

## Order for the week

1. Use the confirmed owners and review the Sprint 6 limitations and handover.
2. Draft the deployment, maintenance and user guides in parallel.
3. Have another teammate follow the instructions and record any help needed.
4. Correct the guides, choose the demo commit and confirm video requirements from the brief.
5. Record and peer-check the video using fictional students.
6. At the 27 October review, link the actual outputs and agree the Sprint 8 handover.

## End-of-sprint check

- Setup instructions cover Windows and macOS and link actual platform evidence.
- The maintenance plan explains updates, recovery and who will provide support.
- The user guide covers both modes, CSV errors, downloads and human review.
- The walkthrough and video have a date, version and teammate review.
- Any unmet test target or unfinished item has an owner and next action.

Next: [Sprint 8 planning](sprint8-planning.md), 27 October-3 November.
The final project deadline remains 7 November; confirm the exact LMS cutoff.
The team makes scope and priority decisions; no extra tutor approval is required.


## 24 October update before the final video

The #77–#79 guides are merged. Benjamin's #80 walkthrough and the study-hours
warning are in PR #108, awaiting review/merge. Anna's video notes are in PR #107;
#81 remains open. Record the final video after #108 is accepted, using the merged
commit. Keep the original demonstration examples, add the 40-hour warning and
its CSV export, and show the actual current automated test result (109 expected).
Record actual recording and peer-review dates. Submit a video file as required
by the brief; a viewing link is an additional convenience. #82 remains the
Phase E review after these outputs are accepted. The local application trial is
not the version to demonstrate.
