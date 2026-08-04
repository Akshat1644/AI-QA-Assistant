import streamlit as st
import pandas as pd
import json
import logging

from gemini_service import generate_ai_response
from prompts import API_TEST_CASE_PROMPT

from utils.session_manager import save, load
from utils.downloads import download_excel


def render_api_test_cases(requirement):

    # ----------------------------------------------------------
    # Generate API Test Cases
    # ----------------------------------------------------------

    if load("api_test_df") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = API_TEST_CASE_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating API Test Cases..."):

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

                    st.error("No API Test Cases were generated.")
                    return

                save("api_test_df", df)

                st.success("✅ API Test Cases generated successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse AI response.")
                return

            except Exception as e:

                logging.exception(e)

                st.error("Failed to generate API Test Cases.")
                return

    # ----------------------------------------------------------
    # Display Saved Output
    # ----------------------------------------------------------

    df = load("api_test_df")

    if df is None:
        return

    st.subheader("🌐 AI Generated API Test Cases")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    download_excel(
        df=df,
        filename="API_Test_Cases.xlsx",
        key="api_test_cases_excel"
    )