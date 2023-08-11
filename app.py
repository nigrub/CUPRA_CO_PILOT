import streamlit as st
import PDF_Chat
import test_3

PAGES = {
    "PDF Chat": PDF_Chat,
    "Test 3": test_3
}

def main():
    st.sidebar.title('Navigation')
    choice = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[choice]
    page.app()

if __name__ == "__main__":
    main()
