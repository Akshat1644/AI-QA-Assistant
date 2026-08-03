import streamlit as st
import pandas as pd
import json

from gemini_service import generate_ai_response
from prompts import RISK_ANALYSIS_PROMPT
from app.export_service import convert_df_to_excel


def render_risk_analysis(requirement):

    if not requirement.strip():
        st.warning("Please enter a software requirement.")
        return

    prompt = RISK_ANALYSIS_PROMPT.format(
        requirement=requirement
    )

    with st.spinner("Analyzing Project Risks..."):

        try:

            result = generate_ai_response(prompt)

            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            data = json.loads(result)

            df = pd.DataFrame(data)

            df.columns = [
                "Risk Area",
                "Severity",
                "Reason",
                "Recommendation"
            ]

            st.session_state["risk_df"] = df

            high = len(df[df["Severity"] == "High"])
            medium = len(df[df["Severity"] == "Medium"])
            low = len(df[df["Severity"] == "Low"])

            total = len(df)

            risk_score = round(
                (
                    (high * 3)
                    + (medium * 2)
                    + (low * 1)
                )
                /
                (total * 3)
                * 100
            )

            st.session_state["risk_score"] = risk_score
            st.session_state["high_risk"] = high
            st.session_state["medium_risk"] = medium
            st.session_state["low_risk"] = low

        except json.JSONDecodeError:

            st.error("Unable to parse Risk Analysis response.")
            return

        except Exception:

            st.error("Failed to analyze project risks.")
            return

    df = st.session_state["risk_df"]

    risk_score = st.session_state["risk_score"]

    high = st.session_state["high_risk"]
    medium = st.session_state["medium_risk"]
    low = st.session_state["low_risk"]

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

        if row["Severity"] == "High":
            icon = "🔴"

        elif row["Severity"] == "Medium":
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
            st.write(f"**{icon} {row['Severity']}**")

            st.markdown("### ❗ Reason")

            reasons = str(row["Reason"]).split(",")

            for reason in reasons:

                reason = reason.strip()

                if reason:
                    st.markdown(f"- {reason}")

            st.markdown("### 💡 Recommendation")

            recommendations = str(row["Recommendation"]).split(",")

            for recommendation in recommendations:

                recommendation = recommendation.strip()

                if recommendation:
                    st.success(recommendation)

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Risk_Analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="risk_excel_download"
    )