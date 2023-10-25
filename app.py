import streamlit as st
import PDF_Chat
import test_3
import CSV_Analyser
import CSV_Summary
import Data_Chat
import Powerpoint_Creator

# Set the page config here, before importing any other modules that might call Streamlit functions
st.set_page_config(page_title="Your App Title", layout="wide")

PAGES = {
    "Home": "home",  # added this line for the home page
    "PDF Co-Pilot": PDF_Chat,
    "CUPRA Co-Pilot": test_3,
    "CSV Analyser": CSV_Analyser,
    "CSV Summary": CSV_Summary,
    "Data Interrogation": Data_Chat,
    "PowerPoint Creation": Powerpoint_Creator
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))
if selection == "Home":
    st.title("Welcome To The App")
    st.write("Please select a Co-Pilot from the sidebar to navigate.")
else:
    page = PAGES[selection]
    page.app()

