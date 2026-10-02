# Sprint 4: Prototype and Assignment Submission

> Historical development record. Tasks and results below describe the position at the time.
> See the [submission verification summary](submission-verification.md) for the later report checks.

**Dates:** 29 September-3 October 2026

**Goal:** Check the prototype, finish the model comparison and report, and submit the assignment by 3 October.

## Starting point

The training code, three saved models and initial results are already in main from PR #48. PR #49 has also merged with the CSV fixes and run instructions. Issues #26 and #27 are closed. We still need to check the final submission files and finish #28 and #30-#35.

There are two modes and three model setups: Early-Warning, Confirmatory with G1 only, and Confirmatory with G1 and G2. Comparing both techniques and both class-weight settings gives **12 combinations**.

## Tasks

| Issue | What we will finish | Ready when |
|---|---|---|
| [#30: Training code](https://github.com/Hakuverse/ICT304/issues/30) | Check the existing code and record the environment and command. The current version does not use StandardScaler; explain this limitation rather than claiming it does. | A teammate can repeat the run. |
| [#31: Logistic Regression](https://github.com/Hakuverse/ICT304/issues/31) | Check its six development results: three setups, with and without balanced weights. | Results and settings match the submitted code. |
| [#32: Decision Tree](https://github.com/Hakuverse/ICT304/issues/32) | Check its six results and explain how depth 4 was selected. | Results and settings match the submitted code. |
| [#33: Compare results](https://github.com/Hakuverse/ICT304/issues/33) | Include all 12 comparisons, the three final test results, confusion matrices and limitations. The earlier issue wording says eight; the optional-G2 decision increased this to twelve. | We can explain the choice using recall, precision and F1 as well as accuracy. |
| [#34: Finish report](https://github.com/Hakuverse/ICT304/issues/34) | Combine the existing sections, diagram, five-part model test plan, results and references. | Another member has read the full report against the assignment brief. |
| [#35: Submit](https://github.com/Hakuverse/ICT304/issues/35) | Check the package, signed Group Declaration and required appendices; upload and check the files on LMS. | The submitted files open and run, and a backup is saved. |

Anna supplied the model work, Jackie supplied the diagram and model test plan, and Benjamin supplied the input checks and system test plan. At Tuesday's meeting, confirm who will finish each report section and who will check it. Benjamin will organise the declaration and upload. Check off the linked issues only when the remaining review is complete.

## Tuesday meeting: 29 September

- Show the tutor a prediction and the comparison results.
- Confirm the two modes, current limitations and what belongs in the assignment.
- Check the updated diagram and Pre-Phase A to Phase F table.
- Confirm report owners, the final tester and any remaining work from #28.
- Agree how to finish any requested coefficient/feature-importance discussion in #33 without claiming it proves the cause of a prediction.

## Plan for the week

- **29 September:** review the current prototype and agree the remaining tasks with the tutor and team.
- **30 September-1 October:** check results, add screenshots and finish the report.
- **2 October:** run the actual submission package on another computer, including a macOS check where available. Record the name, date, versions and outcome.
- **3 October:** submit before the LMS cutoff, reopen the uploaded files and keep the receipt and backup.

## What goes into the assignment

- The system design, requirements and original design work from earlier sprints.
- The working classifier prototype, required data, saved models and package list.
- The 12-row development comparison and separate final results for the 79 reserved students.
- The five-part model test plan, system test plan, actual test evidence and demo instructions.
- Tool-use evidence, references, contributions, signed declaration and required appendices.

Sprint 4 work belongs in the **3 October assignment**. Planned recommendations, dashboard and full-system tests stay clearly marked as project-stage work. Do not mark them as completed prototype features.

After submission, keep the submitted `assignment/` version unchanged and continue in `project/`. Tutorials stay separate.

## Useful files

- [Run instructions](../../README.md) and [mode guide](mode-guide.md)
- [Recorded prototype checks](test-results.md)
- [Model results](evaluation_report.md) and [class-weight comparison](CLASS_IMBALANCE_NOTE.md)
- [Five-part model test plan](model-test-plan.md)
- [Current workflow](system-workflow.md) and [system design](SYSTEM_DESIGN.md)
- [Assignment files and report guide](../report/Document.md)
- [Life-cycle phases](NASA_SE_HANDBOOK_CH3_CH4.md)

[Milestone 4](https://github.com/Hakuverse/ICT304/milestone/4) | [Sprint 1](sprint1-planning.md) | [Sprint 2](sprint2-planning.md) | [Sprint 3](sprint3-planning.md)
