# SARAH — Class Imbalance & Class-Weight Comparison (Issue #19)

This note answers the sprint backlog item directly: it documents SARAH's class imbalance, and
compares `class_weight=None` against `class_weight="balanced"` across **all twelve combinations**
of setup × technique × class-weight setting. It's ready to paste into the report's pre-processing
/ methodology section, and anyone on the team can use it to defend the decision in a viva or demo.

## 1. The dataset and the imbalance

SARAH's dataset is the UCI "Student Performance" dataset, **Math course only**
(`student-mat.csv`, n=395). The Portuguese subset (n=649) was checked and rejected: its High
Risk / Low Risk split is worse (100 / 549, ~15%/85%) with a smaller absolute High Risk count
despite the larger total N — less signal for the model to learn the minority class from.

With `risk = 1` if the final grade `G3 < 10` (the standard pass mark out of 20):

| Class | Count | % of dataset |
|---|---|---|
| High Risk | **130** | **32.9%** |
| Low Risk | **265** | **67.1%** |
| Total | 395 | 100% |

This is a real but moderate imbalance (roughly 1:2), not an extreme one. It still matters: a
model that predicts "Low Risk" for every single student gets 67.1% accuracy for free, without
learning anything about what actually makes a student at-risk — which is exactly why every result
in this project is reported on Precision/Recall/F1 for the High Risk class, never on accuracy
alone.

## 2. Three setups, four features total — why this comparison has twelve combinations, not two

SARAH runs in two **modes**, because the data actually available about a student changes over the
term — but Confirmatory Mode itself splits into two separately trained **setups** (G1 alone, or
G1+G2 averaged), giving three setups in total. Its feature list is deliberately narrow — just
four columns total, team decision (see `docs/feature_selection.md`): no demographic,
family-background, or lifestyle data, even though the raw dataset has it available.

- **Early-Warning Mode** (primary): `attendance_pct`, `study_hours`, `failures` — everything
  SARAH can know before any assessment exists. (The dataset provides absence counts and a
  study-time category, not week-by-week records, so this does not establish accuracy at a
  specific point in the term, such as "day one.")
- **Confirmatory Mode — G1 only**: Early-Warning features **+** `previous_score` derived from G1
  alone, once the first assessment exists.
- **Confirmatory Mode — G1+G2**: Early-Warning features **+** `previous_score` derived from the
  average of G1 and G2, once both assessments exist.

G1 is required for Confirmatory Mode; G2 is optional. Which of the two Confirmatory setups a
student is scored with is decided automatically by whether a valid G2 was supplied — a student
with only G1 is routed to the G1-only model, a student with both is routed to the G1+G2 model,
and each model only ever sees the kind of input it was actually trained on (never one model asked
to handle both patterns — see `assignment/code/predict.py`'s module docstring). A supplied G2
that isn't a usable number (out of range, or not numeric) is reported as invalid, never silently
treated as "G2 absent."

All three setups are trained and compared with **both** AI techniques (Logistic Regression,
Decision Tree) and **both** `class_weight` settings (`None`, `"balanced"`) — **3 setups × 2
techniques × 2 settings = 12 combinations**, each evaluated the same way (Section 4).

## 3. What `class_weight="balanced"` actually does

```python
LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000)
DecisionTreeClassifier(class_weight="balanced", random_state=42)
```

scikit-learn's `class_weight="balanced"` re-weights the training loss so mistakes on the
**minority class (High Risk)** count for more than mistakes on the majority class (Low Risk), in
inverse proportion to how often each class appears (roughly `265/130 ≈ 2.0×` here). This pushes
the model to actually learn the boundary between the two groups instead of defaulting toward the
majority class. We did not use oversampling (e.g. SMOTE) or undersampling, because `class_weight`
needs no extra library or synthetic rows, is simpler to reproduce, and is the standard first
approach for an imbalance at this level (not extreme).

## 4. Method: a reserved held-out test set, plus stratified 5-fold cross-validation for selection

With only 395 students (130 High Risk), a single 80/20 train/test split would leave roughly 26
High Risk students in the test set — too few for a stable precision/recall estimate on its own.
So a stratified 20% test set (79 students, `random_state=42`) is reserved from the full 395
**once, before any model selection happens**, and every combination below is evaluated on the
remaining 316 development students only, using **stratified 5-fold cross-validation**
(`StratifiedKFold`, shuffled, `random_state=42`): the development set is split into 5 folds
preserving the class ratio in each fold, the model is trained on 4 folds and tested on the 5th,
five times, and the metrics below are the **mean across all 5 folds**. The 79 reserved students
are never part of any fold used here — they are not touched until the held-out check described
below, after every setup's best combination has already been chosen.

The Decision Tree's `max_depth` was checked via 5-fold CV recall on Early-Warning **development
data only** (depths 2, 3, 4, 5, 6, unlimited):

| max_depth | High-Risk recall (5-fold CV mean) |
|---|---|
| 2 | 0.365 |
| 3 | 0.367 |
| 4 | **0.482 ← selected** |
| 5 | 0.404 |
| 6 | 0.395 |
| None | 0.462 |

depth=4 is then reused as a fixed depth across every Decision Tree combination in Section 5, for
a fair comparison.

**Held-out test (genuinely non-leaked):** each setup's best combination from Section 5 below is
refit on the full 316-student development set and evaluated exactly once on the 79 reserved test
students — students that were never part of any fold used to pick a technique, a `class_weight`,
or the shared Decision Tree depth. This is what makes the held-out numbers in Section 7 a real
test of generalisation rather than a re-measurement of the same students the model was tuned on.

## 5. Results: all twelve combinations

| Setup | Technique | class_weight | Accuracy | Precision (High Risk) | Recall (High Risk) | F1 (High Risk) |
|---|---|---|---|---|---|---|
| Early-Warning | Logistic Regression | `None` | 0.696 | 0.7 | 0.212 | 0.311 |
| Early-Warning | Logistic Regression | `balanced` | 0.7 | 0.573 | 0.397 | 0.454 |
| Early-Warning | Decision Tree (depth=4) | `None` | 0.703 | 0.657 | 0.299 | 0.4 |
| Early-Warning | Decision Tree (depth=4) | `balanced` | 0.617 | 0.422 | **0.482** | 0.444 ← selected |
| Confirmatory — G1 only | Logistic Regression | `None` | 0.855 | 0.776 | 0.79 | 0.78 |
| Confirmatory — G1 only | Logistic Regression | `balanced` | 0.829 | 0.707 | **0.838** | 0.765 ← selected |
| Confirmatory — G1 only | Decision Tree (depth=4) | `None` | 0.839 | 0.818 | 0.646 | 0.719 |
| Confirmatory — G1 only | Decision Tree (depth=4) | `balanced` | 0.798 | 0.663 | 0.838 | 0.728 |
| Confirmatory — G1+G2 | Logistic Regression | `None` | 0.889 | 0.832 | 0.828 | 0.829 |
| Confirmatory — G1+G2 | Logistic Regression | `balanced` | 0.864 | 0.745 | **0.904** | 0.815 ← selected |
| Confirmatory — G1+G2 | Decision Tree (depth=4) | `None` | 0.893 | 0.824 | 0.857 | 0.839 |
| Confirmatory — G1+G2 | Decision Tree (depth=4) | `balanced` | 0.87 | 0.766 | 0.876 | 0.814 |

*(5-fold stratified cross-validation means on the 316-student development set — selection scores,
not final reported performance. Full precision to 3 d.p. is in `docs/evaluation_report.md`,
regenerated every time `python assignment/code/train_models.py` runs — these are real measured
numbers, not illustrative ones.)*

## 6. What the class-weight comparison shows

In **every one of the six setup/technique pairs**, `class_weight="balanced"` increases recall on
the High Risk class, at a cost to precision, and in most pairs accuracy too (the one exception is
Early-Warning Logistic Regression, where accuracy ticks up very slightly rather than dropping).
This is the expected, textbook effect of class weighting: it trades some overall correctness for
catching more of the minority class, which is the trade SARAH wants — a missed at-risk student
(false negative) is a worse outcome for an early-warning system than a false alarm that costs a
tutor a few minutes checking a student who turns out to be fine.

**Worth reporting honestly rather than glossing over:** the selected Early-Warning combination
(Decision Tree depth=4, balanced) has real weaknesses on development data — accuracy of 0.617 and
precision of only 0.422, meaning a large share of its High Risk flags are false alarms — and this
weakness carries through to the held-out test set too (precision 0.44, recall 0.423 — see
`docs/evaluation_report.md`). This is the direct, measured consequence of the team's decision to
keep Early-Warning mode to just three weak-individually features (`attendance_pct` and
`study_hours` each correlate only -0.08 with risk; only `failures` at +0.34 carries real signal —
see `docs/eda_findings.md`). It is reported as-is, not smoothed over, because it is the honest
cost of the narrow, four-feature design and directly supports the accuracy-vs-earliness
discussion below.

## 7. Selected combination per setup

- **Early-Warning Mode:** Decision Tree (depth=4), `class_weight="balanced"` — development recall
  0.482, F1 0.444.
- **Confirmatory Mode — G1 only:** Logistic Regression, `class_weight="balanced"` — development
  recall 0.838, F1 0.765.
- **Confirmatory Mode — G1+G2:** Logistic Regression, `class_weight="balanced"` — development
  recall 0.904, F1 0.815.

Selection criterion throughout this project: highest recall on the High Risk class (tie-broken by
F1), for the reason in Section 6. These are development/selection scores.

**Held-out test results (reserved students, never used above):** early_warning — accuracy 0.633,
precision 0.44, recall 0.423, F1 0.431; confirmatory_g1 — accuracy 0.823, precision 0.714, recall
0.769, F1 0.741; confirmatory_g1_g2 — accuracy 0.899, precision 0.821, recall 0.885, F1 0.852 (26
High Risk / 79 total test students; confusion matrices in `docs/figures/confusion_*.png`). Full
report: `docs/evaluation_report.md`.

## 8. The accuracy-vs-earliness tradeoff this reveals

Comparing the held-out test rows directly is the core critical-analysis point of this project:
**Early-Warning recall (0.423) is far lower than Confirmatory recall (0.769 with G1 only, 0.885
with G1+G2)** — a gap of 30 to 45 percentage points depending on setup. This is a limitation
observed in our current experiments, not a proven irreducible one: predicting risk before any
grade exists, using only attendance, study habits, and past failures instead of the single
strongest predictor available (`previous_score`, correlation -0.72 with risk), is expected to
perform worse given the narrower feature set — but these results do not prove that better
Early-Warning performance is impossible with more data or additional features. SARAH makes this
tradeoff explicit rather than hiding it: **Early-Warning Mode is the system's primary, default
mode**, because catching risk *earlier* — even less accurately — is the entire point of an
early-warning system; a highly accurate prediction that only arrives once grades already exist is
not early anymore. Confirmatory Mode (either setup) stays available for a more accurate second
look once grades come in, and the two modes together let a tutor see both how early a flag came
and how much to trust it.

## 9. Where this shows up in the report

Maps to report Section 4 ("describe your pre-processing and justify it", including the
class-imbalance handling) and Section 6 (AI technique comparison / justification of final model
choice, including the two-mode accuracy-vs-earliness discussion). Use the Section 5 table
directly; full numbers and confusion matrices regenerate at `docs/evaluation_report.md` and
`docs/figures/confusion_*.png` every time `python assignment/code/train_models.py` runs.
