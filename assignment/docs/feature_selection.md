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

| Feature | Source column(s) | Correlation with risk | Why kept |
|---|---|---|---|
| `attendance_pct` | `absences` | -0.08 to -0.11 (weak alone) | Explicitly promised in the problem statement; combines usefully with other features in the Decision Tree even though its solo correlation is weak |
| `study_hours` | `studytime` | -0.08 to -0.10 (weak alone) | Same as above |
| `previous_score` | `G1`, `G2` | -0.67 to -0.72 (strong) | Strongest individual predictor found |
| `failures` | `failures` | +0.34 to +0.37 (moderate) | Second-strongest predictor; directly reflects prior academic difficulty |

`G3` is excluded from features entirely (see `eda_findings.md` — G1/G2 correlate 0.8-0.9
with it, so using it as an input would leak the label).

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

Final feature list is unchanged from `eda_findings.md`: `attendance_pct`, `study_hours`,
`previous_score`, `failures`. No further columns from the raw dataset are added.