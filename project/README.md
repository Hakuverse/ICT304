# SARAH final project

Continue development here for the final project due on **7 November 2026**.
Keep `assignment/` as the assignment-stage record and keep tutorials separate.

## Starting version

This project copy starts from reviewed main commit
[`a97a9b0`](https://github.com/Hakuverse/ICT304/commit/a97a9b09463017d3b4e0a325cf2d310ec5390081)
(PR #64). This is also the version used to prepare `ICT304_Code_a97a9b0.zip`.
Issue #51 is closed and PR #71 is merged. This identifies the project code
baseline; the exact package uploaded to LMS is recorded separately. The
prepared package alone does not prove which files were submitted.

Code, required datasets, three saved models and selected model documents were
copied into this folder. The models were not retrained. The comparison script and
its tests now use `project/`. Environments, caches, private forms and old sprint
records were not copied. Earlier evidence remains in `assignment/docs/`.

## What works now

- Command-line predictions for Early-Warning, Confirmatory with G1, and
  Confirmatory with G1 and G2.
- CSV validation that skips invalid students and processes valid rows.
- Training, model comparison and the copied automated tests.
- Streamlit dashboard (#54, #55, PR #72): a one-student form and a class CSV
  upload with skipped-row reasons, totals and a results download.

The dashboard is already connected to the recommendation contract agreed in
#52: `recommend(student_fields, prediction)` returning a list of messages, called
for the form and for every valid CSV row. The recommendation function was
implemented in PR #74. High Risk students receive matching support suggestions
or general review guidance; Low Risk students receive routine check-in guidance.
See the [team-approved rules](docs/recommendation-rules.md). The copied evaluation results describe the assignment model
baseline, not new project or dashboard testing. `feature_stats.json` contains
statistics for the G1+G2 training setup only; do not use it for every
recommendation setup.

### Start the dashboard

From the repository root, after the setup below:

```powershell
.venv\Scripts\python.exe -m streamlit run project/code/dashboard.py
```

On macOS:

```bash
.venv/bin/python -m streamlit run project/code/dashboard.py
```

The dashboard opens in the browser at `http://localhost:8501`. Press `Ctrl + C`
in the terminal to stop it. Test files for messy or invalid uploads are in
`project/data/dashboard_checks/`; they use fictional student IDs.

## Set up from the repository root

Use Python 3.11 or newer. Download and extract the repository, or clone it.
The root folder contains `README.md`, `assignment/` and `project/`.
On macOS, open Terminal, type `cd `, drag this root folder from Finder into the
terminal and press Enter. These commands work in zsh or Bash.
On Windows, open PowerShell in the root folder. No activation is needed.

If `.venv` already works, skip the first command. It is a local environment,
not a folder to copy into GitHub or the submission ZIP.

Windows:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r project/code/requirements.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m unittest discover -s project/code -v
.venv\Scripts\python.exe project/code/verify_dataset.py
.venv\Scripts\python.exe project/code/predict.py --mode confirmatory --csv project/data/sample_roster.csv
```

macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r project/code/requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m unittest discover -s project/code -v
.venv/bin/python project/code/verify_dataset.py
.venv/bin/python project/code/predict.py --mode confirmatory --csv project/data/sample_roster.csv
```

Expect 89 tests ending in `OK` (41 copied from the assignment, 37 dashboard
tests from PR #72 and 11 recommendation tests from PR #74). Dataset verification shows 395 students, including
130 High Risk and 265 Low Risk. The sample CSV predicts for A and B and skips C
and D with reasons. See the [migration checks](docs/project-start-checks.md) for
the actual Windows results recorded when the project folder was created, when the
suite had 41 tests; a new macOS run is still pending.

## Working with the models

The saved models are ready to use; training is not needed for normal predictions.
See the [mode guide](docs/mode-guide.md) for all three examples and input rules.
Use scikit-learn 1.8.0, as pinned in the requirements, for these saved models.

To deliberately retrain from the repository root:

```powershell
.venv\Scripts\python.exe project/code/train_models.py
```

Training replaces the project models, evaluation report and confusion matrices.
Afterwards, refresh the comparison outputs if required:

```powershell
.venv\Scripts\python.exe project/code/issue33_comparison.py --overwrite
```

On macOS, replace `.venv\Scripts\python.exe` with `.venv/bin/python`.
All these outputs belong in `project/`; assignment files stay unchanged.
The comparison script retains checks for the original twelve-combination
experiment. Review those checks if the experiment changes; do not silently reuse
the original scores for a different experiment.

## Plans and references

- [Current implementation checks](docs/sprint5-implementation-checks.md)
- [Issue #56 test checklist](docs/prototype-test-checklist.md)
- [Issue #57 demo notes](docs/prototype-demo-notes.md)
- [Current project workflow](docs/system-workflow.md)

- [Sprint 5 plan](docs/sprint5-planning.md)
- [Sprint 6 plan](docs/sprint6-planning.md)
- [Baseline evaluation](docs/evaluation_report.md)
- [Baseline comparison and limitations](docs/issue33_report.md)
- [Assignment system design](../assignment/docs/SYSTEM_DESIGN.md) and
  [model test plan](../assignment/docs/model-test-plan.md), retained as background.
- [Project prompt appendix](report/appendix-ai-prompts.md) and
  [shared prompt log](../ai-prompt-log/log.md), unchanged.

New system results, feedback and project diagrams belong in `project/docs/`.
Keep personal identifiers and signed declarations out of the public repository.
