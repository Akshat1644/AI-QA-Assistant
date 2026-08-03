import streamlit as st
import json
import random
import logging

from datetime import datetime

from gemini_service import generate_ai_response
from prompts import DEFECT_REPORT_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_defect_report(requirement):

    # ==========================================================
    # Generate Defect Report
    # ==========================================================

    if requirement.strip():

        prompt = DEFECT_REPORT_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating Professional Defect Report..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                expected_columns = [
                    "Bug Summary",
                    "Description",
                    "Steps To Reproduce",
                    "Expected Result",
                    "Actual Result",
                    "Severity",
                    "Priority",
                    "Root Cause",
                    "Suggested Fix"
                ]

                if len(df.columns) != len(expected_columns):

                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                save("defect_df", df)

                st.success("✅ Defect Report generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse Defect Report response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to generate Defect Report.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    df = load("defect_df")

    if df is None:
        return

    row = df.iloc[0]

    bug_id = f"AI-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"

    st.subheader("🐞 AI Defect Report Dashboard")

    top1, top2 = st.columns([4, 1])

    with top1:

        st.info(f"🆔 **Bug ID:** {bug_id}")

    with top2:

        st.success("🟢 Open")

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    severity = str(row["Severity"]).title()
    priority = str(row["Priority"]).title()

    if severity == "Critical":
        severity_display = "🚨 Critical"

    elif severity == "High":
        severity_display = "🔴 High"

    elif severity == "Medium":
        severity_display = "🟡 Medium"

    else:
        severity_display = "🟢 Low"

    if priority == "High":
        priority_display = "🔴 High"

    elif priority == "Medium":
        priority_display = "🟡 Medium"

    else:
        priority_display = "🟢 Low"

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Severity", severity_display)
    metric2.metric("Priority", priority_display)
    metric3.metric("Status", "Open")

    st.divider()

    # -------------------------------------------------
    # Bug Summary
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown("### 🐞 Bug Summary")

        st.error(row["Bug Summary"])

    # -------------------------------------------------
    # Description
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown("### 📝 Description")

        st.write(row["Description"])

    # -------------------------------------------------
    # Steps To Reproduce
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown("### 🔄 Steps To Reproduce")

        steps = row["Steps To Reproduce"]

        if not isinstance(steps, list):

            steps = [
                s.strip()
                for s in str(steps).split(",")
                if s.strip()
            ]

        for i, step in enumerate(steps, start=1):

            st.info(f"Step {i}: {step}")

    # -------------------------------------------------
    # Result Comparison
    # -------------------------------------------------

    st.markdown("### 📊 Result Comparison")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("#### ✅ Expected Result")

            st.success(row["Expected Result"])

    with col2:

        with st.container(border=True):

            st.markdown("#### ❌ Actual Result")

            st.error(row["Actual Result"])

    # -------------------------------------------------
    # Root Cause
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown("### 🔍 Root Cause")

        causes = row["Root Cause"]

        if not isinstance(causes, list):

            causes = [
                c.strip()
                for c in str(causes).split(",")
                if c.strip()
            ]

        for cause in causes:

            st.warning(cause)

    # -------------------------------------------------
    # Suggested Fix
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown("### 🛠 Suggested Fix")

        fixes = row["Suggested Fix"]

        if not isinstance(fixes, list):

            fixes = [
                f.strip()
                for f in str(fixes).split(",")
                if f.strip()
            ]

        for fix in fixes:

            st.success(fix)

    # -------------------------------------------------
    # AI Verdict
    # -------------------------------------------------

    st.divider()

    st.markdown("## 🤖 AI Verdict")

    if severity == "Critical":

        verdict = (
            "This defect is release-blocking and should be fixed before deployment."
        )

    elif severity == "High":

        verdict = (
            "This defect has a significant business impact and should be prioritized before production release."
        )

    elif severity == "Medium":

        verdict = (
            "The defect should be resolved before production to maintain application quality."
        )

    else:

        verdict = (
            "This defect has a relatively low impact and can be scheduled for a future release."
        )

    st.info(verdict)

    # -------------------------------------------------
    # Downloads
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        download_excel(
            df=df,
            filename="AI_Defect_Report.xlsx",
            key="defect_report_excel"
        )

    with col2:

        st.download_button(
            label="📄 Download Report",
            data=json.dumps(
                row.to_dict(),
                indent=4
            ),
            file_name="AI_Defect_Report.txt",
            mime="text/plain",
            key="defect_report_txt"
        )