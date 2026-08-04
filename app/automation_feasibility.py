import streamlit as st
import pandas as pd
import json
import logging

from gemini_service import generate_ai_response
from prompts import AUTOMATION_FEASIBILITY_PROMPT

from utils.session_manager import save, load
from utils.downloads import download_excel


def render_automation_feasibility(requirement):

    # ----------------------------------------------------------
    # Generate Automation Feasibility
    # ----------------------------------------------------------

    if load("automation_df") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = AUTOMATION_FEASIBILITY_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Automation Feasibility..."):

            try:

                result = generate_ai_response(prompt)

                result = (
                    result.replace("```json", "")
                          .replace("```", "")
                          .strip()
                )

                data = json.loads(result)

                df = pd.DataFrame(data)

                if df.empty:

                    st.error("No Automation Analysis was generated.")
                    return

                expected_columns = [
                    "Automation Score",
                    "Feasibility",
                    "Recommended Framework",
                    "Framework Reason",
                    "Automation Challenges",
                    "Automation Strategy",
                    "Estimated Effort",
                    "Maintenance Level",
                    "Summary"
                ]

                if len(df.columns) != len(expected_columns):

                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                save("automation_df", df)

                st.success("✅ Automation Feasibility generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse Automation Feasibility response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to analyze Automation Feasibility.")
                return

    # ----------------------------------------------------------
    # Display Saved Output
    # ----------------------------------------------------------

    df = load("automation_df")

    if df is None:
        return

    row = df.iloc[0]

    st.subheader("🤖 AI Automation Feasibility Dashboard")

    score = int(row["Automation Score"])

    feasibility = str(row["Feasibility"]).title()

    if feasibility == "High":
        feasibility_display = "🟢 Highly Automatable"

    elif feasibility == "Medium":
        feasibility_display = "🟡 Partially Automatable"

    else:
        feasibility_display = "🔴 Low Automation Feasibility"

    challenge_count = (
        len(row["Automation Challenges"])
        if isinstance(row["Automation Challenges"], list)
        else len(str(row["Automation Challenges"]).split(","))
    )

    strategy_count = (
        len(row["Automation Strategy"])
        if isinstance(row["Automation Strategy"], list)
        else len(str(row["Automation Strategy"]).split(","))
    )

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Automation Score",
        f"{score}%"
    )

    metric2.metric(
        "Feasibility",
        feasibility_display
    )

    metric3.metric(
        "Framework",
        row["Recommended Framework"]
    )

    st.progress(score / 100)

    st.divider()

    # -------------------------------------------------
    # Framework
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown("### ⚙️ Recommended Framework")

        st.success(row["Recommended Framework"])

        st.markdown("#### Why this framework?")

        st.info(row["Framework Reason"])

    # -------------------------------------------------
    # Challenges
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown(
            f"### ⚠️ Automation Challenges ({challenge_count})"
        )

        challenges = row["Automation Challenges"]

        if not isinstance(challenges, list):

            challenges = [
                c.strip()
                for c in str(challenges).split(",")
                if c.strip()
            ]

        for challenge in challenges:

            st.warning(challenge)

    # -------------------------------------------------
    # Strategy
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown(
            f"### 🚀 Automation Strategy ({strategy_count})"
        )

        strategy = row["Automation Strategy"]

        if not isinstance(strategy, list):

            strategy = [
                s.strip()
                for s in str(strategy).split(",")
                if s.strip()
            ]

        for item in strategy:

            st.success(item)

    # -------------------------------------------------
    # Additional Details
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("### ⏱ Estimated Effort")

            st.info(row["Estimated Effort"])

    with col2:

        with st.container(border=True):

            st.markdown("### 🔧 Maintenance Level")

            st.info(row["Maintenance Level"])

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    with st.container(border=True):

        st.markdown("### 🤖 AI Summary")

        st.write(row["Summary"])

    st.divider()

    # -------------------------------------------------
    # Downloads
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        download_excel(
            df=df,
            filename="Automation_Feasibility.xlsx",
            key="automation_excel"
        )

    with col2:

        st.download_button(
            label="📄 Download Report",
            data=json.dumps(
                row.to_dict(),
                indent=4
            ),
            file_name="Automation_Feasibility.txt",
            mime="text/plain",
            key="automation_txt"
        )