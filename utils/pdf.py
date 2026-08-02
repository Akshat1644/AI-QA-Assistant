import streamlit as st

from app.export_service import (
    convert_rtm_to_pdf
)


pdf_file = convert_rtm_to_pdf(
        df,
        coverage,
        covered,
        partial,
        missing
    )

st.download_button(
    label="📄 Download Executive Report",
    data=pdf_file,
    file_name="QA_Executive_Report.pdf",
    mime="application/pdf",
    key="rtm_pdf_download_for_rtm"
)