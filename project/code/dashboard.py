"""SARAH tutor dashboard (Issues #54 and #55).

Run from the repository root:
    streamlit run project/code/dashboard.py

Tab 1 (#54): enter one student and get a risk prediction.
Tab 2 (#55): upload a class CSV; valid students are predicted and
invalid rows are listed with the reason they were skipped.

This file only handles the screen. Validation and prediction reuse
predict.py, so the dashboard gives the same answers as the command line.
Recommendations (#53) are shown automatically once recommend.py exists.
"""

import csv
import io
from pathlib import Path

import streamlit as st

from predict import predict_one, predict_roster

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

try:  # recommend.py is built in #53; until then the dashboard still works.
    from recommend import recommend
except ImportError:
    recommend = None


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
    kept, skipped = [], []
    for number, row in enumerate(data, start=1):
        if has_id and len(row) == len(header):
            label = row[header.index("student_id")].strip() or f"row {number}"
        else:
            label = f"row {number}"
        if len(row) != len(header):
            skipped.append({"student_id": label, "reason": f"has {len(row)} values but the header has "
                            f"{len(header)} columns (check for a missing or extra comma)"})
            continue
        if has_id:
            row = list(row)
            row[header.index("student_id")] = label
            kept.append(row)
        else:
            kept.append([label] + row)

    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(out_header)
    writer.writerows(kept)
    return buffer.getvalue(), skipped, len(data)


def process_upload(text, mode):
    """Everything the Class CSV tab does, without the screen: check the file's
    structure, then predict with predict.py. Returns (results, skipped, total_rows)."""
    clean_text, skipped, total_rows = prepare_upload(text)
    if clean_text.count("\n") > 1:  # at least one row with the right number of values
        results, value_skipped = predict_roster(io.StringIO(clean_text), mode)
        skipped = skipped + value_skipped
    else:  # every row had the wrong number of values
        results = _empty_results(mode)
    return results, skipped, total_rows


def _empty_results(mode):
    import pandas as pd
    columns = ["student_id", "risk_label", "probability_high_risk"]
    if mode == "confirmatory":
        columns.append("grade_setup")
    return pd.DataFrame(columns=columns)


def show_recommendation(student_fields, label, proba):
    if recommend is None:
        st.caption("Support suggestions will appear here once the recommendation engine (#53) is added.")
        return
    for message in recommend(student_fields, {"risk_label": label, "probability_high_risk": proba}):
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
    fields = {"attendance_pct": attendance, "study_hours": study_hours, "failures": failures}
    show_recommendation(fields, label, proba)


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
        results, skipped, total_rows = process_upload(text, mode)
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
        st.download_button("Download results as CSV", results.to_csv(index=False).encode("utf-8"),
                           file_name="sarah_predictions.csv", mime="text/csv")

    if skipped:
        st.write("**Skipped rows** (no prediction was made for these students):")
        st.dataframe(skipped, hide_index=True)


def main():
    st.set_page_config(page_title="SARAH Dashboard")
    st.title("SARAH - Student Academic Risk Assistance Hub")
    st.caption("Prototype for tutors. Results are suggestions for human review, not decisions.")

    mode = st.radio("Prediction mode", list(MODE_LABELS), format_func=MODE_LABELS.get, horizontal=True)
    st.info(MODE_HELP[mode])

    tab_one, tab_class = st.tabs(["One student", "Class CSV"])
    with tab_one:
        single_student_tab(mode)
    with tab_class:
        class_csv_tab(mode)


if __name__ == "__main__":
    main()
