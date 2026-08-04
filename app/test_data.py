import streamlit as st
import json
import logging

from gemini_service import generate_ai_response
from prompts import TEST_DATA_PROMPT

from utils.formatting import parse_ai_json
from utils.session_manager import save, load
from utils.downloads import download_excel


def render_test_data(requirement):

    if load("test_data_df") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = TEST_DATA_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating Test Data..."):

            try:

                result = generate_ai_response(prompt)

                df = parse_ai_json(result)

                save("test_data_df", df)

                st.success("✅ Test Data Generated Successfully.")

            except json.JSONDecodeError:

                st.error("Unable to parse AI response.")
                return

            except Exception as e:

                logging.exception(e)
                st.error("Failed to generate Test Data.")
                return

    # -------------------------------------------------
    # Display
    # -------------------------------------------------

    df = load("test_data_df")

    if df is None:
        return

    st.subheader("🧪 AI Generated Test Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    download_excel(
        df=df,
        filename="Test_Data.xlsx",
        key="test_data_excel"
    )