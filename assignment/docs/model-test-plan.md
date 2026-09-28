# Fair Comparison Plan for Logistic Regression and Decision Tree

## Part 1 Stratified Five Fold Cross Validation

Logistic Regression and Decision Tree will be compared using stratified five-fold cross-validation. First reserve 79 of the 395 students as a stratified final test set. The remaining 316 development students will be divided into five folds, with each fold containing
approximately the same proportion of High Risk and Low Risk students as the development set. In each of the five rounds, four folds will be used to train the model and the
remaining fold will be used for validation. Each fold will serve as the validation set exactly once. Accuracy, precision, recall and F1-score will be calculated in every round, and the
mean results across the five folds will be reported.

## Part 2 Consistent and Repeatable Data Splits

The same five fold assignments will be used for Logistic Regression and Decision Tree so that both models are trained and tested on exactly the same students. The same fold assignments will also be retained across Early-Warning, Confirmatory G1-only and Confirmatory G1+G2, although these setups use different inputs. The folds will be generated
using stratification, shuffling and `random_state=42`, making the experiment repeatable and preventing differences in data splitting from unfairly influencing the comparison.

## Part 3 Prevention of Target and Preprocessing Leakage

The risk target will first be derived from `G3`, where `G3 < 10` represents High Risk and `G3 >= 10` represents Low Risk. After the target has been created, `G3` and the derived
risk label will never be included as model input features. This rule applies to both prediction modes and both models. The current preprocessing uses fixed numeric mappings and range checks. It does not fit missing-value imputation, categorical encoding or StandardScaler. If learned preprocessing is added, fit it only on the training folds and apply it unchanged to the validation fold. Never fit it using the 79 reserved test students.

## Part 4 Evaluation Metrics and Importance of High Risk Recall

Both models will be evaluated using accuracy, precision, recall and F1-score, with High Risk treated as the positive class. Accuracy measures the overall proportion of correct
predictions, while precision measures how many students predicted as High Risk are actually High Risk. Recall measures how many genuinely High Risk students are successfully
identified, and F1-score balances precision and recall. Recall is particularly important for SARAH because a false negative means that a genuinely at-risk student is incorrectly
classified as Low Risk and may not receive timely academic support. The comparison will therefore consider all four metrics, with particular attention given to High Risk recall
and F1-score rather than selecting a model based on accuracy alone.

## Part 5 Baseline Models and Later Model Adjustment

The initial models are now implemented in `train_models.py`. Compare Logistic Regression and Decision Tree with `class_weight=None` and `balanced` for all three setups: 12 combinations. Use the same student splits, target and metrics throughout.

Depth 4 was selected from depths 2, 3, 4, 5, 6 and unrestricted using Early-Warning development recall with balanced weights. This depth is reused for every tree comparison. Choose each setup's model by development High-Risk recall, breaking ties with F1. Fit the selected model on all 316 development students, then evaluate it on the reserved 79 students.

Do not change settings to improve results already seen on the final test set. Discuss a suitable evaluation approach with the tutor before further tuning. Report development scores separately from final test results, and compare with the always-Low-Risk baseline (67.1% accuracy and zero High-Risk recall on the reserved set).

## Summary

This evaluation plan provides a fair comparison by using the same students, the same cross-validation folds, the same target definition and the same evaluation metrics for both
models. Stratification maintains the High Risk and Low Risk balance in every fold, while training-only preprocessing and the exclusion of `G3` prevent data leakage. The
experiment will be repeatable through the use of `random_state=42`, and the final model decision will consider the system’s main purpose of identifying students who require
early intervention.

## Results and system checks

See [the recorded comparison](evaluation_report.md) for development and final test results. The separate [system test plan](../report/Document.md#8-evaluation-method-and-test-plan) checks input rules, CSV processing and the planned dashboard and recommendations. A passed software test is not a model-accuracy result.
