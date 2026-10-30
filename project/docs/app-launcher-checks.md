# Application launcher checks

Issue #113. Checked on 27 October 2026 by automated development checks, not a
new teammate walkthrough. Source commit: `6874d0eb074762c677251de9abdc7b745cddb00d`.
Base: `7f4914d` after the merged application plan PR #119.

## Environment and scope

Windows 11 Home 25H2 x64, Python 3.12.10. PyInstaller 6.22.3 built a local Windows
application folder using the existing separate build environment from the earlier
trial. Current sources and models were bundled; the old trial executable was not
reused. The [environment record](evidence/app/launcher/windows-build-environment.txt)
records build packages. A later clean package build remains part of #114.

## Results

| Check | Actual outcome |
|---|---|
| Existing project suite | 110 tests passed in 24.589 seconds |
| Focused launcher suite | 13 tests passed in 0.026 seconds |
| Source runtime smoke | Passed fictional predictions, current dashboard form/warning, CSV export, health/HTML and 69 static assets |
| Windows executable build | Completed successfully |
| Packaged runtime smoke | Passed the same checks from an external working folder with Python/Git removed from PATH |
| Normal shutdown | Server port closed in source and executable checks |
| Parent connection lost | Server exited and released the port when the parent pipe closed |
| Hidden source Tk event loop | Reached Ready, requested automatic browser opening, enabled Open dashboard, and Quit released the instance lock; browser opening was mocked |
| Repeated launch lock | Second lock attempt rejected; reacquisition succeeded after release in the focused tests |

[Source runtime results](evidence/app/launcher/source-runtime.json) and
[Windows bundle results](evidence/app/launcher/windows-bundle-runtime.json) retain
fictional predictions and lifecycle outcomes. The smoke test confirms that the
40-hour G1-only example remains High Risk 0.661, with a warning; no model change
is implied. Health-check timings are internal readiness observations, not the
agreed double-click-to-usable-dashboard measurement.

The first restricted test attempt could not access temporary folders. Tests were
rerun with normal local permissions and passed. The first source shutdown probe
checked the port before the Windows Python redirector's interpreter had finished
exiting. The check now waits up to ten seconds for actual port release; source
and executable checks then passed. It does not ignore a port that stays open.

## Commands

From the repository root, using the tested Python environment:

```text
python -m unittest discover -s project/packaging -v
python -m unittest discover -s project/code -v
python project/packaging/check_runtime.py --output source-runtime.json
python -m PyInstaller --noconfirm project/packaging/SARAH.spec
python project/packaging/check_runtime.py --executable dist/SARAH/SARAH.exe --output windows-bundle-runtime.json
```

The hidden Tk check programmatically exercised source GUI callbacks with the
window hidden and browser opening mocked. It was a developer check, not a human
visual review or a packaged GUI walkthrough.

## Follow-up status — 31 October 2026

PR #120 is merged and #113 is closed. The development results above retain their
original scope. The later startup fix and Windows/macOS device records were
reviewed in merged PR #121; #114/#115 are closed. Workflow evidence (#116) was
reviewed in PR #122 and walkthrough evidence (#117) in PR #123.

The [release record](app-release-notes.md) identifies the published ab4a604 ZIPs,
actual routine-startup results, unsigned-app restrictions and evidence limits.
These later results do not turn the earlier mocked browser check into a manual
walkthrough. The tutor's computer remains untested. The
[developer guide](../packaging/README.md) explains rebuilding and smoke checks.
