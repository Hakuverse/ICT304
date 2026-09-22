# SARAH — Class Imbalance & Class-Weight Comparison (Issue #19)

This note answers the sprint backlog item directly: it documents SARAH's class imbalance, and
compares `class_weight=None` against `class_weight="balanced"` across **all eight combinations**
of mode × technique × class-weight setting, as the issue specifies. It's ready to paste into the
report's pre-processing / methodology section, and anyone on the team can use it to defend the
decision in a viva or demo.

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

## 2. Two modes, not one — why this comparison has eight combinations, not two

SARAH runs in two modes, because the data actually available about a student changes over the
term:

- **Early-Warning Mode** (primary): attendance, study hours, past failures, and
  demographic/behavioural signals (family support, parental education, lifestyle). No grades at
  all — this is everything SARAH can know on day one of term, before any assessment exists.
- **Confirmatory Mode** (secondary): Early-Warning features **+** `previous_score` (the average
  of the first two assessment periods), once at least one grade exists.

Both modes are trained and compared with **both** AI techniques (Logistic Regression, Decision
Tree) and **both** `class_weight` settings (`None`, `"balanced"`) — **2 modes × 2 techniques × 2
settings = 8 combinations**, each evaluated the same way (Section 4). This directly answers the
issue's "both modes" requirement, and lets the team see whether `class_weight="balanced"` matters
differently depending on which features are available.

## 3. What `class_weight="balanced"` actually does

```python
LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000)
DecisionTreeClassifier(max_depth=4, class_weight="balanced", random_state=42)
```

scikit-learn's `class_weight="balanced"` re-weights the training loss so mistakes on the
**minority class (High Risk)** count for more than mistakes on the majority class (Low Risk), in
inverse proportion to how often each class appears (roughly `265/130 ≈ 2.0×` here). This pushes
the model to actually learn the boundary between the two groups instead of defaulting toward the
majority class. We did not use oversampling (e.g. SMOTE) or undersampling, because `class_weight`
needs no extra library or synthetic rows, is simpler to reproduce, and is the standard first
approach for an imbalance at this level (not extreme).

## 4. Method: stratified 5-fold cross-validation, not a single train/test split

With only 395 students (130 High Risk), a single 80/20 train/test split would leave roughly 26
High Risk students in the test set — too few for a stable precision/recall estimate; one or two
different predictions would swing the reported numbers noticeably. Instead, every combination
below is evaluated with **stratified 5-fold cross-validation** (`StratifiedKFold`, shuffled,
`random_state=42`): the dataset is split into 5 folds preserving the 32.9%/67.1% class ratio in
each fold, the model is trained on 4 folds and tested on the 5th, five times, and the metrics
below are the **mean across all 5 folds**. This uses every student for both training and testing
(across different folds) and gives a far more stable estimate than one split.

The Decision Tree's depth is fixed at **`max_depth=4`** for all eight combinations (chosen once,
via 5-fold CV recall on Early-Warning mode with `class_weight="balanced"`, trying depths 2, 3, 4,
5, 6, and unlimited — depth 4 gave the best recall, 0.546), so the technique comparison is fair
(same tree complexity in every row).

## 5. Results: all eight combinations

| Mode | Technique | class_weight | Accuracy | Precision (High Risk) | Recall (High Risk) | F1 (High Risk) |
|---|---|---|---|---|---|---|
| Early-Warning | Logistic Regression | `None` | 0.706 | 0.593 | 0.346 | 0.436 |
| Early-Warning | Logistic Regression | `balanced` | 0.681 | 0.512 | **0.554** | **0.530** ← selected |
| Early-Warning | Decision Tree (depth=4) | `None` | 0.673 | 0.513 | 0.362 | 0.420 |
| Early-Warning | Decision Tree (depth=4) | `balanced` | 0.678 | 0.513 | 0.546 | 0.528 |
| Confirmatory | Logistic Regression | `None` | 0.868 | 0.815 | 0.777 | 0.794 |
| Confirmatory | Logistic Regression | `balanced` | 0.868 | 0.757 | **0.885** | **0.815** ← selected |
| Confirmatory | Decision Tree (depth=4) | `None` | 0.851 | 0.779 | 0.762 | 0.769 |
| Confirmatory | Decision Tree (depth=4) | `balanced` | 0.856 | 0.744 | 0.869 | 0.798 |

*(5-fold stratified cross-validation means. Full precision to 3 d.p. and the depth-selection
trial table are in `reports/evaluation_report.md`, regenerated every time `python
src/train_models.py` runs — these are real measured numbers, not illustrative ones.)*

## 6. What the class-weight comparison shows

In **every one of the four mode/technique pairs**, `class_weight="balanced"` increases recall on
the High Risk class, usually substantially (e.g. Early-Warning Logistic Regression: 0.346 →
0.554), at a moderate cost to accuracy and precision. This is the expected, textbook effect of
class weighting: it trades some overall correctness for catching more of the minority class,
which is exactly the trade SARAH wants — a missed at-risk student (false negative) is a worse
outcome for an early-warning system than a false alarm that costs a tutor a few minutes checking
a student who turns out to be fine. **`class_weight="balanced"` is used in SARAH's selected model
for both modes** on this basis.

The comparison also shows the effect is **not identical across modes**: the accuracy/recall
trade-off is steeper in Early-Warning mode (accuracy drops from 0.706 to 0.681, a real but modest
cost, for a recall gain of +0.208) than in Confirmatory mode (accuracy is unchanged at 0.868, for
a recall gain of +0.108). With less predictive signal available (Early-Warning mode has no
grades), pushing the model harder toward the minority class costs relatively more overall
correctness — a useful, honestly-reported nuance rather than a clean "balanced is free" story.

## 7. Selected combination per mode

- **Early-Warning Mode:** Logistic Regression, `class_weight="balanced"` — recall 0.554, F1 0.530.
- **Confirmatory Mode:** Logistic Regression, `class_weight="balanced"` — recall 0.885, F1 0.815.

Selection criterion throughout this project: highest recall on the High Risk class (tie-broken by
F1), for the reason in Section 6.

## 8. The accuracy-vs-earliness tradeoff this reveals

Comparing the two selected rows directly is the core critical-analysis point of this project:
**Early-Warning recall (0.554) is meaningfully lower than Confirmatory recall (0.885)** — a gap
of over 33 percentage points. This is not a modelling shortfall to fix; it is the real,
irreducible cost of predicting risk *before* any grade exists, using only attendance, study
habits, and demographic/behavioural signal instead of the single strongest predictor available
(`previous_score`, correlation -0.72 with risk — see `reports/eda_findings.md`). SARAH makes this
tradeoff explicit rather than hiding it: **Early-Warning Mode is the system's primary, default
mode**, because catching risk *earlier* — even less accurately — is the entire point of an
early-warning system; a highly accurate prediction that only arrives once grades already exist is
not early anymore. Confirmatory Mode stays available for a more accurate second look once grades
come in, and the two modes together let a tutor see both how early a flag came and how much to
trust it.

## 9. Where this shows up in the report

Maps to report Section 4 ("describe your pre-processing and justify it", including the
class-imbalance handling) and Section 6 (AI technique comparison / justification of final model
choice, including the two-mode accuracy-vs-earliness discussion). Use the Section 5 table
directly; full numbers and confusion matrices regenerate at `reports/evaluation_report.md` and
`reports/figures/confusion_*.png` every time `python src/train_models.py` runs.
