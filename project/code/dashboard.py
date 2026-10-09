"""SARAH tutor dashboard (Issues #54 and #55).

Run from the repository root:
    streamlit run project/code/dashboard.py

Tab 1 (#54): enter one student and get a risk prediction.
Tab 2 (#55): upload a class CSV; valid students are predicted and
invalid rows are listed with the reason they were skipped.

This file only handles the screen. Validation and prediction reuse
predict.py, so the dashboard gives the same answers as the command line.
Recommendations (#53) are shown in the form and as a CSV column once
recommend.py exists, using the function contract agreed in #52.
"""

import csv
import io
from pathlib import Path

import streamlit as st

from data_processing import previous_score_from_grades
from predict import _parse_g2, predict_one, predict_roster

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # project/code -> project/
SAMPLE_CSV = PROJECT_ROOT / "data" / "sample_roster.csv"

MODE_LABELS = {
    "early_warning": "Early-Warning (no grades)",
    "confirmatory": "Confirmatory (G1 required, G2 optional)",
}
MODE_HELP = {
    "early_warning": "Uses attendance estimate, study hours and past failures only. No assessment grades are needed.",
    "confirmatory": "Adds assessment grades. G1 is required. G2 is optional: leave it blank if there is no G2 yet (0 is a valid grade).",
}
REQUIRED_COLUMNS = {
    "early_warning": "student_id (optional), attendance_pct, study_hours, failures",
    "confirmatory": "student_id (optional), attendance_pct, study_hours, failures, G1, G2 (optional, may be blank)",
}
PROBABILITY_NOTE = (
    "The probability is the model's estimate, not a guaranteed chance of failing. "
    "Use it alongside your own knowledge of the student."
)

# Recommendation contract agreed in #52 (Section 3):
#   recommend(student_fields, prediction) -> list[str]
#   student_fields keys: mode, attendance_pct, study_hours, failures, previous_score
#   (previous_score is None in Early-Warning); prediction is "High Risk" or "Low Risk".
# recommend.py is built in #53. Until it exists the dashboard still works and shows
# a placeholder. If the file exists but cannot be used (e.g. a different function
# name), the page says so instead of silently showing the placeholder.
RECOMMEND_ERROR = None
try:
    from recommend import recommend
except ModuleNotFoundError as exc:
    recommend = None
    if exc.name != "recommend":
        RECOMMEND_ERROR = f"recommend.py could not be loaded: {exc}"
except ImportError as exc:
    recommend = None
    RECOMMEND_ERROR = f"recommend.py was found but has no usable recommend() function: {exc}"


def parse_grade(text, name, required):
    """Turn a typed grade into a number. Blank -> None (only allowed if not required)."""
    text = (text or "").strip()
    if not text:
        if required:
            raise ValueError(f"{name} is required in Confirmatory mode")
        return None
    try:
        return float(text)
    except ValueError:
        raise ValueError(f"{name} must be a number from 0 to 20") from None


def predict_single(mode, attendance, study_hours, failures, g1_text="", g2_text=""):
    """Validate the form values and return (label, probability, grade_setup).
    Raises ValueError with a readable message if any value is invalid."""
    g1 = g2 = None
    grade_setup = None
    if mode == "confirmatory":
        g1 = parse_grade(g1_text, "G1", required=True)
        g2 = parse_grade(g2_text, "G2", required=False)
        grade_setup = "g1_g2" if g2 is not None else "g1"
    label, proba = predict_one(attendance, study_hours, failures, mode, g1, g2)
    return label, proba, grade_setup


def build_student_fields(mode, attendance, study_hours, failures, g1=None, g2=None):
    """The exact student_fields dictionary agreed in #52. Uses the existing
    previous_score_from_grades() so there is only one grade calculation."""
    return {
        "mode": mode,
        "attendance_pct": float(attendance),
        "study_hours": float(study_hours),
        "failures": int(float(failures)),
        "previous_score": previous_score_from_grades(g1, g2) if mode == "confirmatory" else None,
    }


def form_student_fields(mode, attendance, study_hours, failures, g1_text="", g2_text=""):
    """student_fields for the one-student form (call after predict_single succeeded)."""
    g1 = g2 = None
    if mode == "confirmatory":
        g1 = parse_grade(g1_text, "G1", required=True)
        g2 = parse_grade(g2_text, "G2", required=False)
    return build_student_fields(mode, attendance, study_hours, failures, g1, g2)


def get_recommendations(student_fields, prediction, recommender=None):
    """Call recommend() and check it returned a list of strings.
    Returns (messages, error). messages is None when recommend.py does not exist yet."""
    recommender = recommender if recommender is not None else recommend
    if recommender is None:
        return None, None
    try:
        messages = recommender(student_fields, prediction)
    except Exception as exc:
        return None, f"recommend() failed: {type(exc).__name__}: {exc}"
    if not isinstance(messages, list) or not all(isinstance(m, str) for m in messages):
        return None, "recommend() must return a list of text messages (list[str])."
    return messages, None


KNOWN_COLUMNS = ["student_id", "attendance_pct", "study_hours", "failures", "G1", "G2"]


def prepare_upload(text):
    """Check the CSV's structure before predicting.

    Returns (clean_csv_text, skipped_rows, total_rows). Raises ValueError for a
    problem with the whole file.

    Why: pandas silently shifts every value one column to the left when a row
    has an extra comma, so a student could get a prediction from the wrong
    numbers. Here every row must have exactly as many values as the header;
    a row that does not is skipped with its row number instead of being guessed.
    Header names are also matched ignoring case and spaces (" g1 " -> "G1").
    Rows are numbered 1, 2, 3... after the header, blank lines ignored.
    """
    rows = list(csv.reader(io.StringIO(text)))
    if not rows or not any(cell.strip() for cell in rows[0]):
        raise ValueError("The CSV contains no students.")
    if any("\n" in cell or "\r" in cell for row in rows for cell in row):
        raise ValueError("The file has an unmatched quote mark (\"), so its rows cannot be read reliably. "
                         "Please fix it in the spreadsheet and upload again.")

    canonical = {name.lower(): name for name in KNOWN_COLUMNS}
    header = [canonical.get(name.strip().lower(), name.strip()) for name in rows[0]]
    duplicates = sorted({name for name in header if name and header.count(name) > 1})
    if duplicates:
        raise ValueError(f"Column(s) appear more than once: {', '.join(duplicates)}")

    data = [row for row in rows[1:] if row]  # csv gives [] for a blank line
    if not data:
        raise ValueError("The CSV contains no students.")

    has_id = "student_id" in header
    out_header = header if has_id else ["student_id"] + header
    kept, skipped, rows = [], [], {}
    for number, row in enumerate(data, start=1):
        if has_id and len(row) == len(header):
            label = row[header.index("student_id")].strip() or f"row {number}"
        else:
            label = f"row {number}"
        if len(row) != len(header):
            skipped.append({"student_id": label, "reason": f"has {len(row)} values but the header has "
                            f"{len(header)} columns (check for a missing or extra comma)", "_row": number})
            continue
        # Each row gets a unique internal key, so its prediction and recommendations
        # stay linked to this exact row even if two students share an ID.
        key = f"__row{number}__"
        rows[key] = {"row": number, "label": label, "values": dict(zip(header, row))}
        if has_id:
            row = list(row)
            row[header.index("student_id")] = key
            kept.append(row)
        else:
            kept.append([key] + row)

    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(out_header)
    writer.writerows(kept)
    return buffer.getvalue(), skipped, len(data), rows


def csv_row_student_fields(values, mode):
    """student_fields for one valid CSV row (same keys and conversion as the form)."""
    g1 = g2 = None
    if mode == "confirmatory":
        g1 = float(values["G1"])
        g2 = _parse_g2(values.get("G2"))
    return build_student_fields(mode, values["attendance_pct"], values["study_hours"],
                                values["failures"], g1, g2)


def process_upload(text, mode, recommender=None):
    """Everything the Class CSV tab does, without the screen: check the file's
    structure, predict with predict.py and, when a recommender is given, add a
    "recommendations" column built from each row's own inputs.
    Returns (results, skipped, total_rows). Skipped rows never get recommendations."""
    clean_text, skipped, total_rows, rows = prepare_upload(text)
    if rows:
        results, value_skipped = predict_roster(io.StringIO(clean_text), mode)
        for item in value_skipped:
            info = rows[item["student_id"]]
            skipped.append({"student_id": info["label"], "reason": item["reason"], "_row": info["row"]})
    else:  # every row had the wrong number of values
        results = _empty_results(mode)
    skipped = [{"student_id": s["student_id"], "reason": s["reason"]}
               for s in sorted(skipped, key=lambda s: s["_row"])]

    keys = list(results["student_id"])
    results["student_id"] = [rows[k]["label"] for k in keys]
    if recommender is not None:
        column = []
        for key, label in zip(keys, results["risk_label"]):
            fields = csv_row_student_fields(rows[key]["values"], mode)
            messages, error = get_recommendations(fields, label, recommender)
            column.append(error if error else " | ".join(messages))
        results["recommendations"] = column
    return results, skipped, total_rows


def _empty_results(mode):
    import pandas as pd
    columns = ["student_id", "risk_label", "probability_high_risk"]
    if mode == "confirmatory":
        columns.append("grade_setup")
    return pd.DataFrame(columns=columns)


def show_recommendation(student_fields, label):
    messages, error = get_recommendations(student_fields, label)
    if error:
        st.error(error)
    elif messages is None:
        st.caption("Support suggestions will appear here once the recommendation engine (#53) is added.")
    else:
        st.write("**Support suggestions** (for human review):")
        for message in messages:
            st.write(f"- {message}")


def single_student_tab(mode):
    st.subheader("One student")
    # No st.form here on purpose: every change to an input or the mode reruns
    # the page, and st.button is only True on the click itself, so an old
    # result disappears as soon as anything is changed (#54).
    with st.container(border=True):
        # No min/max on these boxes on purpose: with min/max, Streamlit keeps the
        # last valid value when an out-of-range number is typed, so the screen
        # could show 150 while the prediction silently used 80. Without them,
        # the typed value is sent and predict.py's validation shows an error.
        attendance = st.number_input("Attendance estimate (%) - 0 to 100", value=80.0, step=1.0)
        study_hours = st.number_input("Study hours per week - 0 to 40", value=5.0, step=0.5)
        # A fixed list makes non-whole or out-of-range failures impossible.
        failures = st.selectbox("Past class failures (whole number, 0 to 3)", [0, 1, 2, 3])
        g1_text = g2_text = ""
        if mode == "confirmatory":
            g1_text = st.text_input("G1 (0-20, required)")
            g2_text = st.text_input("G2 (0-20, optional - leave blank if not available)")
        clicked = st.button("Predict")

    if not clicked:
        return
    try:
        label, proba, grade_setup = predict_single(mode, attendance, study_hours, failures, g1_text, g2_text)
    except ValueError as exc:
        st.error(f"Please fix the input: {exc}")
        return
    except Exception as exc:  # last safety net: never show a crash screen
        st.error(f"Something unexpected went wrong ({type(exc).__name__}: {exc}). No prediction was made.")
        return

    show = st.error if label == "High Risk" else st.success
    show(f"**{label}**")
    st.write(f"Estimated High-Risk probability: **{proba:.3f}**")
    if grade_setup:
        st.write(f"Model used: **{'G1 + G2' if grade_setup == 'g1_g2' else 'G1 only'}**")
    st.caption(PROBABILITY_NOTE)
    fields = form_student_fields(mode, attendance, study_hours, failures, g1_text, g2_text)
    show_recommendation(fields, label)


def class_csv_tab(mode):
    st.subheader("Class CSV")
    st.write(f"Required columns for this mode: `{REQUIRED_COLUMNS[mode]}`")
    if SAMPLE_CSV.exists():
        st.download_button("Download sample CSV (fictional students)", SAMPLE_CSV.read_bytes(),
                           file_name="sample_roster.csv", mime="text/csv")
    uploaded = st.file_uploader("Upload a class CSV", type="csv")
    if uploaded is None:
        return

    try:
        text = uploaded.getvalue().decode("utf-8-sig")
    except UnicodeDecodeError:
        st.error("This file cannot be read. Please save it as a UTF-8 CSV and upload again.")
        return
    try:
        results, skipped, total_rows = process_upload(text, mode, recommend)
    except ValueError as exc:
        st.error(f"This file cannot be processed: {exc}")
        return
    except Exception as exc:  # last safety net: never show a crash screen
        st.error(f"Something unexpected went wrong reading this file ({type(exc).__name__}: {exc}). "
                 "No predictions were made. Please check the file and try again.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows in file", total_rows)
    c2.metric("Predicted", len(results))
    c3.metric("Skipped", len(skipped))
    if len(results) + len(skipped) != total_rows:
        st.warning("Predicted + skipped does not match the number of rows. Please check the file.")

    if results.empty:
        st.error("No valid students to process. See the skipped rows below.")
    else:
        st.dataframe(results, hide_index=True)
        st.caption(PROBABILITY_NOTE)
        if recommend is None:
            st.caption("A recommendations column will be added once the recommendation engine (#53) is added.")
        st.download_button("Download results as CSV", results.to_csv(index=False).encode("utf-8"),
                           file_name="sarah_predictions.csv", mime="text/csv")

    if skipped:
        st.write("**Skipped rows** (no prediction was made for these students):")
        st.dataframe(skipped, hide_index=True)


def main():
    st.set_page_config(page_title="SARAH Dashboard")
    st.title("SARAH - Student Academic Risk Assistance Hub")
    st.caption("Prototype for tutors. Results are suggestions for human review, not decisions.")
    if RECOMMEND_ERROR:
        st.error(RECOMMEND_ERROR)

    mode = st.radio("Prediction mode", list(MODE_LABELS), format_func=MODE_LABELS.get, horizontal=True)
    st.info(MODE_HELP[mode])

    tab_one, tab_class = st.tabs(["One student", "Class CSV"])
    with tab_one:
        single_student_tab(mode)
    with tab_class:
        class_csv_tab(mode)


if __name__ == "__main__":
    main()
