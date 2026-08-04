import json
import logging

import streamlit as st

from gemini_service import generate_ai_response
from prompts import SMART_RTM_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import (
    download_excel,
    download_rtm_pdf
)


def render_smart_rtm(requirement):

    # ----------------------------------------------------------
    # Validation
    # ----------------------------------------------------------

    if not requirement.strip():
        st.warning("Please enter a software requirement.")
        return

    generated_tc = load("generated_testcases")

    if generated_tc is None or generated_tc.empty:
        st.warning("Please generate Test Cases before generating Smart RTM.")
        return

    # ----------------------------------------------------------
    # Generate only once
    # ----------------------------------------------------------

    if load("rtm_df") is None:

        test_cases = "\n".join(
            generated_tc["Scenario"].astype(str).tolist()
        )

        prompt = SMART_RTM_PROMPT.format(
            requirement=requirement,
            test_cases=test_cases
        )

        with st.spinner("Generating Smart RTM..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                if df is None or df.empty:
                    st.error("No RTM generated.")
                    return

                expected_columns = [
                    "Requirement",
                    "Status",
                    "Missing Scenario",
                    "Recommendation"
                ]

                if len(df.columns) != len(expected_columns):
                    st.error("Unexpected AI response.")
                    return

                df.columns = expected_columns

                covered = len(
                    df[
                        df["Status"]
                        .str.lower()
                        .str.strip() == "covered"
                    ]
                )

                partial = len(
                    df[
                        df["Status"]
                        .str.lower()
                        .str.strip() == "partial"
                    ]
                )

                missing = len(
                    df[
                        df["Status"]
                        .str.lower()
                        .str.strip() == "missing"
                    ]
                )

                total = len(df)

                coverage = (
                    round((covered / total) * 100)
                    if total else 0
                )

                save("rtm_df", df)
                save("rtm_coverage", coverage)
                save("rtm_covered", covered)
                save("rtm_partial", partial)
                save("rtm_missing", missing)

                st.success("✅ Smart RTM Generated Successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse Smart RTM response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to generate Smart RTM.")
                return

    # ----------------------------------------------------------
    # Display Existing Output
    # ----------------------------------------------------------

    df = load("rtm_df")

    coverage = load("rtm_coverage")
    covered = load("rtm_covered")
    partial = load("rtm_partial")
    missing = load("rtm_missing")

    st.subheader("📑 Smart Requirement Traceability Matrix")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("✅ Covered", covered)

    metric2.metric("🟡 Partial", partial)

    metric3.metric("❌ Missing", missing)

    metric4.metric("Coverage", f"{coverage}%")

    st.progress(coverage / 100)

    if coverage >= 80:

        st.success("🟢 Excellent Requirement Coverage")

    elif coverage >= 60:

        st.warning("🟡 Moderate Requirement Coverage")

    else:

        st.error("🔴 Poor Requirement Coverage")

    st.divider()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ----------------------------------------------------------
    # Downloads
    # ----------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        download_excel(
            df=df,
            filename="Smart_RTM.xlsx",
            key="smart_rtm_excel"
        )

    with col2:

        download_rtm_pdf(
            df=df,
            filename="Smart_RTM.pdf",
            key="smart_rtm_pdf",
            coverage=coverage,
            covered=covered,
            partial=partial,
            missing=missing
        )