# Prototype demonstration record - Issue #57

## Meeting record

- Date: 13 October 2026.
- Attendees: Benjamin, Anna, Jackie and Tutor.
- Record provided by: Benjamin.
- Status: meeting and team decisions recorded; ready for teammate review in PR #83.
- Follow-up decisions confirmed by Benjamin on 19 October 2026.
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

The team agreed to use the completed issue #56 Windows CSV evidence for this
initial review rather than require a repeat live demonstration. Further CSV
workflow and usability checks continue in #66 and #68. This does not change the
record that CSV handling was discussed, not demonstrated live at the meeting.

Benjamin confirmed on 19 October that the meeting covered the model results and
all three limitations: probabilities are estimates, predictions can be wrong,
and recommendations require human review and do not prove the cause of risk.

## Team improvement ideas

These ideas came from the team, not the tutor. They are proposals for Sprint 6
review; no UI or recommendation changes are implemented by this record.

| Proposal | Next action | Follow-up | Owner |
|---|---|---|---|
| Make the UI easier to read | Choose specific screens and identify what is difficult to read | #68, then #69 if agreed | Anna (#68/#69) |
| Explain recommendation reasons more clearly | Review wording while preserving the approved thresholds and human-review limitation | #68 and #69 | Anna (#68/#69) |
| Make text areas larger where needed | Identify the field or results area and check it at the intended screen size | #68 and #69 | Anna (#68/#69) |
| Wrap long messages onto two or three lines where practical | Check form and CSV result displays; avoid requiring one long line or hiding the message | #68 and #69 | Anna (#68/#69) |

Prioritise observed functional failures first. Then agree which readability
changes are useful, implement them in a separate PR and recheck affected cases.
A clearer rule explanation must not imply that a feature caused the risk.

## Confirmed next steps - 19 October 2026

The team agreed the allocation: Benjamin #65/#70, Jackie #66/#67, Anna #68/#69.
The team also agreed to carry the readability ideas forward as team proposals:
wrap long messages first, clarify explanation wording next, and resize fields
where needed. Specific implementation choices and additional findings from #68
are reviewed before changes under #69; this record does not approve those later
findings automatically.

1. Benjamin prepares #65's test plan and brings the resulting evidence together in #70.
2. Jackie coordinates platform checks in #66 and response-time checks in #67.
3. Anna records usability findings in #68 and implements agreed fixes in #69.
4. A teammate reviews PR #83; merging it completes the #57 documentation record.

The evidence alternative, limitations explanation and next-action allocation are
confirmed. The exact meeting checkout remains unrecorded rather than guessed.

No software failures were reported in the supplied meeting feedback. macOS
coverage, response-time results and independent usability checks remain separate
Sprint 6 work. The [current workflow](system-workflow.md) still describes the
implemented system; suggested layout changes do not alter that workflow yet.

Phase E covers deployment/maintenance, user guide and demo video. Phase F covers
closeout, polish, rehearsal and final submission.
