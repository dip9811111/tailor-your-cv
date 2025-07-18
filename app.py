
import json
import os
import pickle
import streamlit as st

from streamlit.components.v1 import html
from support.extractor import InformationExtractor
from support.html_builder import a4_style, render_editable_cv
from support.load_models import load_openAI_model, load_gemini_model
from support.manage_ingestion import process_file
from support.settings import dest_dir, gemini_api_key_value, openai_api_key_value, TESTING


st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>AI CV Builder</h1>", unsafe_allow_html=True)

auto_click_html = """
<script>
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        const button = sidebar.querySelector('button');
        if (button) {
            button.click();
        }
    }
</script>
"""

with st.sidebar.expander("🔐 Models & Info", expanded=True):
    gemini_api_key = st.text_input("Enter your Gemini API key", value=gemini_api_key_value, type="password")
    openai_api_key = st.text_input("Enter your OpenAI API key", value=openai_api_key_value, type="password")
    uploaded_file = st.file_uploader("Upload your CV file", type=["pdf", "txt", "docx", "md"])
    job_description = st.text_area("Paste the job description here")
    if st.button("🪄 Generate my new CV"):
        st.session_state.generate_cv_trigger = True
        st.components.v1.html(auto_click_html, height=0)

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
elif gemini_api_key:
    os.environ["GOOGLE_API_KEY"] = gemini_api_key

left_col, right_col = st.columns([0.3, 0.7], gap="large")
with left_col:
    if uploaded_file:
        if "structured_cv" not in st.session_state:
            if openai_api_key or gemini_api_key:
                with st.spinner("Processing file..."):
                    markdown_cv = process_file(uploaded_file)
                    if markdown_cv:
                        error_ = False  
                        st.session_state.information_extractor = InformationExtractor()
                        if openai_api_key:
                            st.session_state.information_extractor.MODEL = load_openAI_model()
                        else:
                            st.session_state.information_extractor.MODEL = load_gemini_model()
                        structured_cv = st.session_state.information_extractor.extract_data(
                            markdown_cv=markdown_cv,
                            is_new_cv=True
                        )
                        st.session_state.structured_cv = structured_cv
                    else:
                        error_ = True
                if not error_:
                    st.success("File processed successfully.")
                else:
                    st.warning("Error processing file. Are you sure file is .pdf, .txt, .docx, .md?")
            else:
                st.warning("Please provide an API key to start processing your file.")

    if "final_cv" in st.session_state:
        render_editable_cv(st.session_state.final_cv)
        
    if st.session_state.get("generate_cv_trigger"):
        st.session_state.generate_cv_trigger = False  # Reset trigger
        if not (openai_api_key or gemini_api_key) or not os.path.exists(f"{dest_dir}/user_curriculum.md") or not job_description:
            st.warning("Please provide an API key, upload a CV file, and paste a job description.")
        else:
            if "information_extractor" not in st.session_state:
                st.session_state.information_extractor = InformationExtractor()
                st.session_state.information_extractor.MODEL = load_openAI_model()
                st.session_state.information_extractor.extract_data()
            with st.spinner("Generating your CV..."):
                try:
                    if not TESTING:
                        new_cv = st.session_state.information_extractor.create_new_cv(
                            structured_curriculum=st.session_state.information_extractor.structured_cv,
                            job_description=job_description
                        )
                    else:
                        with open(st.session_state.information_extractor.new_cv_path, 'rb') as file:
                            new_cv = pickle.load(file)
                        st.session_state.information_extractor.new_cv = new_cv
                    
                    response_json = new_cv.model_dump()
                    generated_html = st.session_state.information_extractor.build_final_cv()
                    st.session_state.final_cv = st.session_state.information_extractor.final_cv
                    render_editable_cv(st.session_state.information_extractor.final_cv)
                    st.session_state.final_cv_content = st.session_state.information_extractor.final_cv
                    st.session_state.generated_html = generated_html
                except Exception as e:
                    st.error(f"Failed to process the CV with the model: {e}")

with right_col:
    if "final_cv_content" in st.session_state and "generated_html" in st.session_state:
        html(a4_style.format(st.session_state.generated_html), height=1300, scrolling=True)

