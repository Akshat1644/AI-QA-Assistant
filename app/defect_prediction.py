import re
import logging
import streamlit as st

from gemini_service import generate_ai_response
from prompts import DEFECT_PREDICTION_PROMPT

from utils.session_manager import save, load


def render_defect_prediction(requirement):

    # ==========================================================
    # Generate Defect Prediction
    # ==========================================================

    if requirement.strip():

        prompt = DEFECT_PREDICTION_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Predicting Defects..."):

            try:

                result = generate_ai_response(prompt)

                save("defect_prediction", result)

                st.success("✅ Defect Prediction generated successfully.")

            except Exception as e:

                logging.exception(e)

                st.error("Failed to predict defects.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    result = load("defect_prediction")

    if result is None:
        return

    # -------------------------------------------------------
    # Extract Sections
    # -------------------------------------------------------

    defect_areas = re.search(
        r"## Potential Defect-Prone Areas(.*?)## Possible Production Issues",
        result,
        re.S
    )

    production_issues = re.search(
        r"## Possible Production Issues(.*?)## Likely Severity",
        result,
        re.S
    )

    severity = re.search(
        r"## Likely Severity(.*?)## Recommended Testing Focus",
        result,
        re.S
    )

    testing_focus = re.search(
        r"## Recommended Testing Focus(.*?)## Prevention Suggestions",
        result,
        re.S
    )

    prevention = re.search(
        r"## Prevention Suggestions(.*)",
        result,
        re.S
    )

    # -------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------

    st.subheader("🐞 AI Defect Prediction")

    if severity:

        sev = severity.group(1).strip()

        if "High" in sev:

            st.error("🔴 High Defect Probability")

        elif "Medium" in sev:

            st.warning("🟡 Medium Defect Probability")

        else:

            st.success("🟢 Low Defect Probability")

    st.divider()

    # -------------------------------------------------------
    # Potential Defect Areas
    # -------------------------------------------------------

    if defect_areas:

        st.subheader("📌 Potential Defect-Prone Areas")

        for line in defect_areas.group(1).split("\n"):

            if line.strip().startswith("-"):

                st.warning(line.strip()[2:])

    # -------------------------------------------------------
    # Production Issues
    # -------------------------------------------------------

    if production_issues:

        st.subheader("⚠️ Possible Production Issues")

        for line in production_issues.group(1).split("\n"):

            if line.strip().startswith("-"):

                st.error(line.strip()[2:])

    # -------------------------------------------------------
    # Testing Focus
    # -------------------------------------------------------

    if testing_focus:

        st.subheader("🧪 Recommended Testing Focus")

        for line in testing_focus.group(1).split("\n"):

            if line.strip().startswith("-"):

                st.info(line.strip()[2:])

    # -------------------------------------------------------
    # Prevention Suggestions
    # -------------------------------------------------------

    if prevention:

        st.subheader("✅ Prevention Suggestions")

        for line in prevention.group(1).split("\n"):

            if line.strip().startswith("-"):

                st.success(line.strip()[2:])

    # -------------------------------------------------------
    # Download
    # -------------------------------------------------------

    st.download_button(
        label="📄 Download Report",
        data=result,
        file_name="Defect_Prediction_Report.txt",
        mime="text/plain",
        key="defect_prediction_report"
    )