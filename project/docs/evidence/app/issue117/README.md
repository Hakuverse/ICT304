# Issue 117 evidence review

Both walkthroughs were performed on 30 October 2026. Records are ready for review, with follow-up details still outstanding. This is not an all-independent, all-unassisted acceptance claim.

| Area | Windows: Ka Jun | macOS: Jackie |
|---|---|---|
| Prior involvement | None; participant-approved alias | Experienced teammate |
| Download/extraction | Completed after Benjamin's GitHub sign-in advice; nested folders confusing | Completed as reported; exact route/sign-in not recorded |
| Opening | SmartScreen, then working dashboard | Gatekeeper exception, then working dashboard |
| Predictions | Expected results shown | Expected results shown |
| Mixed CSV | 2 valid / 2 skipped | 2 valid / 2 skipped |
| Export | Warning-demo CSV; documented variation | Mixed-roster CSV |
| Quit/reopen | Reported successful; quit screenshot | Quit and reopened screenshots |
| Feedback | Human review understood; warning overinterpreted | Feedback supplied despite stale pending heading |
| Routine startup timing | Not recorded | Not recorded |

- [Windows record and filename mapping](windows/results.md)
- [macOS record](macos/results.md)
- [Shared walkthrough](../../../app-walkthrough.md)
- [Evidence hashes](evidence-manifest.json)

## Evidence review

Both exported CSVs were compared with the current matching source workflow (`dashboard.process_upload` with recommendations): all columns, row order, labels, decimal probabilities, grade setups, warning text and recommendations match. Windows used `study_hours_warning_demo.csv`; macOS used `sample_roster.csv`. This comparison verifies export consistency and is not a new manual device test.

The repository contains 26 supplied screenshots and two exports. Original Windows filenames retain the old U01-U10 numbering; the record maps them to shared U01-U08. The Mac outer-package screenshot remains local because the Finder sidebar includes a personal account name. No image content was changed. Extra warnings and assistance are retained rather than removed from the results.

## Findings and follow-up before completion

1. **Download barrier:** Ka Jun saw a GitHub 404 until given sign-in advice. Instructions now explicitly describe this. Actions artifacts expire; #118 must provide and check the final intended distribution route. This run does not prove an anonymous public release download.
2. **Extraction:** nested ZIPs/folders confused the Windows participant, although he completed extraction independently. The package guide now names the two extraction stages and the files to keep together.
3. **Study warning:** Ka Jun said the model becomes inaccurate above 12. Preserve this answer. Clarify that it may be unreliable outside converted training values, not that all such results are wrong; at/below 12 is not guaranteed reliable either. Record his follow-up understanding before claiming the clarification worked.
4. **Quit/reopen:** Ka Jun first used the window X, then tested Quit SARAH. The guide now explains the expected old-tab connection error and using the new dashboard after restart. No launcher defect is established by this observation.
5. **Timing:** Windows first launch was reported as 23 seconds; Mac security approval to browser opening as 4.25 seconds. Neither is a recorded subsequent double-click-to-usable-Attendance measurement. Add actual routine timings or a reviewed limitation; do not substitute #114/#115 timings as new #117 evidence.
6. **Environment and provenance:** confirm the Mac environment/package/download/help details marked provisional in the source document. Confirm whether the Windows run needed any Python/source/virtual-environment setup. Current ZIP checksum verification was not recorded; do not claim it was performed.

The documentation clarifications are new changes following the walkthrough, not instructions already shown to both testers. Recheck the affected instructions and record the outcome, or retain the limitation for team review. There is no observed need to rebuild the application for these documentation changes.

PR #123 should stay open while the follow-ups are resolved. Issue #117 remains open until the team reviews the results and remaining distribution limitations. Sprint 6 and #116 historical evidence remains separate.
