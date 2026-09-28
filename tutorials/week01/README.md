# Week 1: Rice classification

This tutorial is separate from the SARAH assignment. The [original Word user manual](README_user_manual.docx) is retained. Use the commands below from this folder.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe rice_classification.py
```

On macOS, create the environment with `python3 -m venv .venv` and use `.venv/bin/python` for the other commands. Use Python 3.11 or newer for the listed packages.

The script compares four models and writes results.txt, model_comparison_results.csv, confusion_matrices.png and feature_importance.png. Scaling is fitted within each cross-validation training fold. Fixed seeds help repeat the results; timings and results can still differ between software versions or computers. The model with the highest observed test accuracy is a comparison result, not a separate independent estimate after model selection.
