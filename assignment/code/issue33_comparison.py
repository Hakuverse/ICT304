r"""Generate SARAH Issue #33 evidence without retraining or replacing models.

  Windows: .venv\Scripts\python.exe assignment/code/issue33_comparison.py
  macOS:   .venv/bin/python assignment/code/issue33_comparison.py

Outputs: report, CSV tables and run_details.txt in assignment/docs/;
the new feature-importance chart in assignment/docs/figures/.
Reuses existing confusion matrices without rewriting or copying them.
Uses the existing requirements.txt. Only load the team's trusted joblib files.
Use --repo PATH when running this script from outside the repository.
Use --overwrite to refresh only this script's outputs after reviewing any edits.
"""

import argparse
import hashlib
import importlib.util
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix)
from sklearn.model_selection import train_test_split

SETUPS = {
    "early_warning": ("early_warning", None, "Early-Warning"),
    "confirmatory_g1": ("confirmatory", "g1", "Confirmatory: G1"),
    "confirmatory_g1_g2": ("confirmatory", "g1_g2", "Confirmatory: G1 + G2"),
}
METRICS = ["Accuracy", "Precision", "Recall", "F1"]


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join(["---"] * len(headers)) + " |"] +
                     ["| " + " | ".join(map(str, row)) + " |" for row in rows])

def metrics(y, pred):
    return [round(float(fn(y, pred, **({} if fn is accuracy_score else
                  {"pos_label": 1, "zero_division": 0}))), 3)
            for fn in (accuracy_score, precision_score, recall_score, f1_score)]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--overwrite", action="store_true",
                        help="Replace the generated Issue #33 report, tables, chart and run record.")
    args = parser.parse_args()
    candidates = [Path.cwd(), *Path(__file__).resolve().parents]
    repo = args.repo.resolve() if args.repo else next(
        (p for p in candidates if (p / "assignment/code/data_processing.py").is_file()), None)
    if repo is None:
        parser.error("Cannot find ICT304. Run from its root or supply --repo PATH.")
    root = repo / "assignment"
    output = root / "docs"
    figures = output / "figures"
    generated = [output / name for name in (
        "issue33_report.md", "development_comparison.csv", "final_test_results.csv",
        "feature_importance.csv", "run_details.txt")]
    generated.append(figures / "early_warning_feature_importance.png")
    if not args.overwrite and any(path.exists() for path in generated):
        parser.error("Issue #33 outputs already exist. Review them, then add --overwrite to refresh them.")
    confusion_figures = [figures / f"confusion_{name}.png" for name in SETUPS]
    missing = [path.name for path in confusion_figures if not path.is_file()]
    if missing:
        parser.error("Missing existing confusion matrices: " + ", ".join(missing) +
                     ". Restore these from the reviewed repository before running this script.")
    report_path = root / "docs/evaluation_report.md"
    report = report_path.read_text(encoding="utf-8")
    spec = importlib.util.spec_from_file_location("sarah_issue33_data", root / "code/data_processing.py")
    processing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(processing)

    # Read the recorded development results; do not fit or select on the test set.
    rows = []
    for line in report.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) == 7 and cells[0] in SETUPS:
            rows.append(cells[:3] + [float(v) for v in cells[3:]])
    if len(rows) != 12:
        raise ValueError("Expected 12 development rows in evaluation_report.md.")
    dev = pd.DataFrame(rows, columns=["Setup", "Technique", "Weight", *METRICS])
    for name in SETUPS:
        subset = dev[dev.Setup == name]
        combinations = {(r.Technique, r.Weight) for r in subset.itertuples()}
        expected = {(t, w) for t in ["Logistic Regression", "Decision Tree (depth=4)"]
                    for w in ["None", "balanced"]}
        if combinations != expected or len(subset) != 4:
            raise ValueError("This script expects the current depth-4, 12-row experiment.")

    full = {name: processing.build_training_xy(root / "data", mode, grade)
            for name, (mode, grade, _) in SETUPS.items()}
    y = full["early_warning"][1]
    if len(y) != 395 or int(y.sum()) != 130:
        raise ValueError("Dataset differs from the documented 395-student experiment.")
    dev_idx, test_idx = train_test_split(y.index, test_size=0.2, stratify=y, random_state=42)
    finals, selections, models = [], [], {}
    fingerprints = [report_path, root / "data/student-mat.csv", root / "code/data_processing.py",
                    root / "code/train_models.py", *confusion_figures]
    for name, (_, _, label) in SETUPS.items():
        X, target = full[name]
        if not target.equals(y):
            raise ValueError("Setups do not share the same target and row order.")
        choice = dev[dev.Setup == name].sort_values(["Recall", "F1"], ascending=False,
                                                   kind="stable").iloc[0]
        model_path = root / "models" / f"{name}_model.joblib"
        model = joblib.load(model_path)
        expected_type = "LogisticRegression" if choice.Technique == "Logistic Regression" else "DecisionTreeClassifier"
        if type(model).__name__ != expected_type or model.class_weight != (None if choice.Weight == "None" else choice.Weight):
            raise ValueError(f"{name}: saved model does not match the recorded selection.")
        if list(model.feature_names_in_) != list(X.columns) or list(model.classes_) != [0, 1]:
            raise ValueError(f"{name}: unexpected feature order or class labels.")
        if expected_type == "DecisionTreeClassifier" and model.max_depth != 4:
            raise ValueError("Expected the selected depth-4 tree.")
        pred = model.predict(X.loc[test_idx])
        scores = metrics(target.loc[test_idx], pred)

        # Reject stale artifacts rather than silently generating inconsistent prose.
        final_line = next((line for line in report.splitlines()
                           if line.startswith(f"- **{name}**") and "accuracy " in line), "")
        import re
        match = re.search(r"accuracy ([\d.]+), precision ([\d.]+), recall ([\d.]+), F1 ([\d.]+)", final_line)
        if not match or scores != [float(v) for v in match.groups()]:
            raise ValueError(f"{name}: saved-model test results do not match evaluation_report.md.")

        matrix = confusion_matrix(target.loc[test_idx], pred, labels=[0, 1])
        tn, fp, fn, tp = map(int, matrix.ravel())
        finals.append([label, *scores, tn, fp, fn, tp])
        selections.append([label, choice.Technique, choice.Weight, choice.Recall, choice.F1])
        models[name] = model
        fingerprints.append(model_path)

    # The discussion below describes this specific reviewed experiment. Stop if
    # future models/results differ, rather than publish stale conclusions.
    expected_finals = [
        ["Early-Warning", .633, .44, .423, .431, 39, 14, 15, 11],
        ["Confirmatory: G1", .823, .714, .769, .741, 45, 8, 6, 20],
        ["Confirmatory: G1 + G2", .899, .821, .885, .852, 48, 5, 3, 23],
    ]
    expected_scores = [(.696,.7,.212,.311),(.7,.573,.397,.454),
                       (.703,.657,.299,.4),(.617,.422,.482,.444),
                       (.855,.776,.79,.78),(.829,.707,.838,.765),
                       (.839,.818,.646,.719),(.798,.663,.838,.728),
                       (.889,.832,.828,.829),(.864,.745,.904,.815),
                       (.893,.824,.857,.839),(.87,.766,.876,.814)]
    expected_keys = [(s,t,w) for s in SETUPS
                     for t in ["Logistic Regression", "Decision Tree (depth=4)"]
                     for w in ["None", "balanced"]]
    actual_scores = {tuple(row[:3]): tuple(row[3:]) for row in rows}
    if finals != expected_finals or actual_scores != dict(zip(expected_keys, expected_scores)):
        raise ValueError("Results have changed. Review the discussion before using this version of the script.")

    output.mkdir(parents=True, exist_ok=True)
    dev.to_csv(output / "development_comparison.csv", index=False)
    headers = ["Setup", *METRICS, "Correct Low", "False alarms", "Missed High", "Found High"]
    pd.DataFrame(finals, columns=headers).to_csv(output / "final_test_results.csv", index=False)

    tree = models["early_warning"]
    importance = pd.Series(tree.feature_importances_, index=tree.feature_names_in_).sort_values(ascending=False)
    importance.rename("importance").rename_axis("feature").to_csv(output / "feature_importance.csv")
    labels = {"attendance_pct": "Attendance estimate", "study_hours": "Estimated study hours", "failures": "Past failures"}
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ordered = importance.sort_values()
    bars = ax.barh([labels.get(k, k) for k in ordered.index], ordered.values, color="#32769b")
    ax.bar_label(bars, labels=[f"{v:.1%}" for v in ordered.values], padding=5)
    ax.set_xlim(0, max(0.1, ordered.max() * 1.22))
    ax.set_xlabel("Share of the tree's weighted impurity reduction")
    ax.set_title("Early-Warning Decision Tree\nRelative input importance in the fitted model")
    fig.tight_layout()
    fig.savefig(figures / "early_warning_feature_importance.png", dpi=160)
    plt.close(fig)

    baseline = metrics(y.loc[test_idx], np.zeros(len(test_idx), dtype=int))
    text = ["# SARAH model comparison and discussion", "",
        "## Purpose and method", "",
        "We compared Logistic Regression and Decision Tree for academic-risk classification. "
        "Logistic Regression gives a relatively simple statistical model, while a Decision Tree can "
        "represent branching rules and nonlinear relationships. Both suit our small tabular prototype, "
        "but neither guarantees reliable performance for a new school or cohort.", "",
        "There are two user modes and three trained setups: Early-Warning without grades, Confirmatory "
        "with G1, and Confirmatory with G1 and G2. Each technique was tried with normal and balanced "
        "class weights, giving 12 comparisons. G3 below 10 defines High Risk; G3 is not an input.", "",
        "The existing experiment first reserved 79 of 395 students using a stratified split and seed 42. "
        "The other 316 students were used for five-fold development validation. The same groups were "
        "used across setups. This script reads those recorded development results and checks the saved "
        "models on the same reserved students. It does not retrain, tune models or provide a new independent test.", "",
        "## Development comparison", "",
        table(list(dev.columns), dev.values.tolist()), "",
        "Accuracy measures all correct predictions. Precision measures how many flagged students were "
        "actually High Risk. Recall measures how many High-Risk students were found. F1 combines precision "
        "and recall. In these results, balanced weights improved recall but reduced precision in every "
        "setup for both techniques, meaning more students were found but more false alarms occurred.", "",
        "## Selected models", "",
        table(["Setup", "Technique", "Weight", "Development recall", "Development F1"], selections), "",
        "Selection follows the existing code: highest development recall, then highest F1, using scores "
        "rounded to three decimals. Finding students who may need support was prioritised over avoiding "
        "every false alarm. For G1-only, both balanced techniques had recall 0.838; Logistic Regression "
        "won the tie with F1 0.765 rather than 0.728. For Early-Warning, the tree's higher recall was "
        "preferred even though balanced Logistic Regression had a slightly higher F1.", "",
        "The shared tree depth was chosen from 2, 3, 4, 5, 6 and no limit using balanced Early-Warning "
        "development recall. Depth 4 scored highest at 0.482. It was reused for all tree comparisons; "
        "this does not establish that depth 4 is optimal for every setup.", "",
        "## Reserved test results and baseline", "",
        table(headers, finals), "",
        f"Always predicting Low Risk gives accuracy {baseline[0]:.3f}, precision {baseline[1]:.3f}, "
        f"recall {baseline[2]:.3f} and F1 {baseline[3]:.3f} on these students. Precision is reported as "
        "zero by convention because it flags nobody. It correctly labels 53 of 79 students but misses "
        "all 26 High-Risk students. Early-Warning accuracy (0.633) is below this baseline, although it "
        "finds 11 of the 26 High-Risk students. It also misses 15 and incorrectly flags 14 Low-Risk "
        "students. This is a substantial limitation, not evidence that the prototype is ready for deployment.", "",
        "G1-only finds 20 High-Risk students, misses 6 and produces 8 false alarms. G1 plus G2 finds "
        "23, misses 3 and produces 5 false alarms. Grades improve performance in this experiment, "
        "but waiting for them reduces how early the result can be available.", ""]

    for name in SETUPS:
        text += [f"![{SETUPS[name][2]} confusion matrix](figures/confusion_{name}.png)", ""]

    text += ["Rows in these matrices are actual classes; columns are predicted classes. "
             "False negatives are missed High-Risk students, and false positives are false alarms.", "",
             "## Feature-importance chart and explanation", "",
             "![Early-Warning feature importance](figures/early_warning_feature_importance.png)", "",
             table(["Input", "Relative importance"], [[labels[k], f"{v:.1%}"] for k, v in importance.items()]), "",
             f"The largest importance belongs to {labels[importance.index[0]].lower()} "
             f"({importance.iloc[0]:.1%}). This means it contributed the largest share of weighted "
             "impurity reduction across splits in this fitted tree. The values sum to 100%; they "
             "are not changes in a student's risk probability. This chart describes the Early-Warning "
             "tree only and does not explain every individual prediction.", "",
             "The chart does not show whether an input increases or decreases risk, prove causation, "
             "or tell us that changing that input will improve grades. Tree importance can favour "
             "variables with more possible split values, and related inputs can share importance. "
             "Values may change with a different sample. Raw Logistic Regression coefficients are "
             "not ranked here because the inputs have different scales and the current model has no StandardScaler.", "",
             "## Limitations and next steps", "",
             "- This experiment contains only 395 Math-course students and one fixed 79-student test split. "
             "Results are uncertain and may not transfer to another cohort or institution.",
             "- The data has no week-by-week records. Early-Warning means without grades, not proven day-one accuracy. "
             "Inputs intended for an early prediction would need to be collected by that time.",
             "- Attendance is estimated from capped absence counts, not measured attendance percentage. Study hours "
             "are estimates from categories, including an assumed value for the highest category. The 40-hour "
             "input limit is a validation rule, not a range established by the training data.",
             "- High Risk is defined using G3 below 10. It is a narrow academic outcome and does not capture every support need.",
             "- Logistic Regression currently has no scaling. Different input scales affect coefficient interpretation "
             "and regularisation. A future comparison could fit scaling inside each training fold.",
             "- The tree depth was selected and scored using the same development folds. Those development scores "
             "may be optimistic after selection. The reserved test was excluded from that choice. A fuller future "
             "study could use nested validation and repeated splits, without tuning against the current test results.",
             "- Balanced class weights trade extra false alarms for fewer missed students. The team should discuss "
             "both costs with the tutor rather than claim recall alone proves practical usefulness.",
             "- Predicted probabilities have not been checked for calibration, and subgroup fairness has not been "
             "established. Results should support human review, not automatic decisions about students.",
             "- The working prototype is command-line classification. Dashboard and recommendation work remains planned.", "",
             "## Handoff to Issue #34", "",
             "Use the comparison, selected-model explanation, final results, four figures and limitations above "
             "in the prototype/results/discussion sections. Keep development and reserved-test results separate. "
             "The CSV files provide the underlying tables. The confusion matrices are reused from figures/; "
             "only the feature-importance chart is generated here. This section supplements the existing diagram and "
             "five-part model test plan; it does not replace them.", "",
             "- [ ] Jackie reviews the generated text and charts against the source report.",
             "- [ ] Another teammate reviews the comparison before Issue #33 is closed.",
             "- [ ] The Issue #34 owner integrates the material, figure numbers and references into the report.", "",
             "## Sources", "",
             "- Existing team files: assignment/docs/evaluation_report.md, assignment/code/train_models.py, "
             "assignment/code/data_processing.py and the three assignment/models/*_model.joblib files.",
             "- UCI Student Performance dataset: https://doi.org/10.24432/C5TG7T",
             "- Scikit-learn tree importance example and cautions: https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html",
             "- Scikit-learn coefficient interpretation: https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html", ""]

    (output / "issue33_report.md").write_text("\n".join(text), encoding="utf-8")

    provenance = [
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        f"Python: {platform.python_version()}; scikit-learn: {sklearn.__version__}; "
        f"pandas: {pd.__version__}; numpy: {np.__version__}; joblib: {joblib.__version__}",
        "Checks: 12 development rows; saved-model type/features/classes; matching reserved-test metrics.",
        "Development scores are read from the existing report, not recomputed.",
        "No source evaluation report, training code, model, confusion matrix or prompt log was changed.",
        "",
        "Input SHA-256:",
    ]

    provenance += [
        f"{p.relative_to(repo).as_posix()}: "
        f"{hashlib.sha256(p.read_bytes()).hexdigest()}"
        for p in fingerprints
    ]

    (output / "run_details.txt").write_text(
        "\n".join(provenance) + "\n", encoding="utf-8")

    print(f"Created Issue #33 handoff in: {output}")
    print("Open issue33_report.md. The new chart is in docs/figures/; existing confusion matrices are reused.")
    print("Teammate review is still required.")
    print("Feature importance:")
    print(importance.to_string())

if __name__ == "__main__":
    main()
