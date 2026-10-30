# SARAH application deployment plan

Issue: [#112](https://github.com/Hakuverse/ICT304/issues/112).
Decisions confirmed by Benjamin on 27 October 2026; plan merged in PR #119.
Current status updated 31 October 2026: PRs #121–#124 are merged.
See [published release and handover](app-release-notes.md) for #118.
The original acceptance checklist below records planned requirements; actual
outcomes and limitations remain in the linked platform/workflow evidence.
Starting baseline: `4f4d5ce7bf4912d5825e8bd40a48874d3f985b4a` after PR #111.
This is the build plan, not evidence that a packaged app is ready or tested.

## User experience

The user opens SARAH.exe on Windows or SARAH.app on macOS. A small launcher
starts the local service, waits for readiness and opens the dashboard in the
default browser. No separately installed Python, Git or terminal commands are
required for normal use. The runtime, dependencies and saved models are bundled.
Single-student inputs use the existing form; batch inputs use CSV upload.

The launcher shows Starting, Ready or a readable error and provides Open dashboard
and Quit SARAH. Closing a browser tab alone does not stop the service. Quit stops
only the service started by this launcher. Repeated launches and occupied ports
must be handled predictably without orphan processes. Listen on loopback only.
Core predictions must work offline after downloading the complete package.

## Platforms and application format

| Target | Information available | Release scope |
|---|---|---|
| Benjamin's Windows computer | Windows 11 Home 25H2 reported by Benjamin; local system check confirms x64, 25H2, build 26200.9711 | Windows x64 target; Anna's device tests accepted in PR #121 |
| Jackie's Mac | Apple M3, macOS Tahoe 26.6.2 reported by Benjamin | Apple Silicon target; Jackie's M3/Tahoe device tests accepted in PR #121 |
| Tutor's Mac | Apple M3, macOS Tahoe 26.6.2; Benjamin confirmed it matches Jackie's Mac on 27 October | Same initial Apple Silicon target; actual package launch on the tutor's computer remains to be checked |
| Intel Mac / Windows ARM / other OS versions | No agreed test device | Outside the initial verified support claim |

The agreed preference is an application: SARAH.exe on Windows and SARAH.app on
macOS, not a terminal script. This does not require a single standalone Windows
executable or a traditional installer. If the build needs supporting files, ship
the complete application folder and tell users to keep it together. A ZIP or disk
image could serve as the download container; the current #114/#115 candidates
use ZIP archives. Extract the outer Actions ZIP, then the inner SARAH ZIP.
macOS archives preserve app links and permissions. Jackie's [28 October Mac results](evidence/app/macos/results.md)
were reviewed in merged PR #121. [Anna's Windows evidence](evidence/app/windows/results.md)
was submitted on 29 October; routine post-approval reboot timing was confirmed at 13.20 seconds. PR #121 is merged.

Build Windows on Windows and macOS on macOS. Record the actual source commit,
architecture, runtime, dependencies, build tool, artifact name and checksum.
Do not copy the earlier Windows trial as a final release: it predates later fixes.
Rebuild from the reviewed baseline or a later reviewed commit.

## Unsigned prototype decision

The team will proceed without purchasing signing access. No Windows publisher
certificate or Apple Developer ID/notarization is available for this prototype.
Any technical ad-hoc signing needed by the Mac build tool is not Developer ID
signing or notarization and must not be described as verified publisher identity.

Having the file does not guarantee that every computer will allow it to run.
Windows security controls or macOS Gatekeeper may warn or block the download.
Test the actual download-to-launch route on both targets and record the outcome.
Do not instruct users to disable security protections or claim a blocked launch
passed. If device policy prevents use, record the restriction, seek an approved
route or retain the existing source-based setup as a documented fallback.

Signing can be reconsidered later. Reference guidance:
- [Windows application reputation](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation)
- [Apple Developer ID](https://developer.apple.com/developer-id/)

## Roles

Benjamin confirmed this practical arrangement on 27 October:

| Person | Work |
|---|---|
| Benjamin | Coordinate build preparation and evidence; preliminary Windows launch check |
| Jackie | Full macOS package checks and evidence on his M3 Mac |
| Anna | Full Windows package checks and evidence; wording/instruction review |
| All three | Scope decisions, report discussion and release review |

Work may be shared. Record the person who actually performed each check and have
someone other than the builder review it. This does not assign exclusive ownership
of the existing report, slides and closeout issues.

## Acceptance record

The plan was implemented and its evidence reviewed in merged PRs #120–#123.
These are the recorded outcomes, not new tests performed during documentation cleanup.

| Requirement | Recorded outcome and evidence |
|---|---|
| Double-click launch without project setup | Windows newcomer used the packaged executable without Python/source setup; [#117 evidence](evidence/app/issue117/README.md). Mac app used its bundled runtime on Jackie's developer computer. |
| Default browser, reopen, repeated launch, Quit/restart | Accepted Windows W03/W04/W09 and Mac M03/M04/M09 in [platform records](app-package-testing.md). |
| Routine startup within 30 seconds | Met on Anna's and Jackie's recorded devices. First security-prompt launches are separate; no tutor-device result is claimed. |
| Paths with spaces, outside repository, offline prediction | Recorded in [Windows](evidence/app/windows/results.md) and [Mac](evidence/app/macos/results.md) device checks. |
| All modes/setups, validation, invalid rows, duplicates, recommendations, warning/export alignment and old-result clearance | Recorded B01–C08 and D01 in the [#116 summary](evidence/app/issue116/README.md); approved in PR #122. |
| Startup/lifecycle errors and diagnostic design | [Launcher checks](app-launcher-checks.md) and [build checks](app-package-build-checks.md), with their stated development-test limits. |
| First-opening security restrictions | SmartScreen and Gatekeeper recorded; unsigned-app restrictions remain a limitation. |
| Another-person download-to-use walkthrough | [#117 evidence](evidence/app/issue117/README.md), approved in PR #123. Windows downloading needed sign-in advice; the Mac tester was a teammate. |
| Public release downloads | [Publication record](evidence/app/issue118/published-release-assets.json): all 11 anonymous downloads matched hashes and sizes. Benjamin chose to reuse existing device results. |

## Startup timing method

Benjamin agreed the 30-second target before packaged-app measurements. It applies
to each recorded target computer, not every possible computer. Measure from the
double-click that launches SARAH until the dashboard's normal form controls are
visible and usable. Service readiness alone is not the endpoint.

Record the first downloaded launch separately, including any OS prompts and user
interaction. Do not count a blocked first launch as a successful startup. Exclude
network download and archive extraction from the startup timer and report them
separately if measured. Do not silently subtract security-prompt time.

For routine startup, record one first launch after a reboot and three subsequent
launches after fully quitting SARAH. Report each duration, OS/browser, package
version, and whether the browser was already running. The target is at most
30 seconds for each measured routine launch. A miss remains a miss; investigate,
fix and recheck or disclose it at the release decision. Prediction response-time
results from Sprint 6 are separate and keep their original tested commit.

## Issues and evidence

| Issue | Work | Depends on |
|---|---|---|
| [#112](https://github.com/Hakuverse/ICT304/issues/112) | Review this plan | Merged #111 |
| [#113](https://github.com/Hakuverse/ICT304/issues/113) | Shared launcher | #112 |
| [#114](https://github.com/Hakuverse/ICT304/issues/114) | Windows package | #113 |
| [#115](https://github.com/Hakuverse/ICT304/issues/115) | macOS package | #113 |
| [#116](https://github.com/Hakuverse/ICT304/issues/116) | Packaged workflow checks | Each platform build when ready |
| [#117](https://github.com/Hakuverse/ICT304/issues/117) | Another-person walkthrough | Applicable #116 checks pass |
| [#118](https://github.com/Hakuverse/ICT304/issues/118) | Release and documentation | #116 and #117 for every released platform |

Planned evidence locations are project/docs/evidence/app/windows/ and
project/docs/evidence/app/macos/, with results.md files identifying the actual
builds and outcomes. Keep fictional exports, focused screenshots and safe logs.
Record exact installed dependency versions and third-party licence notices with
each build. Generated executables belong in release assets, not source commits.

## Sprint 8 and release decision

Continue report and slide work alongside packaging. At the 3 November readiness
review, include only platforms with reviewed package evidence and clearly stated
restrictions. If a platform is not ready, disclose it and retain the documented
source setup. Use #97 for the final extracted-package check and #98 for readiness
and actual submission, with 4–7 November reserved for corrections/upload before
the confirmed LMS cutoff. A release is not proof of LMS submission.

Update deployment/user/maintenance instructions, README links, report and slides
when a release is accepted. Consider a short video startup update then; retain
historical evidence and version labels. Packaging does not retrain the models,
improve accuracy, remove the study-hours limitation or turn earlier unmet
usability targets into passes.

## Release and submission follow-ups

Platform checks (#114/#115), workflow checks (#116) and walkthroughs (#117) were
reviewed in merged PRs #121, #122 and #123. The accepted candidate is `ab4a604`.
Issue #118 publishes the same tested ZIPs with a direct app user guide; see
[release notes](app-release-notes.md) for publication status and checksums.

The tutor's device has not been tested simply because it matches Jackie's chip/OS.
The 3 November review and #97/#98 still cover final submission selection, exact
LMS cutoff, uploader and backup. The release is not proof of LMS submission.

## Launcher implementation

The [launcher checks](app-launcher-checks.md) record issue #113 development results.
The [developer build guide](../packaging/README.md) covers the shared launcher and
build recipe. Reviewed platform/user checks are linked from the release record.


## Platform testing allocation update

On 27 October Benjamin confirmed that Anna will test the Windows package and
Jackie will test the Mac package after implementation. Benjamin coordinates the
build preparation. The roles table above reflects this current allocation.
Use the [package testing guide](app-package-testing.md) and record actual results
under #114/#115. This allocation is not a claim that testing is finished.
