# Sprint 8: Closeout, Report Polish and Rehearsal

Original working period: 27 October–3 November 2026, Phase F.
Milestone: [Sprint 8](https://github.com/Hakuverse/ICT304/milestone/8).
Prepared 20 October; final status updated 4 November.

The tables below retain the sprint plan. Current outcomes are in the
[closeout record](sprint8-review.md): implementation/release, slides, declarations
and rehearsal are complete. Final report approval was confirmed on 4 November.
Post-merge LMS package checks/upload remain final handover actions with named owners.

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
| #96 rehearsal and demonstration | All three | Presenters/clip recorded in PR #127; rehearsal completed 3 November, all three, 30-minute session |
| #97 final package checking | Benjamin | Anna or Jackie provides a teammate review; final merged-source archive check follows merge |
| #98 readiness and submission | Benjamin | Anna and Jackie review beforehand; Benjamin is the sole uploader; no backup agreed |

Keep one master report and one master slide deck. Reviewers comment or suggest
edits; the lead resolves them and maintains the current version. This replaces
the earlier plan to edit all deliverables together without a designated lead.
Benjamin confirmed on 4 November that Anna and Jackie reviewed and approved
the final report for submission.

Original planning targets were a readiness review by 3 November and corrections/
submission during 4–7 November. Presenters are recorded in PR #127. Confirm
the LMS cutoff time; 7 November and two separate ZIP submissions are confirmed. No backup uploader is agreed. Keep names, IDs, signatures and
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
- Benjamin is the confirmed uploader; no backup uploader is agreed.
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

The final report and slides are reviewed and approved. Coordinate #97/#98 with the
packaged-app evidence before including releases in the submission. Both platforms already have accepted evidence and published packages;
this planning record does not add new platform tests.

App status on 31 October: #112–#117 are closed following merged PRs #119–#123.
PR #124 merged the release/user-guide preparation. The tested `ab4a604` Windows
and Mac packages are now published as `v0.1.0-preview`; see the
[release record](app-release-notes.md) for exact files, hashes and limitations.
Both devices met the recorded routine-startup target. The first security-prompt
launches retain their separate timings. Benjamin chose to reuse existing device
evidence at publication; Anna's later launch clip is in [presentation notes](presentation-notes.md). Issue #118 records completed publication and app handover; final LMS
packaging and submission are tracked under #97/#98. App work is within Sprint 8, not a separate milestone.

## Final arrangements — updated 4 November

Use the eventual approved PR #126 merge commit for final source submission; obtain
team approval before merging. Capture the real merge SHA after merge and verify the final
extracted ZIP. Historical test/build commits do not change.

Equal one-third contributions (33.3% each rounded) and all three declaration
signatures/confirmations were reported by Benjamin; see [contribution checks](contribution-checks.md).
Benjamin uploads two separate ZIPs: the final-project source/report/guide/evidence/
declaration package, and the presentation deck with both videos. No backup uploader is agreed. Final archive
names and hashes belong in the private submission manifest after assembly. Assessment-period support is coordinated by Benjamin,
with Anna and Jackie assisting; no ongoing service.

## Final status — 4 November

The 3 November rehearsal is complete. See [rehearsal notes](rehearsal-notes.md).
The [closeout record](sprint8-review.md) supersedes the original targets above
and identifies the remaining private report/package/upload actions.
