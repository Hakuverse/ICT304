# S6-19 and S6-20 response-time measurements

Tester: Jackie  
Date: 20 October 2026  
Environment and tested commit: recorded in [results.md](results.md).

## Method

Times are manually recorded full-dashboard times, in seconds. The cold value is the first run after restarting the app and includes any model loading. Each scenario has five subsequent warm runs without restarting.

For S6-19, timing starts when **Predict** is clicked and stops when the label, probability and recommendations are visible. For S6-20, timing starts when file selection completes and stops when counts, valid results, any skipped reasons and the download control are available. Before each warm CSV run, the uploaded file was removed, the old results disappeared, and the same unchanged file was selected again.

Server startup, choosing the file, removing the previous upload, saving a download and taking screenshots are excluded. Screenshots show the resulting interface; they do not independently prove the recorded times.

Timing tool: Jackie used a standalone electronic stopwatch, not a phone or computer timer. The stopwatch was started and stopped manually at the full-dashboard boundaries described below; readings were recorded to two decimal places.

Cold-run restart: For each scenario, Jackie stopped the Streamlit process and restarted it using the dashboard launch command. The first form prediction or CSV upload after the dashboard was ready was recorded as the cold run. Refreshing the browser alone was not treated as an app restart. The five repeat runs used the same running Streamlit process.

## S6-19 — one student

| Scenario | Cold (s) | Warm runs 1–5 (s) | Warm median (s) | Warm maximum (s) |
|---|---:|---|---:|---:|
| Early-Warning | 1.17 | 0.33, 0.26, 0.29, 0.31, 0.35 | 0.31 | 0.35 |
| Confirmatory, G1 only (G2 blank) | 1.12 | 0.31, 0.33, 0.31, 0.33, 0.33 | 0.33 | 0.33 |
| Confirmatory, G1 + G2 (G2 = 0) | 1.53 | 0.39, 0.39, 0.28, 0.36, 0.33 | 0.36 | 0.39 |

Agreed target: cold ≤10 s and **each** warm run ≤3 s. All recorded runs met the target.

## S6-20 — class CSV

| Mode | Fixture | Cold (s) | Warm runs 1–5 (s) | Warm median (s) | Warm maximum (s) |
|---|---|---:|---|---:|---:|
| Early-Warning | `30-valid.csv` | 1.27 | 0.40, 0.32, 0.33, 0.41, 0.44 | 0.40 | 0.44 |
| Early-Warning | `30-mixed.csv` | 1.22 | 0.33, 0.36, 0.42, 0.35, 0.30 | 0.35 | 0.42 |
| Early-Warning | `395-valid.csv` | 2.81 | 1.95, 1.22, 1.24, 1.11, 1.37 | 1.24 | 1.95 |
| Early-Warning | `395-mixed.csv` | 2.53 | 1.17, 1.43, 1.26, 1.33, 1.17 | 1.26 | 1.43 |
| Confirmatory | `30-valid.csv` | 1.97 | 1.00, 0.97, 0.90, 0.56, 0.76 | 0.90 | 1.00 |
| Confirmatory | `30-mixed.csv` | 1.68 | 0.50, 0.58, 0.65, 0.58, 0.63 | 0.58 | 0.65 |
| Confirmatory | `395-valid.csv` | 2.46 | 1.46, 1.01, 1.29, 1.24, 1.10 | 1.24 | 1.46 |
| Confirmatory | `395-mixed.csv` | 2.53 | 1.14, 1.40, 1.19, 1.28, 1.30 | 1.28 | 1.40 |

| Fixture | Expected rows / predicted / skipped | Observed in each mode |
|---|---|---|
| `30-valid.csv` | 30 / 30 / 0 | 30 / 30 / 0 |
| `30-mixed.csv` | 30 / 28 / 2 | 30 / 28 / 2 |
| `395-valid.csv` | 395 / 395 / 0 | 395 / 395 / 0 |
| `395-mixed.csv` | 395 / 393 / 2 | 395 / 393 / 2 |

Agreed targets: for 30 rows, cold ≤10 s and **each** warm run ≤5 s; for 395 rows, cold ≤20 s and **each** warm run ≤10 s. All recorded runs met the applicable target. The retained fictional fixtures include blank and supplied G2 values for Confirmatory testing.
