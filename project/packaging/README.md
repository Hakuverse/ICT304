# Building the SARAH launcher

These instructions are for the team building the app. End users will open the
packaged application, not run these commands. The [application plan](../docs/app-deployment-plan.md)
defines the original targets; the [release record](../docs/app-release-notes.md)
identifies the published tested packages. Rebuilding creates a new candidate that
needs its own checks; these commands are not needed to use the released app.

## Files

- `launcher.py`: shared Windows/macOS launcher and local server entry point.
- `SARAH.spec`: PyInstaller recipe for a Windows application folder or macOS app.
- `test_launcher.py`: focused lifecycle, path, locking and error checks.
- `bundle_check.py`: fictional prediction, form-warning and CSV smoke checks.
- `check_runtime.py`: smoke checks outside the source folder, with Python/Git
  removed from PATH for the executable check. This is not a clean-machine test.

The launcher uses a per-user OS file lock. A second launch shows an already-open
message and does not start another service. The service binds to a free loopback
port with a random session path; the browser opens after its health check passes.
The child watches a pipe owned by the launcher and exits when it closes, including
when the launcher crashes. Quit also terminates only the child it started.
Before starting that watcher, the child loads all three models so native numerical
libraries are initialised before a background read of stdin on Windows.

The GUI reports a slower start after 30 seconds and stops a failed startup after
90 seconds. The 90-second timeout does not change the agreed 30-second target.
Health readiness is not proof that the browser dashboard is usable within target.

Only fixed lifecycle events are written to `launcher.log` under the user's
local SARAH folder (LocalAppData on Windows, Library/Application Support on Mac).
Server stdout/stderr are discarded so uploaded data and exception payloads are
not written there. Report startup problems using app version, OS and the basic
record; do not upload private CSVs. A developer can reproduce with fictional data.

## Developer environment

Use Python 3.12 with Tk support. On Mac, use a native Apple Silicon Python with
Tk support for the M3 build. Verify Tk before building with `python -m tkinter`
using the selected environment. Do not build a Mac release on Windows.

From the repository root, Windows PowerShell:

```powershell
py -3.12 -m venv .build-venv
.build-venv\Scripts\python.exe -m pip install -r project/code/requirements.txt
.build-venv\Scripts\python.exe -m pip install pyinstaller==6.22.3
.build-venv\Scripts\python.exe -m pip check
.build-venv\Scripts\python.exe -m unittest discover -s project/packaging -v
.build-venv\Scripts\python.exe -m unittest discover -s project/code -v
.build-venv\Scripts\python.exe project/packaging/launcher.py
```

macOS Terminal (developer steps; Jackie's M3/Tahoe device checks remain under #115):

```bash
python3.12 -m venv .build-venv
.build-venv/bin/python -m pip install -r project/code/requirements.txt
.build-venv/bin/python -m pip install pyinstaller==6.22.3
.build-venv/bin/python -m pip check
.build-venv/bin/python -m unittest discover -s project/packaging -v
.build-venv/bin/python -m unittest discover -s project/code -v
.build-venv/bin/python project/packaging/launcher.py
```

The application requirements contain version ranges. Record `pip freeze` for
each tested build; an installation on a later date may resolve differently.
There is no package installation or retraining at normal application startup.

## Build and check

Quit any existing SARAH development build before rebuilding. On Windows:

```powershell
.build-venv\Scripts\python.exe -m PyInstaller --noconfirm project/packaging/SARAH.spec
.build-venv\Scripts\python.exe project/packaging/check_runtime.py --executable dist/SARAH/SARAH.exe --output dist/runtime-check.json
.build-venv\Scripts\python.exe -m pip freeze > dist/build-environment.txt
```

On macOS:

```bash
.build-venv/bin/python -m PyInstaller --noconfirm project/packaging/SARAH.spec
.build-venv/bin/python project/packaging/check_runtime.py --executable dist/SARAH.app/Contents/MacOS/SARAH --output dist/runtime-check.json
.build-venv/bin/python -m pip freeze > dist/build-environment.txt
```

Windows output is the complete `dist/SARAH/` folder, including its supporting
files. macOS output is `dist/SARAH.app`. The recipe uses the build environment's
architecture. No Developer ID/notarization or Windows publisher certificate is
configured. Mac build-tool ad-hoc signing is not verified publisher identity.

The development smoke check verifies all three model setups, the 40-hour warning,
CSV export, dashboard rendering, served HTML/static assets, normal stop and
parent-pipe closure. It also opens a live WebSocket session and requires both
the form and a prediction result, catching faults that a health check misses.
The developer check needs `websockets>=12,<17` (included by current Streamlit;
install it separately if using an older environment).
It does not click the native GUI or measure human-visible
startup. For source checking, omit `--executable` and keep `--output`.

## Before distributing

Keep builds and virtual environments out of source commits. PR #121 provides
complete test candidates with notices, version records, checksums and download
instructions, not an accepted release. #114/#115 still require reviewed platform
evidence. #116/#117 must check the actual GUI, downloads,
security prompts, clean-device behaviour, startup timing and another-person use.
Use #118 to publish accepted artifacts and update user-facing instructions.

See the [launcher verification record](../docs/app-launcher-checks.md) for actual
outcomes and remaining platform limits.


## Complete test packages for #114 and #115

After the environment setup above, commit the build sources and ensure the
checkout is clean. Run on the matching platform:

```text
python project/packaging/build_package.py --version 0.1.0-preview
```

Use the selected `.build-venv` Python path in place of `python`. The builder
checks dependencies/Tk, builds, adds samples/notices/build details, runs the
runtime smoke check, archives the app and checks an extracted copy. Output is
under `dist/packages/`, with a source-commit suffix and SHA-256 checksum.
Existing archives are not overwritten. Use a new version for a new candidate.
Mac archives use ditto to preserve .app symlinks and permissions.

The Build SARAH test apps workflow performs this on native Windows x64 and
Apple Silicon macOS runners. The team can also start it through
Actions > Build SARAH test apps > Run workflow. It uploads test artifacts only;
it does not publish a release. Download artifacts within their 14-day retention
period and retain the chosen tested package for submission separately.

See [Anna and Jackie's testing guide](../docs/app-package-testing.md). Signing,
GUI startup, clean-device checks and recipient security behaviour remain
explicit manual follow-ups. The runner OS is recorded in build-info.json and
must not be described as Jackie's or the tutor's actual computer.

Current candidate links and the evidence-before-approval process are maintained
in that guide. Anna tests Windows, Jackie tests macOS, and Benjamin coordinates
builds and evidence. Do not rebuild solely for a documentation-only change;
retain the tested package's own source identity. Recheck affected behaviour when
application or packaging code changes.
