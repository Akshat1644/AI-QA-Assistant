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

from app.quality_score import render_quality_score

from app.coverage import render_coverage_analysis

from app.risk import render_risk_analysis

from app.defect_prediction import render_defect_prediction

from app.smart_rtm import render_smart_rtm

from app.completeness import render_requirement_completeness

from app.bug_prediction import render_bug_prediction

from app.defect_report import render_defect_report

from app.defect_report import render_defect_report

from app.regression_analysis import render_regression_analysis

from app.automation_feasibility import render_automation_feasibility


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



# -------------------------------
# Handle Button Clicks
# -------------------------------

if quality_score:
    st.session_state["active_page"] = "quality"

if requirement_completeness:
    st.session_state["active_page"] = "completeness"

if analyze_gap:
    st.session_state["active_page"] = "gap"

if coverage_analysis:
    st.session_state["active_page"] = "coverage"

if risk_analysis:
    st.session_state["active_page"] = "risk"

if bug_prediction:
    st.session_state["active_page"] = "bug_prediction"

if defect_prediction:
    st.session_state["active_page"] = "defect_prediction"

if regression_analysis:
    st.session_state["active_page"] = "regression"

if automation_feasibility:
    st.session_state["active_page"] = "automation"

if generate_tc:
    st.session_state["active_page"] = "testcase"

if generate_test_data:
    st.session_state["active_page"] = "testdata"

if generate_api_tc:
    st.session_state["active_page"] = "api"

if generate_playwright_script:
    st.session_state["active_page"] = "playwright"

if generate_rtm:
    st.session_state["active_page"] = "rtm"

if defect_report:
    st.session_state["active_page"] = "defect_report"


# ==========================================================
# Render Selected Screen
# ==========================================================

active = st.session_state.get("active_page")

if active == "testcase":
    render_test_case(requirement)

elif active == "gap":
    render_gap_analysis(requirement)

elif active == "testdata":
    render_test_data(requirement)

elif active == "api":
    render_api_test_cases(requirement)

elif active == "playwright":
    render_playwright_script(requirement)

elif active == "quality":
    render_quality_score(requirement)

elif active == "coverage":
    render_coverage_analysis(requirement)

elif active == "risk":
    render_risk_analysis(requirement)

elif active == "defect_prediction":
    render_defect_prediction(requirement)

elif active == "rtm":
    render_smart_rtm(requirement)

elif active == "completeness":
    render_requirement_completeness(requirement)

elif active == "bug_prediction":
    render_bug_prediction(requirement)

elif active == "defect_report":
    render_defect_report(requirement)

elif active == "regression":
    render_regression_analysis(requirement)

elif active == "automation":
    render_automation_feasibility(requirement)



st.divider()

st.caption(
    "🧪 AI QA Assistant • Version 1.0 • Powered by Google Gemini AI"
)