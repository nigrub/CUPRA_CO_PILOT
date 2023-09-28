import streamlit as st

# Import other pages
import CSV_Summary
import Data_Chat
import CSV_Analyser
import Powerpoint_Creator

st.set_page_config(page_title="Your App Title", layout="wide")
st.title("Welcome To The App")

PAGES = {
    "Home": "home",
    "CSV Analyser": CSV_Analyser,
    "CSV Summary": CSV_Summary,
    "Power Point Creator": Powerpoint_Creator,
    "Data Chat": Data_Chat,
}

