# ICT304

Repository for ICT304 (AI System Design) at Murdoch University — covering both weekly workshop tutorials and the group Assignment/Project: **Project SARAH** (Student Academic Risk Assistance Hub).

## Team

|Name | GitHub Handle |
|---|---|
| Benjamin | [@Hakuverse] |
| Anna | [@lee-shi-min] |
| Jackie | [@s123-bit]) |


## What is Project SARAH?

Project SARAH (Student Academic Risk Assistance Hub) is an early-intervention system that identifies students at risk of falling behind before their grades reflect it. Rather than reacting after a poor result or a failed unit, SARAH uses signals available from day one — attendance, study habits, and demographic/behavioural factors — to classify each student as Low or High Risk, then recommends a specific intervention tied to that student's single weakest contributing factor, rather than issuing a generic warning. It supports both a single-student lookup and a whole-class batch upload, so a teacher or academic advisor can screen an entire roster at once rather than entering students one at a time.

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
- Sprint 3 tasks: [assignment/docs/sprint3-planning.md](assignment/docs/sprint3-planning.md)

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

The verification script should show 395 students: 130 High Risk and 265 Low Risk. EDA writes its findings and figures to `assignment/docs/`. These commands run the current data preparation and analysis; model training is still a separate sprint task.


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
