# Study-hours finding and critical discussion

Benjamin found this during the 23 October 2026 guide walkthrough (#80).
On 24 October the agreed response was to keep the 0–40 input range, add a warning
and explain the limitation. No model replacement or new training is claimed.

## Observed example

Attendance 80, study hours 40, failures 0, G1 12 and G2 blank returns High Risk
with estimated High-Risk probability 0.661 using the saved G1-only model.
With the other inputs unchanged, 4 hours returns 0.092 and 12 hours returns 0.163.
These are fictional sensitivity examples, not accuracy measurements.

The G1-only Logistic Regression has a positive study-hours coefficient of about
0.0822. Holding the other model inputs constant, increasing hours increases its
estimated risk. This is an association learned by the fitted model, not evidence
that studying longer causes difficulty or that a student should study less.

## Why this matters

The source dataset records broad study-time categories, converted by the project
to 1.5, 3.5, 7.5 and 12 hours. The highest source category is open-ended; 12 is an
assumed representative value, not the maximum amount real students can study.
Forty is valid under our input contract but lies beyond those converted training
values. A continuous-hours input gives an impression of precision that the source
categories do not support. Inputs at or below 12 are not automatically reliable.

Boundary checks established that 40 was accepted and 41 rejected. They did not
establish prediction quality at 40. Held-out dataset evaluation used the same
conversion, so it did not evaluate this higher-hours scenario. The small usability
study was not a systematic check of model behaviour across all accepted inputs.
This is a gap in coverage, not evidence that the earlier functional tests failed.

## Chosen response and remaining limits

The form and command-line prediction show a warning above 12. Each valid CSV row
carries an `input_warning` field, also kept in downloaded results. Warnings apply
to either risk label and all three model setups. Rows above 12 and at most 40
are not skipped; invalid rows are still skipped for the original reasons.
The warning is not a support recommendation and does not change input values,
predictions or the model's estimated probabilities.

This response improves transparency, not model accuracy or calibration. The team
chose it within the remaining project time. Restricting inputs to 12 would exclude
legitimate higher values without resolving the category-to-hours approximation.
Future work should compare categorical study-time representations and modelling
choices using development data, with criteria agreed before comparison. The known
79-student test results should not be repeatedly used to choose changes.

The report should retain this limitation alongside the weak Early-Warning recall,
approximate attendance input, small dataset and uncalibrated probabilities.
