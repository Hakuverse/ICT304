# SARAH system test plan - Sprint 6

Owner: Benjamin. Prepared: 19 October 2026. Issue: #65.
Status: reviewed; targets agreed by team on 19 October 2026. Planning PR #85 merged; Windows functional results added below.
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

Use the [evidence folder index](evidence/README.md) for ownership, case numbers
and per-folder recording instructions.

Use Not run, Pass, Fail or Blocked for functional cases. Timing/usability cases
use the team-agreed targets below; actual results still require a recorded run.
For user tasks additionally record independent, helped or not completed. A
correct result with assistance is not independent success.

| ID | Windows actual result / status | macOS actual result / status | Evidence / fix / retest link |
|---|---|---|---|
| S6-01 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-02 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-03 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-04 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-05 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-06 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-07 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-08 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-09 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-10 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-11 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-12 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-13 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-14 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-15 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-16 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-17 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-18 | Pass - Benjamin, 19 October 2026, 9dc7132 | Not run | [Windows results and subcases](evidence/issue66/windows/2026-10-19-9dc7132/results.md) |
| S6-19 | Not run | Not run | Pending |
| S6-20 | Not run | Not run | Pending |
| S6-21 | Target not met - Anna, 19 October 2026, 9dc7132 (one tester, same as 17 October): task 1 assisted (non-verbal nod), task 2 independent; G1/G2 and blank vs 0 explained; attendance not described as an estimate | Not run | [#69 retest results](evidence/issue69/2026-10-19-9dc7132/results.md); before: [17 October record](usability-feedback.md) |
| S6-22 | Partly met - Anna, 19 October 2026, 9dc7132: High Risk understood; would not use the result alone; probability read as a percentage but not described as an estimate that can be wrong | Not run | [#69 retest results](evidence/issue69/2026-10-19-9dc7132/results.md); before: [17 October record](usability-feedback.md) |
| S6-23 | Target not met - Anna, 19 October 2026, 9dc7132: task 3 independent (A and B predicted, download worked); task 4 not completed: skipped warning noticed, but C/D reasons and fixes not explained; valid results stayed visible | Not run | [#69 retest results](evidence/issue69/2026-10-19-9dc7132/results.md); before: [17 October record](usability-feedback.md) |
| S6-24 | Pass - Anna, 19 October 2026, 9dc7132: Edge DevTools device mode at 1366 x 768 and 1920 x 1080, 100% zoom; all six subcases Pass | Not run | [#69 retest results and screenshots](evidence/issue69/2026-10-19-9dc7132/results.md); fixes #86, #87 |

For usability, record each tester's actual platform; do not claim both platforms
were assessed when only one was used. Retain the 17 October observations in
#68 separately and add a new record for post-change checks. New evidence can
live in `project/docs/evidence/issue66/`, `issue67/`, `issue68/` or `issue69/`, grouped by
platform and run. Screenshots should show inputs/results; timing needs recorded
measurements, and usability needs the observer's task/assistance notes.

## Response-time method and targets - agreed 19 October 2026

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

The team agreed these targets on 19 October 2026. They are acceptance targets,
not measured results. Reference device: Jackie's MacBook Air, Apple M3,
24 GB RAM, macOS 26.6.2 (as reported in his review). Record other platforms
separately for comparison. Keep all measured repeats, including slow ones;
do not silently relax a target after a failed run.

| Area | Agreed target | Agreed method / conditions | Agreed by / date |
|---|---|---|---|
| Single prediction | First prediction after app restart <=10 s; each of five subsequent predictions <=3 s | Jackie's reference device; all three setups; click Predict to complete visible results/recommendations; exclude server startup | Agreed by team - 19 October 2026 |
| 30-row CSV | First run after app restart <=10 s; each of five subsequent runs <=5 s | Reference device; both modes, valid and mixed files; completed file selection to counts, results, reasons and download control; record exact fixtures and expected totals | Agreed by team - 19 October 2026 |
| 395-row CSV | First run after app restart <=20 s; each of five subsequent runs <=10 s | Same CSV procedure and reference device; record exact fixtures and expected totals | Agreed by team - 19 October 2026 |
| Main user tasks | Complete all four tasks below without verbal help, using on-screen instructions | Observe without coaching; offer help only on request or after about one minute stuck; mark any helped task as assisted, not an independent pass | Agreed by team - 19 October 2026 |
| Understanding limitations | Tester explains that probability is a model estimate, can be wrong and must not be used alone for student decisions | Ask what the probability means and whether the result can be used alone for a decision; record initial answers before explaining | Agreed by team - 19 October 2026 |
| Readability | Readable full messages and accessible controls at 1920x1080 and 1366x768, 100% zoom | Horizontal scrolling permitted only inside the CSV results table, with every recommendation readable in full; form, buttons, warnings and human-review notice fit without horizontal scrolling | Agreed by team - 19 October 2026 |

### Repeat the same CSV with fresh processing

1. For the first run, restart the app, select the mode and upload the fixture.
2. For each subsequent run, remove the uploaded file using the uploader's remove
   control. Wait until the uploader is empty and the previous CSV results disappear.
3. Select the same unchanged file again. Start timing when file selection completes;
   stop when the complete output is available. Do not include the removal/wait step.
4. Keep the app running between these subsequent runs. Do not count a download,
   a screenshot, or viewing an already loaded result as a new prediction.

The current dashboard calls process_upload when a file is present, with no
result-cache decorator on that path. Removing then re-uploading triggers a new
processing cycle. These are first/subsequent app-run measurements, not proof
that model objects remain cached between predictions. If the implementation
changes, verify the procedure still invokes processing before collecting times.

### Four agreed usability tasks

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

### Exact wording checks for S6-24

Check the accepted #68 wording after #69 changes:

- Human review: "Support tool only. Do not use this prediction alone to make decisions about a student."
- For the G1-only example with baseline probability 0.818:
  "Model-estimated High-Risk probability: 81.8%. This estimate may be inaccurate and should be considered alongside other information about the student."
  Other inputs must show their own computed percentage, not a fixed 81.8%.
- Grade help explains first-period and second-period grades, blank versus zero
  for G2, and attendance as an estimate.
- The skipped-row warning shows the actual skipped count and directs users to
  reasons without hiding valid results. #68 does not prescribe a single exact
  sentence for this warning or every field-help label; check the agreed meaning.

Team agreement is sufficient for these targets; no tutor approval is required.
Jackie's review requested the repeat-upload clarification above. Anna requested
exact wording checks, now included here. The remaining fixture filenames/counts,
browser and timing instrument are run-record details to fill before measurement,
not unresolved target approvals.

## Review and completion

| Review item | Status | Reviewer / date / evidence |
|---|---|---|
| Requirement coverage and steps | Reviewed | Team - 19 October 2026; owner confirmation and reviews below |
| Platform and timing procedure | Reviewed; upload-repeat clarification added | [Jackie - 19 October 2026](https://github.com/Hakuverse/ICT304/pull/85#pullrequestreview-5567670191) |
| Rules and usability procedure | Reviewed; exact wording checks added | [Anna review](https://github.com/Hakuverse/ICT304/pull/85#pullrequestreview-5567542513) and [conditions](https://github.com/Hakuverse/ICT304/pull/85#issuecomment-6261076489) - 19 October 2026 |
| Response-time and usability targets | Agreed | Agreed by team - 19 October 2026 |

Close #65 when this reviewed plan is merged. Targets are agreed by the team. The
actual runs need not be finished to close the planning issue; they belong to
#66-#69. Benjamin links their outcomes in #70. Leave failed, blocked and unfinished
work visible. Preserve assignment files and prompt logs.
