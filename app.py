import streamlit as st
from pdf_chat import pdf_chat_page
from test_3 import test_3_page

def home_page():
    st.header("Welcome to My Multipage App")
    st.write("This is the Home page. Choose a page from the sidebar to get started.")

def main():
    st.set_page_config(page_title="My Multipage App", page_icon=":book:")
    st.sidebar.title("Navigation")

    # Create a dictionary with page names as keys and corresponding functions as values
    pages = {
        "Home": home_page,
        "PDF Chat": pdf_chat_page,
        "Test 3": test_3_page
    }

    # Use selectbox to choose the page
    selected_page = st.sidebar.selectbox("Select a page:", list(pages.keys()))

    # Call the selected page function from the dictionary
    pages[selected_page]()

if __name__ == "__main__":
    main()
