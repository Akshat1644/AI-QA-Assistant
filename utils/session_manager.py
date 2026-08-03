import streamlit as st


def save(key, value):
    st.session_state[key] = value


def load(key, default=None):
    return st.session_state.get(key, default)


def exists(key):
    return key in st.session_state


def remove(key):
    if key in st.session_state:
        del st.session_state[key]


def clear_all():
    st.session_state.clear()