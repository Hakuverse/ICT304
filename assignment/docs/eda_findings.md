# SARAH � EDA Findings

Generated from `eda.py` against the dataset in `assignment/data` (395 rows).

## 1. Correlation check

G1 vs G3 correlation: 0.8. G2 vs G3 correlation: 0.9.

This is why G3 is excluded as a model feature and used only to build the risk label: including something this strongly tied to G3 would leak the answer into the model.

Correlation of each engineered feature with risk (1 = High Risk):

- `previous_score`: -0.72
- `study_hours`: -0.08
- `attendance_pct`: -0.08
- `failures`: 0.34

## 2. Outlier check (IQR method)

| Feature | Bounds | Flagged | Decision |
|---|---|---|---|
| attendance_pct | [33.25, 140.05] | 15 | Kept � see reasoning below |
| study_hours | [-1.5, 6.5] | 92 | Kept � see reasoning below |
| previous_score | [8.75, 98.75] | 0 | Kept � see reasoning below |
| failures | [0.0, 0.0] | 83 | Kept � see reasoning below |

**Decision: no rows or values were removed.** Unusual attendance/study/score values are exactly the signal an early-warning system needs to catch, not noise to clean away. IQR bounds are especially unreliable for `study_hours` and `failures`, which only take a few discrete values.

## 3. Final feature list

`attendance_pct`, `study_hours`, `previous_score`, `failures` � confirmed, no feature dropped.
