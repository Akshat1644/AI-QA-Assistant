import streamlit as st


def section(title, body, icon="📌"):

    with st.container(border=True):

        st.markdown(f"### {icon} {title}")

        st.write(body)