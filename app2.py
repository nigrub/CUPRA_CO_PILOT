import streamlit as st

# Import other pages
from pages import CSV_Summary, CSV_Analyser

st.set_page_config(page_title="Your App Title", layout="wide")
st.title("Welcome To The App")

PAGES = {
    "Home": "home",
    "CSV Analyser": CSV_Analyser,
    "CSV Summary": CSV_Summary,
}

