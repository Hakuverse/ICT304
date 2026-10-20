# Local deployment and handover guide

## Scope and version

This guide helps another person start and stop the SARAH prototype on their own Windows or macOS computer. The current deployment is **local Streamlit use only**. Public hosting has not been agreed or tested and is future work.

Handover commit: `fe9685a729864d1caaa68f00daf92a83b3099412` (`main`, merge of PR #103).

Use the complete repository at this commit. The [project README](../README.md) is the canonical reference for setup commands; if those commands change, update this guide to match it.

## What is needed

- Python 3.11 or newer.
- The complete repository, including `project/code/`, `project/data/` and `project/models/`.
- Packages listed in [`project/code/requirements.txt`](../code/requirements.txt). In particular, the saved models require the pinned `scikit-learn==1.8.0`.
- The three committed model files:
  - `project/models/early_warning_model.joblib`
  - `project/models/confirmatory_g1_model.joblib`
  - `project/models/confirmatory_g1_g2_model.joblib`

The saved models are ready to use. **Do not retrain them for a normal installation**: training replaces model and evaluation files. Keep the repository structure intact rather than copying only `dashboard.py`.

## Get the handover version

Either download the repository ZIP from the [handover commit page](https://github.com/Hakuverse/ICT304/commit/fe9685a729864d1caaa68f00daf92a83b3099412) using **Browse files → Code → Download ZIP**, then extract it; or clone the repository and check out the recorded commit:

```text
git clone https://github.com/Hakuverse/ICT304.git
cd ICT304
git checkout fe9685a729864d1caaa68f00daf92a83b3099412
```

The Git commands require Git to be installed. Downloading the ZIP does not. After either method, work from the **repository root**—the folder containing `README.md`, `assignment/` and `project/`. Checking out a commit may show a “detached HEAD” message; that is normal when running a fixed version without editing it.

## Windows PowerShell

Open PowerShell in the repository root. Run these commands in order:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r project/code/requirements.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m unittest discover -s project/code -v
.venv\Scripts\python.exe project/code/verify_dataset.py
.venv\Scripts\python.exe project/code/predict.py --mode confirmatory --csv project/data/sample_roster.csv
```

The package check should report no broken requirements, and the test run should end in `OK`. Record the actual test count and any failures rather than assuming an earlier count still applies. The dataset check and fictional sample CSV provide further installation checks.

Start the dashboard:

```powershell
.venv\Scripts\python.exe -m streamlit run project/code/dashboard.py
```

Open the local URL shown in PowerShell, normally `http://localhost:8501`. To stop the dashboard, return to the PowerShell window and press **Ctrl+C**.

## macOS Terminal

Open Terminal in the repository root. One way to reach it is to type `cd ` (with a space), drag the extracted or cloned root folder from Finder into Terminal, and press Return. Then run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r project/code/requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m unittest discover -s project/code -v
.venv/bin/python project/code/verify_dataset.py
.venv/bin/python project/code/predict.py --mode confirmatory --csv project/data/sample_roster.csv
```

The package check should report no broken requirements, and the test run should end in `OK`. Record the actual test count and any failures.

Start the dashboard:

```bash
.venv/bin/python -m streamlit run project/code/dashboard.py
```

Open the local URL shown in Terminal, normally `http://localhost:8501`. To stop the dashboard, return to Terminal and press **Control+C**.

The commands use the Python executable inside `.venv`; activating the environment separately is not required.

## If setup does not work

| Symptom | Check |
|---|---|
| `project/code/requirements.txt` or `dashboard.py` cannot be found | Check that the terminal is in the repository root, not inside `project/` or `project/code/`. |
| `python` or `python3` is not found | Install Python 3.11 or newer, open a new terminal, and follow the appropriate platform commands in the [project README](../README.md). |
| A module such as `streamlit` is missing | Confirm package installation completed using the `.venv` Python command for your platform. Do not launch with a different Python installation. |
| A saved model is missing or cannot be loaded | Confirm that all three `.joblib` files are present in `project/models/`, the complete repository was obtained, and the requirements installed successfully. Do not retrain as a setup workaround. |
| Port 8501 is already in use | Stop any earlier Streamlit process with Ctrl+C. If Streamlit displays a different local URL, use the URL shown in the terminal. |
| A test or verification command fails | Keep the full error output and report the OS, Python version and handover commit to the team. Do not describe that installation as verified. |

## Evidence and platform limits

The earlier functional setup and workflow runs are recorded in the [Windows #66 results](evidence/issue66/windows/2026-10-19-9dc7132/results.md) and [macOS #66 results](evidence/issue66/macos/2026-10-19-9dc7132/results.md). The main runs were on 19 October 2026; the macOS S6-11 Early-Warning retest was on 20 October 2026. Those runs tested commit `9dc7132`, **not** the handover commit above. Refer to their results and limitations without treating the older evidence as a new test of `fe9685a`.

The documented deployment procedure covers local Windows PowerShell and macOS Terminal use. It does not establish Linux support, public hosting, multi-user operation, or performance on every computer. The prototype is a support tool; its predictions must not be used alone to make decisions about a student.

## Handover check

A teammate should use this guide on their own computer and record:

- the commit obtained, OS and Python version;
- whether installation, `pip check`, automated tests and sample checks completed;
- whether they could open the dashboard and stop it with Ctrl+C;
- any error and the step where it occurred.

Link that actual walkthrough or its issue/PR record when claiming that the handover instructions have been verified.
