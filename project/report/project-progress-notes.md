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

The team proposed improving layout, explanation wording, text-area sizes and
long-line wrapping. Wording and readability changes merged through PRs #86 and
#87; PR #92 added clearer dashboard CSV error reasons. These changes do not by
themselves establish that the usability targets have been met.

The [system test plan](../docs/system-test-plan.md) links Benjamin's 19 October
Windows evidence at commit `9dc7132` and Anna's usability retest at that version.
The Windows record reports 99 passing automated tests. The retest records mixed
usability outcomes, including difficulty explaining probability uncertainty and
correcting skipped rows. New changes need affected checks and updated evidence.
Jackie's macOS evidence is under [PR #90](https://github.com/Hakuverse/ICT304/pull/90)
review; timing evidence remains under [#67](https://github.com/Hakuverse/ICT304/issues/67).
These records are separate from the earlier model evaluation.

## Remaining stages

| Period | Work | Plan |
|---|---|---|
| Sprint 6 carry-forward | Finish platform/timing reviews, follow up usability findings and consolidate evidence in #70 | [Sprint 6](../docs/sprint6-planning.md) |
| 20-27 October | Phase E: deployment, maintenance, user guide, walkthrough and demo video (#77-#82) | [Sprint 7](../docs/sprint7-planning.md) |
| 27 October-3 November | Phase F: final report/forms, slides, rehearsal, package checks and readiness review (#93-#98) | [Sprint 8](../docs/sprint8-planning.md) |
| 4-7 November | Final corrections and actual submission before the confirmed LMS cutoff | Handover recorded under #98 |

Sprint 6 owners remain Benjamin (#65/#70), Jackie (#66/#67) and Anna (#68/#69).
Sprint 7 and Sprint 8 owners are still to be agreed. The milestone dates and
planning pages do not claim that deliverables or submission are complete.
