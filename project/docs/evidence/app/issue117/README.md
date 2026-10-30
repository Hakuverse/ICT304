# Issue 117 evidence review

Both walkthroughs were performed on 30 October 2026. Follow-up confirmations were supplied by Benjamin on 30 October. Anna approved PR #123 on 30 October; it is merged and #117 is closed, with limitations retained. This is not an all-independent, all-unassisted acceptance claim.

| Area | Windows: Ka Jun | macOS: Jackie |
|---|---|---|
| Prior involvement | None; participant-approved alias | Experienced teammate |
| Download/extraction | Completed after Benjamin's GitHub sign-in advice; nested folders confusing | GitHub Actions route confirmed; no help needed |
| Opening | SmartScreen, then working dashboard | Gatekeeper exception, then working dashboard |
| Predictions | Expected results shown | Expected results shown |
| Mixed CSV | 2 valid / 2 skipped | 2 valid / 2 skipped |
| Export | Warning-demo CSV; documented variation | Mixed-roster CSV |
| Quit/reopen | Reported successful; quit screenshot | Quit and reopened screenshots |
| Feedback | Initial warning overinterpretation retained; clarification confirmed | Feedback supplied despite stale pending heading |
| Routine startup timing | Approximately 3 s, reported | Approximately 2 s, reported |

- [Windows record and filename mapping](windows/results.md)
- [macOS record](macos/results.md)
- [Shared walkthrough](../../../app-walkthrough.md)
- [Evidence hashes](evidence-manifest.json)

## Evidence review

Both exported CSVs were compared with the current matching source workflow (`dashboard.process_upload` with recommendations): all columns, row order, labels, decimal probabilities, grade setups, warning text and recommendations match. Windows used `study_hours_warning_demo.csv`; macOS used `sample_roster.csv`. This comparison verifies export consistency and is not a new manual device test.

The repository contains 26 supplied screenshots and two exports. Original Windows filenames retain the old U01-U10 numbering; the record maps them to shared U01-U08. The Mac outer-package screenshot remains local because the Finder sidebar includes a personal account name. No image content was changed. Extra warnings and assistance are retained rather than removed from the results.

## Findings and confirmed follow-up

1. **Download barrier:** Ka Jun saw a GitHub 404 until given sign-in advice. Instructions now explicitly describe this. Actions artifacts expire; #118 must provide and check the final intended distribution route. This run does not prove an anonymous public release download.
2. **Extraction:** nested ZIPs/folders confused the Windows participant, although he completed extraction independently. The package guide now names the two extraction stages and the files to keep together.
3. **Study warning:** Ka Jun said the model becomes inaccurate above 12. The original answer is preserved. Benjamin confirmed that this was clarified: results may be unreliable, not necessarily wrong, and at/below 12 is not guaranteed reliable. He reported that the participant revised his wording to unreliable and requiring human intervention/judgement. This was a clarification, not a repeat unassisted usability test.
4. **Quit/reopen:** Ka Jun first used the window X, then tested Quit SARAH. The guide now explains the expected old-tab connection error and using the new dashboard after restart. No launcher defect is established by this observation.
5. **Timing:** Windows first launch was reported as 23 seconds; Mac security approval to browser opening as 4.25 seconds. These remain separate from the subsequent double-click-to-usable-Attendance times supplied in follow-up: approximately 3 seconds on Windows and 2 seconds on macOS. Both reported estimates are below 30 seconds; no stopwatch logs or repeated-run series were supplied. These are not reused #114/#115 timings.
6. **Environment and provenance:** Benjamin confirmed Jackie used ab4a604 on M3/Tahoe 26.6.2 with Chrome 152.0.7977.75, downloaded through GitHub Actions without help. Ka Jun used only the packaged executable, without installing Python, setting up SARAH source or using a project virtual environment. Current ZIP checksum verification was not recorded; do not claim it was performed.

The documentation clarifications are new changes following the walkthrough, not instructions already shown to both testers. No complete re-run of the revised written instructions is claimed; this limitation remains for team review. The warning clarification follow-up is recorded separately. There is no observed need to rebuild the application for these documentation changes.

The requested factual follow-ups are resolved. PR #123 was reviewed and merged with the stated limitations; issue #117 is closed. Public distribution is recorded separately under #118. Sprint 6 and #116 historical evidence remains separate.
