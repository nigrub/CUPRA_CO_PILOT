import streamlit as st

# Import other pages
from pages import CSV_Summary, CSV_Analyser

st.set_page_config(page_title="Your App Title", layout="wide")

PAGES = {
    "Home": "home",
    "CSV Analyser": CSV_Analyser,
    "CSV Summary": CSV_Summary,
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))

if selection == "Home":
    st.title("Welcome To The App")
    st.write("This is the home page of your app. Please select a page from the sidebar to navigate.")
else:
    page = PAGES[selection]
    page.app2()
