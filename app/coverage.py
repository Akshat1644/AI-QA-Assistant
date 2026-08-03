import streamlit as st
import json
import logging

from gemini_service import generate_ai_response
from prompts import COVERAGE_ANALYSIS_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_coverage_analysis(requirement):

    # ==========================================================
    # Generate Coverage Analysis
    # ==========================================================

    if requirement.strip():

        prompt = COVERAGE_ANALYSIS_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Requirement Coverage..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                expected_columns = [
                    "Requirement Area",
                    "Coverage",
                    "Status",
                    "Recommendation"
                ]

                if len(df.columns) != len(expected_columns):

                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                covered = len(
                    df[df["Status"].str.lower() == "covered"]
                )

                partial = len(
                    df[df["Status"].str.lower() == "partial"]
                )

                missing = len(
                    df[df["Status"].str.lower() == "missing"]
                )

                total = len(df)

                coverage_score = (
                    round(
                        (
                            (covered * 3)
                            + (partial * 2)
                        )
                        /
                        (total * 3)
                        * 100
                    )
                    if total > 0
                    else 0
                )

                save("coverage_df", df)
                save("coverage_score", coverage_score)
                save("covered", covered)
                save("partial", partial)
                save("missing", missing)

                st.success("✅ Coverage Analysis generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse Coverage Analysis response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to analyze coverage.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    df = load("coverage_df")

    if df is None:
        return

    coverage_score = load("coverage_score")
    covered = load("covered")
    partial = load("partial")
    missing = load("missing")

    st.subheader("📊 AI Coverage Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("✅ Covered", covered)
    col2.metric("🟡 Partial", partial)
    col3.metric("❌ Missing", missing)
    col4.metric("Coverage Score", f"{coverage_score}%")

    st.progress(coverage_score / 100)

    if coverage_score >= 80:

        st.success("🟢 Excellent Requirement Coverage")

    elif coverage_score >= 60:

        st.warning("🟡 Moderate Requirement Coverage")

    else:

        st.error("🔴 Poor Requirement Coverage")

    st.divider()

    st.subheader("📋 Coverage Details")

    for _, row in df.iterrows():

        status = str(row["Status"]).strip().title()

        if status == "Covered":
            icon = "✅"

        elif status == "Partial":
            icon = "🟡"

        else:
            icon = "❌"

        with st.expander(
            f"{icon} {row['Requirement Area']}",
            expanded=False
        ):

            st.markdown("### Requirement Area")
            st.info(row["Requirement Area"])

            st.markdown("### Coverage")
            st.write(row["Coverage"])

            st.markdown("### Status")
            st.write(f"**{icon} {status}**")

            st.markdown("### Recommendation")
            st.success(row["Recommendation"])

    download_excel(
        df=df,
        filename="Coverage_Analysis.xlsx",
        key="coverage_excel"
    )