import re
import logging
import streamlit as st

from gemini_service import generate_ai_response
from prompts import QUALITY_SCORE_PROMPT

from utils.session_manager import save, load


def render_quality_score(requirement):

    # ==========================================================
    # Generate Quality Score
    # ==========================================================

    if load("quality_result") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = QUALITY_SCORE_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Requirement Quality..."):

            try:

                result = generate_ai_response(prompt)

                save("quality_result", result)

                st.success("✅ Requirement Quality Analysis generated successfully.")

            except Exception as e:

                logging.exception(e)

                st.error("Failed to analyze requirement quality.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    result = load("quality_result")

    if result is None:
        return

    # -----------------------------
    # Extract Scores
    # -----------------------------

    try:

        completeness = int(re.search(r"COMPLETENESS:\s*(\d+)", result).group(1))
        clarity = int(re.search(r"CLARITY:\s*(\d+)", result).group(1))
        testability = int(re.search(r"TESTABILITY:\s*(\d+)", result).group(1))
        ambiguity = int(re.search(r"AMBIGUITY:\s*(\d+)", result).group(1))

    except Exception:

        st.error("Unable to parse Quality Score response.")
        return

    overall = round(
        (
            completeness
            + clarity
            + testability
            + ambiguity
        ) / 4
    )

    # -----------------------------
    # Dashboard
    # -----------------------------

    st.subheader("📊 Requirement Quality Dashboard")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Overall", f"{overall}%")
    col2.metric("Completeness", f"{completeness}%")
    col3.metric("Clarity", f"{clarity}%")
    col4.metric("Testability", f"{testability}%")
    col5.metric("Ambiguity", f"{ambiguity}%")

    st.progress(overall / 100)

    if overall >= 80:

        st.success("🟢 Excellent Requirement Quality")

    elif overall >= 60:

        st.warning("🟡 Good Requirement Quality")

    else:

        st.error("🔴 Poor Requirement Quality")

    st.divider()

    # -----------------------------
    # Strengths
    # -----------------------------

    strengths = re.search(
        r"STRENGTHS:(.*?)WEAKNESSES:",
        result,
        re.S
    )

    if strengths:

        st.subheader("✅ Strengths")

        for line in strengths.group(1).split("\n"):

            if line.strip().startswith("-"):

                st.success(line.strip()[2:])

    # -----------------------------
    # Weaknesses
    # -----------------------------

    weaknesses = re.search(
        r"WEAKNESSES:(.*?)RECOMMENDATIONS:",
        result,
        re.S
    )

    if weaknesses:

        st.subheader("⚠️ Weaknesses")

        for line in weaknesses.group(1).split("\n"):

            if line.strip().startswith("-"):

                st.warning(line.strip()[2:])

    # -----------------------------
    # Recommendations
    # -----------------------------

    recommendations = re.search(
        r"RECOMMENDATIONS:(.*)",
        result,
        re.S
    )

    if recommendations:

        st.subheader("💡 Recommendations")

        for line in recommendations.group(1).split("\n"):

            if line.strip().startswith("-"):

                st.info(line.strip()[2:])

    # -----------------------------
    # Download Report
    # -----------------------------

    st.download_button(
        label="📄 Download Report",
        data=result,
        file_name="Requirement_Quality_Report.txt",
        mime="text/plain",
        key="quality_report_download"
    )