import streamlit as st
import pandas as pd
import json

from gemini_service import generate_ai_response
from prompts import TEST_DATA_PROMPT
from app.export_service import convert_df_to_excel


def render_test_data(requirement):

    if not requirement.strip():
        st.warning("Please enter a software requirement.")
        return

    prompt = TEST_DATA_PROMPT.format(
        requirement=requirement
    )

    with st.spinner("Generating Test Data..."):

        try:

            result = generate_ai_response(prompt)

            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            data = json.loads(result)

            df = pd.DataFrame(data)

            st.session_state["test_data_df"] = df

        except json.JSONDecodeError:

            st.error("Unable to parse AI response.")

            return

        except Exception:

            st.error("Failed to generate test data.")

            return

    df = st.session_state["test_data_df"]

    st.subheader("🧪 AI Generated Test Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Test_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="test_data_excel"
    )