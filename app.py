
import json
import os
import streamlit as st

from support.extractor import InformationExtractor
from support.load_models import load_openAI_model
from support.manage_ingestion import process_file
from support.settings import api_key_value


st.title("AI CV Builder")
api_key = st.sidebar.text_input(
    "Enter your OpenAI API key",
    value=api_key_value,
    type="password"
)

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

uploaded_file = st.file_uploader("Upload your CV file")
if uploaded_file:
    if "structured_cv" not in st.session_state:
        if api_key:
            with st.spinner("Processing file..."):
                markdown_cv = process_file(uploaded_file)
                if markdown_cv:
                    error_ = False  
                    st.session_state.information_extractor = InformationExtractor()
                    st.session_state.information_extractor.MODEL = load_openAI_model()
                    structured_cv = st.session_state.information_extractor.extract_data(
                        markdown_cv=markdown_cv,
                        is_new_cv=True
                    )
                    st.session_state.structured_cv = structured_cv
                    with st.chat_message("assistant"):
                        response_json = structured_cv.model_dump()
                        st.markdown(f"```json\n{json.dumps(response_json, indent=2)}\n```")
                else:
                    error_ = True
            if not error_:
                st.success("File processed successfully.")
            else:
                st.warning("Error processing file. Are you sure file is .pdf, .txt, .docx, .md?")
        else:
            st.warning("Please provide your API key before.")

job_description = st.text_area("Paste the job description here")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.button("Build my new CV"):
    if not api_key or not os.path.exists("output/user_curriculum.md") or not job_description:
        st.warning("Please provide your API key, upload a CV file, and paste a job description.")
    else:
        if "information_extractor" not in st.session_state:
            st.session_state.information_extractor = InformationExtractor()
            st.session_state.information_extractor.MODEL = load_openAI_model()
            st.session_state.information_extractor.extract_data()
        with st.chat_message("assistant"):
            with st.spinner("Generating your CV..."):
                try:
                    final_cv = st.session_state.information_extractor.create_new_cv(
                        structured_curriculum=st.session_state.information_extractor.structured_cv,
                        job_description=job_description
                    )
                    response_json = final_cv.model_dump()
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": f"```json\n{json.dumps(response_json, indent=2)}\n```"
                        }
                    )
                    st.markdown(f"```json\n{json.dumps(response_json, indent=2)}\n```")
                    st.session_state.information_extractor.build_final_CV()
                    if os.path.exists(st.session_state.information_extractor.generated_pdf_path):
                        with open(st.session_state.information_extractor.generated_pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()

                        st.download_button(
                            label="📄 Download CV as PDF",
                            data=pdf_bytes,
                            file_name="my_new_cv.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"Failed to process the CV with the model: {e}")
