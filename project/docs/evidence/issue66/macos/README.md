# macOS workflow evidence - Issue #66

Tester/coordinator: Jackie.
Cases: **S6-01 to S6-18** in the [system test plan](../../../system-test-plan.md).

Follow the project README setup from a clean checkout. Use `.venv/bin/python`
for the Python commands. Run functional form/CSV checks and save actual outcomes
for all listed subcases. S6-17/18 use recommendation test output; record any
extra boundary case separately.

Save versions/commit, full test output, representative input/error screenshots,
and the fictional downloaded CSV. Link shared evidence to every case it supports.
Windows screenshots cannot establish macOS behaviour.

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
