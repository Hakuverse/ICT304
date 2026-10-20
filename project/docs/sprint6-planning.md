# Sprint 6: Integration and User Testing

Working period: 13-20 October 2026. Owners confirmed by Benjamin on 19 October.
Milestone: [Sprint 6](https://github.com/Hakuverse/ICT304/milestone/6).

## Goal

Check that the complete SARAH prototype works together and is understandable to a user.
This is Phase D. Use project/ for changes and preserve the assignment-stage record.

## Tasks

| Issue | Work | Start after |
|---|---|---|
| [#65](https://github.com/Hakuverse/ICT304/issues/65) | Match project requirements to system tests | Review #56 and #57 |
| [#66](https://github.com/Hakuverse/ICT304/issues/66) | Run complete workflow checks on Windows and macOS | Test plan #65 and integrated Sprint 5 features |
| [#67](https://github.com/Hakuverse/ICT304/issues/67) | Check response times and larger CSV files | Targets in #65 and a working dashboard |
| [#68](https://github.com/Hakuverse/ICT304/issues/68) | Try the prototype with the tutor and collect feedback | Working prototype and demo #57 |
| [#69](https://github.com/Hakuverse/ICT304/issues/69) | Fix and recheck integration and feedback problems | Failures or agreed feedback from #66-#68 |
| [#70](https://github.com/Hakuverse/ICT304/issues/70) | Update project evidence and plan the final stages | Evidence from #65-#69 |

Owners: Benjamin #65/#70, Jackie #66/#67, Anna #68/#69.
The sections below retain the sprint plan. For actual outcomes and the
20 October handover, see the [Sprint 6 review](sprint6-review.md).

## Suggested order

1. Review the Sprint 5 demo and any unfinished work.
2. Agree the test table and targets in #65.
3. Run platform checks, timing checks and user trials (#66-#68).
4. Fix and recheck the problems found (#69).
5. Update the report evidence and next-stage plan (#70).

## End-of-sprint check

- Each required workflow has a passed, failed or pending result and evidence.
- Windows and macOS results identify the actual version tested.
- Tutor/user feedback and agreed changes are recorded.
- Remaining problems have an owner and next action.

## After Sprint 6

Phase E covers the deployment and maintenance plan, user guide and demo video.
Phase F covers closeout, report polish, presentation slides, rehearsal and final
submission. The final project is due on 7 November 2026. Keep model evaluation
separate from software and user testing, and link the evidence in the final report.

## Input from the 13 October meeting

The tutor feedback in [#57's meeting record](prototype-demo-notes.md) was positive,
with no specific changes requested. The team proposed clearer recommendation
wording, larger text areas and wrapping long result messages. Review these in
#68 and implement agreed changes through #69; keep approved rule boundaries
unchanged unless the team separately agrees a rule change.

Start #65 using the merged #56 Windows evidence and the meeting feedback.
Then run #66-#68 against the agreed test plan, address findings in #69 and update
records in #70. The team agreed the ownership below and the readability proposals:
wrapping messages, clarifying wording, then resizing fields where needed. Specific
changes from #68 still require agreement. The demo does not replace user trials.

## Agreed two-issue split - confirmed 19 October 2026

| Person | Issues | Why these fit together |
|---|---|---|
| Benjamin | #65 and #70 | Define the test/evidence table, then bring the resulting evidence into project notes and the next-stage plan. |
| Jackie | #66 and #67 | Coordinate platform workflow checks and timing checks using the same tested version. Benjamin can supply the Windows run; Jackie can run macOS. |
| Anna | #68 and #69 | Collect usability findings, agree improvements, then implement and recheck the changes. |

This allocation is agreed; it is not a claim of equal workload. #69 may need
help if several fixes are found. #70 finishes after other results arrive; its
outline can be prepared early. Readability ideas are agreed as team proposals,
not completed changes. Review #68's specific findings before implementing #69.

## Test plan

Use the [system test plan](system-test-plan.md) for S6-01 to S6-24. It links
earlier evidence separately from new run records. Team review and target agreement
were recorded on 19 October 2026. The table now links Windows and macOS functional results, reference-device
timings and both usability retests. S6-21 remains not met and S6-22 partly met.
The [review](sprint6-review.md) records their follow-up without changing the
historical outcomes.

## Handover to the next sprints

- [Sprint 7](sprint7-planning.md): Phase E, 20-27 October, issues #77-#82.
- [Sprint 8](sprint8-planning.md): Phase F, 27 October-3 November, issues #93-#98.
- Final corrections and actual submission: 4-7 November; confirm the LMS cutoff.

As checked on 20 October, #65–#69 are closed and their evidence is merged.
#70 closes after its consolidation PR is reviewed and merged; milestone 6 can
then close. The confirmed Sprint 7 split is Benjamin #77/#78, Anna #79/#81 and
Jackie #80/#82. Remaining usability explanations continue in #79/#80.
Sprint closure does not mean that every usability target passed.
