# SARAH application deployment plan

Issue: [#112](https://github.com/Hakuverse/ICT304/issues/112).
Decisions confirmed by Benjamin on 27 October 2026; plan prepared for peer review.
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
| Benjamin's Windows computer | Windows 11 Home 25H2 reported by Benjamin; local system check confirms x64, 25H2, build 26200.9711 | Initial Windows x64 target; package testing still required |
| Jackie's Mac | Apple M3, macOS Tahoe 26.6.2 reported by Benjamin | Initial Apple Silicon target; Jackie must record the exact OS version/build from About This Mac when building/testing |
| Tutor's Mac | Apple M3, macOS Tahoe 26.6.2; Benjamin confirmed it matches Jackie's Mac on 27 October | Same initial Apple Silicon target; actual package launch on the tutor's computer remains to be checked |
| Intel Mac / Windows ARM / other OS versions | No agreed test device | Outside the initial verified support claim |

The agreed preference is an application: SARAH.exe on Windows and SARAH.app on
macOS, not a terminal script. This does not require a single standalone Windows
executable or a traditional installer. If the build needs supporting files, ship
the complete application folder and tell users to keep it together. A ZIP or disk
image may be used as the download container; choose and test that container in
#114/#115. Packaging format must preserve the double-click experience.

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
| Benjamin | Windows build/checks and Windows evidence |
| Jackie | Mac build/checks and macOS evidence |
| Anna | Launcher wording, installation instructions and behaviour review |
| All three | Scope decisions, report discussion and release review |

Work may be shared. Record the person who actually performed each check and have
someone other than the builder review it. This does not assign exclusive ownership
of the existing report, slides and closeout issues.

## Acceptance checklist

These are requirements to verify under #113–#117, not completed results.

- [ ] A downloaded package opens by double-click without a developer environment.
- [ ] The default browser opens only after the local service is ready.
- [ ] Startup reaches a usable dashboard within 30 seconds on each declared test device.
- [ ] Open dashboard, Quit, restart and repeated launch work predictably.
- [ ] Paths with spaces and a launch outside the source repository work.
- [ ] Core prediction works offline after extraction/installation.
- [ ] Both modes and all three grade setups match the source version's outputs.
- [ ] Invalid rows are skipped; valid rows, duplicate IDs and downloaded results stay aligned.
- [ ] High-Risk targeted support and Low-Risk routine guidance remain unchanged.
- [ ] Study hours remain 0–40, with the existing warning above 12 and rejection above 40.
- [ ] Form input/mode changes clear old results; missing/invalid inputs show clear errors.
- [ ] CSV screen markers and full downloaded input_warning text match the right students.
- [ ] Startup failures are understandable; diagnostic logs do not contain student records.
- [ ] Actual first-launch security restrictions are recorded on each platform.
- [ ] A person other than the builder tries download, opening, prediction, CSV, export and quit.

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

## Outstanding before release

- Peer review of this plan and its proposed measurement procedure.
- Jackie verifies the reported macOS version/build and captures actual build details.
- Check the downloaded app on the tutor's computer before claiming that device passed; matching chip and OS do not establish its security settings or launch outcome.
- Choose and test the distribution container, downloaded first-launch behaviour
  and final artifact on each platform under #114–#117.
- Complete #97/#98 submission decisions, including exact cutoff, uploader and backup.

These are tracked follow-ups; they do not prevent starting launcher development
once this planning PR is accepted.
