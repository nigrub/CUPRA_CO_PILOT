import streamlit as st
import PDF_Chat
import test_3

# Set page configuration at the very start
st.set_page_config(page_title="Your App Title", layout="wide")

PAGES = {
    "PDF Chat": PDF_Chat,
    "Test 3": test_3
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

