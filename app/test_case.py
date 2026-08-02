import streamlit as st
import pandas as pd
import json
import logging
from datetime import datetime

from gemini_service import generate_ai_response
from prompts import TEST_CASE_PROMPT
from app.export_service import convert_df_to_excel
from utils.formatting import parse_ai_json


def render_test_case():

    if requirement.strip():

                prompt = TEST_CASE_PROMPT.format(
                    requirement=requirement
                )

                with st.spinner("Generating Test Cases..."):

                    try:

                        result = generate_ai_response(prompt)

                        df = parse_ai_json(result)
                        
                        # st.success("Test Cases Generated Successfully")
                        st.subheader("Generated Test Cases")

                        df.columns = [
                            "Test Case ID",
                            "Type",
                            "Scenario",
                            "Expected Result",
                            "Priority"
                        ]

                        # Store for Smart RTM
                        st.session_state["generated_testcases"] = df.copy()
                        st.session_state["requirement"] = requirement

                        st.success("✅ Test cases stored successfully.")

                        excel_file = convert_df_to_excel(df)

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


                        st.download_button(
                            label="Download Excel",
                            data=excel_file,
                            file_name=f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                    except json.JSONDecodeError:

                        st.error("The AI returned an invalid response. Please try again.")

                        if DEBUG:
                            st.code(result)

                    except Exception as e:

                        logging.exception(e)
                        st.error("Unable to generate test cases. Please try again.")