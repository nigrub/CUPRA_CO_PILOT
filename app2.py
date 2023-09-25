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

# The `if` condition to check the page selection might be missing.
# For instance:
selection = st.sidebar.selectbox("Choose a page:", list(PAGES.keys()))

if selection == "Home":
    st.write("This is the homepage content.")  # Or whatever you'd like the home page to show.
else:
    page.app2()

