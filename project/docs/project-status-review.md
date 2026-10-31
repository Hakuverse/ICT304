# Project consistency review — 31 October 2026

The project folders were checked against GitHub's merged PRs, open issues,
release and milestone states. The audit covered 518 tracked files, including
62 Markdown documents; AI disclosure content was excluded from editing.
Merged PRs are treated as completed team review. Historical test dates, results,
assistance and limitations are retained rather than rewritten as fresh passes.

## Folder roles and current status

| Location | Purpose and checked status |
|---|---|
| project/code | Implemented prediction, recommendations, dashboard, training and tests. 110 tests passed during this check. |
| project/data | Dataset and fictional input fixtures; referenced files exist. No new dataset or fixture changes. |
| project/models | The three saved models and their supporting records. The published app uses the previously tested model files. |
| project/packaging | Launcher/build scripts and developer guidance. 18 packaging tests passed; no rebuild performed. |
| project/docs | User/deployment/maintenance guides, sprint records, figures, model results and test evidence. Local Markdown link targets checked; stale review statuses updated. |
| project/demo | The video itself remains in the team's private workspace, as recorded in demo-video-notes.md; no missing public video file is inferred. |
| project/report | Progress notes aligned with the reviewed work and published app. Benjamin is preparing the separate final report; Anna and Jackie will review it. |

## Review and release status

- Sprint 6: #65–#70 closed; #70 reviewed in PR #103. Milestone 6 closed on 23 October.
- Sprint 7: #77–#82 closed; Anna approved handover PR #111 on 27 October. Milestone 7 closed on 30 October.
- App platform evidence: Anna approved PR #121 on 29 October; merged.
- Packaged workflow evidence: Anna approved PR #122 on 30 October; merged.
- App walkthrough evidence: Anna approved PR #123 on 30 October; merged.
- Release preparation: PR #124 merged. The unsigned v0.1.0-preview app was published on 31 October with the unchanged ab4a604 ZIPs.
- Public download verification: all 11 assets matched their hashes and sizes without GitHub authentication. Existing device results are reused by Benjamin's decision; no post-publication device run is claimed.
- Publication/status cleanup was reviewed and merged in PR #125 as `72ea244`.
  Publication is complete; #118 retains the outstanding final-submission handover.

Use the [app user guide](user-guide.md) directly for download and use, and the
[release record](app-release-notes.md) for provenance and limitations.

## Information still unavailable

These are genuine outstanding decisions or limits, not instructions left for
someone to edit a completed evidence file.

| Item | What is known / what remains |
|---|---|
| Final report, slides and declaration | Benjamin leads the report; Anna leads slides; each is reviewed by the other two. Final reviewed versions and completed declarations remain outstanding. |
| Editing sessions, speaking roles and rehearsal | Separate document leads are agreed. Speaking parts, session dates and actual rehearsal results are not recorded. |
| Final submission package | Published app ZIPs are identified. Benjamin leads final checking; source archive/commit selection and clean-extraction results remain outstanding under #97. |
| Submission arrangements | Benjamin is the uploader. Exact LMS cutoff time, required upload arrangement and backup still need a team record. |
| App-startup video addition | The existing reviewed video is retained. Live startup versus a short extra clip has not been decided. |
| Historical assignment upload | Prepared assignment ZIP a97a9b0 is recorded; this does not establish which exact file was uploaded to LMS. No receipt is inferred. |
| Historical test metadata | Some older runs did not record browser/version, viewport/zoom, exact meeting commit, observer or precise timing boundaries. These remain labelled in their original records. They are not guessed from current settings. |
| Tutor-device test / recovery drill | Neither is established by the existing evidence. Matching the tutor's chip/OS or having a written recovery plan is not proof of a performed check. |

No new information is needed to correct merged-PR review status. Report/slides
work is active; the other final checks are outstanding. Missing historical metadata is optional
to supplement only if an actual contemporaneous record exists; no repeat device
test is requested by this documentation review.

## Verification performed

On 31 October, 110 project tests and 18 packaging tests passed using local Python
3.12.10. These are development checks, not new Windows/macOS user runs. The first
restricted attempts encountered temporary-folder restrictions/stalling; the
normal-permission runs completed successfully. Local Markdown link targets and
git diff --check passed. Application code, datasets and saved models were not
changed by the documentation cleanup.
