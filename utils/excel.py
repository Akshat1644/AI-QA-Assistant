import streamlit as st

from app.export_service import (
    convert_df_to_excel,
    convert_df_to_excel,
)

excel_file = convert_df_to_excel(df)

st.download_button(
    label="📊 Download Excel",
    data=excel_file,
    file_name="Automation_Feasibility_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    key="automation_excel_download"
)