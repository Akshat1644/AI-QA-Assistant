import streamlit as st
import json
import logging
from datetime import datetime

from gemini_service import generate_ai_response
from prompts import TEST_CASE_PROMPT
from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_test_case(requirement):

    # ----------------------------------------------------------
    # Generate only once
    # ----------------------------------------------------------

    if "testcase_df" not in st.session_state:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = TEST_CASE_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating Test Cases..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                if df is None or df.empty:
                    st.error("No test cases were generated.")
                    return

                expected_columns = [
                    "Test Case ID",
                    "Type",
                    "Scenario",
                    "Expected Result",
                    "Priority"
                ]

                if len(df.columns) != len(expected_columns):
                    st.error("Unexpected response received from AI.")
                    return

                df.columns = expected_columns

                # Save for Smart RTM
                save("generated_testcases", df.copy())
                save("requirement", requirement)

                # Save output
                save("testcase_df", df)

                st.success(
                    "✅ Test Cases generated successfully.\n\n"
                    "💾 Test cases have been saved and can now be used by Smart RTM."
                )

            except json.JSONDecodeError:

                st.error("Unable to parse AI response.")
                return

            except Exception as e:

                logging.exception(e)
                st.error("Unable to generate test cases.")
                return

    # ----------------------------------------------------------
    # Display Existing Output
    # ----------------------------------------------------------

    df = st.session_state["testcase_df"]

    st.subheader("Generated Test Cases")

    st.dataframe(
        df,
        use_container_width=True
    )

    high_count = len(df[df["Priority"] == "High"])
    medium_count = len(df[df["Priority"] == "Medium"])
    low_count = len(df[df["Priority"] == "Low"])

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("High Priority", high_count)

    with metric_col2:
        st.metric("Medium Priority", medium_count)

    with metric_col3:
        st.metric("Low Priority", low_count)

    download_excel(
        df=df,
        filename=f"Test_Cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        key="testcase_excel"
    )