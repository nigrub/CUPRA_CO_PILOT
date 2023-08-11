import streamlit as st
import PDF_Chat
import test_3

# Set the page config here, before importing any other modules that might call Streamlit functions
st.set_page_config(page_title="Your App Title", layout="wide")

PAGES = {
    "Home": "home",  # added this line for the home page
    "PDF Co-Pilot": PDF_Chat,
    "CUPRA Co-Pilot": test_3
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))
if selection == "Home":
    st.title("Welcome To The App")
    st.write("Please select a Co-Pilot from the sidebar to navigate.")
else:
    page = PAGES[selection]
    page.app()

