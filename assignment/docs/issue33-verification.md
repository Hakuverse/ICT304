# Issue 33 output and environment checks

PR #61 supplied the comparison discussion, tables and feature-importance chart.
This follow-up makes the generated paths agree with the committed files.

## Output locations

- `issue33_report.md`, the three CSV tables and `run_details.txt` stay in this folder.
- The feature-importance chart is in `figures/early_warning_feature_importance.png`.
- The three existing confusion matrices are linked from `figures/`, without copying or rewriting them.
- The script no longer creates an `issue33/` folder. It does not delete any old local output folder.
- Existing output files are protected unless the user supplies `--overwrite`.

## Environment evidence

The original PR #61 run record is preserved unchanged in
[issue33_previous_run_details.txt](issue33_previous_run_details.txt). It records
Python 3.14.0 and scikit-learn 1.9.1 and is historical evidence, not the submission
environment specified by requirements.txt.

[run_details.txt](run_details.txt) records the actual follow-up run using Python
3.12.10 and the pinned scikit-learn 1.8.0. The 12 development rows were read from
the existing evaluation report; saved-model checks reproduced all three final
test results. Feature importance remains 52.9% past failures, 44.1% attendance
estimate and 3.0% estimated study hours. This is a repeat check of the same
experiment, not a new independent accuracy test or a clean-machine installation test.

The input fingerprints are byte-level SHA-256 values. Windows and macOS line
endings can produce different hashes for text files without changing their
content or results; compare the text if only line endings differ.

## Follow-up checks on 29 September 2026

- All 41 automated tests passed on Windows with Python 3.12.10 and scikit-learn 1.8.0.
- The three new tests check output locations and image links, repeat-run protection,
  and a clear error for a missing confusion matrix before outputs are changed.
- Tests use temporary copies and verify that model files, source results, data and
  original confusion matrices remain unchanged.
- The sample CSV still processes A and B with probabilities 0.155 and 0.004 and
  skips C and D for invalid attendance and invalid G2 text.
- The report's three final-result rows match the existing evaluation report. The
  feature-importance CSV has only negligible floating-point differences between
  environments; the reported percentages are unchanged.

These are the follow-up software checks. They do not replace the final teammate
review, macOS run or check of the actual submission package.

## Report and submission handoff

For #34, use the development comparison and model-selection explanation in
Section 7, add the feature-importance figure and interpretation in 7.3, and use
the reserved-test results, confusion matrices and limitations in Section 8.
Keep the original diagram and five-part model test plan. The repository's
[Document.md](../report/Document.md) remains an outline, not the final report.

For #35, use a final agreed commit and test the actual submission package on a
teammate's computer. Record the tester, date, environment and outcome. Windows
checks do not establish a macOS pass. The signed declaration, required appendices,
final report, uploaded-file check and submission receipt remain team tasks.
