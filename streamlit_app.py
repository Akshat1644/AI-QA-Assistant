import streamlit as st
import pandas as pd
import json

from app.gemini_service import generate_test_cases
from app.prompts import (
    TEST_CASE_PROMPT,
    GAP_ANALYSIS_PROMPT,
    TEST_DATA_PROMPT,
    API_TEST_CASE_PROMPT,
    PLAYWRIGHT_SCRIPT_PROMPT
)
from app.export_service import convert_df_to_excel
from datetime import datetime

st.set_page_config(
    page_title="AI QA Assistant",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 AI QA Assistant")
st.caption("AI-powered QA productivity tool using Gemini AI")

st.sidebar.markdown("""
## Features

✅ Generate Test Cases

✅ Requirement Gap Analysis

✅ Test Data Generation

✅ Export to Excel

---

## Tech Stack

- Python
- Gemini AI
- Streamlit
- Pandas
""")

requirement = st.text_area(
    "Enter Requirement",
    height=150
)

# CREATE BUTTONS
button_col1, button_col2, button_col3, button_col4, button_col5= st.columns(5)

with button_col1:
    generate_tc = st.button("Generate Test Cases")

with button_col2:
    analyze_gap = st.button("Analyze Requirement Gaps")

with button_col3:
    generate_data = st.button("Generate Test Data")

with button_col4:
     generate_api_tc = st.button("Generate API Test Cases")

with button_col5:
    generate_script = st.button("Generate Playwright Script")


if generate_tc:

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

                    st.error("Unable to parse JSON response")

                    st.code(result)

                except Exception as e:

                    st.error("Failed to generate test cases")

                    st.exception(e)



if analyze_gap:    

        if requirement.strip():

            prompt = GAP_ANALYSIS_PROMPT.format(
                requirement=requirement
            )

            with st.spinner("Analyzing Requirement..."):

                result = generate_test_cases(prompt)

                st.subheader("Requirement Gap Analysis")

                st.markdown(result)



if generate_data:

        if requirement.strip():

            prompt = TEST_DATA_PROMPT.format(
                requirement=requirement
            )

            with st.spinner("Generating Test Data..."):

                result = generate_test_cases(prompt)

                result = result.replace("```json", "")
                result = result.replace("```", "")
                result = result.strip()

                try:

                    data = json.loads(result)

                    df = pd.DataFrame(data)

                    df.columns = [
                        "Field",
                        "Valid Data",
                        "Invalid Data"
                    ]

                    st.subheader("Generated Test Data")

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(e)

                    st.code(result)


if generate_api_tc:

    if requirement.strip():

        prompt = API_TEST_CASE_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating API Test Cases..."):

            result = generate_test_cases(prompt)

            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            try:

                data = json.loads(result)

                df = pd.DataFrame(data)

                df.columns = [
                    "Test Case ID",
                    "Type",
                    "Scenario",
                    "Expected Result",
                    "Priority"
                ]

                st.subheader("Generated API Test Cases")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                excel_file = convert_df_to_excel(df)

                st.download_button(
                    label="Download API Test Cases",
                    data=excel_file,
                    file_name=f"api_test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            except Exception as e:

                st.error(e)

                st.code(result)



if generate_script:

    if requirement.strip():

        prompt = PLAYWRIGHT_SCRIPT_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating Playwright Script..."):

            try:

                result = generate_test_cases(prompt)

                st.subheader("Generated Playwright Script")

                st.code(
                    result,
                    language="python"
                )

                download_col1, download_col2 = st.columns(2)

                with download_col1:
                    st.download_button(
                    label="📥 Download .py",
                    data=result,
                    file_name=f"playwright_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                    mime="text/plain"
                )
                    

                with download_col2:
                    st.download_button(
                    label="📄 Download .txt",
                    data=result,
                    file_name=f"playwright_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )


            except Exception as e:

                st.error("Failed to generate Playwright script")

                st.exception(e)