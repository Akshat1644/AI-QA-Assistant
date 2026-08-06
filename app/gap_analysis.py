import streamlit as st
import json
import logging

from gemini_service import generate_ai_response
from prompts import GAP_ANALYSIS_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_gap_analysis(requirement):

    # ==========================================================
    # Generate Gap Analysis
    # ==========================================================

    if load("gap_df") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = GAP_ANALYSIS_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Requirement Gaps..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                expected_columns = [
                    "Category",
                    "Finding",
                    "Impact",
                    "Recommendation"
                ]

                if len(df.columns) != len(expected_columns):
                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                if df.empty:

                    st.error("No Requirement Gaps were generated.")
                    return

                save("gap_df", df)

                st.success("✅ Requirement Gap Analysis generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse AI response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to analyze requirement gaps.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    df = load("gap_df")

    if df is None:
        return

    st.subheader("🔍 Requirement Gap Analysis")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    download_excel(
        df=df,
        filename="Requirement_Gap_Analysis.xlsx",
        key="gap_analysis_excel"
    )