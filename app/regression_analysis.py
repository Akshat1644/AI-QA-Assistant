import streamlit as st
import json
import logging

from gemini_service import generate_ai_response
from prompts import REGRESSION_IMPACT_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_regression_analysis(requirement):

    # ==========================================================
    # Generate Regression Analysis
    # ==========================================================

    if load("regression_df") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return
                
        prompt = REGRESSION_IMPACT_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Regression Impact..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                expected_columns = [
                    "Affected Module",
                    "Impact Level",
                    "Reason",
                    "Recommended Regression Tests"
                ]

                if len(df.columns) != len(expected_columns):

                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                high = len(df[df["Impact Level"] == "High"])
                medium = len(df[df["Impact Level"] == "Medium"])
                low = len(df[df["Impact Level"] == "Low"])

                total = len(df)

                score = (
                    round(
                        (
                            high * 3 +
                            medium * 2 +
                            low
                        ) / (total * 3) * 100
                    )
                    if total > 0
                    else 0
                )

                save("regression_df", df)
                save("regression_score", score)
                save("reg_high", high)
                save("reg_medium", medium)
                save("reg_low", low)

                st.success("✅ Regression Impact Analysis generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse Regression Analysis response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to analyze Regression Impact.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    df = load("regression_df")

    if df is None:
        return

    score = load("regression_score")
    high = load("reg_high")
    medium = load("reg_medium")
    low = load("reg_low")

    st.subheader("🔄 AI Regression Impact Dashboard")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("🔴 High", high)
    metric2.metric("🟡 Medium", medium)
    metric3.metric("🟢 Low", low)
    metric4.metric("Impact Score", f"{score}%")

    st.progress(score / 100)

    if score >= 70:

        st.error("🔴 Extensive Regression Testing Required")

    elif score >= 40:

        st.warning("🟡 Moderate Regression Testing Required")

    else:

        st.success("🟢 Minimal Regression Testing Required")

    st.divider()

    st.subheader("📋 Regression Impact Details")

    for _, row in df.iterrows():

        impact = str(row["Impact Level"]).title()

        if impact == "High":
            icon = "🔴"

        elif impact == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        with st.expander(
            f"{icon} {row['Affected Module']}",
            expanded=False
        ):

            st.markdown("### 📦 Affected Module")
            st.info(row["Affected Module"])

            st.markdown("### 📊 Impact Level")
            st.write(f"**{icon} {impact}**")

            st.markdown("### ❓ Reason")

            reasons = row["Reason"]

            if not isinstance(reasons, list):

                reasons = [
                    r.strip()
                    for r in str(reasons).split(",")
                    if r.strip()
                ]

            for reason in reasons:

                st.markdown(f"- {reason}")

            st.markdown("### ✅ Recommended Regression Tests")

            tests = row["Recommended Regression Tests"]

            if not isinstance(tests, list):

                tests = [
                    t.strip()
                    for t in str(tests).split(",")
                    if t.strip()
                ]

            for test in tests:

                st.success(test)

    download_excel(
        df=df,
        filename="Regression_Impact.xlsx",
        key="regression_excel"
    )