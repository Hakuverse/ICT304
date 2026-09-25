"""
SARAH — Model Training & Evaluation
-------------------------------------
Three setups, each compared with Logistic Regression vs Decision Tree, at
class_weight=None and class_weight="balanced" -- 3 setups x 2 techniques x
2 class_weight settings = 12 combinations total:
  - early_warning        (attendance, study hours, failures -- no grades)
  - confirmatory_g1      (Confirmatory mode, G1 only)
  - confirmatory_g1_g2   (Confirmatory mode, G1 and G2 both)

A tutor entering Confirmatory-mode data may only have G1 (partway through
term) or both G1 and G2 (later). Feeding a G1-only value into a model that
only ever saw G1+G2 averages during training would ask that model to
extrapolate outside what it learned from -- so G1-only and G1+G2 are
trained and evaluated as two separate setups, not one shared model.

Evaluation procedure (fixes a real leakage bug from an earlier version of
this script): a stratified 20% test set is reserved from the full 395
students FIRST, using the same split for all three setups (their target
label only depends on G3, not on which setup's features are used). Every
combination's cross-validation score is then computed using ONLY the
remaining 80% "development" data -- the reserved test students are never
part of any fold used to pick a technique, a class_weight, or the shared
Decision Tree depth. Only after a combination is selected per setup is it
refit on the full development set and evaluated ONCE on the untouched
test set -- that result is the genuine held-out check.

Run with:  python assignment/code/train_models.py   (from the repo root,
           or from inside assignment/code/ -- paths are relative to this
           file either way)

Outputs:
  assignment/docs/evaluation_report.md            12-combination table +
                                                    selected setup + real
                                                    held-out test metrics
  assignment/docs/figures/confusion_early_warning.png
  assignment/docs/figures/confusion_confirmatory_g1.png
  assignment/docs/figures/confusion_confirmatory_g1_g2.png
  assignment/models/early_warning_model.joblib
  assignment/models/confirmatory_g1_model.joblib
  assignment/models/confirmatory_g1_g2_model.joblib
  assignment/models/feature_stats.json             mean/std per feature
                                                    (development split
                                                    only, for the
                                                    recommendation
                                                    engine's z-scores)
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

from data_processing import build_training_xy, get_feature_columns

ASSIGNMENT_ROOT = Path(__file__).resolve().parents[1]  # assignment/code -> assignment/
DATA_DIR = ASSIGNMENT_ROOT / "data"
DOCS_DIR = ASSIGNMENT_ROOT / "docs"
FIG_DIR = DOCS_DIR / "figures"
MODELS_DIR = ASSIGNMENT_ROOT / "models"
FIG_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
N_FOLDS = 5
TEST_SIZE = 0.2

# setup name -> (mode, grade_setup or None)
SETUPS = {
    "early_warning": ("early_warning", None),
    "confirmatory_g1": ("confirmatory", "g1"),
    "confirmatory_g1_g2": ("confirmatory", "g1_g2"),
}


def make_model(technique: str, class_weight, max_depth=None):
    if technique == "Logistic Regression":
        return LogisticRegression(class_weight=class_weight, random_state=RANDOM_STATE, max_iter=1000)
    return DecisionTreeClassifier(max_depth=max_depth, class_weight=class_weight, random_state=RANDOM_STATE)


def cv_scores(model, X, y):
    """Mean accuracy/precision/recall/F1 (High Risk class) across N_FOLDS stratified folds."""
    skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    accs, precs, recs, f1s = [], [], [], []
    for train_idx, test_idx in skf.split(X, y):
        model.fit(X.iloc[train_idx], y.iloc[train_idx])
        pred = model.predict(X.iloc[test_idx])
        y_test = y.iloc[test_idx]
        accs.append(accuracy_score(y_test, pred))
        precs.append(precision_score(y_test, pred, pos_label=1, zero_division=0))
        recs.append(recall_score(y_test, pred, pos_label=1, zero_division=0))
        f1s.append(f1_score(y_test, pred, pos_label=1, zero_division=0))
    n = len(accs)
    return {
        "accuracy": round(sum(accs) / n, 3),
        "precision_high_risk": round(sum(precs) / n, 3),
        "recall_high_risk": round(sum(recs) / n, 3),
        "f1_high_risk": round(sum(f1s) / n, 3),
    }


def select_decision_tree_depth(X_dev, y_dev):
    """Pick max_depth for the Decision Tree via 5-fold CV recall on the
    Early-Warning DEVELOPMENT data only (test set excluded), class_weight=
    'balanced' -- the same depth is then used for every setup so the
    12-combination comparison is fair (one fixed depth, not tuned per setup)."""
    depths = [2, 3, 4, 5, 6, None]
    results = {}
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, class_weight="balanced", random_state=RANDOM_STATE)
        results[depth] = cv_scores(model, X_dev, y_dev)["recall_high_risk"]
    best_depth = max(results, key=results.get)
    return best_depth, results


def main():
    # Build all three setups' full (X, y) -- same 395 students, same row order/index
    # (all derived from load_raw_uci() with no reordering), so a single stratified
    # split of indices is valid across every setup.
    full = {name: build_training_xy(DATA_DIR, mode, grade_setup) if grade_setup
            else build_training_xy(DATA_DIR, mode)
            for name, (mode, grade_setup) in SETUPS.items()}

    # Reserve the test set ONCE, from the label only (identical across setups since
    # risk depends only on G3, not on which setup's features are used).
    _, y_any = full["early_warning"]
    dev_idx, test_idx = train_test_split(
        y_any.index, test_size=TEST_SIZE, stratify=y_any, random_state=RANDOM_STATE
    )

    dev = {name: (X.loc[dev_idx], y.loc[dev_idx]) for name, (X, y) in full.items()}
    held_out = {name: (X.loc[test_idx], y.loc[test_idx]) for name, (X, y) in full.items()}

    best_depth, depth_trials = select_decision_tree_depth(*dev["early_warning"])

    lines = []
    lines.append("# SARAH — Model Evaluation Report\n")
    lines.append(
        "Dataset: UCI Student Performance, **Math course only** (student-mat.csv, n=395). "
        "See `docs/CLASS_IMBALANCE_NOTE.md` for the class-imbalance and Portuguese-subset "
        "comparison.\n"
    )
    lines.append(
        f"**Evaluation procedure:** a stratified {int(TEST_SIZE*100)}% test set "
        f"({len(test_idx)} students) was reserved from the full 395 *before* any model "
        f"selection, using the same split for all three setups below. Every "
        "cross-validation score in this report (depth selection and the 12-combination "
        f"table) uses only the remaining {len(dev_idx)} development students -- the "
        "reserved test students are never part of any fold used to pick a technique, a "
        "class_weight, or the shared Decision Tree depth. The 'Held-out test results' "
        "section at the end is the only place the reserved students are used, and each "
        "setup's selected model sees them exactly once, after selection is finalised.\n"
    )

    lines.append("## Decision Tree depth selection (development data only)\n")
    lines.append(
        "One fixed depth is used across all 12 combinations below, for a fair comparison. "
        "Chosen via 5-fold CV recall on Early-Warning development data, "
        "class_weight='balanced':\n"
    )
    lines.append("| max_depth | High-Risk recall (5-fold CV mean) |\n|---|---|")
    for depth in [2, 3, 4, 5, 6, None]:
        marker = " **← selected**" if depth == best_depth else ""
        lines.append(f"| {depth if depth is not None else 'None'} | {depth_trials[depth]}{marker} |")
    lines.append("")

    lines.append("## The 12-combination comparison (5-fold CV on development data only)\n")
    lines.append(
        "3 setups × 2 techniques × 2 class_weight settings. Confirmatory mode has two "
        "setups because a tutor may have only G1, or both G1 and G2 -- each is a "
        "separately trained model, not one model asked to handle both cases (see module "
        "docstring). This grew the comparison from the original 8 rows to 12 once the "
        "team agreed G1-only needed its own trained-and-evaluated model, not just an "
        "extrapolated prediction from the G1+G2 model.\n"
    )
    lines.append(
        "| Setup | Technique | class_weight | Accuracy | Precision (High Risk) | "
        "Recall (High Risk) | F1 (High Risk) |\n|---|---|---|---|---|---|---|"
    )

    all_results = {}
    for name in SETUPS:
        X_dev, y_dev = dev[name]
        for technique in ["Logistic Regression", "Decision Tree"]:
            for class_weight in [None, "balanced"]:
                model = make_model(technique, class_weight, max_depth=best_depth)
                scores = cv_scores(model, X_dev, y_dev)
                all_results[(name, technique, class_weight)] = scores
                tech_label = f"Decision Tree (depth={best_depth})" if technique == "Decision Tree" else technique
                lines.append(
                    f"| {name} | {tech_label} | {class_weight} | {scores['accuracy']} | "
                    f"{scores['precision_high_risk']} | {scores['recall_high_risk']} | "
                    f"{scores['f1_high_risk']} |"
                )
    lines.append("")

    # Selection: highest recall (tie-broken by F1), per setup -- development scores only
    best_per_setup = {}
    for name in SETUPS:
        candidates = [(k, v) for k, v in all_results.items() if k[0] == name]
        best_key, best_scores = max(candidates, key=lambda kv: (kv[1]["recall_high_risk"], kv[1]["f1_high_risk"]))
        best_per_setup[name] = {"technique": best_key[1], "class_weight": best_key[2], **best_scores}

    lines.append("## Selected combination per setup (development CV -- used to choose, not to report final performance)\n")
    for name in SETUPS:
        b = best_per_setup[name]
        tech_label = f"Decision Tree (depth={best_depth})" if b["technique"] == "Decision Tree" else b["technique"]
        lines.append(
            f"- **{name}**: {tech_label}, class_weight={b['class_weight']} — "
            f"development recall {b['recall_high_risk']}, F1 {b['f1_high_risk']} (5-fold CV mean)"
        )
    lines.append(
        "\nSelection criterion (same throughout this project): highest recall on the High "
        "Risk class, since a missed at-risk student (false negative) is costlier for an "
        "early-warning system than a false alarm (false positive).\n"
    )

    # Refit each selected combination on the FULL development set, evaluate ONCE on the
    # reserved (never-before-seen) test set. This is the genuine held-out result.
    lines.append("## Held-out test results (reserved students, never used in selection above)\n")
    feature_stats = None
    for name, (mode, grade_setup) in SETUPS.items():
        X_dev, y_dev = dev[name]
        X_test, y_test = held_out[name]
        b = best_per_setup[name]
        model = make_model(b["technique"], b["class_weight"], max_depth=best_depth)
        model.fit(X_dev, y_dev)

        pred = model.predict(X_test)
        test_metrics = {
            "accuracy": round(accuracy_score(y_test, pred), 3),
            "precision_high_risk": round(precision_score(y_test, pred, pos_label=1, zero_division=0), 3),
            "recall_high_risk": round(recall_score(y_test, pred, pos_label=1, zero_division=0), 3),
            "f1_high_risk": round(f1_score(y_test, pred, pos_label=1, zero_division=0), 3),
        }

        fig, ax = plt.subplots(figsize=(4, 4))
        ConfusionMatrixDisplay.from_estimator(
            model, X_test, y_test, display_labels=["Low Risk", "High Risk"], cmap="Blues", ax=ax
        )
        ax.set_title(f"{name} — held-out test confusion matrix")
        fig.tight_layout()
        fig.savefig(FIG_DIR / f"confusion_{name}.png", dpi=150)
        plt.close(fig)

        joblib.dump(model, MODELS_DIR / f"{name}_model.joblib")

        tech_label = f"Decision Tree (depth={best_depth})" if b["technique"] == "Decision Tree" else b["technique"]
        lines.append(
            f"- **{name}** ({tech_label}, class_weight={b['class_weight']}): accuracy "
            f"{test_metrics['accuracy']}, precision {test_metrics['precision_high_risk']}, "
            f"recall {test_metrics['recall_high_risk']}, F1 {test_metrics['f1_high_risk']} "
            f"— `docs/figures/confusion_{name}.png` ({int(y_test.sum())} High Risk / "
            f"{len(y_test)} total)"
        )

        if name == "confirmatory_g1_g2":
            stat_cols = get_feature_columns("confirmatory")
            feature_stats = {
                col: {"mean": round(float(X_dev[col].mean()), 3), "std": round(float(X_dev[col].std()), 3)}
                for col in stat_cols
            }
    lines.append("")

    lines.append(
        "## Accuracy-vs-earliness tradeoff\n\n"
        f"Early-Warning setup (without assessment grades): "
        f"development recall {best_per_setup['early_warning']['recall_high_risk']}. "
        f"Confirmatory (G1+G2) setup: development recall "
        f"{best_per_setup['confirmatory_g1_g2']['recall_high_risk']}. This is a limitation "
        "observed in our current experiments, not a proven irreducible limit: Early-Warning "
        "mode predicts without assessment grades, using only attendance, study habits, and "
        "past failures, so weaker results here are expected given the narrower feature set "
        "-- but these results do not prove that better Early-Warning performance is "
        "impossible with more data or features. SARAH defaults to Early-Warning mode "
        "regardless, since catching risk earlier -- even less accurately -- is the point of "
        "an early-warning system; Confirmatory mode is available as a second look once "
        "grades exist. This dataset has no week-by-week records, so these results do not "
        "establish day-one or week-specific accuracy.\n"
    )

    with open(MODELS_DIR / "selected_mode.txt", "w", encoding="utf-8") as f:
        f.write("early_warning")

    with open(MODELS_DIR / "feature_stats.json", "w", encoding="utf-8") as f:
        json.dump(feature_stats, f, indent=2)

    lines.append("## Feature statistics (Confirmatory G1+G2 development split, used for recommendation z-scores)\n")
    lines.append("```json")
    lines.append(json.dumps(feature_stats, indent=2))
    lines.append("```")

    with open(DOCS_DIR / "evaluation_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
