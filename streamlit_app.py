import streamlit as st
import pandas as pd
import json
import re

from app.gemini_service import generate_test_cases
from app.prompts import (
    TEST_CASE_PROMPT,
    GAP_ANALYSIS_PROMPT,
    TEST_DATA_PROMPT,
    API_TEST_CASE_PROMPT,
    PLAYWRIGHT_SCRIPT_PROMPT,
    QUALITY_SCORE_PROMPT,
    COVERAGE_ANALYSIS_PROMPT,
    RISK_ANALYSIS_PROMPT,
    DEFECT_PREDICTION_PROMPT

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
button_col1, button_col2, button_col3, button_col4, button_col5, button_col6, button_col7, button_col8, button_col9= st.columns(9)

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

with button_col6:
    quality_score = st.button("Requirement Quality Score")

with button_col7:
    coverage_analysis = st.button("Coverage Analysis")

with button_col8:
    risk_analysis = st.button("Risk Analysis")

with button_col9:
    defect_prediction = st.button("Defect Prediction")


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


if quality_score:

    if requirement.strip():

        prompt = QUALITY_SCORE_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Requirement Quality..."):

            try:

                result = generate_test_cases(prompt)

                import re

                completeness = int(
                    re.search(
                        r"COMPLETENESS:\s*(\d+)",
                        result
                    ).group(1)
                )

                clarity = int(
                    re.search(
                        r"CLARITY:\s*(\d+)",
                        result
                    ).group(1)
                )

                testability = int(
                    re.search(
                        r"TESTABILITY:\s*(\d+)",
                        result
                    ).group(1)
                )

                ambiguity = int(
                    re.search(
                        r"AMBIGUITY:\s*(\d+)",
                        result
                    ).group(1)
                )

                # Calculate overall score
                overall = round(
                    (
                        completeness +
                        clarity +
                        testability +
                        ambiguity
                    ) / 4
                )

                st.subheader("Requirement Quality Dashboard")

                metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

                with metric_col1:
                    st.metric("Overall", f"{overall}/100")

                with metric_col2:
                    st.metric("Completeness", f"{completeness}/100")

                with metric_col3:
                    st.metric("Clarity", f"{clarity}/100")

                with metric_col4:
                    st.metric("Testability", f"{testability}/100")

                with metric_col5:
                    st.metric("Ambiguity", f"{ambiguity}/100")

                st.progress(overall / 100)

                if overall >= 80:
                    st.success(
                        f"Excellent Requirement Quality ({overall}/100)"
                    )

                elif overall >= 60:
                    st.warning(
                        f"Average Requirement Quality ({overall}/100)"
                    )

                else:
                    st.error(
                        f"Poor Requirement Quality ({overall}/100)"
                    )

                st.subheader("Detailed Analysis")

                st.markdown(result)

            except Exception as e:

                st.error(
                    "Failed to analyze requirement quality"
                )

                st.exception(e)



if coverage_analysis:

    if requirement.strip():

        prompt = COVERAGE_ANALYSIS_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Test Coverage..."):

            try:

                result = generate_test_cases(prompt)

                st.subheader("Test Coverage Analysis")

                st.markdown(result)

            except Exception as e:

                st.error(
                    "Failed to analyze coverage"
                )

                st.exception(e)


if risk_analysis:

    if requirement.strip():

        prompt = RISK_ANALYSIS_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Risks..."):

            try:

                result = generate_test_cases(prompt)

                st.subheader("Risk Based Testing Analysis")

                st.markdown(result)

            except Exception as e:

                st.error("Failed to analyze risks")

                st.exception(e)


if defect_prediction:

    if requirement.strip():

        prompt = DEFECT_PREDICTION_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Predicting Potential Defects..."):

            try:

                result = generate_test_cases(prompt)

                st.subheader("AI Defect Prediction")

                st.markdown(result)

            except Exception as e:

                st.error("Failed to predict defects")

                st.exception(e)