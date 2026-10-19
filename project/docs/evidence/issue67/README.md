# Response-time evidence - Issue #67

Owner: Jackie. Cases: **S6-19 and S6-20** in the
[system test plan](../../system-test-plan.md).

Use the agreed reference computer and record its platform. Additional platform
measurements are separate comparisons unless both are required by agreement.
Follow the plan's full-dashboard timing boundaries. Keep the first run after
restart separate from at least five subsequent runs for each scenario. Record
all individual times, warm median/maximum, expected and actual row counts,
fixture files and timing method. A screenshot of results alone does not prove time.

The limits in PR #85 were agreed by the team on 19 October 2026. Use Jackie's
MacBook Air (M3, 24 GB RAM, macOS 26.6.2) as the reference device and follow the
plan's remove-and-reupload procedure for fresh repeated CSV processing.

Suggested files: `results.md`, `timings.csv`, fictional input fixtures, and
optional screenshots showing the resulting counts/results.

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
