# Readability and fix-retest evidence - Issue #69

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

| Case / subcase | Input or fixture | Actual result | Status | Evidence link | Fix / retest link |
|---|---|---|---|---|---|
| Fill after testing | | | Not run | | |

Use Pass, Fail, Blocked or Not run for functional checks. Timing/usability
acceptance stays pending until targets are agreed. Record assistance separately
for user tasks. One screenshot or log can support several cases: link it from
each applicable row. Do not copy older evidence as a new pass.

Save readable PNG screenshots, terminal logs, and fictional CSV fixtures/exports
where useful. Exclude virtual environments, caches, model copies and private data.
Link the run from the corresponding actual-result row in the system test plan.
