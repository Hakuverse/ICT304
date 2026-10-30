# SARAH app release and handover

Published on **31 October 2026** for issue #118 as an unsigned university
prototype pre-release. Documentation preparation was reviewed in merged
[PR #124](https://github.com/Hakuverse/ICT304/pull/124). Benjamin authorised
publication on 31 October and chose to reuse the existing Windows/macOS tests
without another device run. This is not a claim of final LMS submission.

The original [draft asset record](evidence/app/issue118/draft-release-assets.json)
remains historical. Current public download checks and asset digests are in the
[publication record](evidence/app/issue118/published-release-assets.json).
The app ZIPs are unchanged; the separate user guides were updated for direct downloads.

## Version and downloads

Release version: **v0.1.0-preview**. The application identifies itself as
`0.1.0-preview`; it remains an unsigned university prototype.

- [Release page](https://github.com/Hakuverse/ICT304/releases/tag/v0.1.0-preview)
- [Windows x64 ZIP](https://github.com/Hakuverse/ICT304/releases/download/v0.1.0-preview/SARAH-0.1.0-preview-windows-x64-ab4a604.zip)
- [Apple Silicon Mac ZIP](https://github.com/Hakuverse/ICT304/releases/download/v0.1.0-preview/SARAH-0.1.0-preview-macos-arm64-ab4a604.zip)
- [App user guide](user-guide.md) — complete download-to-use instructions.

The public app ZIPs do not need a GitHub account. Each is the app package itself,
without the older Actions ZIP wrapper. The user guide links directly to both ZIPs
and contains all normal-use instructions. Users do not need the source-code archive.

## Exact tested files

Source: `ab4a604a71ecef9f0585a137a014e7dd6fb861e2`, the PR #121 test-merge commit.
Code head: `9cdda7abde222cd8e37743668626cea86db8576b`.
Both packages came from [build run 40556703379](https://github.com/Hakuverse/ICT304/actions/runs/40556703379)
on 27 October. Python 3.12.10 is bundled; the user's installed Python is not used.
The documentation baseline is main `33c1783` after merged PR #123. A source
comparison found no changes to application code, models or packaging Python
files between that main commit and the tested source; only packaging README
wording changed in that scope.

| ZIP | SHA-256 |
|---|---|
| SARAH-0.1.0-preview-windows-x64-ab4a604.zip | `8828121aa9b343c07138657f6d827df168d33211782204fd5b019bf2577f4bc2` |
| SARAH-0.1.0-preview-macos-arm64-ab4a604.zip | `0996cc189a435d1e1a4509a7fd754cdcf7366a36fed8a5cdb8c173fa4fedf875` |

Both archives were read and hashed again on 30 October: they match the recorded
tested packages. The release copies are not rebuilt, renamed as a new app version
or repacked. New guide files are separate release assets. `build-info.json` and
`START-HERE.txt` inside the ZIPs retain their original candidate/pending wording
from build time; the reviewed evidence below supplies the later acceptance record.
This preserves the original bytes and their link to testing.

Each package includes fictional CSV samples, the saved models, build information,
a dependency inventory and `third-party-notices`. The archive review found 328
Windows and 464 Mac entries under the notices folder, including dependency and
runtime material. Counts describe included files, not a legal certification.
Retain all notices when sharing the package; individual third-party licences apply.
No new licence for the team's source code is granted by these release notes.

## Platform checks and limits

| Platform | Recorded checks | Scope |
|---|---|---|
| Windows x64 | [Anna's package checks](evidence/app/windows/results.md), [workflow checks](evidence/app/issue116/windows/results.md), [Ka Jun's walkthrough](evidence/app/issue117/windows/results.md) | Windows 11 test devices. Ka Jun used only the packaged app; downloading initially needed sign-in advice. |
| Apple Silicon Mac | [Jackie's package checks](evidence/app/macos/results.md), [workflow checks](evidence/app/issue116/macos/results.md), [walkthrough](evidence/app/issue117/macos/results.md) | Apple M3, macOS Tahoe 26.6.2. Jackie is an experienced teammate, not an independent newcomer. |

These records were reviewed through merged PRs #121, #122 and #123. A historical
record saying approval was pending describes its preparation date; the merge
history records the later review. No new device test is claimed by this handover.

Routine startup met the 30-second target on the recorded devices: Windows
post-approval reboot 13.20 s and later 11.15/6.46/4.35 s; Mac post-reboot 6.72 s
and later 4.29/3.64/3.58 s. First security-prompt launches are separate; Windows'
initial 74.67 s is not hidden or relabelled as a routine pass. #117 later reported
approximately 3 s Windows / 2 s Mac; these estimates are not repeated stopwatch
benchmarks. The tutor's computer, Intel Macs, Windows ARM and other OS versions
have not been verified by these results.

## Known limitations

- Unsigned Windows app and no Apple notarization: first-opening security approval
  may be required; managed devices may block use. Do not disable protections.
- The launcher starts a local browser dashboard. It is not a hosted service, a
  native dashboard window, a production system or an automatic updater.
- Packaging does not improve prediction accuracy. The same saved models, input
  mappings and recommendation rules are used.
- Study hours remain 0–40; above 12 a warning indicates potential unreliability.
  Twelve is not a proven reliability boundary and lower values are not guaranteed
  accurate. Keep actual inputs and use human judgement.
- Recommendations are discussion prompts, not causal explanations or proven
  interventions. Low-Risk students receive routine guidance only.
- The dataset, reserved-test performance and small usability sample still limit
  generalisation. See [evaluation](evaluation_report.md) and
  [study-hours discussion](study-hours-limitation.md).

## Publication and remaining handover

- PR #124 is merged. Benjamin authorised publication on 31 October 2026.
- Version `v0.1.0-preview` uses the same tested Windows/macOS ZIPs and source.
- Public downloads are checked without GitHub authentication and their bytes
  compared with the recorded hashes; see the publication record for actual outcomes.
- Benjamin chose **not to repeat device testing**. Existing #114–#117 evidence is
  reused for unchanged packages. No launch from the published download is claimed.
- Report, declaration, presentation/rehearsal, final submission-package checking
  and closeout work are **paused at Benjamin's request on 31 October**. This release
  does not complete those tasks or establish a 3 November meeting decision.

| Paused work | Handover when resumed |
|---|---|
| #93 report | Link this version, user guide and #114–#117 evidence. Keep deployment improvements separate from accuracy and retain limitations. |
| #94 declaration | Confirm actual contributions and required disclosures. |
| #95 slides | Show the app opening route and tested platforms, alongside the existing model results. |
| #96 rehearsal/video | Retain Anna's original video and metadata. A live startup demonstration or separate short clip remains a team choice; no new recording is claimed. |
| #97 package | Use the exact app ZIPs/hashes alongside the selected source archive. Final source-package extraction/checking remains outstanding. |
| #98 closeout | Confirm final deliverables, exact LMS cutoff, uploader and backup; retain receipts privately after submission. |

Issue #118's publication work is complete once its documentation update is merged;
final submission handover remains paused. Keep that distinction in the issue status.
