import streamlit as st
import json
import logging

from gemini_service import generate_ai_response
from prompts import RISK_ANALYSIS_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_risk_analysis(requirement):

    # ==========================================================
    # Generate Risk Analysis
    # ==========================================================

    if load("risk_df") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = RISK_ANALYSIS_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Project Risks..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                expected_columns = [
                    "Risk Area",
                    "Severity",
                    "Reason",
                    "Recommendation"
                ]

                if len(df.columns) != len(expected_columns):

                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                high = len(df[df["Severity"] == "High"])
                medium = len(df[df["Severity"] == "Medium"])
                low = len(df[df["Severity"] == "Low"])

                total = len(df)

                risk_score = (
                    round(
                        (
                            (high * 3)
                            + (medium * 2)
                            + (low * 1)
                        )
                        /
                        (total * 3)
                        * 100
                    )
                    if total > 0
                    else 0
                )

                save("risk_df", df)
                save("risk_score", risk_score)
                save("high_risk", high)
                save("medium_risk", medium)
                save("low_risk", low)

                st.success("✅ Risk Analysis generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse Risk Analysis response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to analyze project risks.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    df = load("risk_df")

    if df is None:
        return

    risk_score = load("risk_score")
    high = load("high_risk")
    medium = load("medium_risk")
    low = load("low_risk")

    st.subheader("⚠️ AI Risk Analysis Dashboard")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("🔴 High", high)
    metric2.metric("🟡 Medium", medium)
    metric3.metric("🟢 Low", low)
    metric4.metric("Risk Score", f"{risk_score}%")

    st.progress(risk_score / 100)

    if risk_score >= 70:

        st.error("🔴 Overall Risk: High")

    elif risk_score >= 40:

        st.warning("🟡 Overall Risk: Medium")

    else:

        st.success("🟢 Overall Risk: Low")

    st.divider()

    st.subheader("📋 Risk Details")

    for _, row in df.iterrows():

        severity = str(row["Severity"]).title()

        if severity == "High":
            icon = "🔴"

        elif severity == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        with st.expander(
            f"{icon} {row['Risk Area']}",
            expanded=False
        ):

            st.markdown("### 📌 Risk Area")
            st.info(row["Risk Area"])

            st.markdown("### 📊 Severity")
            st.write(f"**{icon} {severity}**")

            st.markdown("### ❗ Reason")

            reasons = row["Reason"]

            if not isinstance(reasons, list):

                reasons = [
                    r.strip()
                    for r in str(reasons).split(",")
                    if r.strip()
                ]

            for reason in reasons:

                st.markdown(f"- {reason}")

            st.markdown("### 💡 Recommendation")

            recommendations = row["Recommendation"]

            if not isinstance(recommendations, list):

                recommendations = [
                    r.strip()
                    for r in str(recommendations).split(",")
                    if r.strip()
                ]

            for recommendation in recommendations:

                st.success(recommendation)

    download_excel(
        df=df,
        filename="Risk_Analysis.xlsx",
        key="risk_excel_download"
    )