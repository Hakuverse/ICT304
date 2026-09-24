"""
SARAH — Model Training & Evaluation
-------------------------------------
Compares Logistic Regression vs Decision Tree for both modes
(early_warning, confirmatory), at class_weight=None and
class_weight="balanced" -- 8 combinations total -- using stratified 5-fold
cross-validation on the full dataset (not a single train/test split: with
only 130 High Risk students out of 395, a single 80/20 split leaves too
few High Risk examples in the test set for a stable precision/recall
estimate).

Run with:  python assignment/code/train_models.py   (from the repo root,
           or from inside assignment/code/ -- paths are relative to this
           file either way)

Outputs:
  assignment/docs/evaluation_report.md            8-combination table +
                                                    selected model per mode
  assignment/docs/figures/confusion_early_warning.png
  assignment/docs/figures/confusion_confirmatory.png
  assignment/models/early_warning_model.joblib
  assignment/models/confirmatory_model.joblib
  assignment/models/feature_stats.json             mean/std per feature
                                                    (train split only, for
                                                    the recommendation
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

from data_processing import VALID_MODES, build_training_xy, get_feature_columns

ASSIGNMENT_ROOT = Path(__file__).resolve().parents[1]  # assignment/code -> assignment/
DATA_DIR = ASSIGNMENT_ROOT / "data"
DOCS_DIR = ASSIGNMENT_ROOT / "docs"
FIG_DIR = DOCS_DIR / "figures"
MODELS_DIR = ASSIGNMENT_ROOT / "models"
FIG_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
N_FOLDS = 5


def make_model(technique: str, class_weight):
    if technique == "Logistic Regression":
        return LogisticRegression(class_weight=class_weight, random_state=RANDOM_STATE, max_iter=1000)
    return DecisionTreeClassifier(class_weight=class_weight, random_state=RANDOM_STATE)


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


def select_decision_tree_depth(X, y):
    """Pick max_depth for the Decision Tree via 5-fold CV recall, Early-Warning mode,
    class_weight='balanced' -- same depth is then used for both modes so the
    8-combination comparison is fair (one fixed depth, not tuned per mode)."""
    depths = [2, 3, 4, 5, 6, None]
    results = {}
    for depth in depths:
        model = DecisionTreeClassifier(max_depth=depth, class_weight="balanced", random_state=RANDOM_STATE)
        results[depth] = cv_scores(model, X, y)["recall_high_risk"]
    best_depth = max(results, key=results.get)
    return best_depth, results


def main():
    datasets = {mode: build_training_xy(DATA_DIR, mode) for mode in VALID_MODES}

    best_depth, depth_trials = select_decision_tree_depth(*datasets["early_warning"])

    lines = []
    lines.append("# SARAH — Model Evaluation Report\n")
    lines.append(
        "Dataset: UCI Student Performance, **Math course only** (student-mat.csv, n=395). "
        "See `docs/CLASS_IMBALANCE_NOTE.md` for the class-imbalance and Portuguese-subset "
        "comparison.\n"
    )
    lines.append("## Decision Tree depth selection\n")
    lines.append(
        "One fixed depth is used across all 8 combinations below, for a fair comparison. "
        "Chosen via 5-fold CV recall on Early-Warning mode, class_weight='balanced':\n"
    )
    lines.append("| max_depth | High-Risk recall (5-fold CV mean) |\n|---|---|")
    for depth in [2, 3, 4, 5, 6, None]:
        marker = " **← selected**" if depth == best_depth else ""
        lines.append(f"| {depth if depth is not None else 'None'} | {depth_trials[depth]}{marker} |")
    lines.append("")

    lines.append("## The 8-combination comparison (5-fold stratified cross-validation)\n")
    lines.append(
        "2 modes × 2 techniques × 2 class_weight settings. Metrics are the mean across 5 "
        "folds of the whole 395-student dataset (not a single train/test split -- with only "
        "130 High Risk students, a single 80/20 split leaves too few High Risk examples in "
        "the test set for a stable estimate).\n"
    )
    lines.append(
        "| Mode | Technique | class_weight | Accuracy | Precision (High Risk) | "
        "Recall (High Risk) | F1 (High Risk) |\n|---|---|---|---|---|---|---|"
    )

    all_results = {}
    for mode in VALID_MODES:
        X, y = datasets[mode]
        for technique in ["Logistic Regression", "Decision Tree"]:
            for class_weight in [None, "balanced"]:
                model = make_model(technique, class_weight)
                if technique == "Decision Tree":
                    model = DecisionTreeClassifier(max_depth=best_depth, class_weight=class_weight, random_state=RANDOM_STATE)
                scores = cv_scores(model, X, y)
                all_results[(mode, technique, class_weight)] = scores
                tech_label = f"Decision Tree (depth={best_depth})" if technique == "Decision Tree" else technique
                lines.append(
                    f"| {mode} | {tech_label} | {class_weight} | {scores['accuracy']} | "
                    f"{scores['precision_high_risk']} | {scores['recall_high_risk']} | "
                    f"{scores['f1_high_risk']} |"
                )
    lines.append("")

    # Selection: highest recall (tie-broken by F1), per mode
    best_per_mode = {}
    for mode in VALID_MODES:
        candidates = [(k, v) for k, v in all_results.items() if k[0] == mode]
        best_key, best_scores = max(candidates, key=lambda kv: (kv[1]["recall_high_risk"], kv[1]["f1_high_risk"]))
        best_per_mode[mode] = {"technique": best_key[1], "class_weight": best_key[2], **best_scores}

    lines.append("## Selected combination per mode\n")
    for mode in VALID_MODES:
        b = best_per_mode[mode]
        tech_label = f"Decision Tree (depth={best_depth})" if b["technique"] == "Decision Tree" else b["technique"]
        lines.append(
            f"- **{mode}**: {tech_label}, class_weight={b['class_weight']} — "
            f"recall {b['recall_high_risk']}, F1 {b['f1_high_risk']} (5-fold CV mean)"
        )
    lines.append(
        "\nSelection criterion (same throughout this project): highest recall on the High "
        "Risk class, since a missed at-risk student (false negative) is costlier for an "
        "early-warning system than a false alarm (false positive).\n"
    )

    lines.append(
        "## Accuracy-vs-earliness tradeoff\n\n"
        f"Early-Warning mode (no grades, available before any assessment exists): recall "
        f"{best_per_mode['early_warning']['recall_high_risk']}. "
        f"Confirmatory mode (adds previous_score once G1/G2 exist): recall "
        f"{best_per_mode['confirmatory']['recall_high_risk']}. "
        "This is the core tradeoff SARAH makes explicit: Early-Warning mode is what actually "
        "lets a tutor intervene before it's too late, at whatever accuracy cost that "
        "involves; Confirmatory mode is more accurate but only available once it's partly "
        "too late to act on the 'early' half of 'early warning'. SARAH defaults to "
        "Early-Warning mode for this reason, with Confirmatory available for a second look "
        "once grades exist.\n"
    )

    # Refit selected combination on an 80/20 holdout, for confusion matrix + deployable model
    lines.append("## Holdout confusion matrices (80/20 split, best combination per mode)\n")
    feature_stats = None
    for mode in VALID_MODES:
        X, y = datasets[mode]
        b = best_per_mode[mode]
        model = make_model(b["technique"], b["class_weight"])
        if b["technique"] == "Decision Tree":
            model = DecisionTreeClassifier(max_depth=best_depth, class_weight=b["class_weight"], random_state=RANDOM_STATE)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
        )
        model.fit(X_train, y_train)

        fig, ax = plt.subplots(figsize=(4, 4))
        ConfusionMatrixDisplay.from_estimator(
            model, X_test, y_test, display_labels=["Low Risk", "High Risk"], cmap="Blues", ax=ax
        )
        ax.set_title(f"{mode} — holdout confusion matrix")
        fig.tight_layout()
        fig.savefig(FIG_DIR / f"confusion_{mode}.png", dpi=150)
        plt.close(fig)

        joblib.dump(model, MODELS_DIR / f"{mode}_model.joblib")

        tech_label = f"Decision Tree (depth={best_depth})" if b["technique"] == "Decision Tree" else b["technique"]
        lines.append(
            f"- **{mode}**: `docs/figures/confusion_{mode}.png` ({tech_label}, "
            f"class_weight={b['class_weight']}, {int(y_test.sum())} High Risk / "
            f"{len(y_test)} total in the holdout test set)"
        )

        if mode == "confirmatory":
            stat_cols = get_feature_columns("confirmatory")
            feature_stats = {
                col: {"mean": round(float(X_train[col].mean()), 3), "std": round(float(X_train[col].std()), 3)}
                for col in stat_cols
            }
    lines.append("")

    with open(MODELS_DIR / "selected_mode.txt", "w", encoding="utf-8") as f:
        f.write("early_warning")

    with open(MODELS_DIR / "feature_stats.json", "w", encoding="utf-8") as f:
        json.dump(feature_stats, f, indent=2)

    lines.append("## Feature statistics (Confirmatory-mode train split, used for recommendation z-scores)\n")
    lines.append("```json")
    lines.append(json.dumps(feature_stats, indent=2))
    lines.append("```")

    with open(DOCS_DIR / "evaluation_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
