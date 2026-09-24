# SARAH — Model Evaluation Report

Dataset: UCI Student Performance, **Math course only** (student-mat.csv, n=395). See `docs/CLASS_IMBALANCE_NOTE.md` for the class-imbalance and Portuguese-subset comparison.

## Decision Tree depth selection

One fixed depth is used across all 8 combinations below, for a fair comparison. Chosen via 5-fold CV recall on Early-Warning mode, class_weight='balanced':

| max_depth | High-Risk recall (5-fold CV mean) |
|---|---|
| 2 | 0.446 |
| 3 | 0.477 |
| 4 | 0.477 |
| 5 | 0.462 |
| 6 | 0.477 |
| None | 0.492 **← selected** |

## The 8-combination comparison (5-fold stratified cross-validation)

2 modes × 2 techniques × 2 class_weight settings. Metrics are the mean across 5 folds of the whole 395-student dataset (not a single train/test split -- with only 130 High Risk students, a single 80/20 split leaves too few High Risk examples in the test set for a stable estimate).

| Mode | Technique | class_weight | Accuracy | Precision (High Risk) | Recall (High Risk) | F1 (High Risk) |
|---|---|---|---|---|---|---|
| early_warning | Logistic Regression | None | 0.716 | 0.704 | 0.246 | 0.361 |
| early_warning | Logistic Regression | balanced | 0.711 | 0.611 | 0.408 | 0.48 |
| early_warning | Decision Tree (depth=None) | None | 0.681 | 0.533 | 0.315 | 0.393 |
| early_warning | Decision Tree (depth=None) | balanced | 0.552 | 0.371 | 0.492 | 0.419 |
| confirmatory | Logistic Regression | None | 0.876 | 0.825 | 0.792 | 0.806 |
| confirmatory | Logistic Regression | balanced | 0.871 | 0.756 | 0.9 | 0.821 |
| confirmatory | Decision Tree (depth=None) | None | 0.851 | 0.787 | 0.754 | 0.768 |
| confirmatory | Decision Tree (depth=None) | balanced | 0.848 | 0.762 | 0.785 | 0.772 |

## Selected combination per mode

- **early_warning**: Decision Tree (depth=None), class_weight=balanced — recall 0.492, F1 0.419 (5-fold CV mean)
- **confirmatory**: Logistic Regression, class_weight=balanced — recall 0.9, F1 0.821 (5-fold CV mean)

Selection criterion (same throughout this project): highest recall on the High Risk class, since a missed at-risk student (false negative) is costlier for an early-warning system than a false alarm (false positive).

## Accuracy-vs-earliness tradeoff

Early-Warning mode (no grades, available before any assessment exists): recall 0.492. Confirmatory mode (adds previous_score once G1/G2 exist): recall 0.9. This is the core tradeoff SARAH makes explicit: Early-Warning mode is what actually lets a tutor intervene before it's too late, at whatever accuracy cost that involves; Confirmatory mode is more accurate but only available once it's partly too late to act on the 'early' half of 'early warning'. SARAH defaults to Early-Warning mode for this reason, with Confirmatory available for a second look once grades exist.

## Holdout confusion matrices (80/20 split, best combination per mode)

- **early_warning**: `docs/figures/confusion_early_warning.png` (Decision Tree (depth=None), class_weight=balanced, 26 High Risk / 79 total in the holdout test set)
- **confirmatory**: `docs/figures/confusion_confirmatory.png` (Logistic Regression, class_weight=balanced, 26 High Risk / 79 total in the holdout test set)

## Feature statistics (Confirmatory-mode train split, used for recommendation z-scores)

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