# SARAH — System Design (Sprint backlog: write the System Design section)

Ready to paste into report Section 5 ("System Overview: Subsystems, Workflow & Test Plan"). This
expands the template's bare bones with content that's actually true of the built prototype —
copy the prose in, adjust tone if you want it to sound less like a doc and more like your team's
voice, but keep the facts as they are (they're pulled straight from the code and evaluation
report).

## 5.1 System flow

A tutor first chooses a **mode** — Early-Warning (no grades needed yet) or Confirmatory (recent
assessment scores available) — then enters a student's information either one at a time
(individual entry, via form fields) or as a whole class at once (bulk entry, by uploading a CSV
roster). Both paths converge on the same pipeline: the raw input is cleaned, scaled, and converted
into the feature set for the chosen mode (data processing); the mode's trained classifier
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
Student data (attendance, study hours, past failures, [assessment score if Confirmatory])
        │
        ▼
Data processing — cleaning, scaling, feature engineering (mode-specific schema)
        │
        ▼
AI Prediction Model — Logistic Regression / Decision Tree (one trained model per mode)
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

A rendered, colour-coded version of this diagram (with each stage labelled by which sub-system
owns it) is in `docs/diagrams/system_flow.md` — screenshot the GitHub-rendered version for the
report rather than retyping the diagram as an image.

### 5.1.1 Inputs and outputs, by mode

| | Early-Warning Mode | Confirmatory Mode |
|---|---|---|
| **When a tutor uses it** | Any time — day one of term, no grades needed | Once at least one assessment/grade exists |
| **Inputs** | Attendance %, study hours/week, past failures (3 fields) | Same, **plus** recent average assessment score % (4 fields) |
| **Output** | Low Risk / High Risk label, a confidence %, and (if High Risk) the weakest factor among attendance, study hours, or past failures | Low Risk / High Risk label, a confidence %, and (if High Risk) the weakest factor among attendance, study hours, or recent assessment score |
| **Accuracy (High-Risk recall, 5-fold CV)** | 0.492 | 0.9 |

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
  per file: `data_processing.validate_students()` checks every row against
  `FEATURE_VALID_RANGES`, and any row that fails is **skipped and reported**, not silently scored
  or allowed to crash the whole batch. The tutor sees exactly which student(s) were skipped and
  why (e.g. "attendance_pct is missing", "study_hours=999.0 is outside the valid range [0, 40]"),
  and the rest of the class is still scored normally. This is covered by an automated test
  (`test_validate_students_catches_missing_and_invalid_rows`).

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
| Risk Prediction Model | **AI** | Two trained classifiers, one per mode (Logistic Regression compared against a Decision Tree for each), that take that mode's processed features (3 for Early-Warning, 4 for Confirmatory) and predict Low Risk or High Risk with a confidence score | `assignment/code/train_models.py`, `assignment/models/` |
| Recommendation / Intervention Engine | Non-AI (rule-based) | For any student predicted High Risk, computes how far each feature sits from the training-set average (z-score) and identifies the weakest factor, then returns a targeted recommendation text | `assignment/code/recommend.py` |
| Batch Roster Processor + Dashboard | Non-AI | Accepts either a single-student form entry or a CSV upload of a whole class roster, runs every student through the selected mode's pipeline, and displays a sorted risk table (whole class) or a single detailed result (one student), with a sidebar toggle to switch mode | `assignment/app/dashboard.py`, `assignment/code/predict.py` |

**Why the Recommendation Engine is non-AI, deliberately:** the brief asks for at least one
non-AI sub-system, and a rule-based weakest-factor lookup is the right tool for this job anyway —
it needs to be transparent and easy for a tutor to trust ("this student is flagged mainly because
of attendance"), not a second black-box model. It also stays cheap to run and re-run, with no
separate training step of its own, and never contradicts itself between runs.

## 5.3 How the sub-systems connect (data contract)

- **Dashboard → Data processing:** raw fields for the selected mode (attendance, study hours,
  failures, and — Confirmatory Mode only — recent assessment score) are validated and converted
  into the exact feature columns that mode's model expects (`EARLY_WARNING_FEATURES` /
  `CONFIRMATORY_FEATURES` in `assignment/code/data_processing.py`).
- **Data processing → Risk Prediction Model:** the processed features are passed straight into
  `model.predict()` / `model.predict_proba()`; Logistic Regression additionally scales them first
  (`StandardScaler` inside its pipeline), the Decision Tree does not need scaling.
- **Risk Prediction Model → Recommendation Engine:** the engine receives the *raw* (unscaled)
  feature values, the predicted label, and the active mode, and only runs its weakest-factor
  analysis when the label is High Risk (a Low Risk student gets a "no urgent intervention"
  message, not a forced recommendation — see `test_low_risk_gives_no_intervention_message` in the
  test suite).
- **Recommendation Engine → Dashboard:** returns a small structured result (predicted label,
  confidence, weakest actionable factor, recommendation text) that the dashboard renders per
  student, and aggregates into the sorted class-wide table for the bulk-upload path.

## 5.4 Model selection (feeds into Section 6, AI Technique Comparison)

Both models, for both modes, are compared using **stratified 5-fold cross-validation** on the
full dataset (`random_state=42`) — not a single train/test split, since with only 395 students
(130 High Risk) a single 80/20 split would leave too few High Risk examples in the test set for a
stable estimate. The Decision Tree's `max_depth` was checked via 5-fold CV recall on Early-Warning
mode (depths 2, 3, 4, 5, 6, unlimited); with only 3-4 features, an unrestricted tree performed
best, so no depth cap is applied. Every combination of mode × technique × `class_weight` (8 total)
is compared; full table and reasoning in `docs/CLASS_IMBALANCE_NOTE.md`. Selected combination per
mode (5-fold CV means):

| Mode | Model | Accuracy | Precision (High Risk) | Recall (High Risk) | F1 (High Risk) |
|---|---|---|---|---|---|
| Early-Warning | Decision Tree, class_weight=balanced | 0.552 | 0.371 | 0.492 | 0.419 |
| Confirmatory | Logistic Regression, class_weight=balanced | 0.871 | 0.756 | 0.9 | 0.821 |

**Selected per mode on highest recall on the High Risk class** — in an early-warning system, a
missed at-risk student (false negative) is a worse outcome than a false alarm (false positive), so
recall on the minority class is the deciding metric rather than raw accuracy. Note Early-Warning
mode's numbers are honestly weak (0.552 accuracy, 0.371 precision) — a direct, reported
consequence of the team's decision to keep the feature list to just three individually-weak
columns (`docs/feature_selection.md`); this is discussed openly in Section 5.5 rather than
smoothed over. Full numbers, depth-selection trials, and confusion matrices regenerate
automatically at `docs/evaluation_report.md` and `docs/figures/confusion_*.png` every time
`python assignment/code/train_models.py` runs.

## 5.5 The accuracy-vs-earliness tradeoff

Early-Warning Mode's recall (0.492) is far lower than Confirmatory Mode's (0.9) — a direct,
honestly-reported consequence of predicting risk before any grade exists, using only attendance,
study habits, and past failures instead of the far stronger `previous_score` predictor
(correlation -0.72 with risk, versus -0.08 for attendance and study hours individually — see
`docs/eda_findings.md`). SARAH treats this as the core design tradeoff, not a flaw to hide:
Early-Warning Mode is the system's **primary, default mode** because catching risk earlier — even
less accurately — is the entire point of an early-warning system, while Confirmatory Mode stays
available as a more accurate second look once grades exist. Full discussion:
`docs/CLASS_IMBALANCE_NOTE.md` §8.

## 5.6 What this replaces in the report template

This content replaces/fills report template Section 5 (`5.1 System flow`, `5.2 Sub-systems`) and
supplies the numbers that Section 6's `[TEAM TODO]` was waiting on (the model comparison table,
now per-mode). Section 5.3 (Test plan) is handled separately in `docs/TEST_PLAN.md` (issue #27),
which this document links to. **Note:** issue #21's checklist also references "the evaluation
plan from #18" — that is a separate, not-yet-completed sprint item (how the team decided to test
the models, as opposed to the test *results* in `docs/TEST_PLAN.md`); this document does not
cover it, since it wasn't part of what #21/#27 asked to be fixed here.

