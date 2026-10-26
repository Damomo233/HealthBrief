import streamlit as st


st.set_page_config(
    page_title="HealthBrief",
    page_icon="🩺",
    layout="wide"
)


homepage = st.Page(
    "homepage.py",
    title="Home",
    default=True
)


dashboard = st.Page(
    "dashboard.py",
    title="Dashboard"
)


navigation = st.navigation(
    [
        homepage,
        dashboard
    ],
    position="hidden"
)


navigation.run()