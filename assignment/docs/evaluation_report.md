# SARAH — Model Evaluation Report

Dataset: UCI Student Performance, **Math course only** (student-mat.csv, n=395). See `docs/CLASS_IMBALANCE_NOTE.md` for the class-imbalance and Portuguese-subset comparison.

**Evaluation procedure:** a stratified 20% test set (79 students) was reserved from the full 395 *before* any model selection, using the same split for all three setups below. Every cross-validation score in this report (depth selection and the 12-combination table) uses only the remaining 316 development students -- the reserved test students are never part of any fold used to pick a technique, a class_weight, or the shared Decision Tree depth. The 'Held-out test results' section at the end is the only place the reserved students are used, and each setup's selected model sees them exactly once, after selection is finalised.

## Decision Tree depth selection (development data only)

One fixed depth is used across all 12 combinations below, for a fair comparison. Chosen via 5-fold CV recall on Early-Warning development data, class_weight='balanced':

| max_depth | High-Risk recall (5-fold CV mean) |
|---|---|
| 2 | 0.365 |
| 3 | 0.367 |
| 4 | 0.482 **← selected** |
| 5 | 0.404 |
| 6 | 0.395 |
| None | 0.462 |

## The 12-combination comparison (5-fold CV on development data only)

3 setups × 2 techniques × 2 class_weight settings. Confirmatory mode has two setups because a tutor may have only G1, or both G1 and G2 -- each is a separately trained model, not one model asked to handle both cases (see module docstring). This grew the comparison from the original 8 rows to 12 once the team agreed G1-only needed its own trained-and-evaluated model, not just an extrapolated prediction from the G1+G2 model.

| Setup | Technique | class_weight | Accuracy | Precision (High Risk) | Recall (High Risk) | F1 (High Risk) |
|---|---|---|---|---|---|---|
| early_warning | Logistic Regression | None | 0.696 | 0.7 | 0.212 | 0.311 |
| early_warning | Logistic Regression | balanced | 0.7 | 0.573 | 0.397 | 0.454 |
| early_warning | Decision Tree (depth=4) | None | 0.703 | 0.657 | 0.299 | 0.4 |
| early_warning | Decision Tree (depth=4) | balanced | 0.617 | 0.422 | 0.482 | 0.444 |
| confirmatory_g1 | Logistic Regression | None | 0.855 | 0.776 | 0.79 | 0.78 |
| confirmatory_g1 | Logistic Regression | balanced | 0.829 | 0.707 | 0.838 | 0.765 |
| confirmatory_g1 | Decision Tree (depth=4) | None | 0.839 | 0.818 | 0.646 | 0.719 |
| confirmatory_g1 | Decision Tree (depth=4) | balanced | 0.798 | 0.663 | 0.838 | 0.728 |
| confirmatory_g1_g2 | Logistic Regression | None | 0.889 | 0.832 | 0.828 | 0.829 |
| confirmatory_g1_g2 | Logistic Regression | balanced | 0.864 | 0.745 | 0.904 | 0.815 |
| confirmatory_g1_g2 | Decision Tree (depth=4) | None | 0.893 | 0.824 | 0.857 | 0.839 |
| confirmatory_g1_g2 | Decision Tree (depth=4) | balanced | 0.87 | 0.766 | 0.876 | 0.814 |

## Selected combination per setup (development CV -- used to choose, not to report final performance)

- **early_warning**: Decision Tree (depth=4), class_weight=balanced — development recall 0.482, F1 0.444 (5-fold CV mean)
- **confirmatory_g1**: Logistic Regression, class_weight=balanced — development recall 0.838, F1 0.765 (5-fold CV mean)
- **confirmatory_g1_g2**: Logistic Regression, class_weight=balanced — development recall 0.904, F1 0.815 (5-fold CV mean)

Selection criterion (same throughout this project): highest recall on the High Risk class, since a missed at-risk student (false negative) is costlier for an early-warning system than a false alarm (false positive).

## Held-out test results (reserved students, never used in selection above)

- **early_warning** (Decision Tree (depth=4), class_weight=balanced): accuracy 0.633, precision 0.44, recall 0.423, F1 0.431 — `docs/figures/confusion_early_warning.png` (26 High Risk / 79 total)
- **confirmatory_g1** (Logistic Regression, class_weight=balanced): accuracy 0.823, precision 0.714, recall 0.769, F1 0.741 — `docs/figures/confusion_confirmatory_g1.png` (26 High Risk / 79 total)
- **confirmatory_g1_g2** (Logistic Regression, class_weight=balanced): accuracy 0.899, precision 0.821, recall 0.885, F1 0.852 — `docs/figures/confusion_confirmatory_g1_g2.png` (26 High Risk / 79 total)

## Accuracy-vs-earliness tradeoff

Early-Warning setup (without assessment grades): development recall 0.482. Confirmatory (G1+G2) setup: development recall 0.904. This is a limitation observed in our current experiments, not a proven irreducible limit: Early-Warning mode predicts without assessment grades, using only attendance, study habits, and past failures, so weaker results here are expected given the narrower feature set -- but these results do not prove that better Early-Warning performance is impossible with more data or features. SARAH defaults to Early-Warning mode regardless, since catching risk earlier -- even less accurately -- is the point of an early-warning system; Confirmatory mode is available as a second look once grades exist. This dataset has no week-by-week records, so these results do not establish day-one or week-specific accuracy.

## Feature statistics (Confirmatory G1+G2 development split, used for recommendation z-scores)

```json
{
  "attendance_pct": {
    "mean": 81.569,
    "std": 21.528
  },
  "study_hours": {
    "mean": 4.097,
    "std": 2.811
  },
  "failures": {
    "mean": 0.335,
    "std": 0.753
  },
  "previous_score": {
    "mean": 54.035,
    "std": 17.154
  }
}
```
