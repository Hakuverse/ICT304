"""Tests for the approved recommendation rules in Issues #52 and #53."""

import unittest

from recommend import LOW_RISK_MESSAGE, NO_MATCH_MESSAGE, recommend


def student(
    mode="early_warning",
    attendance=80,
    study_hours=4,
    failures=0,
    previous_score=None,
):
    return {
        "mode": mode,
        "attendance_pct": attendance,
        "study_hours": study_hours,
        "failures": failures,
        "previous_score": previous_score,
    }


class RecommendationRules(unittest.TestCase):

    def test_low_risk_gets_only_routine_message(self):
        fields = student(
            mode="confirmatory",
            attendance=40,
            study_hours=1.5,
            failures=2,
            previous_score=30,
        )
        self.assertEqual(recommend(fields, "Low Risk"), [LOW_RISK_MESSAGE])

    def test_attendance_boundary(self):
        at_boundary = recommend(
            student(attendance=60),
            "High Risk",
        )
        above_boundary = recommend(
            student(attendance=60.1),
            "High Risk",
        )

        self.assertTrue(at_boundary[0].startswith("Attendance support:"))
        self.assertEqual(above_boundary, [NO_MATCH_MESSAGE])

    def test_study_hours_boundary(self):
        at_boundary = recommend(
            student(study_hours=1.5),
            "High Risk",
        )
        above_boundary = recommend(
            student(study_hours=1.6),
            "High Risk",
        )

        self.assertTrue(at_boundary[0].startswith("Study planning:"))
        self.assertEqual(above_boundary, [NO_MATCH_MESSAGE])

    def test_previous_failure_boundary(self):
        no_failure = recommend(
            student(failures=0),
            "High Risk",
        )
        one_failure = recommend(
            student(failures=1),
            "High Risk",
        )

        self.assertEqual(no_failure, [NO_MATCH_MESSAGE])
        self.assertTrue(
            one_failure[0].startswith("Previous-failure support:")
        )

    def test_assessment_score_boundary(self):
        below_50 = recommend(
            student(
                mode="confirmatory",
                previous_score=40,
            ),
            "High Risk",
        )
        exactly_50 = recommend(
            student(
                mode="confirmatory",
                previous_score=50,
            ),
            "High Risk",
        )

        self.assertTrue(below_50[0].startswith("Assessment review:"))
        self.assertEqual(exactly_50, [NO_MATCH_MESSAGE])

    def test_early_warning_never_uses_assessment_rule(self):
        messages = recommend(
            student(
                mode="early_warning",
                previous_score=None,
            ),
            "High Risk",
        )

        self.assertEqual(messages, [NO_MATCH_MESSAGE])
        self.assertFalse(
            any(message.startswith("Assessment review:") for message in messages)
        )

    def test_multiple_rules_use_approved_order_without_duplicates(self):
        messages = recommend(
            student(
                mode="confirmatory",
                attendance=60,
                study_hours=1.5,
                failures=1,
                previous_score=49,
            ),
            "High Risk",
        )

        self.assertEqual(
            [message.split(":")[0] for message in messages],
            [
                "Attendance support",
                "Study planning",
                "Previous-failure support",
                "Assessment review",
            ],
        )
        self.assertEqual(len(messages), len(set(messages)))

    def test_targeted_messages_include_a_reason(self):
        messages = recommend(
            student(
                mode="confirmatory",
                attendance=60,
                study_hours=1.5,
                failures=1,
                previous_score=49,
            ),
            "High Risk",
        )

        self.assertTrue(all("because" in message.lower() for message in messages))

    def test_high_risk_with_no_matching_rule_gets_fallback(self):
        messages = recommend(
            student(
                mode="confirmatory",
                attendance=80,
                study_hours=4,
                failures=0,
                previous_score=70,
            ),
            "High Risk",
        )

        self.assertEqual(messages, [NO_MATCH_MESSAGE])

    def test_invalid_prediction_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "prediction"):
            recommend(student(), "Unknown")

    def test_invalid_mode_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "mode"):
            recommend(student(mode="wrong_mode"), "High Risk")


if __name__ == "__main__":
    unittest.main()
    