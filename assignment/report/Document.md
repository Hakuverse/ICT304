# SARAH assignment files and report guide

The assignment report is maintained separately for LMS submission. This public
repository contains the prototype, supporting analysis and development records;
this page is a guide to those files, not the full assessment report. The report
and signed Group Declaration contain personal details and are not copied here.

## Assignment scope

SARAH predicts academic risk for one student or a class CSV. Early-Warning uses
attendance estimates, estimated study hours and past failures without grades.
Confirmatory requires G1 and accepts optional G2, using separate G1-only and
G1+G2 models. Invalid student rows are skipped with reasons. Dashboard and
recommendation features remain planned for the project stage.

The Math dataset contains 395 students: 130 High Risk and 265 Low Risk. G3 below
10 defines High Risk; G3 is never a prediction input. Model selection uses five
folds on 316 development students, with 79 students reserved for final testing.
There are twelve comparisons across three setups, two techniques and two
class-weight settings. The dataset does not establish day-one accuracy or
performance with university students.

## Report sections and supporting files

The section numbers below follow the team's assignment report.

| Report section | Repository material |
|---|---|
| 1-2: Scope and requirements | [Mode guide](../docs/mode-guide.md) and [system design](../docs/SYSTEM_DESIGN.md) |
| 3: Systems engineering | [Pre-Phase A to F and NASA Chapter 4](../docs/NASA_SE_HANDBOOK_CH3_CH4.md) |
| 4: Dataset and preparation | [EDA findings](../docs/eda_findings.md) and [feature selection](../docs/feature_selection.md) |
| 5: Design and workflow | [Current architecture diagram](../docs/figures/SARAH_System_Architecture_Diagram_Final%20Version.png) and [workflow](../docs/system-workflow.md) |
| 6: Techniques and evaluation | [Five-part model test plan](../docs/model-test-plan.md) and [class weights](../docs/CLASS_IMBALANCE_NOTE.md) |
| 7: Model comparison | [Twelve development comparisons and feature importance](../docs/issue33_report.md) |
| 8: Initial results and discussion | [Evaluation report](../docs/evaluation_report.md), [figures](../docs/figures/) and [final results CSV](../docs/final_test_results.csv) |
| 9: System tests and evidence | [Verification summary and T1-T12 mapping](../docs/submission-verification.md) |
| 10: User guide | [Setup and run commands](../../README.md#setup--how-to-run) and [mode examples](../docs/mode-guide.md) |
| 11: Development and teamwork | [Sprint 4 record](../docs/sprint4-planning.md) and [project transition](../../project/README.md) |
| 12: Sources and repository evidence | Source references in the linked analysis documents and [repository history](https://github.com/Hakuverse/ICT304/commits/main/) |

## Versions and evidence

The report records Jackie's macOS checks against commit `0fff0f8` on 1 October
2026. Later documentation changes do not change the commit he tested. The
[verification summary](../docs/submission-verification.md) distinguishes the
reported teammate run from the earlier Windows checks and later maintenance.

The submitted package should identify its own exact commit. Testing and merged
code do not establish that the LMS upload, signatures or final report review
have been completed. [Issue #34](https://github.com/Hakuverse/ICT304/issues/34)
tracks report completion; [issue #35](https://github.com/Hakuverse/ICT304/issues/35)
tracks final checking and submission.

## Submission materials

The LMS submission comprises the completed report, required declarations and
appendices, and the files needed to run the prototype. The repository's
[prompt appendix](appendix-ai-prompts.md) is currently a placeholder, not a
completed record. The required actual prompt record belongs in the submitted
report; a repository link alone does not replace it.

Historical sprint plans and dated test notes remain as development evidence.
Their task lists describe the position at the time; the current verification
summary is the reference for the report's T1-T12 checks.

After submission, preserve the submitted assignment snapshot and continue work
in [project/](../../project/README.md). Tutorials remain separate.
