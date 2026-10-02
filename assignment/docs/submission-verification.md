# Assignment verification summary

## Scope and evidence sources

This summary uses the team's assignment report, Section 9.1, supplied on
1 October 2026, together with the dated repository checks linked below.
It records the reported macOS results; it is not a new macOS run. Screenshots
are in the separately maintained report. The raw macOS environment, comparison
and test-output files are not committed in this repository.

| Record | Environment and version | Result and source |
|---|---|---|
| Benjamin's Sprint 4 model checks, 29 September | Windows; recorded versions in the linked note | Reproduced twelve comparisons and final results; 38 tests at that time. [PR #58 evidence](sprint4-model-checks.md) |
| Output-path and saved-model checks, 29 September | Windows, Python 3.12.10, scikit-learn 1.8.0 | 41 tests passed; original models and confusion matrices preserved. [PR #62 evidence](issue33-verification.md) |
| Jackie's reported final prototype checks, 1 October | macOS 26.6.2, arm64; Python 3.13.9; scikit-learn 1.8.0; commit `0fff0f8` | Report Section 9.1 records T1-T9 passed and 41 tests before and after training. Screenshots include sample predictions, export and model results. |

Anna's earlier Windows sample prediction is preserved in report Figure 8.4.
The macOS reproduction used step-by-step guidance. It does not establish an
unassisted usability pass. The report's statement that evaluation reports
matched exactly and tests passed after training should be read alongside
Jackie's original comparison and test-output records.

## System checks used in the report

These identifiers match the final report, replacing the earlier outline's
T01-T13 numbering. Software checks are separate from predictive accuracy.

| Test | Behaviour | Status recorded in the report |
|---|---|---|
| T1 | Early-Warning predicts without assessment grades | Passed in the reported automated checks |
| T2 | Correct G1-only/G1+G2 routing; G2 zero accepted | Passed in the reported automated checks |
| T3 | Missing G1 and invalid supplied G2 rejected; blank G2 allowed | Passed in the reported automated checks |
| T4 | Attendance, study-hour and failure boundaries enforced | Passed in the reported automated checks |
| T5 | Mixed CSV processes valid students and explains skipped rows | Anna's earlier Windows example and Jackie's macOS run process A/B and skip C/D |
| T6 | Missing columns, empty input and all-invalid classes handled | Passed in the reported automated checks |
| T7 | Exported CSV matches terminal predictions | Jackie reports two rows, A/B, with matching labels, probabilities and grade setups |
| T8 | Another teammate installs and runs the prototype | Jackie reports successful macOS setup and all three single-student setups; guidance was used |
| T9 | Reproduce development comparisons and reserved-test results | Benjamin's earlier checks and Jackie's reported reproduction agree with the reference evaluation |
| T10 | Recommendation rules | Planned for the project stage |
| T11 | Dashboard and usability | Planned for the project stage |
| T12 | Complete-system integration | Planned for the project stage |

## Reference results

| Setup | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Early-Warning | 0.633 | 0.440 | 0.423 | 0.431 |
| Confirmatory G1 | 0.823 | 0.714 | 0.769 | 0.741 |
| Confirmatory G1+G2 | 0.899 | 0.821 | 0.885 | 0.852 |

These results use the same 79 reserved students. Reproduction is a check of the
same experiment, not a new independent performance test. The capacity files
added in PR #63 are runtime inputs, not new model-evaluation data.

## Repeatable commands

Run from the repository root after the [setup steps](../../README.md#setup--how-to-run).
On macOS:

```bash
.venv/bin/python -m unittest discover -s assignment/code -v
.venv/bin/python assignment/code/predict.py --mode confirmatory --csv assignment/data/sample_roster.csv
.venv/bin/python assignment/code/predict.py --mode confirmatory --csv assignment/data/sample_roster.csv --out predictions.csv
```

On Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe`.
Training reproduction should use a separate copy because `train_models.py`
overwrites model files, the evaluation report and confusion figures.

## Documentation maintenance check — 2 October 2026

The documentation cleanup passed all 41 automated tests on Windows. A separate
temporary-folder check confirmed that the comparison script produces exactly
the checked-in comparison report. Local Markdown file links resolve. The update
changes the comparison report's explanatory text, not prediction or training
behaviour; models, datasets, numerical results and original confusion matrices
remain unchanged. Prompt logs and appendices were not edited.

## Submission boundary

The report and signed declaration are submitted separately through LMS and are
not reproduced here with personal details. Final report formatting, completed
prompt records, signatures, upload verification and the receipt are separate
from a passing prototype test. The submission owner records the final packaged
commit in issue #35. A later merge does not retroactively change Jackie's tested
commit. After submission, the submitted assignment snapshot is retained and
further development continues under `project/`.
