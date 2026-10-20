# Issue #67 — macOS response-time results

Tester: Jackie  
Run date: 20 October 2026 (Singapore time)  
Tested commit: `6395d82b2e94f4da622e2bca83722d617162730c`  
Device and OS: MacBook Air, Apple M3, 24 GB RAM; macOS 26.6.2  
Browser and version: Google Chrome 152.0.7977.75 (arm64)  
Screen size and browser zoom: Not recorded during the timed run.  
Python and relevant package versions: Python 3.14.0; Streamlit 1.64.0; pandas 3.0.6; NumPy 2.5.3; scikit-learn 1.8.0; joblib 1.6.0. These versions were checked in the project `.venv` after the run; no version log was captured during timing.

[Full timing method and individual measurements](timings.md)

## Method and scope

For each scenario, the first measurement followed an app restart and included model loading. Five further measurements used the running app. Form timing started when **Predict** was clicked and stopped when the label, probability and recommendations were visible. CSV timing started when file selection was completed and stopped when row counts, valid results, skipped reasons where applicable, and the download control were available. Before each warm CSV run, the previous upload was cleared and the same unchanged file was selected again.

Choosing a file, saving a downloaded export and starting the server were excluded. These are manual, full-dashboard observations, not backend-only timings. Screenshots document representative outputs; the individual elapsed times are recorded in [timings.md](timings.md).

Agreed targets: form cold ≤10 s and every warm run ≤3 s; 30-row CSV cold ≤10 s and every warm run ≤5 s; 395-row CSV cold ≤20 s and every warm run ≤10 s.

## S6-19 — Form response time

| Scenario | Observed result | Cold / warm median / warm maximum | Timing target | Evidence |
|---|---|---|---|---|
| Early-Warning: attendance 40, study hours 4, failures 0 | High Risk, 85.9%; attendance-support recommendation visible | 1.17 / 0.31 / 0.35 s | Met | [Form](screenshots/S6-19/S6-19-early-warning-form.png), [result](screenshots/S6-19/S6-19-early-warning-result.png) |
| Confirmatory, G1 only: attendance 80, study hours 4, failures 0, G1 8, G2 blank | High Risk, 81.8%; G1-only setup and assessment-review recommendation visible | 1.12 / 0.33 / 0.33 s | Met | [Form](screenshots/S6-19/S6-19-g1-only-form.png), [result](screenshots/S6-19/S6-19-g1-only-result.png) |
| Confirmatory, G1 + G2: attendance 80, study hours 4, failures 0, G1 12, G2 0 | High Risk, 99.6%; G1+G2 setup and assessment-review recommendation visible | 1.53 / 0.36 / 0.39 s | Met | [Form](screenshots/S6-19/S6-19-g1-g2-form.png), [result](screenshots/S6-19/S6-19-g1-g2-result.png) |

All three form scenarios met the agreed cold target and every warm measurement met the agreed warm target. Individual measurements are in [timings.md](timings.md).

## S6-20 — Class CSV response time

Four fixed fictional fixtures were tested in both prediction modes. The Confirmatory fixtures include rows with blank G2 and rows with supplied G2. Counts below are in the order **rows in file / predicted / skipped**. Each observed count matched the expected count.

| Mode and fixture | Expected → observed counts | Cold / warm median / warm maximum | Timing target | Evidence |
|---|---|---|---|---|
| Early-Warning, [30 valid rows](fixtures/30-valid.csv) | 30/30/0 → 30/30/0 | 1.27 / 0.40 / 0.44 s | Met | [Upload](screenshots/S6-20/S6-20-ew-30-valid-upload.png), [results](screenshots/S6-20/S6-20-ew-30-valid-results.png), [download control](screenshots/S6-20/S6-20-ew-30-valid-download.png), [export](exports/S6-20-ew-30-valid-export.csv) |
| Early-Warning, [30 mixed rows](fixtures/30-mixed.csv) | 30/28/2 → 30/28/2 | 1.22 / 0.35 / 0.42 s | Met | [Upload](screenshots/S6-20/S6-20-ew-30-mixed-upload.png), [results](screenshots/S6-20/S6-20-ew-30-mixed-results.png), [skipped reasons](screenshots/S6-20/S6-20-ew-30-mixed-skipped.png), [export](exports/S6-20-ew-30-mixed-export.csv) |
| Early-Warning, [395 valid rows](fixtures/395-valid.csv) | 395/395/0 → 395/395/0 | 2.81 / 1.24 / 1.95 s | Met | [Upload](screenshots/S6-20/S6-20-ew-395-valid-upload.png), [results and download control](screenshots/S6-20/S6-20-ew-395-valid-results.png), [export](exports/S6-20-ew-395-valid-export.csv) |
| Early-Warning, [395 mixed rows](fixtures/395-mixed.csv) | 395/393/2 → 395/393/2 | 2.53 / 1.26 / 1.43 s | Met | [Upload](screenshots/S6-20/S6-20-ew-395-mixed-upload.png), [results](screenshots/S6-20/S6-20-ew-395-mixed-results.png), [skipped reasons](screenshots/S6-20/S6-20-ew-395-mixed-skipped.png), [export](exports/S6-20-ew-395-mixed-export.csv) |
| Confirmatory, [30 valid rows](fixtures/30-valid.csv) | 30/30/0 → 30/30/0 | 1.97 / 0.90 / 1.00 s | Met | [Upload](screenshots/S6-20/S6-20-confirm-30-valid-upload.png), [results](screenshots/S6-20/S6-20-confirm-30-valid-results.png), [download control](screenshots/S6-20/S6-20-confirm-30-valid-download.png), [export](exports/S6-20-confirm-30-valid-export.csv) |
| Confirmatory, [30 mixed rows](fixtures/30-mixed.csv) | 30/28/2 → 30/28/2 | 1.68 / 0.58 / 0.65 s | Met | [Upload](screenshots/S6-20/S6-20-confirm-30-mixed-upload.png), [results](screenshots/S6-20/S6-20-confirm-30-mixed-results.png), [skipped reasons](screenshots/S6-20/S6-20-confirm-30-mixed-skipped.png), [export](exports/S6-20-confirm-30-mixed-export.csv) |
| Confirmatory, [395 valid rows](fixtures/395-valid.csv) | 395/395/0 → 395/395/0 | 2.46 / 1.24 / 1.46 s | Met | [Upload](screenshots/S6-20/S6-20-confirm-395-valid-upload.png), [results and download control](screenshots/S6-20/S6-20-confirm-395-valid-results.png), [export](exports/S6-20-confirm-395-valid-export.csv) |
| Confirmatory, [395 mixed rows](fixtures/395-mixed.csv) | 395/393/2 → 395/393/2 | 2.53 / 1.28 / 1.40 s | Met | [Upload](screenshots/S6-20/S6-20-confirm-395-mixed-upload.png), [results](screenshots/S6-20/S6-20-confirm-395-mixed-results.png), [skipped reasons](screenshots/S6-20/S6-20-confirm-395-mixed-skipped.png), [export](exports/S6-20-confirm-395-mixed-export.csv) |

For each mixed fixture, the two skipped rows received no prediction. In the 30-row fixture, S01 has an out-of-range `attendance_pct` and S02 has out-of-range `study_hours`. In the 395-row fixture, the corresponding IDs are S001 and S002. The dashboard displayed the respective reasons: `attendance_pct must be 0 to 100` and `study_hours must be 0 to 40`.

All eight CSV scenarios met the agreed cold target and every warm measurement met the applicable 30-row or 395-row target. Individual measurements are in [timings.md](timings.md). The retained exports show that the download control was available; saving each export was outside the timed interval.

## Conclusion

The reported full-dashboard timings met the agreed targets for S6-19 and S6-20. CSV row counts and skipped-row reasons matched the fixed fixtures in both modes.
