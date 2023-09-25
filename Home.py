import streamlit as st

# Import other pages
from pages import CSV_Summary, CSV_Analyser, PDF_Chat, Powerpoint_Creator

st.set_page_config(page_title="Your App Title", layout="wide")
st.title("Welcome To The App")

PAGES = {
    "Home": "home",
    "CSV Analyser": CSV_Analyser,
    "CSV Summary": CSV_Summary,
    "Power Point Creator": Powerpoint_Creator,
    "PDF Chat": PDF_Chat,
}

