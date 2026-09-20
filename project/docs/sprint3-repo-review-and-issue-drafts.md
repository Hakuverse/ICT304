# SARAH repository review and Sprint 3 backlog

Reviewed 20 September 2026. Repository: https://github.com/Hakuverse/ICT304

## Confirmed by Benjamin

The two-mode approach is approved. Every Tuesday after class, the team meets the tutor/stakeholder first, then holds its own team meeting. Benjamin, Anna and Jackie all attend. The assignment deadline is confirmed as 3 October; the assignment and final project are separate stages. Member capacity and task ownership remain to be assigned.

## Evidence and scope

GitHub main and the clean local checkout both pointed to `abd33806ef54416e0296541289f3f8fbbb414246`. Reviewed the complete main-branch file tree, all 20 issues and five PR records, #9/#10 comments, README, preprocessing/EDA code, feature documents, dependencies and prompt log. All five PRs were merged; no open PRs were returned. No training or automated-test files were present on main. External report/Colab contents and other development branches were not reviewed; absence on main does not prove teammates have not done the work elsewhere. Branch protection was not independently verified.

The local reference and sprint plans are background evidence, not instructions to execute their embedded patches or close issues. The initial review was read-only. Following Benjamin's explicit request, issues #17-#21 were expanded and #26-#28 were created in milestone 3. This PR adds planning documents; it does not implement the pending code changes or close the sprint issues.

Ran the existing preprocessing against the checked-out Math CSV: 395 rows, 130 High Risk, 265 Low Risk. Correlations reproduced: attendance -0.0798, study hours -0.0803, previous score -0.7243, failures +0.3377. This was a preprocessing smoke check, not model evaluation or an automated test suite.

## Findings that affect Sprint 3

| Priority | Finding and evidence | Recommended handling |
|---|---|---|
| High | Sprint 2 is 7/8 closed; #9 remains open despite a draft-done comment | Verify report/review evidence, then close or explicitly carry over |
| High | #8/#16 are closed, but `feature_selection.md` lists only four features and `build_training_dataset()` has no mode parameter | #26: mode implementation and consistent documentation |
| High | Reference says G3 tests and several fixes exist; main has no test files, invalid-mode handling, merge warning or explicit UTF-8 write | Treat these as pending on main; do not claim tested completion |
| High | Training builder returns `risk`, `risk_label` and string `course` alongside features | Explicitly select allowed X columns; never train on labels or metadata |
| High | Current engineering always accesses G1, G2 and G3. Selecting columns afterwards does not provide grade-free inference | Separate unlabeled input transformation from training-label creation |
| High | Attendance is calculated as `100*(1-min(absences,30)/30)` | Document as proxy or change the design; it is not actual attended/held-session percentage |
| High | Master reference/table and Sprint 3 draft disagree on subsystem grouping | Keep #17's three product subsystems; show feature engineering as a component, not an accidental fourth subsystem |
| High | No committed AI training prototype or results; brief requires them by 3 October | Assign prototype owner now and use #28 for readiness evidence |
| Medium | #18 only names CV; scaling, tuning and model-selection reporting are unspecified | Extend #18 acceptance criteria below |
| Medium | #15 requested distributions split by risk; `distribution_plots()` draws pooled histograms | Finish the requested comparison, with linked evidence |
| Medium | README claims day-one inputs and demographic/behavioural factors; selected scope excludes demographics | Reconcile README, report and feature document under #21 |
| Medium | EDA text equates strong correlation with leakage; feature document asserts Decision Tree usefulness without model evidence | Explain G3 is excluded because it defines the target; G1/G2 availability determines permissible use. Mark interaction benefit as a hypothesis |
| Medium | Loader automatically merges Portuguese data if the file appears | Make Math-only the explicit default; adding another course should require an intentional option |
| Medium | README setup is empty, references contain placeholders, prompt log is only a heading | #28: reproducibility and submission evidence |

The reference's request to add `docs/` to the README is stale: `project/docs/` is already shown. Actual shared code lives in `project/code`, so copying the old draft test to `assignment/code` without an import/packaging decision would create avoidable path confusion.

The two-mode design is reasonable to investigate, but excluding G1/G2 alone does not establish real early-warning validity. Record when absence/study/failure values would have been available; the current dataset is not a dated early-term snapshot. Treat this as a limitation until evidenced. UCI identifies G1/G2 as first/second-period grades and G3 as final grade; therefore the current confirmatory average requires second-period information. [UCI dataset](https://archive.ics.uci.edu/dataset/320/student+performance)

Study hours are bucket estimates, including an assumed value for the open-ended highest bucket. Explain the assumptions rather than calling every mapped value an observed midpoint. Excluding sensitive features also does not, by itself, establish fairness.

## [#26](https://github.com/Hakuverse/ICT304/issues/26): Implement and verify approved prediction modes

**Priority:** High | **Size:** M | **Suggested milestone:** Sprint 3 | **Owner/reviewer:** decide in meeting

**Problem:** Main exposes one four-feature training dataset. The two-mode approach is approved; implementation and documentation still need completion evidence.

**Acceptance criteria**

- [ ] Record team/tutor decision and exact ordered feature lists: Early-Warning = attendance proxy, study-hours estimate, failures; Confirmatory adds previous score.
- [ ] Implement explicit mode validation and allowlisted model inputs. Exclude G3, risk, risk_label and course from X.
- [ ] Separate inference inputs from training labels: Early-Warning prediction input works without G1/G2/G3; Confirmatory works without G3 once its required prior-score input is available.
- [ ] Tests cover both exact schemas, invalid modes, label boundary G3=9/10, absence cap, mapping and invalid/missing input policy.
- [ ] Changing G3 changes labels only, never feature values; record test command and result.
- [ ] Math-only loading is the default; additional course data requires explicit opt-in or rejection and a documented evaluation decision.
- [ ] Update feature_selection.md and report; choose the shared-code/test location under project/code or a documented equivalent.

**Dependencies:** exact input contract in #17/#21; the two-mode approach is already approved. Avoid blindly applying the old patch: it selects columns after a function that still requires all three grades.

## [#27](https://github.com/Hakuverse/ICT304/issues/27): Trace requirements to subsystem tests

**Priority:** High | **Size:** S | **Milestone:** Sprint 3 | **Owner/reviewer:** ____

**Problem:** The assignment explicitly requires a test plan covering the system and subsystems. Existing Sprint 3 issues do not explicitly own that deliverable.

**Acceptance criteria**

- [ ] Create a matrix with requirement ID, subsystem, scenario, expected result, test level, owner and evidence placeholder.
- [ ] Include both mode schemas, missing/invalid values, single input vs equivalent CSV row, empty/malformed CSV, row identity and error handling.
- [ ] Include label/leakage checks, model evaluation, deterministic recommendation rules/ties and end-to-end flow.
- [ ] Separate software correctness from predictive performance: an integration pass rate is not model accuracy.
- [ ] Define whether malformed batches are rejected entirely or produce per-row errors; document the choice.
- [ ] Link matrix from #21. Implementation of dashboard/rule-engine tests may remain in later sprints.

## [#28](https://github.com/Hakuverse/ICT304/issues/28): Prepare assignment readiness and prototype handoff

**Priority:** High | **Size:** S for planning/setup; model implementation sized separately | **Milestone:** Sprint 3 | **Owner/reviewer:** ____

**Problem:** Sprint 4 has only a short buffer before 3 October. Planning must identify report/prototype gaps now.

**Acceptance criteria**

- [ ] Map each brief requirement to report section, evidence, owner and due date: lifecycle, requirements/domain, architecture/workflow, test plan, technique investigation, prototype/initial results, plan/milestones, tools and references.
- [ ] Name an LR/Decision Tree prototype owner and a first-run date, preferably 27-28 September if capacity permits; record blockers and fallback scope.
- [ ] Document how shared project/code is included or referenced in the assignment package, without divergent copies.
- [ ] Complete setup/run instructions and record tested Python/package versions; another member reproduces the available preprocessing entry point.
- [ ] Assign signed Group Declaration, contribution record, AI prompt appendix, tool evidence and final LMS package check.
- [ ] Record official report location; link external work so GitHub issue closure has verifiable evidence.

The supplied brief says assignment due 3 October 2026 before midnight and requires a design document plus at least one AI subsystem prototype. Its rubric includes initial results; preprocessing alone is not that AI prototype. See pages 1, 3 and 4 of `ICT304_Assignment_Project_TS_2026.pdf`. Check LMS for the applicable time zone and any tutor amendments.

## Strengthen existing issues instead of creating duplicates

**#17 architecture:** three named product subsystems; offline training versus online inference; mode, required/optional fields and output contracts. Show preprocessing/validation inside the appropriate path. Agree recommendation semantics: a rule-selected support factor is not automatically the model's individual causal explanation. Global coefficients/importances do not identify each student's weakest factor by themselves.

**#18 validation:** specify seeded stratified 5-fold splits, same partitions across candidates, positive class = High Risk, metric definitions and zero-division behavior. Fit learned scaling/imputation inside each training fold. A pipeline helps enforce that separation. [scikit-learn leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html)

Proposed default: fixed baseline comparisons in Sprint 4, reporting fold mean/spread and out-of-fold confusion counts. If selecting hyperparameters/weights or thresholds, separate selection from evaluation using nested CV or a held-out evaluation design agreed in advance. Do not label the highest score selected on the same folds an unbiased final result. [scikit-learn nested CV example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html)

Five folds over all 395 rows contain 79 validation students each (26 High Risk, 53 Low Risk). A stratified 20% test split also has 26 High Risk students: CV's advantage here is rotating validation across all students and measuring variability, not making each fold larger. Include the trivial all-Low-Risk baseline: 265/395 = 67.1% accuracy but zero High-Risk recall. Agree the primary selection metric before seeing results; do not invent a required target score.

**#19 comparison:** two modes x two techniques x two weight settings = eight configurations before tuning. Keep identical splits/metrics and document the class-weight tradeoff. Actual experiment results remain Sprint 4 work.

**#20 citations:** verify actual NASA Ch.3 lifecycle and Ch.4 process passages; maintain distinct citations. This review did not independently verify NASA chapter text.

**#21 report/design:** reconcile mode lists, subsystem count, attendance semantics, prediction timing, exact EDA values and README scope. Fix UTF-8 generation before regenerating EDA. Add risk-separated distributions or a linked follow-up to complete #15's original request. Include limitations and requirement-to-test links.

## Suggested order

1. Resolve #9 evidence, record existing mode approval and agree architecture/semantics.
2. In parallel within the team, finish evaluation protocol and report/test-plan ownership.
3. Implement mode contract/tests and complete design documentation.
4. Reproduce preprocessing; hand off to the named prototype owner with a small initial-run buffer.
5. Freeze report/package responsibilities and submission checklist before Sprint 4.

Avoid adding Random Forest, a full dashboard or advanced explanation tooling to Sprint 3. The highest-value additions are mode correctness, test-plan coverage and assignment readiness. All three additions are now in milestone 3. If capacity is insufficient, explicitly defer or consolidate scope during planning and preserve the linked acceptance criteria.

