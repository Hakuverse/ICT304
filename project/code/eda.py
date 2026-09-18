"""
SARAH — Exploratory Data Analysis
------------------------------------
Covers Sprint 2: Correlation check, EDA visualisations, and outlier
decision/documentation.

Run with:  python eda.py   (from inside project/code, with venv active)
Outputs: project/docs/eda_findings.md and project/docs/figures/*.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from data_processing import engineer_features, load_raw_uci

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # project/code -> project/
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
FIG_DIR = DOCS_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def correlation_check(raw: pd.DataFrame, feats: pd.DataFrame):
    raw_cols = ["absences", "studytime", "failures", "G1", "G2", "G3"]
    corr_raw = raw[raw_cols].corr()

    feat_cols = ["attendance_pct", "study_hours", "previous_score", "failures", "risk"]
    corr_feat = feats[feat_cols].corr()

    for name, corr in [("raw_columns", corr_raw), ("engineered_features", corr_feat)]:
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr.columns)
        for i in range(len(corr.columns)):
            for j in range(len(corr.columns)):
                ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
        fig.colorbar(im, ax=ax, shrink=0.8)
        ax.set_title(f"Correlation matrix — {name}")
        fig.tight_layout()
        fig.savefig(FIG_DIR / f"eda_correlation_{name}.png", dpi=150)
        plt.close(fig)

    return corr_raw, corr_feat


def distribution_plots(feats: pd.DataFrame):
    cols = ["attendance_pct", "study_hours", "previous_score", "failures"]
    fig, axes = plt.subplots(1, len(cols), figsize=(4 * len(cols), 3.5))
    for ax, col in zip(axes, cols):
        ax.hist(feats[col], bins=20, color="#4C72B0", edgecolor="white")
        ax.set_title(col)
    fig.suptitle(f"SARAH feature distributions (n={len(feats)})")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "eda_distributions.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(4, 3.5))
    feats["risk_label"].value_counts().plot(kind="bar", ax=ax, color=["#4C72B0", "#C44E52"])
    ax.set_title("Risk label class balance")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "eda_class_balance.png", dpi=150)
    plt.close(fig)


def outlier_check(feats: pd.DataFrame):
    cols = ["attendance_pct", "study_hours", "previous_score", "failures"]
    fig, axes = plt.subplots(1, len(cols), figsize=(4 * len(cols), 3.5))
    summary = {}
    for ax, col in zip(axes, cols):
        q1, q3 = feats[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_outliers = int(((feats[col] < lower) | (feats[col] > upper)).sum())
        summary[col] = {"lower": round(float(lower), 2), "upper": round(float(upper), 2), "n_outliers": n_outliers}
        ax.boxplot(feats[col], vert=True)
        ax.set_title(f"{col}\n({n_outliers} IQR outliers)")
    fig.suptitle("Outlier check (IQR method, 1.5x whiskers)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "eda_outliers.png", dpi=150)
    plt.close(fig)
    return summary


def write_findings_md(corr_raw, corr_feat, outlier_summary, n_rows):
    g1_g3 = round(float(corr_raw.loc["G1", "G3"]), 2)
    g2_g3 = round(float(corr_raw.loc["G2", "G3"]), 2)
    risk_corr = corr_feat["risk"].drop("risk").sort_values()

    lines = [
        "# SARAH — EDA Findings\n",
        f"Generated from `eda.py` against the dataset in `project/data` ({n_rows} rows).\n",
        "## 1. Correlation check\n",
        f"G1 vs G3 correlation: {g1_g3}. G2 vs G3 correlation: {g2_g3}.\n",
        "This is why G3 is excluded as a model feature and used only to build the risk "
        "label: including something this strongly tied to G3 would leak the answer into "
        "the model.\n",
        "Correlation of each engineered feature with risk (1 = High Risk):\n",
    ]
    for feat, val in risk_corr.items():
        lines.append(f"- `{feat}`: {round(float(val), 2)}")
    lines.append("\n## 2. Outlier check (IQR method)\n")
    lines.append("| Feature | Bounds | Flagged | Decision |")
    lines.append("|---|---|---|---|")
    for feat, s in outlier_summary.items():
        lines.append(f"| {feat} | [{s['lower']}, {s['upper']}] | {s['n_outliers']} | Kept — see reasoning below |")
    lines.append(
        "\n**Decision: no rows or values were removed.** Unusual attendance/study/score "
        "values are exactly the signal an early-warning system needs to catch, not noise "
        "to clean away. IQR bounds are especially unreliable for `study_hours` and "
        "`failures`, which only take a few discrete values.\n"
    )
    lines.append("## 3. Final feature list\n")
    lines.append(
        "`attendance_pct`, `study_hours`, `previous_score`, `failures` — confirmed, no "
        "feature dropped.\n"
    )

    with open(DOCS_DIR / "eda_findings.md", "w") as f:
        f.write("\n".join(lines))


def main():
    raw = load_raw_uci(DATA_DIR)
    feats = engineer_features(raw)

    corr_raw, corr_feat = correlation_check(raw, feats)
    distribution_plots(feats)
    outlier_summary = outlier_check(feats)
    write_findings_md(corr_raw, corr_feat, outlier_summary, len(feats))

    print(f"Done. {len(feats)} rows processed.")
    print(f"Figures -> {FIG_DIR}")
    print(f"Findings -> {DOCS_DIR / 'eda_findings.md'}")


if __name__ == "__main__":
    main()