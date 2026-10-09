"""Support recommendations for SARAH risk predictions.

The dashboard passes validated student inputs using the function contract
approved in Issue #52. Recommendations support human review and do not
explain the cause of a prediction or guarantee improved outcomes.
"""

LOW_RISK_MESSAGE = (
    "The model predicts Low Risk. Under the current recommendation rules, "
    "targeted suggestions are shown only for High Risk predictions. "
    "Continue routine check-ins and offer support where needed."
)

NO_MATCH_MESSAGE = (
    "The model identified elevated risk, but no individual recommendation "
    "threshold was triggered. A staff member should review the student's "
    "circumstances and discuss whether support is needed."
)


def recommend(student_fields, prediction):
    """Return recommendation messages for one validated student.

    student_fields contains exactly:
      mode, attendance_pct, study_hours, failures, previous_score

    previous_score is None for Early-Warning mode. prediction is either
    "High Risk" or "Low Risk".
    """
    if prediction == "Low Risk":
        return [LOW_RISK_MESSAGE]

    if prediction != "High Risk":
        raise ValueError("prediction must be 'High Risk' or 'Low Risk'")

    mode = student_fields["mode"]
    if mode not in ("early_warning", "confirmatory"):
        raise ValueError("mode must be 'early_warning' or 'confirmatory'")

    messages = []

    if student_fields["attendance_pct"] <= 60:
        messages.append(
            "Attendance support: Ask about attendance barriers and discuss "
            "available support because the attendance estimate is 60% or below."
        )

    if student_fields["study_hours"] <= 1.5:
        messages.append(
            "Study planning: Help the student prepare a realistic weekly study "
            "plan and discuss study-support options because estimated study "
            "hours are 1.5 per week or below."
        )

    if student_fields["failures"] >= 1:
        messages.append(
            "Previous-failure support: Discuss previous academic difficulties "
            "and suitable support options because the student has one or more "
            "previous class failures."
        )

    if (
        mode == "confirmatory"
        and student_fields["previous_score"] < 50
    ):
        messages.append(
            "Assessment review: Review the student's assessment performance "
            "and discuss appropriate academic support because the normalised "
            "previous score is below 50."
        )

    if not messages:
        messages.append(NO_MATCH_MESSAGE)

    return messages
