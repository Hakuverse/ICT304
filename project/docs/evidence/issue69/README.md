# Readability and fix-retest evidence - Issue #69

Current status: reviewed through merged PR #102; the issue is closed.
[Recorded results](2026-10-20-e246495/results.md) retain the original outcomes and assistance limits.
The instructions below apply only to future runs.

Owner: Anna. Case: **S6-24**, plus affected S6-01 to S6-23 cases, in the
[system test plan](../../system-test-plan.md).

After changes, record the fix PR, new commit, browser, screen size and zoom.
Capture the updated form (mode/field help, probability explanation and human-review
notice) and CSV view (counts, skipped warning, full readable messages). Check
controls and text are not clipped. Benjamin and Jackie can provide Windows/macOS
layout observations; record each platform actually checked.

Repeat affected functional cases and the automated suite after code changes.
For new user observations under S6-21/22/23, link to the dated run in issue68
rather than duplicating it. Link any repeat platform run in issue66 the same way.
Keep before/after evidence with its correct commit; implementation is not proof
of a successful retest.

## Recording a run

Create a subfolder named `YYYY-MM-DD-shortcommit` for the actual run. Record date,
tester, commit, OS, Python/package versions and browser/screen size where relevant.
Use fictional students only. Keep earlier runs; do not overwrite their evidence.

Add a `results.md` file inside the run folder:

For any future run, record the case/subcase, input or fixture, actual result,
status, evidence link and any fix/retest link. Existing results are linked above;
there is no unfinished run table in this index.

Use Pass, Fail, Blocked or Not run for functional checks. Timing/usability
results use the targets agreed by the team on 19 October 2026. Record assistance separately
for user tasks. One screenshot or log can support several cases: link it from
each applicable row. Do not copy older evidence as a new pass.

Save readable PNG screenshots, terminal logs, and fictional CSV fixtures/exports
where useful. Exclude virtual environments, caches, model copies and private data.
Link the run from the corresponding actual-result row in the system test plan.
