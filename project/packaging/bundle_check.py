"""Developer-only smoke check using fictional records inside the built app."""
import json
import sys


def self_test(output, root):
    import io
    import pandas as pd
    import sklearn.linear_model
    import sklearn.tree
    from streamlit.testing.v1 import AppTest
    sys.path.insert(0, str(root / "project/code"))
    from predict import predict_one, predict_roster, STUDY_HOURS_WARNING
    import dashboard
    from recommend import recommend
    results = {}
    for name, args, expected in [
        ("early_warning", (40, 4, 0, "early_warning"), ("High Risk", .859)),
        ("g1", (80, 4, 0, "confirmatory", 8, None), ("High Risk", .818)),
        ("g1_g2", (55, 1.5, 1, "confirmatory", 9, 8), ("High Risk", .842)),
        ("warning", (80, 40, 0, "confirmatory", 12, None), ("High Risk", .661)),
    ]:
        actual = predict_one(*args)
        assert actual == expected, (name, actual)
        results[name] = list(actual)
    rows, skipped = predict_roster(root / "project/data/sample_roster.csv", "confirmatory")
    assert len(rows) == 2 and len(skipped) == 2
    text = (root / "project/data/study_hours_warning_demo.csv").read_text(encoding="utf-8")
    rows, skipped, total = dashboard.process_upload(text, "confirmatory", recommender=recommend)
    assert (len(rows), len(skipped), total) == (2, 0, 2)
    assert list(rows.input_warning) == [STUDY_HOURS_WARNING, ""]
    shown = dashboard.display_results(rows)
    assert list(shown.study_hours_warning) == [dashboard.WARNING_MARK, ""]
    exported = pd.read_csv(io.StringIO(rows.to_csv(index=False)), keep_default_na=False)
    assert list(exported.input_warning) == [STUDY_HOURS_WARNING, ""]
    assert "recommendations" in exported.columns
    app = AppTest.from_file(str(root / "project/code/dashboard.py")).run(timeout=60)
    assert not app.exception, str(app.exception)
    app.radio[0].set_value("confirmatory").run()
    app.number_input[0].set_value(80.0).run()
    app.number_input[1].set_value(40.0).run()
    app.text_input[0].set_value("12").run()
    app.button[0].click().run()
    assert not app.exception, str(app.exception)
    assert any("66.1%" in m.value for m in app.markdown)
    assert any(STUDY_HOURS_WARNING in w.value for w in app.warning)
    results["dashboard_form_warning_and_csv_export"] = "passed"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
