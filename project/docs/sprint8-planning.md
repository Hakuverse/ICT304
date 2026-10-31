# Sprint 8: Closeout, Report Polish and Rehearsal

Working period: 27 October-3 November 2026. Phase F.
Milestone: [Sprint 8](https://github.com/Hakuverse/ICT304/milestone/8).
Prepared: 20 October 2026. Status updated: 31 October 2026.
Benjamin is drafting the final report; Anna is preparing the slides. Each lead
receives review from the other two members. Benjamin handles final overall
checking and submission. Forms, rehearsal and final package/closeout checks are
still outstanding; owner allocation does not mean they have been performed.
The dates below remain planning targets, not completed events.

## Goal

Finish a consistent report, presentation and checked code package, then review
whether the team is ready for submission. The milestone is due on 3 November
for the readiness review. It is not the LMS deadline. Keep 4-7 November for
final corrections and the actual submission by 7 November.

## Tasks

| Issue | Work | Start after | Planned output |
|---|---|---|---|
| [#93](https://github.com/Hakuverse/ICT304/issues/93) | Polish the report and evidence links | #70 and #82; draft early | Final report and `project/docs/final-report-checks.md` |
| [#94](https://github.com/Hakuverse/ICT304/issues/94) | Check contributions and required private declarations | Contribution evidence and report draft | Private forms and `project/docs/contribution-checks.md` |
| [#95](https://github.com/Hakuverse/ICT304/issues/95) | Prepare presentation slides | Report outline and Phase E materials | Deck and `project/docs/presentation-notes.md` |
| [#96](https://github.com/Hakuverse/ICT304/issues/96) | Rehearse presentation and demo | #95, #81 and reviewed prototype | `project/docs/rehearsal-notes.md` |
| [#97](https://github.com/Hakuverse/ICT304/issues/97) | Check final code package and handover files | #77-#80 and agreed submission commit | Package and `project/docs/submission-package-checks.md` |
| [#98](https://github.com/Hakuverse/ICT304/issues/98) | Closeout and submission-readiness review | #82 and Sprint 8 outputs | `project/docs/sprint8-review.md` and final handover list |

These are planned outputs. A planning PR does not complete the issues or prove
that the report, rehearsal, package checks or submission have happened.

## Agreed leads and review — 31 October

| Work | Lead | Review / participation |
|---|---|---|
| #93 final report | Benjamin | Anna and Jackie review and suggest corrections |
| #95 presentation slides | Anna | Benjamin and Jackie review and edit |
| #94 contributions and declaration | Benjamin coordinates final checking | Each member confirms their own contributions and private details |
| #96 rehearsal and demonstration | All three | Speaking parts, rehearsal date and app-startup format still need decisions |
| #97 final package checking | Benjamin | Anna or Jackie provides a teammate review; actual check remains outstanding |
| #98 readiness and submission | Benjamin | Anna and Jackie review beforehand; backup uploader still needs agreement |

Keep one master report and one master slide deck. Reviewers comment or suggest
edits; the lead resolves them and maintains the current version. This replaces
the earlier plan to edit all deliverables together without a designated lead.
The new local report is a draft, not a reviewed final submission.

Original planning targets were a readiness review by 3 November and corrections/
submission during 4–7 November. Confirm practical session dates, speaking roles,
exact LMS cutoff/formats and a backup uploader. Keep names, IDs, signatures and
receipts private; use Benjamin, Anna and Jackie in public project records.

## Order for the week

1. On 27 October, review [Sprint 7](sprint7-planning.md) and agree remaining work and owners.
2. Polish the report and prepare slides in parallel, using actual evidence.
3. Choose the submission version once required fixes are reviewed. Link earlier
   results to their original commits; do not relabel them as new runs.
4. Rehearse with all presenters and check a clean extracted copy of the package.
5. Correct problems and have another teammate review the final materials.
6. On 3 November, record readiness, missing items, owners and the 4-7 November handover.

## Submission handover: 4-7 November

- Confirm the exact LMS cutoff, required formats and upload location from the current brief/LMS.
- Confirm the uploader and backup person. Do not assume the assignment-stage allocation still applies.
- Check the final report, required forms, code package and any separately submitted video or slides.
- Keep one agreed final version and check that links work for the intended reviewer.
- Make the actual upload before the confirmed cutoff and retain its receipt privately.
- Record the upload status only after it happens. Readiness on 3 November is not proof of submission.

## End-of-sprint check

The report, slides, guides, video and package refer to compatible versions.
Model evaluation, functional tests, response times and usability findings are
clearly distinguished. Unmet targets and limitations remain visible. Existing
unfinished issues keep their owners and next actions rather than being duplicated.

This plan supports [#70](https://github.com/Hakuverse/ICT304/issues/70) and
[#82](https://github.com/Hakuverse/ICT304/issues/82); it does not close them.

## Application work alongside Sprint 8

Benjamin confirmed the [application deployment plan](app-deployment-plan.md)
decisions on 27 October. #112–#118 cover the launcher, Windows/macOS packages,
checks, first-use walkthrough and release. Benjamin coordinates builds, Anna
tests Windows and Jackie tests macOS, with shared release decisions.
Builds are unsigned prototypes; platform security restrictions must be tested.
The 30-second startup target is separate from earlier prediction timings.

Report and slides are being prepared under the leads above. Coordinate #97/#98 with the
packaged-app evidence before including releases in the submission. The 3 November
review decides which platforms are ready; no package test or release is claimed
by this plan.

App status on 31 October: #112–#117 are closed following merged PRs #119–#123.
PR #124 merged the release/user-guide preparation. The tested `ab4a604` Windows
and Mac packages are now published as `v0.1.0-preview`; see the
[release record](app-release-notes.md) for exact files, hashes and limitations.
Both devices met the recorded routine-startup target. The first security-prompt
launches retain their separate timings. Benjamin chose to reuse existing device
evidence without another post-publication run. Issue #118 retains its final
handover link to outstanding #97/#98 work. App work is within Sprint 8, not a separate milestone.
