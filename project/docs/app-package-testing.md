# Windows and macOS test packages

Originally prepared for #114/#115 on 27 October 2026. Their device evidence was
reviewed in merged PR #121; #116 workflow evidence was reviewed in merged PR #122.
Continue with the [#117 download-to-use walkthrough](app-walkthrough.md).
The same ab4a604 packages remain test candidates, not a final published release.

## Get the correct package

Current candidate, checked 28 October 2026: source `ab4a604`, built from PR #121
code head `9cdda7a`. Later evidence/documentation commits do not change these files.
Both platform jobs passed in [run 40556703379](https://github.com/Hakuverse/ICT304/actions/runs/40556703379).

- [Anna: Windows package -4](https://github.com/Hakuverse/ICT304/actions/runs/40556703379/artifacts/12757642322)
- [Jackie: Apple Silicon macOS package -4](https://github.com/Hakuverse/ICT304/actions/runs/40556703379/artifacts/12758175843)

Earlier candidates are superseded after the Windows loading fault. Use `-4`,
record its own build-info.json, and retain it locally before the 14-day artifact
retention expires. These are review candidates, not a published release.

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

Keep the checksum, build-info and extracted-check JSON files alongside the
extracted package as evidence. They do not need to be combined into one file or
re-zipped. Keep SARAH.exe beside its complete _internal folder on Windows.

## Unsigned-app first launch

Windows may show "Windows protected your PC". Only consider continuing for the
team's verified download, with a matching package checksum. More info shows the
application and publisher. If it identifies SARAH.exe and Run anyway is offered,
the tester may choose it where their device policy permits. Record the warning,
the decision and actual launch outcome. Do not disable security protections.
If no permitted option is available, stop and report the block.

Benjamin's [preliminary check](evidence/app/windows/benjamin-preliminary/README.md)
recorded Unknown publisher and a successful launch after Run anyway. This does
not establish that Anna's computer will behave the same way. Mac testers must
record their own Gatekeeper outcome; Windows steps do not apply to macOS.

Jackie's [macOS first-opening guide](evidence/app/macos/results.md#first-opening-on-macos)
records the Done > Privacy & Security > Open Anyway sequence observed on his Mac.
His M01-M09 tests used the app's bundled Python 3.12.10, not the Python 3.13.3
or 3.13.9 installations on his computer.

## Historical #114/#115 evidence procedure (PR #121, now merged)

Testing can start before approval or merge. Anna fills the Windows record and
Jackie fills the Mac record. Add screenshots and fictional exports in their
platform folders, using the filenames below. Keep personal details out of images.

While PR #121 is open, commit evidence to its `app-platform-packages` branch, or
send it to Benjamin to add there. Review and approve the latest PR after evidence
is included and blockers are resolved. Approval alone does not record tests.
If the PR has already merged, add subsequent evidence through a new branch/PR.
Keep #114/#115 open until the relevant platform evidence is reviewed.

The workflow uses native Windows x64 and macOS Apple Silicon build machines.
A hosted Mac build is not a test on Jackie's M3/Tahoe computer. The actual OS
version/build and chip must be recorded from his Mac. The tutor has the same
reported platform, but their security settings and launch result remain separate.

## First platform check

Anna records results in `project/docs/evidence/app/windows/results.md` and Jackie
in `project/docs/evidence/app/macos/results.md`. Jackie's 28 October device evidence
is submitted for review. Anna's 29 October Windows evidence is also submitted;
W03 now includes a 13.20-second post-approval reboot launch, meeting the routine startup target. Peer review remains pending.
Record actual results, including failures, rather than replacing every row with Pass.

| Check | What to do | Screenshot when useful |
|---|---|---|
| W01 / M01 | Record OS/build/chip, browser, package name/source commit and whether Python is installed. Extract into a folder with spaces, outside the repo. | `01-package-and-platform.png` (hide personal details) |
| W02 / M02 | Double-click SARAH.exe or SARAH.app. Record any downloaded-file/security warning exactly. Stop and report a block; do not disable security protections. | `02-first-launch.png` |
| W03 / M03 | Check Starting then Ready, automatic browser opening and usable form controls. Record actual startup time; repeat according to the application plan. | `03-ready-dashboard.png` |
| W04 / M04 | Close the browser tab, then use Open dashboard. Double-click the app again and record what happens. On macOS Finder may bring the existing launcher forward without a separate already-open message; confirm it remains usable. | `04-open-and-repeat.png` |
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
loss of the launcher pipe. The corrected build also opens a live WebSocket session,
requires the form, presses Predict and requires a probability result. The workflow
also runs application and packaging tests.
Those automated results do not establish GUI usability, Gatekeeper/SmartScreen
behaviour, offline use on the recipient's machine or the 30-second target.

## After the checks

PR #121 merged on 29 October; #114/#115 are closed following review. Continue
with the [#116 packaged workflow run sheet](app-workflow-testing.md), which reuses
the recorded checks and lists the remaining form, CSV and occupied-port cases.

Add the actual evidence in a PR and identify the tested package. A teammate reviews
the results. Fix any blocker and repeat affected checks on the rebuilt package.
Only #118 publishes the accepted release; #97/#98 still cover submission packaging
and readiness. Earlier video and platform results retain their original versions.

## Developer fallback

If GitHub Actions is unavailable, the build can run on a matching developer machine.
Follow [the build guide](../packaging/README.md), then run the packaging command.
Jackie should not need this route merely to test a successfully built artifact.
