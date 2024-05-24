import streamlit as st
from lib.engine import transcript_processing, docs_generation

st.set_page_config(page_title="Transcript2Docs", layout="centered", page_icon="📑", initial_sidebar_state="auto", menu_items=None)
st.title(":bookmark_tabs: Transcript2Docs")

context_keywords = st.text_area("Enter context keywords:", help="Separate keywords with commas. This helps to optimize the original transcript and write the documentation.")
docs_structure = st.text_area("Enter document structure:", help="Separate by commas. Outline the desired structure of the final documentation.")
transcript_type = st.selectbox("Transcript type:", ("Live Tutorial", "Technical Walk-Through", "Knowledge Sharing", "General Meeting"), help="Specify the type of transcript")
transcript_file = st.file_uploader("Upload transcript file:", type=['txt'], help="Upload the transcript .txt file here.")

if st.button('Generate Docs'):
    if transcript_file is not None and context_keywords and docs_structure:
        with st.spinner('Processing transcript…'):
            final_transcript = transcript_processing(file=transcript_file, context=context_keywords, type=transcript_type)
            st.text_area("Optimized Transcript:", value=final_transcript, height=300)

        st.success("Transcript processing complete! Now, generating docs…")

        with st.spinner('Creating docs…'):
            final_docs = docs_generation(transcript=final_transcript, structure=docs_structure, context=context_keywords, type=transcript_type)
            st.code(final_docs, language="markdown")

        st.success("Docs creation complete!")
    else:
        st.error("Please upload a transcript file and ensure all inputs are filled.")