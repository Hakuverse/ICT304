# ICT304

Repository for ICT304 (AI System Design) at Murdoch University — covering both weekly workshop tutorials and the group Assignment/Project: **Project SARAH** (Student Academic Risk Assistance Hub).

## Team

|Name | GitHub Handle |
|---|---|
| Benjamin | [@Hakuverse] |
| Anna | [@lee-shi-min] |
| Jackie | [@s123-bit]) |


## What is Project SARAH?

Project SARAH (Student Academic Risk Assistance Hub) is a prototype for estimating academic risk. Early-Warning Mode uses an attendance estimate, estimated study hours and past failures without assessment grades. Confirmatory Mode requires G1 and can also use G2, with separate models for G1 alone and the G1/G2 average. Neither mode uses demographic or family-background inputs. The current dataset lets us compare predictions against final outcomes, but does not establish day-one or week-specific accuracy.

The code can process a class list, skip invalid students with an explanation and send valid students to the matching model. A tutor-facing dashboard and intervention recommendations are planned work. See [Using the two modes](assignment/docs/mode-guide.md) for examples and dataset limitations.

## Repository structure

```
ICT304/
├── ai-prompt-log/         # Running log of AI-tool prompts, snapshotted into each report's appendix
│   └── log.md
├── assignment/            # Current work: design report + AI prototype, due 3 October
│   ├── report/
│   ├── code/
│   ├── data/
│   └── docs/              # EDA findings, figures, feature selection and sprint tasks
├── project/               # Next stage: continue here after assignment submission
│   ├── README.md
│   ├── report/
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
- **AI prompt log:** keep using the shared `ai-prompt-log/log.md`. Each submission has its own prompt appendix in its `report/` folder.

When starting the project stage, leave out virtual environments, caches and temporary files. Check the copied scripts and instructions before continuing. Work in one assessment folder at a time.


## Tools in use

| Purpose | Tool |
|---|---|
| Project Management | GitHub Issues + Milestones + [Project board link] |
| Version Control | GitHub |
| Collaboration (code) | GitHub (branches + Pull Requests) |
| Communication | Microsoft Teams, WhatsApp (quick/informal) |

## Sprint tracking

- Milestones: see the [Milestones tab](../../milestones)
- Board: [SARAH Sprint Board](../../projects)
- [Sprint 1: Getting Started](assignment/docs/sprint1-planning.md)
- [Sprint 2: Requirements and Data Exploration](assignment/docs/sprint2-planning.md)
- [Sprint 3: System Design](assignment/docs/sprint3-planning.md)
- [Sprint 4: Prototype and Assignment Submission](assignment/docs/sprint4-planning.md)

## Setup / how to run

From the repository root, with Python installed:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r assignment/code/requirements.txt
.venv\Scripts\python.exe assignment/code/verify_dataset.py
.venv\Scripts\python.exe assignment/code/data_processing.py
.venv\Scripts\python.exe assignment/code/eda.py
```

On macOS/Linux, use `python3` to create the environment and `.venv/bin/python` in place of `.venv\Scripts\python.exe`.

The verification script should show 395 students: 130 High Risk and 265 Low Risk. EDA writes its findings and figures to `assignment/docs/`. These commands run data preparation and analysis.

To compare Logistic Regression and Decision Tree for Early-Warning, G1-only and G1+G2:

```powershell
.venv\Scripts\python.exe assignment/code/train_models.py
```

This prints development cross-validation results for each setup. It does not prove early-term performance or automatically select a final model.

To check both input modes:

```powershell
.venv\Scripts\python.exe -m unittest discover -s assignment/code -v
```

See [Using the two modes](assignment/docs/mode-guide.md) for examples. The testing plan
and assignment preparation checklist are in [the report draft](assignment/report/Document).


## Contribution workflow

1. Create a branch off `main`, named after the issue you're working on (e.g. `dataset-download-verify`)
2. Commit your changes with a short, clear message
3. Push the branch and open a Pull Request
4. **At least one other teammate must review and approve before merging** — direct pushes to `main` are blocked
5. Delete the branch once merged

## AI tool usage

All prompts used for this project are logged in `ai-prompt-log/log.md` as they're used, and summarised in each submission's report appendix, per the unit's generative-AI declaration requirement.

## References

- [Dataset citation]
- [NASA SE Handbook citation]
- [Any other sources — see individual report References sections for the full list]
