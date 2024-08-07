import streamlit as st
from lib.engine import transcript_processing, docs_generation
import logging
import os

# Load the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API key not found. Please set the API_KEY environment variable.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(page_title="Transcript2Docs", layout="centered", page_icon="📑", initial_sidebar_state="auto", menu_items=None)
st.title(":bookmark_tabs: Transcript2Docs")

# Sidebar for inputs
st.sidebar.header("Input Parameters")
context_keywords = st.sidebar.text_area("Enter context keywords:", help="Separate keywords with commas. This helps to optimize the original transcript and write the documentation.")
docs_structure = st.sidebar.text_area("Enter document structure:", help="Separate by commas. Outline the desired structure of the final documentation.")
transcript_type = st.sidebar.selectbox("Transcript type:", ("Live Tutorial", "Technical Walk-Through", "Knowledge Sharing", "General Meeting"), help="Specify the type of transcript")
transcript_file = st.sidebar.file_uploader("Upload transcript file:", type=['txt', 'docx', 'vtt'], help="Upload the transcript .txt, .docx, or .vtt file here.")

# Initialize session state for storing the generated document
if 'final_docs' not in st.session_state:
    st.session_state.final_docs = None

if st.sidebar.button('Generate Docs'):
    if transcript_file is not None and context_keywords and docs_structure:
        try:
            with st.spinner('Processing transcript...'):
                final_transcript = transcript_processing(file=transcript_file, context=context_keywords, type=transcript_type)
                st.text_area("Optimized Transcript:", value=final_transcript, height=300)

            st.success("Transcript processing complete! Now, generating docs...")

            with st.spinner('Creating docs...'):
                final_docs = docs_generation(transcript=final_transcript, structure=docs_structure, context=context_keywords, type=transcript_type)
                st.session_state.final_docs = final_docs  # Store the generated document in session state

            st.success("Docs creation complete!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            logging.error(f"Error during processing: {e}")
    else:
        st.error("Please upload a transcript file and ensure all inputs are filled.")

# Display the generated document if it exists in session state
if st.session_state.final_docs:
    # Render the final document as HTML markdown with custom CSS class
    st.markdown(st.session_state.final_docs)
    # Provide a download button to save the document as a .md file
    st.download_button(label="Download Docs", data=st.session_state.final_docs, file_name="generated_docs.md", mime="text/markdown")