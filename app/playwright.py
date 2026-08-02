import streamlit as st

from gemini_service import generate_ai_response
from prompts import PLAYWRIGHT_SCRIPT_PROMPT
from utils.formatting import clean_code_response


def render_playwright_script(requirement):

    if not requirement.strip():
        st.warning("Please enter a software requirement.")
        return

    prompt = PLAYWRIGHT_SCRIPT_PROMPT.format(
        requirement=requirement
    )

    with st.spinner("Generating Playwright Script..."):

        try:

            result = generate_ai_response(prompt)

            result = clean_code_response(result)

            st.session_state["playwright_script"] = result

        except Exception:

            st.error("Failed to generate Playwright Script.")
            return

    script = st.session_state["playwright_script"]

    st.subheader("🎭 AI Generated Playwright Script")

    st.code(
        script,
        language="typescript"
    )

    st.download_button(
        label="📥 Download Playwright Script",
        data=script,
        file_name="playwright_script.spec.ts",
        mime="text/plain",
        key="playwright_script_download"
    )