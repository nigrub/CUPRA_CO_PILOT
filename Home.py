import streamlit as st

# Import other pages
from pages import Powerpoint_Creator_2, CSV_Analyser_2, Data_Chat_2, CSV_Summary_2

st.set_page_config(page_title="Your App Title", layout="wide")
st.title("Welcome To The App")

PAGES = {
    "Home": "home",
    "CSV Analyser": CSV_Analyser,
    "CSV Summary": CSV_Summary,
    "Power Point Creator": Powerpoint_Creator,
    "Data Chat": Data_Chat,
}

