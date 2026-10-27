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

## Still required

- Anna or Jackie reviews the launcher PR before merge.
- #114: Windows artifact preparation, visual/double-click checks, licences,
  checksums and actual downloaded first-launch restrictions.
- #115: actual M3/macOS build, Tk support, Finder launch, quit behaviour and
  Gatekeeper checks. The shared Mac build recipe is not a tested Mac release.
- #116: full packaged workflow and real GUI startup timing on each target device.
- #117: another person's download-to-use walkthrough and clean-device evidence.
- #118: accepted release assets and user-facing guide/report updates.

No claim is made that the 30-second GUI target passed, that the tutor's computer
was tested, or that the unsigned package will run on every computer. The existing
source setup remains available. The [developer guide](../packaging/README.md)
explains how to build and repeat the smoke checks.
