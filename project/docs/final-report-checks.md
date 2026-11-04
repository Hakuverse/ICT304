# Final report and repository alignment — 4 November 2026

Benjamin supplied ICT304_Final_Report_Project_SARAH.docx for repository alignment.
The Word report stays private. Anna and Jackie still need to review the final
report; that confirmation was supplied by Benjamin on 4 November.

## Aligned in PR #126

- Fixed recommendation thresholds, G1-required/G2-optional routing, skipped-row
  handling, study-hours warning and retained evaluation results match the report.
- App source ab4a604, historical tests and video commits remain separate from
  the final source-submission version selected through this PR.
- All 92 supplied Appendix D entries are copied unchanged to the
  [shared prompt log](../../ai-prompt-log/log.md). The project appendix links to
  that single copy. Source/provenance limits are stated; no dates are invented.
- The final plan is two LMS ZIPs, as in report Section 12.5, not one combined ZIP.
- Rehearsal on 3 November is recorded: all three members, 30-minute session,
  no problems reported, final presentation version agreed.
- Equal contributions, signed/confirmed declaration and assessment-period
  support retain their confirmed status.

## Report-side corrections before submission

The supplied report still identifies PR #127 main (`9f2f406`) on its cover and
Section 10.1, while Section 12.5 selects the eventual PR #126 merge. After this
PR is reviewed and merged, Benjamin must use that actual merge SHA consistently
for the final source/version references. Keep historical evidence pinned to its
original tested commits; do not relabel ab4a604 as the final documentation commit.

Section 10.1 still contains `[TO DO — #97] Select and check separately`. Replace
that drafting cell with the actual archive identity from the private manifest
after packaging. The candidate f9c9d12 check is not the final assembled ZIP check.
Anna and Jackie should complete their final report review, and Benjamin should
refresh the contents/cross-reference fields and inspect the final exported PDF.

The supplied Appendix D does not retain entry dates or original session sources.
The repository reproduces it as requested; copying it does not independently
verify transcript accuracy or completeness. This distinction also applies to
historical AI replies describing then-pending work.

## Repository verification

110 application tests and 18 packaging tests passed on 4 November in the existing
Windows Python 3.12.10 environment with normal permissions. The initial restricted
runs encountered temporary-folder errors. All repository local Markdown paths
and anchors were checked. No fresh predictive evaluation or app rebuild was needed.

See [closeout](sprint8-review.md) for ownership and [package checks](submission-package-checks.md)
for the post-merge archive/receipt records retained outside GitHub.
