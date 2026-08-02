# Standard Library
import json
import logging
import re
from datetime import datetime

# Third-party
import pandas as pd
import streamlit as st

# Local Modules
from gemini_service import generate_ai_response

from app.test_case import render_test_case

from app.gap_analysis import render_gap_analysis

from app.test_data import render_test_data

from app.api_test import render_api_test_cases

from app.playwright import render_playwright_script

from prompts import (
    QUALITY_SCORE_PROMPT,
    COVERAGE_ANALYSIS_PROMPT,
    RISK_ANALYSIS_PROMPT,
    DEFECT_PREDICTION_PROMPT,
    SMART_RTM_PROMPT,
    COMPLETENESS_ANALYSIS_PROMPT,
    BUG_PREDICTION_PROMPT,
    DEFECT_REPORT_PROMPT,
    REGRESSION_IMPACT_PROMPT,
    AUTOMATION_FEASIBILITY_PROMPT

)

from app.export_service import (
    convert_df_to_excel,
    convert_rtm_to_pdf
)
from datetime import datetime

st.set_page_config(
    page_title="AI QA Assistant",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 AI QA Assistant")
st.markdown("""
### AI-Powered Software Testing Platform

Generate intelligent test artifacts, analyze requirements,
predict risks, automate QA workflows and produce professional reports
using **Google Gemini AI**.

---
""")

with st.sidebar:

    st.title("🧪 AI QA Assistant")

    st.caption("Version 1.0")

    st.divider()

    st.markdown("""
    ## Features

    ✅ Test Case Generator

    ✅ Smart RTM

    ✅ Risk Analysis

    ✅ Bug Prediction

    ✅ Defect Prediction

    ✅ Automation Score

    ✅ Regression Analysis

    ✅ Playwright

    ✅ API Testing

    ✅ Defect Report

---

## Tech Stack

- Python
- Gemini AI
- Streamlit
- Pandas
""")


st.subheader("📝 Software Requirement")

requirement = st.text_area(
    "Paste your Software Requirement",
    height=180,
    placeholder="""
Example:

The user should be able to login using email and password.

After successful login, the user is redirected to the dashboard.

Forgot password functionality should send a reset email.

Account should be locked after 5 invalid login attempts.
"""
)


# CREATE BUTTONS

# ==========================================================
# 📋 Requirement Analysis
# ==========================================================

with st.container():

    st.markdown("## 📋 Requirement Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        quality_score = st.button("Quality Score", use_container_width=True)

    with col2:
        requirement_completeness = st.button("Completeness", use_container_width=True)

    with col3:
        analyze_gap = st.button("Gap Analysis", use_container_width=True)

st.divider()


# ==========================================================
# 🤖 AI Insights
# ==========================================================

with st.container():

    st.markdown("## 🤖 AI Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        coverage_analysis = st.button("Coverage", use_container_width=True)

    with col2:
        risk_analysis = st.button("Risk", use_container_width=True)

    with col3:
        bug_prediction = st.button("Bug Prediction", use_container_width=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        defect_prediction = st.button("Defect Prediction", use_container_width=True)

    with col5:
        regression_analysis = st.button("Regression", use_container_width=True)

    with col6:
        automation_feasibility = st.button("Automation", use_container_width=True)

st.divider()


# ==========================================================
# 🧪 Test Generation
# ==========================================================

with st.container():

    st.markdown("## 🧪 Test Generation")

    col1, col2 = st.columns(2)

    with col1:
        generate_tc = st.button("Test Cases", use_container_width=True)

    with col2:
        generate_test_data = st.button("Test Data", use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        generate_api_tc = st.button("API Test Cases", use_container_width=True)

    with col4:
        generate_playwright_script = st.button("Playwright", use_container_width=True)

st.divider()


# ==========================================================
# 📄 Reports
# ==========================================================

with st.container():

    st.markdown("## 📄 Reports")

    col1, col2 = st.columns(2)

    with col1:
        generate_rtm = st.button("Smart RTM", use_container_width=True)

    with col2:
        defect_report = st.button("Defect Report", use_container_width=True)

st.divider()


if generate_tc:
    render_test_case(requirement)


if analyze_gap:    
    render_gap_analysis(requirement)


if generate_test_data:
    render_test_data(requirement)


if generate_api_tc:
    render_api_test_cases(requirement)



if generate_playwright_script:
     render_playwright_script(requirement)

   

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

                logging.exception(e)
                
                st.error("Something went wrong while processing your request. Please try again.")
                



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

                logging.exception(e)
                
                st.error("Something went wrong while processing your request. Please try again.")
                



if risk_analysis:

    if requirement.strip():

        prompt = RISK_ANALYSIS_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Risks..."):

            try:

                result = generate_test_cases(prompt)

                result = clean_ai_response(result)

                data = json.loads(result)

                df = pd.DataFrame(data)

                df.columns = [
                    "Risk Area",
                    "Severity",
                    "Reason",
                    "Recommendation"
                ]

                # Store in Session State
                st.session_state["risk_df"] = df

                # Normalize Severity
                df["Severity"] = (
                    df["Severity"]
                    .astype(str)
                    .str.strip()
                    .str.title()
                )

                high = len(df[df["Severity"] == "High"])
                medium = len(df[df["Severity"] == "Medium"])
                low = len(df[df["Severity"] == "Low"])

                total = len(df)

                # Risk Score
                risk_score = round(
                    ((high * 3) + (medium * 2) + (low * 1))
                    / (total * 3) * 100
                ) if total > 0 else 0

                st.session_state["risk_score"] = risk_score
                st.session_state["high_risk"] = high
                st.session_state["medium_risk"] = medium
                st.session_state["low_risk"] = low

            except json.JSONDecodeError:

                st.error("The AI returned an invalid response. Please try again.")
                
                if DEBUG:
                    st.code(result)

            except Exception as e:

                logging.exception(e)
                st.error("Unable to complete the risk analysis. Please try again.")
                


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

                logging.exception(e)
                
                st.error("Something went wrong while processing your request. Please try again.")
                


if generate_rtm:

    if "generated_testcases" not in st.session_state or st.session_state["generated_testcases"].empty:

        st.warning("⚠ Please generate test cases first.")
        st.stop()

    requirement_text = st.session_state["requirement"]

    test_cases = "\n".join(
        st.session_state["generated_testcases"]["Scenario"].tolist()
    )

    prompt = SMART_RTM_PROMPT.format(
        requirement=requirement_text,
        test_cases=test_cases
    )

    with st.spinner("Analyzing Requirement Coverage..."):

        try:

            result = generate_test_cases(prompt)

            result = clean_ai_response(result)

            data = json.loads(result)

            df = pd.DataFrame(data)

            df.columns = [
                "Requirement",
                "Status",
                "Missing Scenario",
                "Recommendation"
            ]

            st.session_state["rtm_df"] = df


            # -----------------------------
            # Normalize Status
            # -----------------------------

            df["Status"] = (
                df["Status"]
                .astype(str)
                .str.strip()
                .str.title()
            )

            covered = len(df[df["Status"] == "Covered"])
            partial = len(df[df["Status"] == "Partial"])
            missing = len(df[df["Status"] == "Missing"])

            total = len(df)

            coverage = round((covered / total) * 100) if total > 0 else 0

            st.session_state["coverage"] = coverage
            st.session_state["covered"] = covered
            st.session_state["partial"] = partial
            st.session_state["missing"] = missing


        except json.JSONDecodeError:

            st.error("The AI returned an invalid response. Please try again.")
            
            if DEBUG:
                st.code(result)

        except Exception as e:

            logging.exception(e)
            st.error("Unable to generate the Smart RTM. Please try again.")
            



# ============================================
# Display RTM from Session State
# ============================================

if "rtm_df" in st.session_state:

    df = st.session_state["rtm_df"]

    coverage = st.session_state["coverage"]
    covered = st.session_state["covered"]
    partial = st.session_state["partial"]
    missing = st.session_state["missing"]

    # -----------------------------
    # Dashboard
    # -----------------------------

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("🟢 Covered", covered)
    metric2.metric("🟡 Partial", partial)
    metric3.metric("🔴 Missing", missing)
    metric4.metric("Coverage", f"{coverage}%")

    st.progress(coverage / 100)

    if coverage >= 90:
        st.success("🟢 Overall Verdict : Excellent Test Coverage")

    elif coverage >= 70:
        st.warning("🟡 Overall Verdict : Requirement Needs Minor Improvements")

    else:
        st.error("🔴 Overall Verdict : High Risk Requirement")

    st.divider()

    st.subheader("📄 Smart Requirement Traceability Matrix")

    for index, row in df.iterrows():

        if row["Status"] == "Covered":
            icon = "🟢"

        elif row["Status"] == "Partial":
            icon = "🟡"

        else:
            icon = "🔴"

        with st.expander(
            f"{icon} Requirement {index+1}",
            expanded=False
        ):

            st.markdown("### 📌 Requirement")
            st.info(row["Requirement"])

            st.markdown("### 📊 Status")
            st.write(f"**{icon} {row['Status']}**")

            st.markdown("### ❌ Missing Scenarios")

            missing_points = str(row["Missing Scenario"]).split(",")

            for point in missing_points:

                point = point.strip()

                if point and point.lower() != "none":
                    st.markdown(f"- {point}")

            if str(row["Missing Scenario"]).lower() == "none":
                st.success("No Missing Scenario")

            st.markdown("### 💡 Recommendation")

            recommendation_text = str(row["Recommendation"])

            st.markdown(recommendation_text)

    st.divider()

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Smart_RTM.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="rtm_excel_download_for_rtm"
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



if "risk_df" in st.session_state:

    df = st.session_state["risk_df"]

    risk_score = st.session_state["risk_score"]

    high = st.session_state["high_risk"]
    medium = st.session_state["medium_risk"]
    low = st.session_state["low_risk"]

    st.subheader("⚠️ AI Risk Analysis Dashboard")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("🔴 High", high)
    metric2.metric("🟡 Medium", medium)
    metric3.metric("🟢 Low", low)
    metric4.metric("Risk Score", f"{risk_score}%")

    st.progress(risk_score / 100)

    if risk_score >= 70:
        st.error("🔴 Overall Risk: High")

    elif risk_score >= 40:
        st.warning("🟡 Overall Risk: Medium")

    else:
        st.success("🟢 Overall Risk: Low")

    st.divider()

    st.subheader("📋 Risk Details")

    for index, row in df.iterrows():

        if row["Severity"] == "High":
            icon = "🔴"

        elif row["Severity"] == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        with st.expander(
            f"{icon} {row['Risk Area']}",
            expanded=False
        ):

            st.markdown("### 📌 Risk Area")
            st.info(row["Risk Area"])

            st.markdown("### 📊 Severity")
            st.write(f"**{icon} {row['Severity']}**")

            st.markdown("### ❗ Reason")
            st.write(row["Reason"])

            st.markdown("### 💡 Recommendation")
            st.success(row["Recommendation"]) 

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Risk_Analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="risk_excel_download_for_risk"
    )



if requirement_completeness:

    if requirement.strip():

        prompt = COMPLETENESS_ANALYSIS_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Requirement Completeness..."):

            try:

                result = generate_test_cases(prompt)

                result = clean_ai_response(result)
                
                data = json.loads(result)

                df = pd.DataFrame(data)

                df.columns = [
                    "Category",
                    "Status",
                    "Details",
                    "Recommendation"
                ]

                st.session_state["completeness_df"] = df

                df["Status"] = (
                    df["Status"]
                    .astype(str)
                    .str.strip()
                    .str.title()
                )

                complete = len(df[df["Status"] == "Complete"])
                partial = len(df[df["Status"] == "Partial"])
                missing = len(df[df["Status"] == "Missing"])

                total = len(df)

                score = round(
                    ((complete * 3) + (partial * 2) + (missing * 1))
                    / (total * 3) * 100
                ) if total > 0 else 0

                st.session_state["completeness_score"] = score
                st.session_state["complete"] = complete
                st.session_state["partial_complete"] = partial
                st.session_state["missing_complete"] = missing

            except json.JSONDecodeError:

                st.error("The AI returned an invalid response. Please try again.")
                
                if DEBUG:
                    st.code(result)

            except Exception as e:

                logging.exception(e)
                st.error("Unable to analyze requirement completeness. Please try again.")
                


if "completeness_df" in st.session_state:

    df = st.session_state["completeness_df"]

    score = st.session_state["completeness_score"]

    complete = st.session_state["complete"]
    partial = st.session_state["partial_complete"]
    missing = st.session_state["missing_complete"]

    st.subheader("📋 Requirement Completeness Dashboard")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("✅ Complete", complete)
    metric2.metric("🟡 Partial", partial)
    metric3.metric("🔴 Missing", missing)
    metric4.metric("Score", f"{score}%")

    st.progress(score / 100)

    if score >= 90:
        st.success("🟢 Requirement is Ready for Testing")

    elif score >= 70:
        st.warning("🟡 Requirement Needs Minor Improvements")

    else:
        st.error("🔴 Requirement Needs Significant Refinement")


    st.divider()

    st.subheader("📄 Requirement Review")

    for index, row in df.iterrows():

        if row["Status"] == "Complete":
            icon = "🟢"

        elif row["Status"] == "Partial":
            icon = "🟡"

        else:
            icon = "🔴"

        with st.expander(
            f"{icon} {row['Category']}",
            expanded=False
        ):

            st.markdown("### 📌 Category")
            st.info(row["Category"])

            st.markdown("### 📊 Status")
            st.write(f"**{icon} {row['Status']}**")

            st.markdown("### 📝 Details")
            st.write(row["Details"])

            st.markdown("### 💡 Recommendation")
            st.success(row["Recommendation"])


    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Requirement_Completeness.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="requirement_completeness_excel"
    )




if bug_prediction:

    if requirement.strip():

        prompt = BUG_PREDICTION_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Predicting Potential Bug Hotspots..."):

            try:

                result = generate_test_cases(prompt)

                result = clean_ai_response(result)

                data = json.loads(result)

                df = pd.DataFrame(data)

                df.columns = [
                    "Module",
                    "Risk",
                    "Probability",
                    "Reason",
                    "Recommendation"
                ]

                st.session_state["bug_prediction_df"] = df

                df["Risk"] = (
                    df["Risk"]
                    .astype(str)
                    .str.strip()
                    .str.title()
                )

                df["Probability"] = (
                    pd.to_numeric(
                        df["Probability"],
                        errors="coerce"
                    )
                    .fillna(0)
                    .astype(int)
                )

                high = len(df[df["Risk"] == "High"])
                medium = len(df[df["Risk"] == "Medium"])
                low = len(df[df["Risk"] == "Low"])

                overall_probability = round(
                    df["Probability"].mean()
                )

                st.session_state["bug_high"] = high
                st.session_state["bug_medium"] = medium
                st.session_state["bug_low"] = low
                st.session_state["bug_score"] = overall_probability

            except json.JSONDecodeError:

                st.error("Unable to parse Bug Prediction response.")

            except Exception as e:

                logging.exception(e)

                st.error("Unable to predict software defects. Please try again.")



if "bug_prediction_df" in st.session_state:

    df = st.session_state["bug_prediction_df"]

    df = df.sort_values(
        by="Probability",
        ascending=False
    ).reset_index(drop=True)

    ranking = []

    for i in range(len(df)):

        if i == 0:
            ranking.append("🥇")

        elif i == 1:
            ranking.append("🥈")

        elif i == 2:
            ranking.append("🥉")

        else:
            ranking.append(str(i + 1))

    df.insert(0, "Rank", ranking)


    score = st.session_state["bug_score"]

    high = st.session_state["bug_high"]
    medium = st.session_state["bug_medium"]
    low = st.session_state["bug_low"]

    st.subheader("🤖 AI Bug Prediction Dashboard")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("🔴 High", high)
    metric2.metric("🟡 Medium", medium)
    metric3.metric("🟢 Low", low)

    if score >= 70:
        verdict = "Critical"

    elif score >= 40:
        verdict = "Moderate"

    else:
        verdict = "Low"

    metric4.metric(
        "Prediction Score",
        f"{score}%",
        verdict
    )

    st.progress(score / 100)

    if score >= 70:
        st.error("🔴 High Probability of Defects")

    elif score >= 40:
        st.warning("🟡 Moderate Probability of Defects")

    else:
        st.success("🟢 Low Probability of Defects")

        # ---------------------------------
        # Bug Hotspot Ranking
        # ---------------------------------

        ranking_df = df.copy()

        ranking_df["Risk"] = ranking_df["Risk"].replace({
            "High": "🔴 High",
            "Medium": "🟡 Medium",
            "Low": "🟢 Low"
        })

        ranking_df["Probability"] = (
            ranking_df["Probability"].astype(str) + "%"
        )

        st.subheader("🏆 Bug Hotspot Ranking")

        st.dataframe(
            ranking_df[
                [
                    "Rank",
                    "Module",
                    "Risk",
                    "Probability"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )

        st.divider()

    st.subheader("🐞 Potential Bug Hotspots")

    for index, row in df.iterrows():

        if row["Risk"] == "High":
            icon = "🔴"

        elif row["Risk"] == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        with st.expander(
            f"{icon} {row['Module']}",
            expanded=False
        ):

            st.markdown("### 📌 Module")
            st.info(row["Module"])

            st.markdown("### ⚠️ Risk")

            st.write(f"**{icon} {row['Risk']}**")

            st.markdown("### 📊 Probability")

            st.progress(int(row["Probability"]) / 100)

            st.write(f"**{row['Probability']}%**")

            st.markdown("### ❓ Reason")

            if isinstance(row["Reason"], list):

                for point in row["Reason"]:
                    st.markdown(f"- {point}")

            else:
                st.markdown(f"- {row['Reason']}")


            st.markdown("### 💡 Recommendation")

            if isinstance(row["Recommendation"], list):

                for rec in row["Recommendation"]:
                    st.markdown(f"- {rec}")

            else:

                st.markdown(f"- {row['Recommendation']}")

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Bug_Prediction.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="bug_prediction_excel"
    )



# ==========================================================
# AI Defect Report
# ==========================================================

if defect_report:

    if requirement.strip():

        prompt = DEFECT_REPORT_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating AI Defect Report..."):

            try:

                result = generate_test_cases(prompt)

                result = clean_ai_response(result)
                
                data = json.loads(result)

                df = pd.DataFrame(data)

                df.columns = [
                    "Bug Summary",
                    "Description",
                    "Steps To Reproduce",
                    "Expected Result",
                    "Actual Result",
                    "Severity",
                    "Priority",
                    "Root Cause",
                    "Suggested Fix"
                ]

                st.session_state["defect_df"] = df

            except json.JSONDecodeError:

                st.error(
                    "AI returned an unexpected response. Please try again."
                )

            except Exception:

                st.error(
                    "Something went wrong while processing your request."
                )


# ==========================================================
# Display Dashboard
# ==========================================================

if "defect_df" in st.session_state:

    df = st.session_state["defect_df"]

    row = df.iloc[0]

    from datetime import datetime

    bug_id = f"AI-BUG-{datetime.now().strftime('%Y%m%d')}-001"

    st.subheader("🐞 AI Defect Report Dashboard")

    st.info(f"🆔 **Bug ID:** {bug_id}")

    # -------------------------------------
    # Metrics
    # -------------------------------------

    metric1, metric2 = st.columns(2)

    severity = row["Severity"]
    priority = row["Priority"]

    if severity == "Critical":
        severity_display = "🚨 Critical"

    elif severity == "High":
        severity_display = "🔴 High"

    elif severity == "Medium":
        severity_display = "🟡 Medium"

    else:
        severity_display = "🟢 Low"

    if priority == "High":
        priority_display = "🔴 High"

    elif priority == "Medium":
        priority_display = "🟡 Medium"

    else:
        priority_display = "🟢 Low"

    metric1.metric(
        "Severity",
        severity_display
    )

    metric2.metric(
        "Priority",
        priority_display
    )

    st.divider()

    # -------------------------------------
    # Bug Summary
    # -------------------------------------

    st.markdown("## 🐞 Bug Summary")

    st.error(f"**{row['Bug Summary']}**")

    # -------------------------------------
    # Description
    # -------------------------------------

    st.markdown("## 📝 Description")

    st.info(row["Description"])

    # -------------------------------------
    # Steps To Reproduce
    # -------------------------------------

    st.markdown("## 🔄 Steps To Reproduce")

    if isinstance(row["Steps To Reproduce"], list):

        for i, step in enumerate(
            row["Steps To Reproduce"],
            start=1
        ):

            st.markdown(f"**{i}.** {step}")

    else:

        st.write(row["Steps To Reproduce"])
    
    # -------------------------------------
    # Results
    # -------------------------------------

    st.markdown("## 📊 Result Comparison")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ✅ Expected")

        st.success(row["Expected Result"])

    with col2:

        st.markdown("### ❌ Actual")

        st.error(row["Actual Result"])

    # -------------------------------------
    # Root Cause
    # -------------------------------------

    st.markdown("## 🔍 Root Cause")

    if isinstance(row["Root Cause"], list):

        for cause in row["Root Cause"]:
            st.markdown(f"- {cause}")

    else:

        st.warning(row["Root Cause"])

    # -------------------------------------
    # Suggested Fix
    # -------------------------------------

    st.markdown("## 🛠 Suggested Fix")

    if isinstance(row["Suggested Fix"], list):

        for fix in row["Suggested Fix"]:
            st.markdown(f"- {fix}")

    else:

        st.success(row["Suggested Fix"])

    # -------------------------------------
    # Download Excel
    # -------------------------------------

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="AI_Defect_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="defect_report_excel"
    )



# ==========================================================
# Regression Impact Analysis
# ==========================================================

if regression_analysis:

    if requirement.strip():

        prompt = REGRESSION_IMPACT_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Regression Impact..."):

            try:

                result = generate_test_cases(prompt)

                result = clean_ai_response(result)

                data = json.loads(result)

                df = pd.DataFrame(data)

                df.columns = [
                    "Risk Level",
                    "Affected Modules",
                    "Regression Suites",
                    "Focus Areas",
                    "Summary"
                ]

                st.session_state["regression_df"] = df

            except json.JSONDecodeError:

                st.error(
                    "AI returned an unexpected response. Please try again."
                )

            except Exception:

                st.error(
                    "Something went wrong while processing your request."
                )


# ==========================================================
# Dashboard
# ==========================================================

if "regression_df" in st.session_state:

    df = st.session_state["regression_df"]

    row = df.iloc[0]

    st.subheader("📈 AI Regression Impact Dashboard")

    # -------------------------------------------------
    # Risk Display
    # -------------------------------------------------

    risk = str(row["Risk Level"]).title()

    if risk == "High":
        risk_display = "🔴 High"

    elif risk == "Medium":
        risk_display = "🟡 Medium"

    else:
        risk_display = "🟢 Low"

    affected_modules = row["Affected Modules"]
    regression_suites = row["Regression Suites"]
    focus_areas = row["Focus Areas"]

    affected_count = len(affected_modules)
    suite_count = len(regression_suites)
    focus_count = len(focus_areas)

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Risk Level",
        risk_display
    )

    metric2.metric(
        "Affected Modules",
        affected_count
    )

    metric3.metric(
        "Regression Suites",
        suite_count
    )

    metric4.metric(
        "Focus Areas",
        focus_count
    )

    st.divider()

    # -------------------------------------------------
    # Affected Modules
    # -------------------------------------------------

    st.markdown("## 📦 Affected Modules")

    for module in affected_modules:

        impact = module["impact"]

        if impact == "High":
            icon = "🔴"

        elif impact == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        st.markdown(
            f"**{module['module']}** &nbsp;&nbsp; {icon} {impact}",
            unsafe_allow_html=True
        )

    st.divider()

    # -------------------------------------------------
    # Regression Suites
    # -------------------------------------------------

    st.markdown("## 🧪 Recommended Regression Suites")

    for suite in regression_suites:

        priority = suite["priority"]

        if priority == "High":
            icon = "🔴"

        elif priority == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        st.markdown(
            f"**{suite['suite']}** &nbsp;&nbsp; {icon} {priority}",
            unsafe_allow_html=True
        )

    st.divider()

    # -------------------------------------------------
    # Focus Areas
    # -------------------------------------------------

    st.markdown("## 🎯 Testing Focus Areas")

    cols = st.columns(2)

    for i, area in enumerate(focus_areas):

        with cols[i % 2]:

            st.success(area)

    st.divider()

    # -------------------------------------------------
    # AI Summary
    # -------------------------------------------------

    st.markdown("## 📋 AI Regression Summary")

    st.info(row["Summary"])

    st.divider()

    # -------------------------------------------------
    # Download Excel
    # -------------------------------------------------

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Regression_Impact_Analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="regression_impact_excel"
    )



# ==========================================================
# Automation Feasibility Analysis
# ==========================================================

if automation_feasibility:

    if requirement.strip():

        prompt = AUTOMATION_FEASIBILITY_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Analyzing Automation Feasibility..."):

            try:

                result = generate_test_cases(prompt)

                result = clean_ai_response(result)

                data = json.loads(result)

                df = pd.DataFrame(data)

                df.columns = [
                    "Automation Score",
                    "Feasibility",
                    "Recommended Framework",
                    "Framework Reason",
                    "Automation Challenges",
                    "Automation Strategy",
                    "Estimated Effort",
                    "Maintenance Level",
                    "Summary"
                ]

                st.session_state["automation_df"] = df

            except json.JSONDecodeError:

                st.error(
                    "AI returned an unexpected response. Please try again."
                )

            except Exception:

                st.error(
                    "Something went wrong while processing your request."
                )


# ==========================================================
# Automation Dashboard
# ==========================================================

if "automation_df" in st.session_state:

    df = st.session_state["automation_df"]

    row = df.iloc[0]

    st.subheader("🤖 AI Automation Feasibility Dashboard")

    # -------------------------------------------------
    # Score
    # -------------------------------------------------

    score = int(row["Automation Score"])

    feasibility = str(row["Feasibility"]).title()

    if feasibility == "High":
        feasibility_display = "🟢 Highly Automatable"

    elif feasibility == "Medium":
        feasibility_display = "🟡 Partially Automatable"

    else:
        feasibility_display = "🔴 Low Automation Feasibility"

    framework = row["Recommended Framework"]

    challenges = row["Automation Challenges"]

    strategies = row["Automation Strategy"]

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Automation Score",
        f"{score}%"
    )

    metric2.metric(
        "Feasibility",
        feasibility
    )

    metric3.metric(
        "Framework",
        framework
    )

    metric4.metric(
        "Challenges",
        len(challenges)
    )

    metric5, metric6 = st.columns(2)

    metric5.metric(
        "Estimated Effort",
        row["Estimated Effort"]
    )

    metric6.metric(
        "Maintenance",
        row["Maintenance Level"]
    )

    st.progress(score / 100)

    if score >= 80:

        st.success("🟢 Excellent Candidate for Automation")

    elif score >= 50:

        st.warning("🟡 Partial Automation Recommended")

    else:

        st.error("🔴 Mostly Manual Testing Recommended")

    st.divider()

    # -------------------------------------------------
    # Recommended Framework
    # -------------------------------------------------

    st.markdown("## 🧰 Recommended Framework")

    st.info(framework)

    st.divider()

    st.markdown("## 🧰 Why This Framework?")

    st.info(row["Framework Reason"])

    st.divider()

    # -------------------------------------------------
    # Automation Challenges
    # -------------------------------------------------

    st.markdown("## ⚠️ Automation Challenges")

    for challenge in challenges:

        st.markdown(f"- {challenge}")

    st.divider()

    # -------------------------------------------------
    # Automation Strategy
    # -------------------------------------------------

    st.markdown("## 💡 Suggested Automation Strategy")

    for strategy in strategies:

        st.markdown(f"- {strategy}")

    st.divider()

    # -------------------------------------------------
    # AI Summary
    # -------------------------------------------------

    st.markdown("## 📋 AI Summary")

    st.info(row["Summary"])

    st.divider()

    # -------------------------------------------------
    # Download Excel
    # -------------------------------------------------

    excel_file = convert_df_to_excel(df)

    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name="Automation_Feasibility_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="automation_excel_download"
    )



st.divider()

st.caption(
    "🧪 AI QA Assistant • Version 1.0 • Powered by Google Gemini AI"
)