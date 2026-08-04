import streamlit as st
import json
import logging

from gemini_service import generate_ai_response
from prompts import COMPLETENESS_ANALYSIS_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_requirement_completeness(requirement):

    # ==========================================================
    # Generate Completeness Analysis
    # ==========================================================

    if load("completeness_df") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = COMPLETENESS_ANALYSIS_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Requirement Completeness..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                expected_columns = [
                    "Category",
                    "Status",
                    "Details",
                    "Recommendation"
                ]

                if len(df.columns) != len(expected_columns):

                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                complete = len(df[df["Status"] == "Complete"])
                partial = len(df[df["Status"] == "Partial"])
                missing = len(df[df["Status"] == "Missing"])

                total = len(df)

                score = round(
                    (
                        (complete * 3)
                        + (partial * 2)
                    )
                    /
                    (total * 3)
                    * 100
                )

                save("completeness_df", df)
                save("completeness_score", score)
                save("complete", complete)
                save("partial", partial)
                save("missing", missing)

                st.success("✅ Requirement Completeness generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse Completeness Analysis response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to analyze requirement completeness.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    df = load("completeness_df")

    if df is None:
        return

    score = load("completeness_score")
    complete = load("complete")
    partial = load("partial")
    missing = load("missing")

    st.subheader("📋 Requirement Completeness Dashboard")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("✅ Complete", complete)
    metric2.metric("🟡 Partial", partial)
    metric3.metric("❌ Missing", missing)
    metric4.metric("Score", f"{score}%")

    st.progress(score / 100)

    if score >= 80:

        st.success("🟢 Requirement is highly complete.")

    elif score >= 60:

        st.warning("🟡 Requirement is partially complete.")

    else:

        st.error("🔴 Requirement requires further refinement.")

    st.divider()

    st.subheader("📑 Completeness Details")

    for _, row in df.iterrows():

        if row["Status"] == "Complete":
            icon = "✅"

        elif row["Status"] == "Partial":
            icon = "🟡"

        else:
            icon = "❌"

        with st.expander(
            f"{icon} {row['Category']}",
            expanded=False
        ):

            st.markdown("### 📌 Category")
            st.info(row["Category"])

            st.markdown("### 📊 Status")
            st.write(f"**{icon} {row['Status']}**")

            st.markdown("### 📝 Details")
            st.write(row["Details"])

            st.markdown("### 💡 Recommendation")
            st.success(row["Recommendation"])

    download_excel(
        df=df,
        filename="Requirement_Completeness.xlsx",
        key="requirement_completeness_excel"
    )