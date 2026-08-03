import streamlit as st
import pandas as pd
import json

from gemini_service import generate_ai_response
from prompts import SMART_RTM_PROMPT
from app.export_service import (
    convert_df_to_excel,
    convert_rtm_to_pdf
)


def render_smart_rtm(requirement):

    if not requirement.strip():
        st.warning("Please enter a software requirement.")
        return

    prompt = SMART_RTM_PROMPT.format(
        requirement=requirement
    )

    with st.spinner("Generating Smart RTM..."):

        try:

            result = generate_ai_response(prompt)

            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            data = json.loads(result)

            df = pd.DataFrame(data)

            df.columns = [
                "Requirement",
                "Status",
                "Missing Scenario",
                "Recommendation"
            ]

            st.session_state["rtm_df"] = df

            covered = len(
                df[df["Status"].str.lower() == "covered"]
            )

            partial = len(
                df[df["Status"].str.lower() == "partial"]
            )

            missing = len(
                df[df["Status"].str.lower() == "missing"]
            )

            total = len(df)

            coverage = round(
                (
                    covered
                    / total
                )
                * 100
            ) if total else 0

            st.session_state["rtm_coverage"] = coverage
            st.session_state["rtm_covered"] = covered
            st.session_state["rtm_partial"] = partial
            st.session_state["rtm_missing"] = missing

        except json.JSONDecodeError:

            st.error("Unable to parse Smart RTM response.")
            return

        except Exception:

            st.error("Failed to generate Smart RTM.")
            return

    df = st.session_state["rtm_df"]

    coverage = st.session_state["rtm_coverage"]

    covered = st.session_state["rtm_covered"]
    partial = st.session_state["rtm_partial"]
    missing = st.session_state["rtm_missing"]

    st.subheader("📑 Smart Requirement Traceability Matrix")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("✅ Covered", covered)
    metric2.metric("🟡 Partial", partial)
    metric3.metric("❌ Missing", missing)
    metric4.metric("Coverage", f"{coverage}%")

    st.progress(coverage / 100)

    if coverage >= 80:
        st.success("🟢 Excellent Requirement Coverage")

    elif coverage >= 60:
        st.warning("🟡 Moderate Requirement Coverage")

    else:
        st.error("🔴 Poor Requirement Coverage")

    st.divider()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    excel_file = convert_df_to_excel(df)

    pdf_file = convert_rtm_to_pdf(df)

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📊 Download Excel",
            data=excel_file,
            file_name="Smart_RTM.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="smart_rtm_excel"
        )

    with col2:

        st.download_button(
            label="📄 Download PDF",
            data=pdf_file,
            file_name="Smart_RTM.pdf",
            mime="application/pdf",
            key="smart_rtm_pdf"
        )