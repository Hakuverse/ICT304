# ICT304

Repository for ICT304 (AI System Design) at Murdoch University — covering both weekly workshop tutorials and the group Assignment/Project: **Project SARAH** (Student Academic Risk Assistance Hub).

## Team

|Name | GitHub Handle |
|---|---|
| Benjamin | [@Hakuverse](https://github.com/Hakuverse) |
| Anna | [@lee-shi-min](https://github.com/lee-shi-min) |
| Jackie | [@s123-bit](https://github.com/s123-bit) |


## What is Project SARAH?

Project SARAH (Student Academic Risk Assistance Hub) is a prototype for estimating academic risk. Early-Warning uses an attendance estimate, estimated study hours and past failures without assessment grades. Confirmatory requires G1 and accepts optional G2, with separate models for G1 alone and the G1/G2 average. Neither mode uses demographic or family-background inputs. The dataset does not establish day-one or week-specific accuracy.

The command-line prototype predicts for one student or a class CSV, skips invalid rows and reports why. The project stage now includes a Streamlit dashboard and High-Risk-only support recommendations, with routine guidance for Low Risk predictions.

**Current project work:** use [project/](project/README.md) for setup, tests and new features.
The assignment commands below remain for reproducing the earlier prototype.

## Repository structure

```
ICT304/
├── ai-prompt-log/         # Shared prompt-log file (currently blank)
│   └── log.md
├── assignment/            # Assignment-stage record; preserve after submission
│   ├── report/            # File guide and appendix; full report submitted separately
│   ├── code/
│   ├── data/
│   └── docs/              # EDA findings, figures, feature selection and sprint tasks
├── project/               # Current project development, due 7 November
│   ├── README.md
│   ├── report/            # Project report files and appendix placeholder
│   ├── code/
│   ├── data/
│   ├── docs/
│   └── demo/
├── tutorials/            # workshop exercises, not part of the assessed project
│   ├── week01/
│   └── ...
├── .gitignore
└── README.md
```

## Where to work

- **Before the assignment submission:** put SARAH code, data, report and supporting documents in `assignment/`.
- **After submitting the assignment on 3 October:** keep the submitted `assignment/` folder unchanged. Copy the code, required data and useful documents into `project/`, then continue development there for the final project due on 7 November.
- **Tutorials:** keep weekly exercises in `tutorials/`; they are separate from the assessed SARAH system.
- **Shared prompt log:** [ai-prompt-log/log.md](ai-prompt-log/log.md) is retained as a blank file for the team to maintain.
- **Submission records:** the report, signed declaration and actual prompt records are maintained for LMS submission. The repository appendix is a placeholder; it does not establish that those records are complete.

When starting the project stage, leave out virtual environments, caches and temporary files. Check the copied scripts and instructions before continuing. Work in one assessment folder at a time.


## Tools in use

| Purpose | Tool |
|---|---|
| Project Management | GitHub Issues + [Milestones](https://github.com/Hakuverse/ICT304/milestones) + [SARAH Sprint Board](https://github.com/Hakuverse/ICT304/projects) |
| Version Control | GitHub |
| Collaboration (code) | GitHub (branches + Pull Requests) |
| Communication | Microsoft Teams, WhatsApp (quick/informal) |

## Sprint tracking

- Milestones: see the [Milestones tab](https://github.com/Hakuverse/ICT304/milestones)
- Board: [SARAH Sprint Board](https://github.com/Hakuverse/ICT304/projects)
- [Sprint 1: Getting Started](assignment/docs/sprint1-planning.md)
- [Sprint 2: Requirements and Data Exploration](assignment/docs/sprint2-planning.md)
- [Sprint 3: System Design](assignment/docs/sprint3-planning.md)
- [Sprint 4: Prototype and Assignment Submission](assignment/docs/sprint4-planning.md)
- [Sprint 5: Recommendations and Dashboard Prototype](project/docs/sprint5-planning.md)
- [Sprint 6: Integration and User Testing](project/docs/sprint6-planning.md)

## Assignment prototype: setup and reproduction

Download and extract the submitted ZIP, or check out the agreed Git commit.
The repository root is the folder containing `README.md` and `assignment/`.
Use the submitted version for reproduction; a later download of `main` may differ.

On macOS, open Terminal, type `cd` followed by a space, drag that folder from
Finder into Terminal and press Enter. Run `pwd` and `ls` to check the location.
The commands work in both zsh and Bash; no shell switch is needed. On Windows,
open PowerShell in the same folder.

From the repository root, with Python 3.11 or newer installed:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r assignment/code/requirements.txt
.venv\Scripts\python.exe assignment/code/verify_dataset.py
.venv\Scripts\python.exe assignment/code/data_processing.py
.venv\Scripts\python.exe assignment/code/eda.py
```

On macOS/Linux, use `python3` to create the environment and `.venv/bin/python` in place of `.venv\Scripts\python.exe`.

For **macOS**, open Terminal in the repository folder and run
these commands with Python 3.11 or newer. 

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r assignment/code/requirements.txt
.venv/bin/python -m unittest discover -s assignment/code -v
.venv/bin/python assignment/code/predict.py --mode confirmatory --csv assignment/data/sample_roster.csv
```

No environment activation is needed. The test command should finish with `OK`
(currently 41 tests). The sample should predict A and B and skip C and D with reasons.
The team's report records Jackie's successful macOS run on 1 October at commit
`0fff0f8`. See the [verification summary](assignment/docs/submission-verification.md)
for the environment, results and evidence scope.

The verification script should show 395 students: 130 High Risk and 265 Low Risk. EDA writes its findings and figures to `assignment/docs/`. These commands run data preparation and analysis. Training and prediction are now available:

```powershell
.venv\Scripts\python.exe assignment/code/train_models.py
.venv\Scripts\python.exe assignment/code/predict.py --mode confirmatory --attendance 60 --study-hours 4 --failures 1 --g1 12
.venv\Scripts\python.exe assignment/code/predict.py --mode confirmatory --csv assignment/data/sample_roster.csv
```

Training rewrites the model files, evaluation report and confusion figures. The sample
roster is invented for checking the program; it is not evaluation data. G1/G2 use the
0-20 scale. See the mode guide below for G1+G2 examples and all input rules.

To check input preparation, model routing and CSV handling:

```powershell
.venv\Scripts\python.exe -m unittest discover -s assignment/code -v
```

See [Using the two modes](assignment/docs/mode-guide.md) for examples, the
[system checks](assignment/docs/submission-verification.md) for T1-T12, and the
[assignment file guide](assignment/report/Document.md) for the separately maintained report.

### Issue #33 comparison and figures

Read the [model comparison discussion](assignment/docs/issue33_report.md) for the
report sections on model choices, errors, feature importance and limitations.
The script checks the saved models against the recorded results; it does not retrain.

To refresh its generated report, CSV tables, run record and feature-importance chart:

```powershell
.venv\Scripts\python.exe assignment/code/issue33_comparison.py --overwrite
```

On macOS:

```bash
.venv/bin/python assignment/code/issue33_comparison.py --overwrite
```

The report and tables stay in `assignment/docs/`, and the feature-importance chart
stays in `assignment/docs/figures/`. The existing confusion matrices are reused.
`--overwrite` replaces only the script's generated outputs, so save any manual
report edits elsewhere first. Without this option, existing outputs are protected.
Use the versions in `assignment/code/requirements.txt` for the submission check.
See [the run evidence](assignment/docs/issue33-verification.md) for the version history
and the [later verification summary](assignment/docs/submission-verification.md).


## Assignment submission

The assignment is due on **3 October 2026**. The completed report and signed Group
Declaration are maintained separately for LMS submission. This public repository
contains the prototype and supporting documents; [Document.md](assignment/report/Document.md)
is a file guide, not the full report. It does not include the private report's
student identifiers or signatures.

The report records tests against commit `0fff0f8`. Record the exact packaged commit
if later changes are included; historical test records retain their original
versions. The [Sprint 4 plan](assignment/docs/sprint4-planning.md) remains a dated
development record. Submission completion is tracked in [issue #35](https://github.com/Hakuverse/ICT304/issues/35).

The project dashboard and recommendation function are implemented. Preserve the
submitted assignment snapshot and use the [project setup guide](project/README.md)
for current work and the 89-test project suite.

See the [five-part model test plan](assignment/docs/model-test-plan.md), [current workflow](assignment/docs/system-workflow.md) and [Pre-Phase A to F mapping](assignment/docs/NASA_SE_HANDBOOK_CH3_CH4.md).

## Contribution workflow

1. Create a branch off `main`, named after the issue you're working on (e.g. `dataset-download-verify`)
2. Commit your changes with a short, clear message
3. Push the branch and open a Pull Request
4. **At least one other teammate must review and approve before merging** — direct pushes to `main` are blocked
5. Delete the branch once merged

## AI tool usage

The assignment brief requires disclosure of actual AI-tool use and the prompts in
the submitted report. The [assignment appendix](assignment/report/appendix-ai-prompts.md)
is a placeholder and has not been completed by this documentation update. The
[shared prompt log](ai-prompt-log/log.md) is present and currently blank. The team
maintains the actual records for submission; the blank file is not a completed log.

## References

- [UCI Student Performance dataset](https://doi.org/10.24432/C5TG7T)
- [NASA Systems Engineering Handbook, 2016](https://www.nasa.gov/reference/systems-engineering-handbook/)
- See the report References section for the other sources used.
