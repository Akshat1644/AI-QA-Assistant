import streamlit as st
import pandas as pd
import json

from gemini_service import generate_ai_response
from prompts import REGRESSION_IMPACT_PROMPT
from app.export_service import convert_df_to_excel


def render_regression_analysis(requirement):

    if not requirement.strip():
        st.warning("Please enter a software requirement.")
        return

    prompt = REGRESSION_IMPACT_PROMPT.format(
        requirement=requirement
    )

    with st.spinner("Analyzing Regression Impact..."):

        try:

            result = generate_ai_response(prompt)

            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            data = json.loads(result)

            df = pd.DataFrame(data)

            df.columns = [
                "Affected Module",
                "Impact Level",
                "Reason",
                "Recommended Regression Tests"
            ]

            st.session_state["regression_df"] = df

            high = len(df[df["Impact Level"] == "High"])
            medium = len(df[df["Impact Level"] == "Medium"])
            low = len(df[df["Impact Level"] == "Low"])

            total = len(df)

            score = round(
                (
                    high * 3 +
                    medium * 2 +
                    low
                ) / (total * 3) * 100
            ) if total else 0

            st.session_state["regression_score"] = score
            st.session_state["reg_high"] = high
            st.session_state["reg_medium"] = medium
            st.session_state["reg_low"] = low

        except json.JSONDecodeError:

            st.error("Unable to parse Regression Analysis response.")
            return

        except Exception:

            st.error("Failed to analyze Regression Impact.")
            return

    df = st.session_state["regression_df"]

    score = st.session_state["regression_score"]

    high = st.session_state["reg_high"]
    medium = st.session_state["reg_medium"]
    low = st.session_state["reg_low"]

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

        if row["Impact Level"] == "High":
            icon = "🔴"

        elif row["Impact Level"] == "Medium":
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
            st.write(f"**{icon} {row['Impact Level']}**")

            st.markdown("### ❓ Reason")

            reasons = str(row["Reason"]).split(",")

            for reason in reasons:

                reason = reason.strip()

                if reason:
                    st.markdown(f"- {reason}")

            st.markdown("### ✅ Recommended Regression Tests")

            tests = str(
                row["Recommended Regression Tests"]
            ).split(",")

            for test in tests:

                test = test.strip()

                if test:
                    st.success(test)

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Regression_Impact.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="regression_excel"
    )