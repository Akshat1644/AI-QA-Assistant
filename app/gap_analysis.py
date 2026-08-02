import streamlit as st
import pandas as pd
import json

from gemini_service import generate_ai_response
from prompts import GAP_ANALYSIS_PROMPT
from app.export_service import convert_df_to_excel


def render_gap_analysis(requirement):

    if not requirement.strip():
        st.warning("Please enter a software requirement.")
        return

    prompt = GAP_ANALYSIS_PROMPT.format(
        requirement=requirement
    )

    with st.spinner("Analyzing Requirement Gaps..."):

        try:

            result = generate_ai_response(prompt)

            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            data = json.loads(result)

            df = pd.DataFrame(data)

            st.session_state["gap_df"] = df

        except json.JSONDecodeError:

            st.error("Unable to parse AI response.")

            return

        except Exception:

            st.error("Failed to analyze requirement gaps.")

            return

    df = st.session_state["gap_df"]

    st.subheader("🔍 Requirement Gap Analysis")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Requirement_Gap_Analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="gap_analysis_excel"
    )