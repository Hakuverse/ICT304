# Issue #66 — macOS functional test evidence

Tester/coordinator: Jackie  
Test date: 19 October 2026  
Tested commit: `9dc7132dc0a1a735b508447b99f49b70afb84f6d`  
Covered cases: S6-01 to S6-18 in the [system test plan](../../../system-test-plan.md)

## Where to start

Open the [19 October macOS run results](2026-10-19-9dc7132/results.md). This file records each case’s inputs, actual outcome, status, and supporting evidence links.

## Evidence directory

| Location | What to find there |
|---|---|
| [results.md](2026-10-19-9dc7132/results.md) | Case-by-case results, boundary subcases, test commands, and limitations |
| [screenshots/](2026-10-19-9dc7132/screenshots/) | Dashboard inputs, results, validation messages, and test-output screenshots |
| [fixtures/](2026-10-19-9dc7132/fixtures/) | Fictional CSV files used as test inputs |
| [exports/](2026-10-19-9dc7132/exports/) | CSV result files downloaded from the dashboard |
| [logs/](2026-10-19-9dc7132/logs/) | Full unit-test output and recommendation boundary-check output |
| [environment-verified.md](2026-10-19-9dc7132/environment-verified.md) | Supplementary environment details collected during evidence review |
| [evidence-inventory.md](2026-10-19-9dc7132/evidence-inventory.md) | Retained artifact inventory, original filenames, and SHA-256 hashes |

The filenames and case-specific links are listed in `results.md`; use its results table to locate evidence for a particular S6 case. Repository test fixtures that were not copied into this run are identified there as well.

## Scope and limitations

This folder documents the macOS functional checks for Issue #66 only. S6-19 and S6-20 response-time checks belong to Issue #67 and are not claimed here. Windows evidence is stored separately. The evidence-submission branch is not the tested commit, and the saved models at the tested commit were used without retraining.

The checks were performed manually by Jackie with step-by-step guidance. Where a screenshot does not show a complete operation, `results.md` distinguishes tester confirmation from what the retained image independently shows. Browser, viewport, and zoom details were not recorded, so this run does not claim a readability or usability pass.
