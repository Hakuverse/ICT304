# Project progress notes - updated 19 October 2026

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
long-line wrapping. These are candidates for Sprint 6 review, not implemented
changes. Sprint 6 covers requirements-to-test mapping, Windows/macOS workflow
checks, timing, user trials, fixes and updated evidence. The agreed owners are
Benjamin (#65/#70), Jackie (#66/#67) and Anna (#68/#69). The team agreed to
prioritise wrapping long messages, clearer wording and resizing fields where
needed as proposals for review, not completed changes. Deployment and maintenance guidance, the user guide and
demo video follow in Phase E; closeout and final submission follow in Phase F.
