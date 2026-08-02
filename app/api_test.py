import streamlit as st
import pandas as pd
import json

from gemini_service import generate_ai_response
from prompts import API_TEST_CASE_PROMPT
from app.export_service import convert_df_to_excel


def render_api_test_cases(requirement):

    if not requirement.strip():
        st.warning("Please enter a software requirement.")
        return

    prompt = API_TEST_CASE_PROMPT.format(
        requirement=requirement
    )

    with st.spinner("Generating API Test Cases..."):

        try:

            result = generate_ai_response(prompt)

            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            data = json.loads(result)

            df = pd.DataFrame(data)

            st.session_state["api_test_df"] = df

        except json.JSONDecodeError:

            st.error("Unable to parse AI response.")
            return

        except Exception:

            st.error("Failed to generate API Test Cases.")
            return

    df = st.session_state["api_test_df"]

    st.subheader("🌐 AI Generated API Test Cases")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="API_Test_Cases.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="api_test_cases_excel"
    )