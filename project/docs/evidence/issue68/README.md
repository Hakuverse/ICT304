# Usability evidence - Issue #68

Owner: Anna. Cases: **S6-21 to S6-23** in the
[system test plan](../../system-test-plan.md).

Record the tester's actual platform, date, tested commit and each task/question.
Record initial answers and independent/helped/not-completed outcomes before
coaching. Include what help was provided and the outcome afterwards. Use anonymous
tester labels; do not include private details or participant photographs.

One dated session record can support all three cases. Screenshots are optional;
they do not replace the task/assistance notes. Both Windows and macOS are not
automatically required for each usability session. Mark the other platform
not assessed rather than implying a second run.

Keep the [17 October record](../../usability-feedback.md) as earlier evidence.
Retests after changes need a new dated record and commit. This folder does not
change existing findings or approve new changes on issue #68.

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
