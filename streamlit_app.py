import streamlit as st
import pandas as pd
import json

from app.gemini_service import generate_test_cases
from app.prompts import TEST_CASE_PROMPT

st.set_page_config(
    page_title="AI QA Assistant",
    page_icon="🧪"
)

st.title("🧪 AI QA Assistant")

requirement = st.text_area(
    "Enter Requirement",
    height=150
)

if st.button("Generate Test Cases"):

    if requirement.strip():

        prompt = TEST_CASE_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating Test Cases..."):

            try:

                result = generate_test_cases(prompt)

                result = result.replace("```json", "")
                result = result.replace("```", "")
                result = result.strip()

                data = json.loads(result)

                # st.success("Test Cases Generated Successfully")
                st.subheader("Generated Test Cases")

                df = pd.DataFrame(data)

                df.columns = [
                    "Test Case ID",
                    "Type",
                    "Scenario",
                    "Expected Result",
                    "Priority"
                ]

                st.dataframe(
                    df,
                    use_container_width=True
                )

            except Exception:

                st.error("Unable to parse JSON response")

                st.text(result)