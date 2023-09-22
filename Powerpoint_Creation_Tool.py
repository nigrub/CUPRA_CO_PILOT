import streamlit as st
from pptx import Presentation

def create_powerpoint(data_frames):
    # Create a PowerPoint presentation
    presentation = Presentation()

    # Add slides to the presentation based on your data frames
    for table_name, df in data_frames.items():
        # Create a new slide
        slide = presentation.slides.add_slide(presentation.slide_layouts[5])  # Customize the slide layout as needed

        # Set the title for the slide
        title = slide.shapes.title
        title.text = f"Table: {table_name}"  # Customize the title as needed

        # Add content to the slide (e.g., tables, charts, text, etc.)
        # You can use the data in df to populate the slide content

    return presentation

def app():
    st.title("PowerPoint Creation Tool")

    # Check if data frames are available in the session state
    if "tables_dataframes" in st.session_state:
        data_frames = st.session_state["tables_dataframes"]

        st.sidebar.header("Create PowerPoint")
        if st.sidebar.button("Generate PowerPoint"):
            presentation = create_powerpoint(data_frames)

            # Offer the presentation download link
            st.sidebar.markdown(get_pptx_download_link(presentation), unsafe_allow_html=True)

    else:
        st.write("No data available. Please upload a CSV file on the home page.")

if __name__ == '__main__':
    app()
