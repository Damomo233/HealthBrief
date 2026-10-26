from pathlib import Path

import requests

import streamlit as st
import pandas as pd
import navigation_state
from branding import LOGO_SVG, render_brand


# =========================================================
# Configuration
# =========================================================

API_BASE_URL = "http://127.0.0.1:8000"
api_session = requests.Session()
api_session.trust_env = False

# =========================================================
# API client function 1: 
# Upload file to frontend API, 
# whose endpoint is for analyzing the uploaded report.
# =========================================================


def analyze_report_via_api(
    uploaded_file
):

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf"
        )
    }


    response = api_session.post(
        f"{API_BASE_URL}/reports/analyze",
        files=files,
        timeout= 20
    )


    response.raise_for_status()


    return response.json()


# =========================================================
# API client function 2: 
# Ask question to Frontend API, 
# whose endpoint is for answering the question
# =========================================================



def ask_agent_via_api(question, current_report, previous_report):

    payload = {
        "question": question,

        "current_report": current_report,

        "previous_report": previous_report
    }


    response = api_session.post(
        f"{API_BASE_URL}/agent/query",
        json=payload,
        timeout=20
    )


    response.raise_for_status()


    return response.json()


# =========================================================
# API client function 3: 
# Save report to Frontend API
# whose endpoint is for persist the report data.
# =========================================================


def save_report_via_api(
    filename,
    report_date,
    lab_results
):

    payload = {
        "filename": filename,
        "report_date": report_date,
        "lab_results": lab_results
    }


    response = api_session.post(
        f"{API_BASE_URL}/reports/save",
        json=payload,
        timeout=20
    )


    response.raise_for_status()

    return response.json()



# =========================================================
# API client function 4: 
# process saved reports from Frontend API，
# whose endpoint is for listing / accessing /  removing saved reports.
# =========================================================


def get_saved_reports_via_api():

    response = api_session.get(
        f"{API_BASE_URL}/reports/saved",
        timeout=20
    )

    response.raise_for_status()

    return response.json()


def get_saved_report_via_api(report_id):

    response = api_session.get(
        f"{API_BASE_URL}/reports/saved/{report_id}",
        timeout=20
    )

    response.raise_for_status()

    return response.json()



def delete_saved_report_via_api(report_id):

    response = api_session.delete(
        f"{API_BASE_URL}/reports/saved/{report_id}",
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# API client function 5: 
# analyze current report from Frontend API，
# whose endpoint is for changing the session state and returning the analysis result.
# =========================================================


def analyze_current_report(uploaded_file):

    api_result = (
        analyze_report_via_api(
            uploaded_file
        )
    )

    st.session_state.lab_results = (
        api_result["lab_results"]
    )

    st.session_state.pdf_text = (
        api_result["extracted_text"]
    )

    st.session_state.current_filename = (
        uploaded_file.name
    )

    st.session_state.current_report_date = (
        api_result.get("report_date")
    )

    st.session_state.current_ready = True
    st.session_state.current_report_saved = False

    st.session_state.last_agent_result = None

    return api_result



# =========================================================
# UI helper function 1:
# Biomarkers classification rules
# =========================================================



def classify_status(value, lower_bound, upper_bound):

    if lower_bound is not None and value < lower_bound:
        return "LOW"

    if upper_bound is not None and value > upper_bound:
        return "HIGH"

    return "NORMAL"


def format_reference_range(lower_bound, upper_bound):

    if lower_bound is not None and upper_bound is not None:
        return f"{lower_bound} - {upper_bound}"

    if lower_bound is not None:
        return f">= {lower_bound}"

    if upper_bound is not None:
        return f"<= {upper_bound}"

    return "Not provided"


# =========================================================
# UI helper function 2:
# Demonstrate report overview by dataframe
# =========================================================


def build_report_dataframe(lab_results):
    
    biomarkers = []

    for item in lab_results["biomarkers"]:

        status = classify_status(
            item["value"],
            item["lower_bound"],
            item["upper_bound"]
        )

        reference_range = format_reference_range(
            item["lower_bound"],
            item["upper_bound"]
        )

        biomarkers.append(
            {
                "Biomarker": item["name"],
                "Value": item["value"],
                "Unit": item["unit"],
                "Reference Range": reference_range,
                "Status": status
            }
        )

    return pd.DataFrame(biomarkers)


# =========================================================
# UI helper function 3:
# Get error message from API response
# =========================================================


def get_api_error_message(
    error
):

    try:

        detail = (
            error.response
            .json()
            .get("detail")
        )

        if isinstance(
            detail,
            dict
        ):

            message = detail.get(
                "message",
                "The request failed."
            )

            request_id = detail.get(
                "request_id"
            )

            if request_id:

                return (
                    f"{message} "
                    f"(Request ID: "
                    f"{request_id})"
                )

            return message


        if isinstance(
            detail,
            str
        ):

            return detail


    except Exception:

        pass


    return (
        "Something went wrong while communicating with HealthBrief."
    )


# =========================================================
# UI helper function 4:
# Reset session state for current and previous reports
# =========================================================


# when the current uploaded file changes.
def reset_current_report_state():
    st.session_state.lab_results = None
    st.session_state.pdf_text = None

    st.session_state.current_ready = False
    st.session_state.current_report_saved = False
    st.session_state.current_filename = None
    st.session_state.current_report_date = None

    st.session_state.last_agent_result = None


 # Clear the previously active report when previous-report source switched.
def reset_previous_source_state():

    st.session_state.previous_lab_results = None
    st.session_state.previous_pdf_text = None

    st.session_state.previous_status = "EMPTY"
    st.session_state.selected_saved_report_id = None
    st.session_state.active_saved_report_id = None

    st.session_state.last_agent_result = None


# =========================================================
# UI helper function 5:
# Change session state when a new previous report is uploaded.
# =========================================================


def previous_upload_changed():
    """
    A newly uploaded previous PDF is only a candidate.
    It is not READY until Analyze Previous Report is clicked.
    """

    st.session_state.previous_lab_results = None
    st.session_state.previous_pdf_text = None
    st.session_state.active_saved_report_id = None
    st.session_state.last_agent_result = None

    uploaded_file = (
        st.session_state.previous_report_uploader
    )

    if uploaded_file is None:
        st.session_state.previous_status = "EMPTY"
    else:
        st.session_state.previous_status = "PENDING"


# -----------------------------
# Page settings
# -----------------------------

st.set_page_config(
    page_title="HealthBrief",
    page_icon=LOGO_SVG,
    layout="wide"
)



# -----------------------------
# Streamlit Initializaiton
# -----------------------------

if "lab_results" not in st.session_state:
    st.session_state.lab_results = None


if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None


if "previous_lab_results" not in st.session_state:
    st.session_state.previous_lab_results = None

    
if "previous_pdf_text" not in st.session_state:
    st.session_state.previous_pdf_text = None


if "last_agent_result" not in st.session_state:
    st.session_state.last_agent_result = None


if "current_report_saved" not in st.session_state:
    st.session_state.current_report_saved = False


if "current_filename" not in st.session_state:
    st.session_state.current_filename = None


if "current_report_date" not in st.session_state:
    st.session_state.current_report_date = None


if "current_ready" not in st.session_state:
    st.session_state.current_ready = False


if "previous_status" not in st.session_state:
    st.session_state.previous_status = "EMPTY"


if "selected_saved_report_id" not in st.session_state:
    st.session_state.selected_saved_report_id = None


if "active_saved_report_id" not in st.session_state:
    st.session_state.active_saved_report_id = None



# -----------------------------
# Title
# -----------------------------

# Dashboard-only styles; homepage and navigation remain untouched.
st.html("<style>" + (Path(__file__).parent / "styles" / "dashboard.css").read_text(encoding="utf-8") + "</style>")

with st.container(key="hb_dashboard"):
    with st.container(key="hb_header"):
        render_brand("Health report analysis workspace", heading=True)


    # =========================================================
    # 1. Current report
    # =========================================================

    with st.container(key="hb_current"):
        st.subheader("Current Health Report")

        uploaded_file = navigation_state.file_uploader(
            "Upload your current PDF health report",
            type=["pdf"],
            key="current_report_uploader",
            on_change=reset_current_report_state
        )

        current_already_saved = False 


        if uploaded_file is None:

            st.info(
                "No current report uploaded yet. "
                "Upload a text-based PDF health report to begin."
            )

        else:

            st.caption(
                f"Selected: {uploaded_file.name}"
            )


            try:

                saved_reports_for_check = (
                    get_saved_reports_via_api()
                )


                current_already_saved = any(
                    report["filename"]
                    ==
                    uploaded_file.name

                    for report
                    in saved_reports_for_check
                )


            except requests.exceptions.RequestException:
                current_already_saved = False


            if current_already_saved:

                st.caption(
                    "This report is already saved in history."
                )


            with st.container(key="hb_current_actions"):
                button_col1, button_col2, _ = st.columns(
                [2.3, 1.7, 5],
                gap="small"
                )


                with button_col1:

                    analyze_current_clicked = st.button(
                        "Analyze Current Report",
                        key="analyze_current",
                        type="primary",
                        width="stretch",
                        disabled=(
                            uploaded_file is None
                        )
                    )


                with button_col2:

                    save_current_clicked = st.button(
                        "Save to History",
                        key="save_current_report",
                        width="stretch",
                        disabled=(
                            uploaded_file is None
                            or st.session_state.current_report_saved
                            or current_already_saved
                        )
                    )


            if analyze_current_clicked:

                try:

                    with st.spinner(
                        "Analyzing current report..."
                    ):

                        analyze_current_report(
                            uploaded_file
                        )

                    st.success(
                         "Current report analyzed successfully."
                    )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "HealthBrief backend is not running."
                        "Make sure FastAPI is running on port 8000."
                    )


                except requests.exceptions.HTTPError as error:

                    st.error(
                        get_api_error_message(error)
                    )


                except requests.exceptions.RequestException as error:

                    st.error(
                                f"Request failed: {type(error).__name__}: {error}"
                                )


            if save_current_clicked:

                try:
                    # Auto-analyze if necessary
                    if not st.session_state.current_ready:

                        with st.spinner(
                            "Analyzing report before saving..."
                        ):

                            analyze_current_report(
                                uploaded_file
                            )

                    save_report_via_api(
                        filename=(
                            st.session_state.current_filename
                        ),
                        report_date=(
                            st.session_state.current_report_date
                        ),
                        lab_results=(
                            st.session_state.lab_results
                        )
                    )

                    st.session_state.current_report_saved = True

                    st.success(
                        "Report saved to history."
                    )


                except requests.exceptions.HTTPError as error:

                    st.error(
                        get_api_error_message(error)
                    )


                except requests.exceptions.RequestException:

                    st.error(
                        "Unable to connect to the HealthBrief backend."
                    )

    

        # =========================================================
        # 2. Current report overview
        # =========================================================


    with st.container(key="hb_overview"):
        st.subheader("Report Overview")

        if st.session_state.pdf_text:
            with st.expander("View full extracted report text"):
                st.text(st.session_state.pdf_text)

        with st.container(key="hb_overview_columns"):
            results_column, summary_column = st.columns([3.1, 1.35], gap="large")

            with results_column:
                with st.container(key="hb_biomarkers"):
                    st.markdown("#### Biomarker Results")

                    if st.session_state.lab_results is None:
                        st.info(
                            "Analyze your current health report to view the extracted biomarkers."
                        )
                    else:
                        df = build_report_dataframe(
                            st.session_state.lab_results
                        )
                        status_styles = {
                            "NORMAL": "color: #226c59; background-color: #edf7f2; font-weight: 600",
                            "HIGH": "color: #855e24; background-color: #fbf3e5; font-weight: 600",
                            "LOW": "color: #935266; background-color: #fbf0f3; font-weight: 600",
                        }
                        st.dataframe(
                            df.style.format({"Value": str}).map(lambda value: status_styles.get(value, ""), subset=["Status"]),
                            width="stretch",
                            hide_index=True,
                            row_height=36,
                            column_config={
                                "Biomarker": st.column_config.TextColumn(width="medium"),
                                "Reference Range": st.column_config.TextColumn(width="medium"),
                                "Status": st.column_config.TextColumn(width="small"),
                            },
                        )
                        abnormal_count = len(
                            df[
                                df["Status"] != "NORMAL"
                            ]
                        )

            with summary_column:
                with st.container(key="hb_summary"):
                    st.markdown("#### Report Summary")

                    if st.session_state.lab_results is not None:
                        with st.container(key="hb_summary_counts"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Total biomarkers", len(df))
                            with col2:
                                st.metric("Markers needing attention", abnormal_count)

                    with st.container(key="hb_date"):
                        st.caption("Check-up Date")
                        if st.session_state.current_report_date is not None:
                            st.caption(
                                "Detected check-up date: "
                                f"{st.session_state.current_report_date}"
                            )
                        else:
                            st.caption("Check-up date could not be detected.")


    # =========================================================
    # 3. Previous report
    # =========================================================

    with st.container(key="hb_previous"):
        with st.container(key="hb_previous_heading"):
            st.html('<div class="hb-previous-title"><h3>Previous Report</h3><span class="hb-optional">Optional</span></div>')

        st.caption(
            "Upload an older report if you want HealthBrief to compare biomarker changes."
        )


        previous_source = st.radio(
            "Previous report source",
            [
                "Upload PDF",
                "Saved Report"
            ],
            key="previous_source",
            horizontal=True,
            persist_state="session",
            on_change=navigation_state.previous_source_changed,
            args=(reset_previous_source_state,)
        )



        if previous_source == "Upload PDF":

            previous_file = navigation_state.file_uploader(
                "Upload a previous PDF report for trend comparison",
                type=["pdf"],
                key="previous_report_uploader",
                on_change=previous_upload_changed
            )
    
            if previous_file is not None:

                   if previous_file is not None:

                    if st.button(
                        "Analyze Previous Report",
                        key="analyze_previous"
                    ):

                        try:

                            with st.spinner(
                                "Analyzing previous report..."
                            ):

                                api_result = (
                                    analyze_report_via_api(
                                        previous_file
                                    )
                                )


                            st.session_state.previous_lab_results = (
                                api_result["lab_results"]
                            )

                            st.session_state.previous_pdf_text = (
                                api_result["extracted_text"]
                            )


                            st.session_state.previous_status = (
                                "READY"
                            )

                            st.session_state.active_saved_report_id = (
                                None
                            )

                            st.session_state.last_agent_result = (
                                None
                            )


                            st.success(
                                "Previous report analyzed."
                            )


                        except requests.exceptions.HTTPError as error:

                            st.error(
                                get_api_error_message(
                                    error
                                )
                            )


                        except requests.exceptions.RequestException:

                            st.error(
                                "Unable to connect to "
                                "the HealthBrief backend."
                            )
                    

        else:

            try:

                saved_reports = (
                    get_saved_reports_via_api()
                )

            except requests.exceptions.RequestException:

                saved_reports = []

                st.error(
                    "Unable to load saved reports."
                )


            if not saved_reports:

                st.info(
                    "No saved reports are available."
                )

            else:
                selected_report = None

                for report in saved_reports:

                    if (
                        report["id"]
                        ==
                        st.session_state.selected_saved_report_id
                    ):
                        selected_report = report
                        break


                if selected_report is None:

                    current_saved_label = (
                        "Select a saved report"
                    )

                else:

                    checkup_date = (
                        selected_report.get(
                            "report_date"
                        )
                        or
                        "Check-up date unavailable"
                    )

                    current_saved_label = (
                        f"{checkup_date} — "
                        f"{selected_report['filename']}"
                    )


                with st.popover(
                    current_saved_label,
                    use_container_width=True
                ):
            

                    for report in saved_reports:

                        checkup_date = (
                            report.get(
                                "report_date"
                            )
                            or
                            "Check-up date unavailable"
                        )


                        label = (
                            f"{checkup_date} — "
                            f"{report['filename']}"
                        )


                        name_col, delete_col = (
                            st.columns(
                                [9, 1],
                                gap="small"
                            )
                        )


                        with name_col:

                            if st.button(
                                label,
                                key=(
                                    f"choose_saved_"
                                    f"{report['id']}"
                                ),
                                type="tertiary",
                                use_container_width=True
                            ):

                                st.session_state.selected_saved_report_id = (
                                    report["id"]
                                )

                                st.session_state.previous_lab_results = (
                                    None
                                )

                                st.session_state.active_saved_report_id = (
                                    None
                                )

                                st.session_state.previous_status = (
                                    "PENDING"
                                )

                                st.session_state.last_agent_result = (
                                    None
                                )

                                st.rerun()


                        with delete_col:

                            if st.button(
                                "✕",
                                key=(
                                    f"delete_saved_"
                                    f"{report['id']}"
                                ),
                                help="Delete saved report"
                            ):

                                delete_saved_report_via_api(
                                    report["id"]
                                )


                                if (
                                    st.session_state.selected_saved_report_id
                                    ==
                                    report["id"]
                                ):

                                    st.session_state.selected_saved_report_id = (
                                        None
                                    )


                                if (
                                    st.session_state.active_saved_report_id
                                    ==
                                    report["id"]
                                ):

                                    st.session_state.active_saved_report_id = (
                                        None
                                    )

                                    st.session_state.previous_lab_results = (
                                        None
                                    )

                                    st.session_state.previous_status = (
                                        "EMPTY"
                                    )


                                st.session_state.last_agent_result = (
                                    None
                                )

                                st.rerun()


                use_saved_clicked = st.button(
                    "Use as Previous Report",
                    key="use_saved_previous",
                    disabled=(
                        st.session_state.selected_saved_report_id is None
                    )
                )            


                if use_saved_clicked:

                    try:

                        report = (
                            get_saved_report_via_api(
                                st.session_state.selected_saved_report_id
                            )
                        )


                        st.session_state.previous_lab_results = (
                            report["lab_results"]
                        )

                        st.session_state.previous_pdf_text = (
                            None
                        )

                        st.session_state.active_saved_report_id = (
                            report["id"]
                        )

                        st.session_state.previous_status = (
                            "READY"
                        )

                        st.session_state.last_agent_result = (
                            None
                        )


                        st.success(
                            "Saved report is ready for comparison."
                        )


                    except requests.exceptions.HTTPError as error:

                        st.error(
                            get_api_error_message(
                                error
                            )
                        )
    
    

        # -----------------------------
        # Chat area
        # -----------------------------

    with st.container(key="hb_ask"):
        st.subheader("Ask HealthBrief")


        ask_disabled = (
        not st.session_state.current_ready
        or
        st.session_state.previous_status == "PENDING"
        )

        st.caption("Ask about your results and prepare questions for your next doctor visit.")

        with st.container(key="hb_composer"):
            question_column, ask_column = st.columns([5, 1.2], gap="small", vertical_alignment="bottom")
            with question_column:
                question = st.text_input(
                    "Ask a question about your report",
                    placeholder=(
                        "e.g. Why is my LDL high? "
                        "Has it improved since my previous report?"
                    ),
                    disabled=ask_disabled,
                    key="healthbrief_question",
                    persist_state="session"
                )

            with ask_column:
                ask_button = st.button(
                    "Ask HealthBrief",
                    key="ask_healthbrief",
                    type="primary",
                    disabled=ask_disabled,
                    width="stretch"
                )

        if ask_button:

            if not question.strip():

                st.warning(
                    "Please enter a question first."
                )

            elif st.session_state.lab_results is None:

                st.caption(
                "Analyze your current report first to enable HealthBrief."
                )

            else:

                try:

                    with st.spinner(
                        "HealthBrief is analyzing your question..."
                    ):

                        result = ask_agent_via_api(
                            question=question,

                            current_report=(
                                st.session_state.lab_results
                            ),

                            previous_report=(
                                st.session_state.previous_lab_results
                            )
                        )

                        st.session_state.last_agent_result = result

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Unable to connect to the HealthBrief backend. "
                        "Make sure FastAPI is running."
                    )

                except requests.exceptions.HTTPError as error:

                  st.error(get_api_error_message(error))

                except requests.exceptions.RequestException:

                    st.error(
                        "A network error occurred while contacting the backend."
                    )


        # =========================================================
        # Agent answer
        # =========================================================

        if st.session_state.last_agent_result:

            with st.container(key="hb_answer"):
                result = st.session_state.last_agent_result

                st.subheader(
                    "HealthBrief Answer"
                )

                st.write(
                    result["answer"]
                )


                with st.expander(
                    "View agent execution details"
                ):

                    st.write(
                        "Category:",
                        result["category"]
                    )

                    st.write(
                        "Selected biomarker:",
                        result["biomarker"]
                    )

                    st.write(
                        "Tool result:"
                    )

                    st.json(
                        result["tool_result"]
                    )

    # -----------------------------
    # Disclaimer
    # -----------------------------

    st.divider()

    st.caption(
        "HealthBrief is an educational project and does not provide medical diagnosis or medical advice."
    )