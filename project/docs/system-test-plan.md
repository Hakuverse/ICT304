# SARAH system test plan - Sprint 6

Owner: Benjamin. Prepared: 19 October 2026. Issue: #65.
Status: draft for team review and tutor agreement on measurable targets.
Plan baseline: `051596275aab007a5e22704147ff1dc8becbaaa4`.

## Purpose and scope

Check the connected prototype: setup, validation, model routing, recommendations,
form results, CSV processing, response times and usability. Software checks do
not measure predictive accuracy or prove the effectiveness of recommendations.
No new run is claimed by this plan. No model retraining is required.

There are two user-facing modes and three model setups. Early-Warning has no
grade inputs. Confirmatory requires G1 and uses G1-only when G2 is blank, or
G1+G2 when G2 is supplied (zero is valid). G3 must never enter prediction inputs.
Check this exclusion and mode routing in the existing automated tests as well
as the examples below; do not add grade fields to Early-Warning for testing.

## Sources and earlier evidence

- [Project README](../README.md): setup and implemented features.
- [System workflow](system-workflow.md) and [mode guide](mode-guide.md).
- [Approved recommendation rules](recommendation-rules.md): fixed thresholds and policy.
- [Assignment system design](../../assignment/docs/SYSTEM_DESIGN.md) and
  [model comparison plan](../../assignment/docs/model-test-plan.md): background only.
- [Issue #56 checklist](prototype-test-checklist.md): P1-P16 passed on Windows
  on 12 October at `2bbb083`; [screenshots](evidence/issue56/windows/README.md).
  These are historical results, not new Sprint 6 passes or macOS evidence.
- [Issue #57 meeting](prototype-demo-notes.md): team accepted #56 CSV evidence
  for the initial review; no repeat live CSV demonstration is claimed.
- [Issue #68 usability record](usability-feedback.md): 17 October, one non-team
  tester at `13d85f9`; tasks 1, 2 and 4 needed help. Accepted changes dated
  19 October are requirements for #69, not evidence that changes are implemented.

#57's follow-up decisions are recorded; implementation, platform checks and
usability retests remain under their existing Sprint 6 issues. Do not duplicate
those tasks. Where historical accounts differ, retain their source and do not
infer new meeting events or independent test results from them.

## Ownership and sequence

Benjamin prepares/reviews this plan (#65) and consolidates results (#70).
Jackie coordinates Windows/macOS runs (#66) and timing (#67), with Benjamin
available for Windows evidence. Anna coordinates user tasks (#68), fixes and
retesting (#69). No task is completed merely by being listed here.

Review the plan and agree targets, record a tested commit, run the applicable
cases, link problems to #69, then retest fixes against their new commit. If #69
changes the UI during testing, keep separate before/after records. Run affected
cases and the automated suite after code changes.

## Run record and commands

For each platform/run, record:

- Date, tester, commit and branch; clean checkout or any local changes.
- OS, Python/package versions, browser, screen size and zoom where relevant.
- Model version (the tested commit if models are unchanged).
- Fixture names and exact inputs, evidence paths, failures and fix/retest links.

From repository root after README setup, Windows:

```powershell
git rev-parse HEAD
git status --short
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -m pip show scikit-learn pandas numpy joblib streamlit
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m unittest discover -s project/code -v
.venv\Scripts\python.exe -m unittest discover -s project/code -p "test_recommend.py" -v
.venv\Scripts\python.exe -m streamlit run project/code/dashboard.py
```

On macOS use `.venv/bin/python` in place of `.venv\Scripts\python.exe`.
Keep the dashboard terminal open. The recommendation tests are included in the
full suite, so do not count the separate run as extra tests.

For S6-05 use `project/code/predict.py` with `--attendance`, `--study-hours`,
`--failures`, and for Confirmatory `--mode confirmatory --g1` and optional `--g2`.
Save exact commands. The CLI comparison concerns labels/probabilities; compare
recommendation text between form and CSV, not an assumed CLI recommendation output.

Use existing fixtures under `project/data/` and `project/data/dashboard_checks/`.
For extra cases, save fictional CSVs with IDs and retain exact inputs. Change
one value at a time in range tests; include a valid control row in mixed CSVs.
No real student records. Do not edit the original #56 screenshots or results.

## Functional, performance and usability cases

Each S6 ID maps the requirement directly to steps and expected results.
Record subcases individually (for example S6-09-G2-NA). A grouped case passes
only when every listed subcase passes. Baseline prediction numbers apply only
to the existing saved models, not arbitrary future models.

| ID | Requirement | Steps / input | Expected result | Earlier evidence |
|---|---|---|---|---|
| S6-01 | Setup and automated checks | Follow project README setup on each platform; run pip check and the full unittest command below. | Setup works; package check succeeds and all tests pass. Record actual count (89 at the plan baseline). | P1 |
| S6-02 | Early-Warning model routing | Form: attendance 40, study 4, failures 0; select Early-Warning. | No grades needed. Baseline: High Risk, 0.859, attendance suggestion. | P2 |
| S6-03 | G1-only model routing | Confirmatory form: 80, 4, 0, G1 8, G2 blank. | G1-only model; previous score 40. Baseline: High Risk, 0.818, assessment suggestion. | P3 |
| S6-04 | G1+G2 model routing | Confirmatory form: 80, 4, 0, G1 12, G2 0. | Zero accepted; G1+G2 model, previous score 30. Baseline: High Risk, 0.996. | P4 |
| S6-05 | Consistent form, CLI and CSV results | Run S6-02/03/04 inputs through form, CLI and a fictional CSV. Also use G1 12/G2 14. Record mode and models. | Labels, grade setup and probabilities match at displayed precision; form/CSV recommendation messages match for each student. | P6, P13 |
| S6-06 | Attendance range | Keep other values valid. Try attendance 0, 100, -1 and 101 in form and mixed CSV. | 0/100 accepted; -1/101 rejected. Invalid CSV rows skipped while valid rows continue. | P7, extended boundaries |
| S6-07 | Study-hours range | Try study hours 0, 40, -1 and 41 in form and mixed CSV. | 0/40 accepted; -1/41 rejected with a useful reason. | P7 |
| S6-08 | Whole-number failures | Check form options. CSV: failures 0, 1, 2, 3, -1, 4 and 1.5. | Form offers 0-3. CSV accepts whole numbers 0-3; other cases skipped. | P16 |
| S6-09 | Grade validation | Confirmatory: try blank G1; G1 0/20/-1/21/NA; valid G1 with G2 blank/0/20/-1/21/NA. Change one field at a time. | G1 required; blank G2 routes to G1-only. 0/20 valid grades; invalid text and out-of-range grades rejected. Repeat through mixed CSV. | P3/P4/P8, extended boundaries |
| S6-10 | Mixed valid/invalid CSV | Confirmatory: upload project/data/sample_roster.csv. | 4 rows: A/B predicted, C/D skipped with attendance/G2 reasons. Skipped rows receive no prediction/recommendation. | P9 |
| S6-11 | Missing columns and empty files | Upload dashboard_checks/missing_g1_column.csv in Confirmatory; also empty.csv and header_only.csv. | Clear file errors; no invented predictions. Test missing required Early-Warning columns with a separate fictional fixture. | P10 |
| S6-12 | All-invalid CSV | Confirmatory: upload dashboard_checks/all_invalid.csv. | 4 rows, 0 predicted, 4 skipped; each reason shown; no valid result invented. | P10 |
| S6-13 | CSV structure and row identity | Confirmatory: extra_comma.csv, no_student_ids.csv, messy_headers.csv and unmatched_quote.csv from dashboard_checks. | Extra comma: 2 rows, 1 valid/1 skipped. No IDs: row 1/3 valid, row 2 skipped. Normalised valid headers accepted; malformed quote rejected clearly. | P11; added header/quote cases |
| S6-14 | Duplicate IDs | Upload project/data/issue56-duplicate-and-invalid.csv in Confirmatory. | 5 rows, 2 predicted, 3 skipped. First DUP is G1-only High Risk; second is G1+G2 Low Risk. Messages stay with their own rows. | P12/P16 |
| S6-15 | Downloaded results | Download the results for S6-14 and compare each valid row and full message with the dashboard. | Two valid rows and their labels, probabilities, setup and recommendations retained; no results for skipped rows. Keep the fictional export as evidence. | P13 |
| S6-16 | Clear stale form results | Predict; change attendance without pressing Predict. Predict again; switch mode. Commit the edit by leaving the field. | Previous prediction and recommendations disappear after each change, until Predict is pressed again. | P14 |
| S6-17 | Recommendation boundaries | Run test_recommend.py. With a supplied High Risk label, vary attendance 60/60.1, study 1.5/1.6, failures 0/1 and Confirmatory score 49/50; keep other thresholds inactive. | Rules trigger only at attendance <=60, study <=1.5, failures >=1 and Confirmatory score <50. Existing tests plus any extra exact inputs must be identified in evidence. | P15 |
| S6-18 | Recommendation policy and order | Run rule tests: all thresholds match; High Risk with none matching; Low Risk with matching thresholds; Early-Warning with no grade. | Unique messages in attendance/study/failure/assessment order. High Risk fallback when none match; Low Risk routine guidance only; no assessment rule in Early-Warning. | P5/P15 |
| S6-19 | Single-student response time | Measure S6-02/03/04 using the timing method below. | Record cold and warm measurements; compare against approved targets only. | New #67 run |
| S6-20 | Class CSV response time | Measure fictional 30-row and 395-row files in both modes, with fixed valid/mixed cases and recorded expected totals. | Results and skipped totals correct; record timings and compare against approved targets only. | New #67 run |
| S6-21 | Find modes and understand inputs | Give a tester the three prediction tasks without coaching. Ask what attendance estimate, G1 and blank/zero G2 mean. | Record independent/helped/not completed for each task and actual explanations. Compare to agreed usability target. | 17 October #68 findings |
| S6-22 | Understand results and limitations | Ask what the risk label and displayed probability mean and whether the prediction can be used alone to decide. | Record answers before explaining. Intended understanding: model estimate may be wrong; human review needed; recommendations do not prove causes. | 17 October #68 findings |
| S6-23 | Notice and correct CSV problems | Ask tester to upload sample_roster.csv in Confirmatory, find skipped rows and explain how C/D could be corrected. | Record whether warning/reasons were noticed without help; valid results remain visible. Do not silently treat NA as a blank grade. | 17 October #68 findings |
| S6-24 | Readability and accepted UI changes | After #69, check mode help, percentage explanation, human-review notice, skipped-count warning, message wrapping and field sizes. Record viewport and zoom; repeat S6-21/22/23. | Full text can be read without clipped content or lost controls; accepted help/notice wording visible. Values and rules unchanged; before/after assistance recorded. | Accepted #68 changes; implementation/retest pending |

Rule-only tests supply a risk label directly. They do not require the classifier
to become High Risk at a rule threshold. A rule trigger is not a causal explanation.

## Actual results and evidence

Use Not run, Pass, Fail or Blocked for functional cases. Timing/usability cases
remain Pending target until a target is agreed; observations can still be saved.
For user tasks additionally record independent, helped or not completed. A
correct result with assistance is not independent success.

| ID | Windows actual result / status | macOS actual result / status | Evidence / fix / retest link |
|---|---|---|---|
| S6-01 | Not run | Not run | Pending |
| S6-02 | Not run | Not run | Pending |
| S6-03 | Not run | Not run | Pending |
| S6-04 | Not run | Not run | Pending |
| S6-05 | Not run | Not run | Pending |
| S6-06 | Not run | Not run | Pending |
| S6-07 | Not run | Not run | Pending |
| S6-08 | Not run | Not run | Pending |
| S6-09 | Not run | Not run | Pending |
| S6-10 | Not run | Not run | Pending |
| S6-11 | Not run | Not run | Pending |
| S6-12 | Not run | Not run | Pending |
| S6-13 | Not run | Not run | Pending |
| S6-14 | Not run | Not run | Pending |
| S6-15 | Not run | Not run | Pending |
| S6-16 | Not run | Not run | Pending |
| S6-17 | Not run | Not run | Pending |
| S6-18 | Not run | Not run | Pending |
| S6-19 | Not run | Not run | Pending |
| S6-20 | Not run | Not run | Pending |
| S6-21 | Not run | Not run | Pending |
| S6-22 | Not run | Not run | Pending |
| S6-23 | Not run | Not run | Pending |
| S6-24 | Not run | Not run | Pending |

For usability, record each tester's actual platform; do not claim both platforms
were assessed when only one was used. Retain the 17 October observations in
#68 separately and add a new record for post-change checks. New evidence can
live in `project/docs/evidence/issue66/`, `issue67/` or `issue68/`, grouped by
platform and run. Screenshots should show inputs/results; timing needs recorded
measurements, and usability needs the observer's task/assistance notes.

## Response-time method and targets - pending agreement

Jackie records the device, commit, models, browser, files and timing method.
For a form, measure from clicking Predict until the label, probability and
recommendations are visible. For CSV, measure from completing file selection
until counts, valid results, skipped reasons and download control are available.
State any exclusions (for example choosing the file, saving the download, or
server startup). Do not label a backend-only timer as full dashboard timing.

Record one first prediction after restarting the app (including model load),
then at least five repeat predictions per scenario. Keep cold and warm results
separate; report individual values plus warm median and maximum. For CSV use
fixed fictional 30-row and 395-row fixtures, valid and mixed cases, in both
modes; include blank and supplied G2 in Confirmatory fixtures. Record expected
valid/skipped counts. If fixtures need preparing, retain them with the run.

The following are proposed classroom-prototype targets, not measured results or
approved requirements. Confirm them before judging pass/fail. Agree one reference
computer for acceptance timing; record other platforms separately for comparison
unless the team requires both to meet the limits. Keep all measured repeats,
including slow ones. Do not silently relax a target after a failed run.

| Area | Proposed target | Decision needed | Agreed by / date |
|---|---|---|---|
| Single prediction | First prediction after app restart <=10 s; each of five subsequent predictions <=3 s | Confirm reference computer, all three model setups and timing through visible prediction/recommendations; server startup excluded | Pending tutor/team agreement |
| 30-row CSV | First run after app restart <=10 s; each of five subsequent runs <=5 s | Confirm fictional fixtures, both modes, valid/mixed cases and expected totals; time from completed file selection to complete results and download control | Pending tutor/team agreement |
| 395-row CSV | First run after app restart <=20 s; each of five subsequent runs <=10 s | Confirm same measurement boundary and limits for valid/mixed cases; record expected valid/skipped counts | Pending tutor/team agreement |
| Main user tasks | Complete all four tasks below without verbal help, using on-screen instructions | Confirm task list and permitted help; record assistance and repeat affected tasks after improvements | Pending tutor/team agreement |
| Understanding limitations | Tester explains that the probability is a model estimate, can be wrong and must not be used alone for student decisions | Agree questions; assess the initial answer before explaining | Pending tutor/team agreement |
| Readability | At agreed laptop screen sizes and 100% browser zoom, labels/messages are readable, full recommendations accessible and controls not clipped | Record screen sizes; agree whether horizontal scrolling for CSV tables is acceptable; long recommendations must remain easy to read | Pending tutor/team agreement |

### Four proposed usability tasks

1. Make an Early-Warning prediction with attendance 40, study hours 4 and
   failures 0. The baseline result is High Risk (0.859) with attendance support.
2. Make a Confirmatory prediction with attendance 80, study hours 4, failures 0,
   G1 8 and G2 blank. The baseline result is High Risk (0.818), using G1 only.
3. Upload `project/data/sample_roster.csv` in Confirmatory mode and download
   the valid results.
4. Find the skipped rows and explain what needs correcting for C and D.

Early-Warning means predicting without grades; it does not mean Low Risk.
Both modes can return High Risk or Low Risk. The agreed High-Risk-only policy
applies to targeted recommendations: Low-Risk predictions are still displayed
with routine guidance. They are not skipped. Only invalid CSV rows are skipped.
The first usability task uses a known High-Risk example, so it is consistent
with the agreed policy. Functional tests still check Low-Risk routine guidance.

Observe task completion without coaching, then ask the tester to explain the
result and why it should not be used alone for decisions. Record any help after
the initial attempt. A correct result with help is not independent success.
Do not convert one tester's result into a claim about all users. S6-21 also
checks understanding of G1+G2; its functional routing is covered by S6-04/05.

Issue #65 asks for practical response-time and usability targets to be agreed
with the tutor. Ask for those limits and record the actual decision here before
judging pass/fail. Tutor feedback that the prototype can proceed is not an
agreement to numerical targets. This is separate from team-approved rules.

## Review and completion

| Review item | Status | Reviewer / date / evidence |
|---|---|---|
| Requirement coverage and steps | Pending team review | Pending |
| Platform and timing procedure | Pending Jackie review | Pending |
| Rules and usability procedure | Pending Anna review | Pending |
| Response-time and usability targets | Pending tutor/team agreement | Pending |

Close #65 after this plan is reviewed, targets agreed and the PR merged. The
actual runs need not be finished to close the planning issue; they belong to
#66-#69. Benjamin links their outcomes in #70. Leave failed, blocked and unfinished
work visible. Preserve assignment files and prompt logs.
