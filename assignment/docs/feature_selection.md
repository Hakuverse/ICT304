# SARAH — Feature Selection

## Candidate features considered

The UCI Student Performance dataset provides 30+ raw columns per student, covering
academics (G1, G2, G3, studytime, failures, absences), demographics (sex, age, address,
famsize, Pstatus), family background (Medu, Fedu, Mjob, Fjob, guardian), lifestyle
(traveltime, freetime, goout, Dalc, Walc, health, romantic, internet, activities), and
school-support flags (schoolsup, famsup, paid, nursery, higher).

## Selection criteria

A candidate feature was kept only if it satisfied **both**:

1. **In scope** — it matches something SARAH's problem statement actually promises to
   collect from a tutor: attendance, study hours, assessment/test performance, and
   previous grades. A tutor entering a student into SARAH does not have (and should not
   need) that student's family background or personal life to get a risk prediction.
2. **Evidenced** — it shows a real, non-leaked relationship with academic risk, checked
   in `eda_findings.md`'s correlation analysis.

## Final selected features

The two approved modes use these exact model inputs, in this order:

| Mode | Model inputs |
|---|---|
| `early_warning` | `attendance_pct`, `study_hours`, `failures` |
| `confirmatory` | `attendance_pct`, `study_hours`, `failures`, `previous_score` |

No demographics or family-background fields are included. `previous_score` is the
average of G1 and G2, rescaled to 0-100, so both grades are needed for that calculation.
Neither mode needs G3 to prepare a prediction input. The attendance value is a capped
absence-based estimate, not a measured attendance percentage. Study hours are estimates
from categories; 12 hours for the open-ended top category is an assumption.

| Feature | Source column(s) | Correlation with risk | Why kept |
|---|---|---|---|
| `attendance_pct` | `absences` | -0.08 (weak alone) | Relevant to the intended teacher workflow; usefulness alongside other inputs still needs model testing |
| `study_hours` | `studytime` | -0.08 (weak alone) | Relevant to study support; usefulness still needs model testing |
| `previous_score` | `G1`, `G2` | -0.72 (strong) | Strongest individual relationship found; Confirmatory only |
| `failures` | `failures` | +0.34 (moderate) | Reflects prior academic difficulty |

These rounded values come from the Math-only [EDA findings](eda_findings.md).
`G3` is excluded because it defines the target (`G3 < 10`), not simply because it is
correlated with other grades. `risk`, `risk_label` and `course` are also excluded from X.

## Explicitly rejected candidates and why

- **Demographic/family background** (`sex`, `age`, `address`, `famsize`, `Pstatus`,
  `Medu`, `Fedu`, `Mjob`, `Fjob`, `guardian`): out of scope, and risks encoding unfair
  bias into an academic risk score based on background rather than behaviour.
- **Lifestyle/personal** (`Dalc`, `Walc`, `romantic`, `health`, `freetime`, `goout`):
  same reasoning — sensitive personal information a tutor shouldn't need to supply, and
  not part of SARAH's stated data collection.
- **School-support flags** (`schoolsup`, `famsup`, `paid`, `nursery`, `activities`,
  `internet`, `higher`, `traveltime`): plausible future extensions, but out of scope for
  this prototype; not investigated in this sprint.

## Conclusion

Use three inputs for Early-Warning and add `previous_score` for Confirmatory.
Math-only loading is fixed: adding `student-por.csv` does not change the training data.
The dataset does not establish when every input was measured, so grade-free inputs alone
do not prove that this prototype works on day one of a term.

## Using the code

See [the mode guide](mode-guide.md) for run commands and examples. Training code can use
`build_training_xy(data_dir, mode)` to get inputs and labels separately. The existing
`engineer_features()` function remains available for the four-feature EDA charts.
