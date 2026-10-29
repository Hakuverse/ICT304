# Platform package build checks

## Windows loading fix — 28 October 2026

Benjamin reported that candidate `c7440f7` opened its launcher and browser but
stayed loading. This was reproduced locally. A diagnostic trace showed a native
numerical-library import blocked while the launcher watcher read its parent pipe.
The launcher now loads all three saved models and their dependencies before
starting that watcher. This changes startup order, not the predictions.

The earlier smoke checks below are historical results, not acceptance of those
packages. Their in-process model tests preloaded dependencies; their separate
live-server checks only fetched health, HTML and static assets. They missed the
first live dashboard/prediction import. Do not use earlier candidates for acceptance.

The strengthened check opens a live WebSocket session, requires the form controls,
presses Predict and requires a probability result. It runs before archiving and
on the extracted package, for both normal stop and parent-pipe closure.

A corrected local Windows executable passed these checks, all model examples,
the study-hours warning and CSV checks. A browser check also displayed the full
form and returned High Risk, 85.9% for attendance 40, study hours 4, failures 0.
All 18 launcher/package unit tests passed. See the
[corrected local runtime record](evidence/app/windows/startup-fix-runtime-check.json).
This was a local development check. Anna and Jackie subsequently tested the
rebuilt ab4a604 candidate; see the device records below for outcomes and gaps.

The replacement [hosted build](https://github.com/Hakuverse/ICT304/actions/runs/40556703379)
passed on Windows and Apple Silicon macOS for PR head `9cdda7a`. Both platforms
passed the live form/prediction checks before archiving and after extraction.
Benjamin's [preliminary Windows launch record](evidence/app/windows/benjamin-preliminary/README.md)
identifies downloaded candidate `ab4a604` and its observed SmartScreen warning.
Full platform acceptance remains pending.

## Earlier build records

Recorded 27 October 2026. These are development/build checks, separate from
Anna and Jackie's manual results. PR #121 implements packaging for #114/#115;
those issues remain open until their platform evidence is reviewed.

## Local Windows candidate

- Source: `a47f7f6` (package builder on top of merged #120).
- Platform: Windows x64, Python 3.12.10, PyInstaller 6.22.3.
- File: `SARAH-0.1.0-preview-windows-x64-a47f7f6.zip`.
- Size: 134,453,307 bytes (about 128 MiB).
- SHA-256: `cebeb8f4553ca2c3f3040eb6f3a4cb68a5eca5f051bea61185f3df11d55cc96b`.
- Package/launcher tests: 18 passed in 0.067 seconds.
- Build and runtime smoke: passed before archiving and after extracting the ZIP
  into a separate folder with spaces. Python/Git were removed from the child's PATH.
- Extracted checks passed all three grade setups, the 40-hour warning, form
  rendering, CSV warning export, HTML/static assets and shutdown on normal stop
  and parent-pipe closure.

The complete archive includes the application folder, samples, opening guide,
build metadata, package versions and available dependency/runtime licence notices.
This is not a claim that final licence review under #118 is complete.
The build used the existing separate Windows build environment; it was not a
new Windows clean-machine installation.

Evidence:
- [Build details](evidence/app/windows/SARAH-0.1.0-preview-windows-x64-a47f7f6-build-info.json)
- [Extracted runtime checks](evidence/app/windows/SARAH-0.1.0-preview-windows-x64-a47f7f6-extracted-check.json)
- [Archive checksum](evidence/app/windows/SARAH-0.1.0-preview-windows-x64-a47f7f6.sha256)

The archive itself is a generated local artifact, not committed source. The
GitHub Actions builds may have a later commit containing documentation updates;
record each actual artifact's own metadata, not this local artifact's checksum.

## Hosted builds and manual follow-up

[Build run](https://github.com/Hakuverse/ICT304/actions/runs/40467181355) builds
Windows and Apple Silicon macOS from the PR version. Check the actual run result
and artifact metadata. A green hosted build is not an M3/Tahoe or recipient
security test. Later reruns must be identified separately.

[Anna's Windows record](evidence/app/windows/results.md), submitted 29 October,
records working functional checks and launch after SmartScreen. The first download
launch took 74.67 seconds including the warning; later starts were 11.15, 6.46
and 4.35 seconds. The separate post-approval reboot launch was reported at 13.20 seconds, with Edge initially closed and no SmartScreen; the routine startup target is met.
[Jackie's Mac record](evidence/app/macos/results.md), submitted 28 October for
candidate ab4a604 from run 40556703379, records M01-M09, offline prediction,
routine startup times and launch after a Gatekeeper exception. Peer review is
pending. This was a developer computer; clean-device and tutor-device results
are not established. #116/#117 and #97/#98 retain their roles.
