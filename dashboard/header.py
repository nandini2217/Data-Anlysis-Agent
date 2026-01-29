import streamlit as st
from datetime import datetime

def render_header(dataset_name, chart_type, theme):
    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        st.markdown("## 📊 AI Business Intelligence Dashboard")

    with col2:
        st.markdown(f"**Chart Type:** {chart_type}")
        st.markdown(f"**Theme:** {theme}")

    with col3:
        st.markdown(f"**Generated:** {datetime.now().strftime('%d %b %Y %H:%M')}")

    st.markdown("---")
