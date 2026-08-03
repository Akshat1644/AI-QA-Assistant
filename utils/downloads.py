import json
import streamlit as st

from app.export_service import (
    convert_df_to_excel,
    convert_rtm_to_pdf
)


def download_excel(df, filename, key):

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=key
    )


def download_json(data, filename, key):

    st.download_button(
        label="📄 Download JSON",
        data=json.dumps(data, indent=4),
        file_name=filename,
        mime="application/json",
        key=key
    )


def download_rtm_pdf(
    df,
    coverage,
    covered,
    partial,
    missing,
    filename="QA_Executive_Report.pdf",
    key="rtm_pdf_download"
):

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
        file_name=filename,
        mime="application/pdf",
        key=key
    )