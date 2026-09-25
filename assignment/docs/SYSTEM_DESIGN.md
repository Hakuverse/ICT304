# SARAH — System Design (Sprint backlog: write the System Design section)

Ready to paste into report Section 5 ("System Overview: Subsystems, Workflow & Test Plan"). This
expands the template's bare bones with content that's actually true of the built prototype —
copy the prose in, adjust tone if you want it to sound less like a doc and more like your team's
voice, but keep the facts as they are (they're pulled straight from the code and evaluation
report).

## 5.1 System flow

A tutor first chooses a **mode** — Early-Warning (no grades needed yet) or Confirmatory (at
least one assessment score available) — then enters a student's information either one at a time
(individual entry, via form fields) or as a whole class at once (bulk entry, by uploading a CSV
roster). Confirmatory Mode itself has two cases, each served by its own separately trained
model: a student with only a first assessment score (G1) is predicted by the G1-only model, and
a student with both a first and second assessment score (G1+G2 average) is predicted by the
G1+G2 model — the system routes automatically based on which grades are supplied (see 5.1.1).
Both paths converge on the same pipeline: the raw input is cleaned, scaled, and converted
into the feature set for the chosen setup (data processing); that setup's trained classifier
predicts Low Risk or High Risk for each student (AI prediction); a rule-based engine looks at
*why* that student is High Risk and picks the single weakest **actionable** factor
(recommendation); and the dashboard displays the result — a sorted, colour-coded table for a
whole roster, or a single result with an explanation for one student — for the tutor to act on.
SARAH never contacts a student or takes any action itself; the tutor always makes the final call
(see the README's "Human-in-the-loop by design" section).

```
Tutor selects mode: Early-Warning (no grades) or Confirmatory (grades available)
        │
        ▼
Student data (attendance, study hours, past failures, [G1, and G2 if available, if Confirmatory])
        │
        ▼
Data processing — cleaning, scaling, feature engineering (setup-specific schema)
        │
        ▼
AI Prediction Model — Logistic Regression / Decision Tree (one trained model per setup: Early-Warning, Confirmatory G1-only, Confirmatory G1+G2)
        │
        ▼
Risk Classification: LOW RISK or HIGH RISK
        │
        ▼
Rule-based Recommendation Engine — weakest ACTIONABLE-factor analysis
        │
        ▼
Tutor Dashboard — display + human decision
```

Jackie's architecture diagram is in [the figures folder](figures/SARAH_system_architecture.drawio.png).
Check its labels against the current three model setups before putting it in the report.

### 5.1.1 Inputs and outputs, by setup

| | Early-Warning Mode | Confirmatory Mode — G1 only | Confirmatory Mode — G1+G2 |
|---|---|---|---|
| **When a tutor uses it** | Any time — no assessment grades needed | Once the first assessment (G1) exists | Once both the first and second assessments (G1, G2) exist |
| **Inputs** | Attendance estimate, study hours/week, past failures | Same, plus G1 entered on the 0-20 scale | Same, plus G1 and G2 each entered on the 0-20 scale |
| **Output** | Low Risk / High Risk label, a confidence %, and (if High Risk) the weakest factor among attendance, study hours, or past failures | Low Risk / High Risk label, a confidence %, and (if High Risk) the weakest factor among attendance, study hours, or G1 score | Low Risk / High Risk label, a confidence %, and (if High Risk) the weakest factor among attendance, study hours, or G1+G2 average score |
| **High-Risk recall (held-out test set)** | 0.423 | 0.769 | 0.885 |

The code converts G1 or the G1/G2 average to a 0-100 `previous_score` internally.
Tutors supply grades out of 20, not percentages.

A student with only G1 is always scored by the G1-only model, never the G1+G2 model — each
model only ever sees the kind of input it was actually trained on. A supplied G2 that isn't a
usable number (out of range, or not numeric) is treated as invalid and reported to the tutor; it
is never silently ignored and quietly downgraded to the G1-only model.

**On the "day one" framing:** Early-Warning Mode working without assessment grades is real and
tested. What the current evaluation does *not* establish is accuracy at a specific point in the
term (day one, week three, etc.) — the dataset provides an absence count and a study-time
category, not week-by-week records, so there is no way to test performance tied to a particular
week. The supported claim is that the model predicts without assessment grades; the data
does not establish performance before the first assessment or in a particular week.

SARAH's feature list is deliberately this narrow — team decision, see `docs/feature_selection.md`
— no demographic, family-background, or lifestyle columns, even though the raw UCI dataset has
them available.

### 5.1.2 Entering data: one student, or a whole class

- **Individual entry:** the tutor fills in a form (dashboard sliders / CLI flags) for one
  student, providing all fields required for the selected mode.
- **Bulk entry (CSV upload):** the tutor uploads a spreadsheet of a whole class. SARAH first
  checks the CSV has every required **column** for the selected mode — if a column is missing
  entirely, it stops and tells the tutor which column(s), rather than guessing.
- **Missing or invalid data within a CSV** (a blank cell, a typo, or a value outside a sane range
  — e.g. `attendance_pct = 150`, or text where a number is expected) is handled per **row**, not
  per file: `predict.predict_roster()` validates each row (via `data_processing.prepare_model_inputs()`'s
  range checks), and any row that fails is **skipped and reported**, not silently scored or
  allowed to crash the whole batch. The tutor sees exactly which student(s) were skipped and why
  (e.g. "attendance_pct is missing", "study_hours must be 0 to 40"), and the rest of the class is
  still scored normally. For Confirmatory Mode specifically: G1 is required, G2 is optional — a
  row missing G1 is skipped and reported ("Confirmatory mode needs at least G1"), and a row with
  an invalid supplied G2 is skipped and reported too, never silently treated as "G2 absent."
  This is now covered by automated tests in `assignment/code/test_predict.py`
  (`TestPredictRoster`), which check both the Early-Warning skip-invalid-rows behaviour
  (including the inclusive 0–40 study-hours boundary) and the Confirmatory routing/invalid-G2
  behaviour described above.

### 5.1.3 Attendance and study hours are estimates, not measurements

Worth stating plainly, since it affects how confidently the report can talk about these numbers:
`attendance_pct` is not a direct measurement from an attendance-tracking system — it is
**derived** from the UCI dataset's `absences` count (capped at 30, then rescaled), and in a real
deployment would similarly be computed from whatever absence records exist, not read off a
sensor. `study_hours` is derived from a **4-category bucket** (`studytime` — "<2 hrs", "2-5",
"5-10", ">10 hrs/week") converted to each bucket's midpoint (1.5 / 3.5 / 7.5 / 12.0) — it is a
reasonable estimate representing a self-reported range, not an exact hours-per-week figure. SARAH
and its documentation should describe both as estimates throughout (report, README, dashboard
labels), never as precise measurements — see `assignment/code/data_processing.py`'s module docstring for the
full derivation of each.

## 5.2 Sub-systems

SARAH is split into three sub-systems, one AI and two non-AI, satisfying the brief's requirement
to identify at least one non-AI sub-system alongside the AI one.

| Sub-system | Type | Role | Where it lives |
|---|---|---|---|
| Risk Prediction Model | **AI** | Three trained classifiers, one per setup (Early-Warning, Confirmatory G1-only, Confirmatory G1+G2) — Logistic Regression compared against a Decision Tree for each — that take that setup's processed features (3 for Early-Warning, 4 for both Confirmatory setups) and predict Low Risk or High Risk with a confidence score | `assignment/code/train_models.py`, `assignment/models/` |
| Recommendation / Intervention Engine | Non-AI (rule-based) | For any student predicted High Risk, computes how far each feature sits from the training-set average (z-score) and identifies the weakest factor, then returns a targeted recommendation text | `assignment/code/recommend.py` |
| Batch Roster Processor + Dashboard | Non-AI | Accepts either a single-student form entry or a CSV upload of a whole class roster, runs every student through the selected mode's pipeline, and displays a sorted risk table (whole class) or a single detailed result (one student), with a sidebar toggle to switch mode | `assignment/app/dashboard.py`, `assignment/code/predict.py` |

**Implementation status:** as of this PR, only the Risk Prediction Model and the CSV/roster
prediction path (`predict.py`) are built and tested. The Recommendation Engine (`recommend.py`)
and the Dashboard (`dashboard.py`) are designed but not yet implemented — the paths listed above
are their planned locations, not evidence they currently exist.

**Why the Recommendation Engine is non-AI, deliberately:** the brief asks for at least one
non-AI sub-system, and a rule-based weakest-factor lookup is the right tool for this job anyway —
it needs to be transparent and easy for a tutor to trust ("this student is flagged mainly because
of attendance"), not a second black-box model. It also stays cheap to run and re-run, with no
separate training step of its own, and never contradicts itself between runs.

## 5.3 How the sub-systems connect (data contract)

- **Dashboard → Data processing:** raw fields for the selected mode (attendance, study hours,
  failures, and — Confirmatory Mode only — G1, and G2 if available) are validated and converted
  into the exact feature columns that setup's model expects (`EARLY_WARNING_FEATURES` /
  `CONFIRMATORY_FEATURES` in `assignment/code/data_processing.py`).
- **Confirmatory routing (G1-only vs G1+G2):** the system decides which of the two Confirmatory
  models to use per student based on whether a valid G2 was supplied — G1 alone routes to the
  G1-only model (`assignment/models/confirmatory_g1_model.joblib`), a valid G1+G2 pair routes to
  the G1+G2 model (`assignment/models/confirmatory_g1_g2_model.joblib`). Each model only ever
  sees the kind of input it was trained on (`predict.py`'s `load_model()`).
- **Data processing → Risk Prediction Model:** the processed features are passed straight into
  `model.predict()` / `model.predict_proba()` for both techniques. **Note:** the current
  implementation does not apply feature scaling (e.g. `StandardScaler`) before Logistic
  Regression — a known simplification, not yet accounting for scale differences between features
  like `attendance_pct` (0–100) and `failures` (0–3).
- **Risk Prediction Model → Recommendation Engine (planned):** the design is for the engine to
  receive the *raw* (unscaled) feature values, the predicted label, and the active mode, running
  its weakest-factor analysis only when the label is High Risk. Not yet implemented — see the
  "Implementation status" note above.
- **Recommendation Engine → Dashboard:** returns a small structured result (predicted label,
  confidence, weakest actionable factor, recommendation text) that the dashboard renders per
  student, and aggregates into the sorted class-wide table for the bulk-upload path.

## 5.4 Model selection (feeds into Section 6, AI Technique Comparison)

Every model is compared using **stratified 5-fold cross-validation on a development set** — not
the full dataset. Before any comparison or selection happens, a stratified 20% test set (79
students, `random_state=42`) is reserved from the full 395 and set aside; all cross-validation in
this section uses only the remaining 316 development students, so the reserved students never
influence which technique, `class_weight`, or Decision Tree depth gets chosen. This matters
because reusing the same students for both selection and final evaluation would make the final
numbers optimistically biased.

The Decision Tree's `max_depth` was checked via 5-fold CV recall on Early-Warning **development**
data only (depths 2, 3, 4, 5, 6, unlimited):

| max_depth | High-Risk recall (5-fold CV mean) |
|---|---|
| 2 | 0.365 |
| 3 | 0.367 |
| 4 | **0.482 ← selected** |
| 5 | 0.404 |
| 6 | 0.395 |
| None | 0.462 |

depth=4 is then reused as a fixed depth across every Decision Tree comparison below, for a fair
comparison. Every combination of setup × technique × `class_weight` (**3 setups × 2 techniques ×
2 settings = 12 total**) is compared on development data; full table and reasoning in
`docs/CLASS_IMBALANCE_NOTE.md`. There are 3 setups, not 2 modes, because Confirmatory Mode itself
splits into two separately trained models (G1-only, G1+G2) — see 5.1.1. Selected combination per
setup (5-fold CV means, development data):

| Setup | Model | Accuracy | Precision (High Risk) | Recall (High Risk) | F1 (High Risk) |
|---|---|---|---|---|---|
| Early-Warning | Decision Tree (depth=4), class_weight=balanced | 0.617 | 0.422 | 0.482 | 0.444 |
| Confirmatory — G1 only | Logistic Regression, class_weight=balanced | 0.829 | 0.707 | 0.838 | 0.765 |
| Confirmatory — G1+G2 | Logistic Regression, class_weight=balanced | 0.864 | 0.745 | 0.904 | 0.815 |

**Selected per setup on highest recall on the High Risk class** — in an early-warning system, a
missed at-risk student (false negative) is a worse outcome than a false alarm (false positive), so
recall on the minority class is the deciding metric rather than raw accuracy.

**These are development/selection scores, not the final reported performance.** Each selected
combination is then refit on the full 316-student development set and evaluated exactly once on
the 79 reserved, never-before-touched test students — the genuine, non-leaked result of that
check is the "High-Risk recall (held-out test set)" row in the 5.1.1 table above (0.423 / 0.769 /
0.885), with full numbers and confusion matrices in `docs/evaluation_report.md` and
`docs/figures/confusion_*.png`, regenerated every time `python assignment/code/train_models.py`
runs.

## 5.5 The accuracy-vs-earliness tradeoff

Early-Warning Mode's held-out recall (0.423) is far lower than Confirmatory Mode's (0.769 with G1
only, 0.885 with G1+G2) — a direct, honestly-reported difference observed when predicting risk without
assessment grades, using only attendance, study habits, and past failures instead of the far stronger
`previous_score` predictor (correlation -0.72 with risk, versus -0.08 for attendance and study
hours individually — see `docs/eda_findings.md`). SARAH treats this as the core design tradeoff,
not a flaw to hide: Early-Warning Mode is the system's **primary, default mode** because catching
risk earlier — even less accurately — is the entire point of an early-warning system, while
Confirmatory Mode (either setup) stays available as a more accurate second look once grades
exist. Full discussion: `docs/CLASS_IMBALANCE_NOTE.md` §8.

## 5.6 Where to use this in the report

Use this design in report Section 5, and the comparison results in Sections 6-7.
Benjamin's test-plan table (#27) is in [report section 8](../report/Document).
Jackie's earlier evaluation plan (#18) is in [Model Test plan](<Model Test plan>);
use the implemented split described above when reporting the current results.
