# Prototype demonstration record - Issue #57

## Meeting record

- Date: 13 October 2026.
- Attendees: Benjamin, Anna, Jackie and Tutor.
- Record provided by: Benjamin.
- Status: tutor feedback recorded; live CSV follow-up and Sprint 6 ownership
  remain outstanding before closing #57.
- Demonstration basis: Benjamin used the recent issue #56 work. Its tested code
  commit was `2bbb083074e265bb8931b053bd262bbf47d29b19`. The exact checkout
  commit used at the meeting was not recorded; the test commit is a reference,
  not a confirmed meeting checkout.
- Earlier checks: Benjamin's Windows P1-P16 checks on 12 October, recorded in
  [issue #56 evidence](prototype-test-checklist.md) and merged PR #76. The suite
  showed 89 passing tests. This is separate from the tutor meeting.

## Tutor feedback

| Question | Response reported by Benjamin |
|---|---|
| Are the two modes and G1/G2 requirements clear? | Yes, clear. |
| Are the risk label, probability and support messages understandable? | Yes, easy to understand. |
| Do the skipped-row messages explain what needs correcting? | Yes. |
| What should improve before the next demonstration? | No specific changes suggested; the current prototype is suitable to proceed to the next steps. |

The tutor gave positive feedback on the current design and did not request
specific changes. This records feedback on the demonstration, not independent
acceptance testing, proof of predictive accuracy or approval of intervention
outcomes. Recommendation rules remain the team's internal decision.

## Demonstration coverage

Benjamin confirmed that the team briefly went through the prediction examples
from issue #56: Early-Warning, Confirmatory with G1 only, and Confirmatory with
G1 and G2. CSV handling with invalid rows was mentioned, not demonstrated live.
The tutor's positive response about skipped-row messages reflects that discussion;
it must not be described as a hands-on CSV usability check.

The mixed valid/invalid CSV behaviour already has Windows evidence under #56.
The live CSV example requested by #57 still needs a short follow-up demonstration,
or an explicit team decision to accept the existing evidence in its place.
Whether model results, limitations and human review were explained at the meeting
was not recorded in the supplied account and needs confirmation.

## Team improvement ideas

These ideas came from the team, not the tutor. They are proposals for Sprint 6
review; no UI or recommendation changes are implemented by this record.

| Proposal | Next action | Follow-up | Owner |
|---|---|---|---|
| Make the UI easier to read | Choose specific screens and identify what is difficult to read | #68, then #69 if agreed | To agree |
| Explain recommendation reasons more clearly | Review wording while preserving the approved thresholds and human-review limitation | #68 and #69 | To agree |
| Make text areas larger where needed | Identify the field or results area and check it at the intended screen size | #68 and #69 | To agree |
| Wrap long messages onto two or three lines where practical | Check form and CSV result displays; avoid requiring one long line or hiding the message | #68 and #69 | To agree |

Prioritise observed functional failures first. Then agree which readability
changes are useful, implement them in a separate PR and recheck affected cases.
A clearer rule explanation must not imply that a feature caused the risk.

## Next steps and completion

1. Complete the live CSV follow-up or record the team's decision to use the
   existing #56 evidence. Confirm whether results, limitations and human review
   were explained; cover them at the follow-up if needed. The unrecorded exact
   meeting commit is explicitly noted above.
2. Agree Sprint 6 priorities and owners for #65-#70; the suggested split is in the
   [Sprint 6 plan](sprint6-planning.md).
3. Start #65 by mapping requirements to tests. Use #66 for Windows/macOS
   checks, #67 for response times and #68 for observed user tasks.
4. Use #69 for agreed fixes and improvements, and #70 for report evidence.
5. Have a teammate review this record and link its PR in #57 before closing it.

No software failures were reported in the supplied meeting feedback. macOS
coverage, response-time results and independent usability checks remain separate
Sprint 6 work. The [current workflow](system-workflow.md) still describes the
implemented system; suggested layout changes do not alter that workflow yet.

Phase E covers deployment/maintenance, user guide and demo video. Phase F covers
closeout, polish, rehearsal and final submission.
