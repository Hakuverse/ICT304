# Windows and macOS test packages

Prepared for #114 and #115 on 27 October 2026. Anna will test Windows and Jackie
will test macOS, as confirmed by Benjamin. Packages are test candidates, not an
approved public release. Do not close either issue until its actual platform
results have been reviewed.

## Get the correct package

1. Open the packaging PR and its **Checks**, or the repository **Actions** tab.
2. Choose **Build SARAH test apps** for the exact commit being reviewed. Wait for
   the platform build to finish successfully; do not use an artifact from a failed run.
3. Download `SARAH-windows-x64-...` for Anna or `SARAH-macos-arm64-...` for Jackie.
   GitHub may require you to sign in to download Actions artifacts.
4. Extract the outer Actions download. It contains the actual versioned SARAH
   ZIP, its SHA-256 checksum, build details and extracted-package smoke results.
5. Extract the inner SARAH ZIP. On macOS use Archive Utility so the app's links
   and permissions are preserved. Keep the Windows application folder together.
6. Read START-HERE.txt and record the package filename and source commit from
   build-info.json. Files built on different source commits must not be described
   as the same tested version.

The workflow uses native Windows x64 and macOS Apple Silicon build machines.
A hosted Mac build is not a test on Jackie's M3/Tahoe computer. The actual OS
version/build and chip must be recorded from his Mac. The tutor has the same
reported platform, but their security settings and launch result remain separate.

## First platform check

Anna records results in `project/docs/evidence/app/windows/results.md` and Jackie
in `project/docs/evidence/app/macos/results.md`. These files start as pending.
Record actual results, including failures, rather than replacing every row with Pass.

| Check | What to do | Screenshot when useful |
|---|---|---|
| W01 / M01 | Record OS/build/chip, browser, package name/source commit and whether Python is installed. Extract into a folder with spaces, outside the repo. | `01-package-and-platform.png` (hide personal details) |
| W02 / M02 | Double-click SARAH.exe or SARAH.app. Record any downloaded-file/security warning exactly. Stop and report a block; do not disable security protections. | `02-first-launch.png` |
| W03 / M03 | Check Starting then Ready, automatic browser opening and usable form controls. Record actual startup time; repeat according to the application plan. | `03-ready-dashboard.png` |
| W04 / M04 | Close the browser tab, then use Open dashboard. Double-click the app again and check the already-open message. | `04-open-and-repeat.png` |
| W05 / M05 | Early-Warning: attendance 40, study 4, failures 0. Expect High Risk 85.9% and attendance support. | `05-prediction.png` |
| W06 / M06 | Confirmatory: attendance 80, study 40, failures 0, G1 12, G2 blank. Expect High Risk 66.1% and the study-hours warning. | `06-study-warning.png` |
| W07 / M07 | In Confirmatory CSV mode upload sample_roster.csv: two valid, two skipped. Upload study_hours_warning_demo.csv: two valid, one warning. Download results and open the file. | `07-csv-results.png`, `08-downloaded-results.png`; retain fictional exported CSV |
| W08 / M08 | With the app already downloaded/extracted, disconnect the test computer from the network if practical and repeat a prediction. Reconnect afterwards. If not performed, record Not tested. | Optional screenshot; record actual method |
| W09 / M09 | Quit SARAH from the launcher. Confirm the old URL no longer responds after refresh, then reopen the app. Use a normal account, not Run as administrator. | `09-quit-and-restart.png` |

Screenshots may cover multiple checks if all relevant information is visible.
Record browser version, assistance, start/end times and exact errors in the results
table. Do not use server health timings as user-visible startup evidence. A known
developer computer is not a clean-machine check; describe that limitation.

These are the package-specific #114/#115 checks. #116 adds the full packaged
workflow/boundary checks; #117 adds another-person download-to-use evidence.
Reuse correctly labelled evidence where it covers both issues rather than repeat
the same action solely to produce another screenshot.

## What the build already checks

The builder runs the fictional model/form/CSV smoke check before archiving and
again after extraction. It checks health, HTML/static assets, normal shutdown and
loss of the launcher pipe. The workflow also runs application and packaging tests.
Those automated results do not establish GUI usability, Gatekeeper/SmartScreen
behaviour, offline use on the recipient's machine or the 30-second target.

## After the checks

Add the actual evidence in a PR and identify the tested package. A teammate reviews
the results. Fix any blocker and repeat affected checks on the rebuilt package.
Only #118 publishes the accepted release; #97/#98 still cover submission packaging
and readiness. Earlier video and platform results retain their original versions.

## Developer fallback

If GitHub Actions is unavailable, the build can run on a matching developer machine.
Follow [the build guide](../packaging/README.md), then run the packaging command.
Jackie should not need this route merely to test a successfully built artifact.
