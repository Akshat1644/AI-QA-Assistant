import streamlit as st
import pandas as pd
import json
import logging

from gemini_service import generate_ai_response
from prompts import BUG_PREDICTION_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_bug_prediction(requirement):

    # ==========================================================
    # Generate Bug Prediction
    # ==========================================================

    if load("bug_prediction_df") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = BUG_PREDICTION_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Predicting Bug Hotspots..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                expected_columns = [
                    "Module",
                    "Risk",
                    "Probability",
                    "Reason",
                    "Recommendation"
                ]

                if len(df.columns) != len(expected_columns):

                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                df["Probability"] = (
                    df["Probability"]
                    .astype(int)
                )

                high = len(
                    df[df["Risk"].str.strip().str.title() == "High"]
                )

                medium = len(
                    df[df["Risk"].str.strip().str.title() == "Medium"]
                )

                low = len(
                    df[df["Risk"].str.strip().str.title() == "Low"]
                )

                score = round(df["Probability"].mean())

                save("bug_prediction_df", df)
                save("bug_score", score)
                save("bug_high", high)
                save("bug_medium", medium)
                save("bug_low", low)

                st.success("✅ Bug Prediction generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse Bug Prediction response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to predict bug hotspots.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    df = load("bug_prediction_df")

    if df is None:
        return

    score = load("bug_score")
    high = load("bug_high")
    medium = load("bug_medium")
    low = load("bug_low")

    df = df.sort_values(
        by="Probability",
        ascending=False
    ).reset_index(drop=True)

    ranking = []

    for i in range(len(df)):

        if i == 0:
            ranking.append("🥇")

        elif i == 1:
            ranking.append("🥈")

        elif i == 2:
            ranking.append("🥉")

        else:
            ranking.append(str(i + 1))

    display_df = df.copy()

    display_df.insert(
        0,
        "Rank",
        ranking
    )

    st.subheader("🤖 AI Bug Prediction Dashboard")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("🔴 High", high)
    metric2.metric("🟡 Medium", medium)
    metric3.metric("🟢 Low", low)
    metric4.metric("Prediction Score", f"{score}%")

    st.progress(score / 100)

    if score >= 70:

        st.error("🔴 High Probability of Defects")

    elif score >= 40:

        st.warning("🟡 Moderate Probability of Defects")

    else:

        st.success("🟢 Low Probability of Defects")

    st.subheader("🏆 Bug Hotspot Ranking")

    st.dataframe(
        display_df[
            [
                "Rank",
                "Module",
                "Risk",
                "Probability"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🐞 Potential Bug Hotspots")

    for _, row in df.iterrows():

        if row["Risk"] == "High":
            icon = "🔴"

        elif row["Risk"] == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        with st.expander(
            f"{icon} {row['Module']}",
            expanded=False
        ):

            st.markdown("### 📌 Module")
            st.info(row["Module"])

            st.markdown("### ⚠️ Risk")
            st.write(f"**{icon} {row['Risk']}**")

            st.markdown("### 📊 Probability")

            st.progress(
                int(row["Probability"]) / 100
            )

            st.write(
                f"**{row['Probability']}%**"
            )

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
        df=display_df,
        filename="Bug_Prediction.xlsx",
        key="bug_prediction_excel"
    )