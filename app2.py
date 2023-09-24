import streamlit as st

# Import other pages
from pages import Document_Chatter, Powerpoint_Creation_Tool, Document_Chat_Creation
import Summary_Chat

st.set_page_config(page_title="Your App Title", layout="wide")

PAGES = {
    "Home": "home",
    "CSV Data Analyzer": Document_Chat_Creation,
    "Document Chatter": Document_Chatter,
    "Summary Chat": Summary_Chat,
    "PowerPoint Creation Tool": Powerpoint_Creation_Tool,
}

selection = st.sidebar.radio("Go to", list(PAGES.keys()))

if selection == "Home":
    st.title("Welcome To The App")
    st.write("This is the home page of your app. Please select a page from the sidebar to navigate.")
else:
    page = PAGES[selection]
    page.app2()
