# Sprint 5: Recommendations and Dashboard Prototype

Proposed dates: 6-13 October 2026. Confirm dates and owners at the Tuesday meeting.
Milestone: [Sprint 5](https://github.com/Hakuverse/ICT304/milestone/5).

## Goal

Start the final project in project/ and build a first connected prototype.
This is Phase C. Keep assignment/ unchanged.

| Issue | Work | Dependency |
|---|---|---|
| [#51](https://github.com/Hakuverse/ICT304/issues/51) | Prepare project folder | Confirm submitted version; Benjamin is assigned |
| [#52](https://github.com/Hakuverse/ICT304/issues/52) | Agree recommendation rules | Team agreement |
| [#53](https://github.com/Hakuverse/ICT304/issues/53) | Build and test recommendations | #51 and agreed rules in #52 |
| [#54](https://github.com/Hakuverse/ICT304/issues/54) | Single-student dashboard | #51; connect #53 when ready |
| [#55](https://github.com/Hakuverse/ICT304/issues/55) | CSV upload and results | #51 and dashboard structure in #54 |
| [#56](https://github.com/Hakuverse/ICT304/issues/56) | Initial integration checks | #53, #54 and #55 connected |
| [#57](https://github.com/Hakuverse/ICT304/issues/57) | Tutor demo and project notes | Working prototype and #56 results |

## Work that fits together

- #51, #56 and #57: project setup, testing and tutor demonstration. Prepare the
  test checklist early; the full checks must wait for the new features.
- #52 and #53: agree the recommendation rules, then implement and test them.
- #54 and #55: build the form and CSV page together to avoid conflicting edits.

These are suggested groupings, not new assignments. Agree the remaining owners
at the team meeting. #52 can be discussed while #51 is being reviewed.

## Review before moving on

Try Early-Warning, G1-only and G1-plus-G2 examples and a mixed valid/invalid CSV.
Record what works, what was tested and what remains unfinished. Keep the
recommendation rules separate from the model's probability estimate.

Continue with the [Sprint 6 plan](sprint6-planning.md) for fuller system testing,
user feedback and fixes. Do not mark unfinished Sprint 5 tasks as complete.

## Status on 9 October 2026

Issues #51-#55 are closed following PRs #71-#74. Benjamin can now run
[#56 checks](prototype-test-checklist.md), then prepare the
[#57 demonstration](prototype-demo-notes.md). These two issues remain open.
Recommendation rules are agreed internally by the team; the tutor meeting in
#57 is for demonstrating progress and collecting feedback.
