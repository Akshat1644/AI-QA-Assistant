import logging
import streamlit as st

from gemini_service import generate_ai_response
from prompts import PLAYWRIGHT_SCRIPT_PROMPT

from utils.formatting import clean_code_response
from utils.session_manager import save, load


def render_playwright_script(requirement):

    # ==========================================================
    # Generate Playwright Script
    # ==========================================================

    if load("playwright_script") is None:

        if not requirement.strip():
            st.warning("Please enter a software requirement.")
            return

        prompt = PLAYWRIGHT_SCRIPT_PROMPT.format(
            requirement=requirement
        )

        with st.spinner("Generating Playwright Script..."):

            try:

                result = generate_ai_response(prompt)

                script = clean_code_response(result)

                save("playwright_script", script)

                st.success("✅ Playwright Script generated successfully.")

            except Exception as e:

                logging.exception(e)

                st.error("Failed to generate Playwright Script.")
                return

    # ==========================================================
    # Display Saved Output
    # ==========================================================

    script = load("playwright_script")

    if script is None:
        return

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