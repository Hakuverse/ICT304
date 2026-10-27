# Platform package build checks

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

[Anna's Windows record](evidence/app/windows/results.md) and
[Jackie's Mac record](evidence/app/macos/results.md) remain pending until they
perform the [package checks](app-package-testing.md). No double-click timing,
offline recipient workflow, Gatekeeper/SmartScreen acceptance, clean-device use
or tutor-device pass is claimed here. #116/#117 and #97/#98 retain their roles.
