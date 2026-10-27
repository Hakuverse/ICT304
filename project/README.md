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

### Review on 13 October 2026

The tutor found the modes, displayed results and skipped-row messages clear and
suggested proceeding to the next steps. See the [meeting record](docs/prototype-demo-notes.md)
for the feedback and decisions confirmed on 19 October. The team proposed clearer
wording, larger text areas and wrapping long messages for Sprint 6 review; these
were team proposals, not tutor requests. Reviewed wording and readability changes
subsequently merged in PRs #86, #87, #92 and #100. See the system test plan for recorded
usability results and remaining follow-up; merged changes do not establish that
all usability targets have been met.
Windows checks are recorded in [issue #56](docs/prototype-test-checklist.md).
The [Sprint 6 review](docs/sprint6-review.md) now brings together Windows/macOS
functional checks, reference-device timing and usability retests. S6-21 remains
not met and S6-22 partly met, with guide follow-up under #79/#80.

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
in the terminal to stop it.
For step-by-step instructions on using the dashboard, see the
[user guide](docs/user-guide.md). Test files for messy or invalid uploads are in
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

Expect 110 tests ending in `OK`: the previous 106 plus three study-hours warning
tests added after the #80 walkthrough and one test for showing that warning once in the
CSV view. Dataset verification shows 395 students, including
130 High Risk and 265 Low Risk. The sample CSV predicts for A and B and skips C
and D with reasons. See the [migration checks](docs/project-start-checks.md) for
the actual Windows results recorded when the project folder was created, when the
suite had 41 tests. Later [Windows and macOS functional evidence](docs/sprint6-review.md)
records 99 tests at `9dc7132`; Anna's 20 October retest records 106 at `e246495`.

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

- [Sprint 6 evidence and handover](docs/sprint6-review.md)
- [Sprint 6 system test plan](docs/system-test-plan.md) (team-reviewed; targets agreed 19 October 2026)

- [Current implementation checks](docs/sprint5-implementation-checks.md)
- [Issue #56 test checklist](docs/prototype-test-checklist.md)
- [Issue #57 meeting record](docs/prototype-demo-notes.md)
- [Project progress notes](report/project-progress-notes.md)
- [Current project workflow](docs/system-workflow.md)

- [Sprint 5 plan](docs/sprint5-planning.md)
- [Sprint 6 plan](docs/sprint6-planning.md)
- [Sprint 7 plan](docs/sprint7-planning.md) - Phase E, 20-27 October
- [Sprint 7 review and handover](docs/sprint7-review.md) (#82; pending peer review)
- [Guide walkthrough](docs/guide-walkthrough.md) (#80)
- [Demonstration video record](docs/demo-video-notes.md) (#81; video file held in the team workspace)
- [Local deployment and handover guide](docs/deployment-guide.md) (#77)
- [Maintenance and recovery plan](docs/maintenance-plan.md) (#78)
- [Sprint 8 plan](docs/sprint8-planning.md) - Phase F, 27 October-3 November; final submission by 7 November
- [Baseline evaluation](docs/evaluation_report.md)
- [Baseline comparison and limitations](docs/issue33_report.md)
- [Assignment system design](../assignment/docs/SYSTEM_DESIGN.md) and
  [model test plan](../assignment/docs/model-test-plan.md), retained as background.
- [Project prompt appendix](report/appendix-ai-prompts.md) and
  [shared prompt log](../ai-prompt-log/log.md), unchanged.

New system results, feedback and project diagrams belong in `project/docs/`.
Keep personal identifiers and signed declarations out of the public repository.

### Windows Python launcher fallback

If `python --version` opens the Microsoft Store message, try `py --version`.
If several versions are installed, choose Python 3.12 explicitly:

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.venv\Scripts\python.exe --version
```

Then continue with the package-installation commands using `.venv\Scripts\python.exe`.
`py --version` can show a different default version; the explicit `-3.12` chooses
3.12. If that version is not installed, install it before running these commands.
Do not copy another checkout's virtual environment. Benjamin used this route
successfully on 23 October; see the [walkthrough](docs/guide-walkthrough.md).

## Walkthrough and input limitation

See the [23 October walkthrough](docs/guide-walkthrough.md) and
[study-hours finding and warning](docs/study-hours-limitation.md).

## Planned double-click applications

The [application deployment plan](docs/app-deployment-plan.md) records the Windows
and Apple Silicon Mac targets, unsigned prototype decision and 30-second startup
target. Work is tracked in #112–#118 alongside Sprint 8. Packages are not yet
released or verified; use the existing setup instructions above for now.
