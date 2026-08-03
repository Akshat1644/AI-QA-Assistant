import streamlit as st


def show_metrics(metrics):

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        with col:

            st.metric(
                metric["label"],
                metric["value"]
            )