import os
import pickle
import time
import streamlit as st
from support.extractor import InformationExtractor
from support.load_models import load_openAI_model, load_gemini_model
from support.html_builder import render_editable_cv, render_editable_cover_letter
from support.file_manager import FileManager
from support.settings import TESTING

st.set_page_config(page_title="New Submission", layout="wide")

st.title("📝 New Job Submission")
st.markdown("Create tailored CV and cover letter for a specific job application.")

# Initialize file manager
file_manager = FileManager()

# Initialize submission tracking
if "current_submission_id" not in st.session_state:
    st.session_state.current_submission_id = None
if "is_new_submission" not in st.session_state:
    st.session_state.is_new_submission = True

# Check if portfolio exists in session state or load from file
if "structured_cv" not in st.session_state:
    # Try to load existing portfolio from file
    existing_portfolio = file_manager.load_portfolio_data()
    if existing_portfolio:
        st.session_state.structured_cv = existing_portfolio
        st.success("✅ Existing portfolio loaded automatically!")
    else:
        st.warning("⚠️ Please create your portfolio first in the 'Portfolio' page.")
        st.page_link("pages/portfolio.py", label="Go to Portfolio", icon="📁")
        st.stop()

# Check if API keys are configured
if "selected_model" not in st.session_state:
    st.warning("⚠️ Please configure your API keys in 'Manage Settings' first.")
    st.page_link("pages/manage_settings.py", label="Go to Manage Settings", icon="🔑")
    st.stop()

# Get API keys and model from session state
openai_api_key = st.session_state.get("openai_api_key", "")
gemini_api_key = st.session_state.get("gemini_api_key", "")
selected_model = st.session_state.get("selected_model", "openai")

# Set environment variables
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
if gemini_api_key:
    os.environ["GOOGLE_API_KEY"] = gemini_api_key

# Job Description Input
st.subheader("📋 Job Description")
job_description = st.text_area(
    "Paste the job description here", 
    height=200,
    placeholder="Paste the complete job description including requirements, responsibilities, and company information..."
)

# Generate Button
if st.button("🪄 Generate Tailored Documents", type="primary"):
    if not job_description:
        st.error("Please provide a job description.")
    else:
        # Reset submission state for new generation
        st.session_state.is_new_submission = True
        st.session_state.current_submission_id = None
        
        with st.spinner("Generating your tailored CV and cover letter..."):
            try:
                # Initialize information extractor if not present
                if "information_extractor" not in st.session_state:
                    st.session_state.information_extractor = InformationExtractor()
                
                # Load the appropriate model
                if selected_model == "gemini" and gemini_api_key:
                    st.session_state.information_extractor.MODEL = load_gemini_model()
                elif selected_model == "openai" and openai_api_key:
                    st.session_state.information_extractor.MODEL = load_openAI_model()
                else:
                    st.error("❌ No valid API key found for the selected model")
                    st.stop()
                
                # Set the structured CV
                st.session_state.information_extractor.structured_cv = st.session_state.structured_cv
                
                # Debug information
                st.info(f"🔍 Debug Info: Using {selected_model.upper()} model")
                st.info(f"🔍 Debug Info: Structured CV loaded: {st.session_state.structured_cv is not None}")
                
                if not TESTING:
                    # Generate new CV
                    st.info("🔄 Generating new CV...")
                    new_cv = st.session_state.information_extractor.create_new_cv(
                        structured_curriculum=st.session_state.structured_cv,
                        job_description=job_description,
                    )
                    
                    # Generate cover letter
                    st.info("🔄 Generating cover letter...")
                    cover_letter = st.session_state.information_extractor.create_new_cover_letter(
                        structured_curriculum=st.session_state.structured_cv,
                        job_description=job_description,
                    )
                else:
                    # Load test data
                    with open(st.session_state.information_extractor.new_cv_path, "rb") as file:
                        new_cv = pickle.load(file)
                    with open(st.session_state.information_extractor.cover_letter_path, "rb") as file:
                        cover_letter = pickle.load(file)
                    with open(st.session_state.information_extractor.jd_information_path, "rb") as file:
                        jd_information = pickle.load(file)
                    
                    st.session_state.information_extractor.new_cv = new_cv
                    st.session_state.information_extractor.cover_letter = cover_letter
                    st.session_state.information_extractor.jd_information = jd_information
                
                # Build final documents
                st.info("🔄 Building final CV...")
                generated_html = st.session_state.information_extractor.build_final_cv()
                st.info("🔄 Building final cover letter...")
                generated_html_cover_letter = st.session_state.information_extractor.build_final_cover_letter()
                
                # Store in session state
                st.session_state.final_cv_content = st.session_state.information_extractor.final_cv
                st.session_state.generated_html = generated_html
                st.session_state.final_cover_letter_content = st.session_state.information_extractor.final_cover_letter
                st.session_state.generated_html_cover_letter = generated_html_cover_letter
                
                st.success("✅ Tailored documents generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Failed to process the CV with the model: {e}")
                st.error(f"❌ Error type: {type(e).__name__}")
                
                # Show more detailed error information
                import traceback
                st.error("📋 Full error traceback:")
                st.code(traceback.format_exc())
                
                # Show debug information
                st.info("🔍 Debug Information:")
                st.info(f"   - Selected model: {selected_model}")
                st.info(f"   - OpenAI API key configured: {bool(openai_api_key)}")
                st.info(f"   - Gemini API key configured: {bool(gemini_api_key)}")
                st.info(f"   - Structured CV in session: {bool('structured_cv' in st.session_state)}")
                st.info(f"   - Information extractor in session: {bool('information_extractor' in st.session_state)}")
                
                if 'information_extractor' in st.session_state:
                    st.info(f"   - Model initialized: {st.session_state.information_extractor.MODEL is not None}")
                    if st.session_state.information_extractor.MODEL:
                        st.info(f"   - Model type: {type(st.session_state.information_extractor.MODEL)}")

# Document Editor and Preview
if "generated_html" in st.session_state and "generated_html_cover_letter" in st.session_state:
    st.subheader("✏️ Edit & Preview Documents")
    
    # Create tabs for CV and Cover Letter
    tab1, tab2 = st.tabs(["📄 CV Editor & Preview", "✉️ Cover Letter Editor & Preview"])
    
    with tab1:
        # CV Editor and Preview
        col1, col2 = st.columns([0.4, 0.6], gap="large")
        
        with col1:
            st.markdown("**📝 Edit Your CV**")
            render_editable_cv(st.session_state.final_cv_content)
        
        with col2:
            st.markdown("**👀 CV Preview**")
            st.components.v1.html(
                st.session_state.generated_html, 
                height=1300, 
                scrolling=True
            )
    
    with tab2:
        # Cover Letter Editor and Preview
        col1, col2 = st.columns([0.4, 0.6], gap="large")
        
        with col1:
            st.markdown("**📝 Edit Your Cover Letter**")
            render_editable_cover_letter(st.session_state.final_cover_letter_content)
        
        with col2:
            st.markdown("**👀 Cover Letter Preview**")
            st.components.v1.html(
                st.session_state.generated_html_cover_letter, 
                height=1300, 
                scrolling=True
            )
    
    # Save and Download Section
    st.subheader("💾 Save & Download")
    
    # Check if submission exists in database
    submission_exists = False
    if "information_extractor" in st.session_state and hasattr(st.session_state.information_extractor, 'jd_information'):
        if st.session_state.information_extractor.jd_information:
            submission_exists = True
    
    # Display submission status
    if submission_exists:
        st.success("✅ Submission is ready for database")
        st.info("💡 Your documents have been generated and are ready to save to the database.")
        
        # Show submission info
        jd_info = st.session_state.information_extractor.jd_information
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Company:** {jd_info.company_name}")
            st.info(f"**Position:** {jd_info.job_title}")
        with col2:
            st.info(f"**CV Generated:** ✅")
            st.info(f"**Cover Letter Generated:** ✅")
    else:
        st.warning("⚠️ Documents need to be generated before saving")
        st.info("💡 Click 'Generate Tailored Documents' to create your CV and cover letter.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save to Database", type="primary"):
            try:
                # Validate job description information before saving
                if not st.session_state.information_extractor.jd_information:
                    st.error("❌ Job description information is missing. Please regenerate the documents.")
                elif not st.session_state.information_extractor.jd_information.company_name:
                    st.error("❌ Company name is missing. Please check the job description or update the cover letter.")
                elif not st.session_state.information_extractor.jd_information.job_title:
                    st.error("❌ Job title is missing. Please check the job description or update the cover letter.")
                else:
                    if st.session_state.is_new_submission:
                        # Create new submission
                        st.session_state.information_extractor.create_pdf()
                        st.session_state.is_new_submission = False
                        st.session_state.current_submission_id = "new"  # Will be set after save
                        st.success("✅ New submission created in database!")
                    else:
                        # Update existing submission
                        from support.submission_manager import update_submission, get_all_submissions
                        all_submissions = get_all_submissions()
                        if all_submissions:
                            latest_submission_id = all_submissions[-1][0]
                            update_submission(
                                latest_submission_id,
                                st.session_state.information_extractor.final_cv,
                                st.session_state.information_extractor.final_cover_letter,
                                st.session_state.information_extractor.jd_information
                            )
                            st.session_state.current_submission_id = latest_submission_id
                            st.success("✅ Existing submission updated in database!")
                        else:
                            st.error("❌ No existing submission found to update")
                    
                    st.rerun()  # Refresh to show updated status
            except Exception as e:
                st.error(f"❌ Error saving to database: {e}")
                # Show more detailed error information
                if "NOT NULL constraint failed" in str(e):
                    st.error("💡 This error usually means job description information is missing. Try updating the cover letter with the correct company name and job title.")
    
    with col2:
        if submission_exists:
            if st.button("⬇️ Download PDFs"):
                try:
                    # Set session state to show download buttons
                    st.session_state.show_downloads = True
                    st.session_state.download_generated = False
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error preparing downloads: {e}")
        else:
            st.button("⬇️ Download PDFs", disabled=True, help="Generate documents first")

# Handle PDF generation and download display
if "show_downloads" not in st.session_state:
    st.session_state.show_downloads = False
if "download_generated" not in st.session_state:
    st.session_state.download_generated = False

if st.session_state.show_downloads and not st.session_state.download_generated:
    st.subheader("⬇️ Download Documents")
    
    if st.button("🔄 Generate PDFs for Download"):
        try:
            st.info("🔄 Generating PDFs for download...")
            
            # Use current submission ID if available, otherwise get latest
            submission_id_to_use = None
            if st.session_state.current_submission_id and st.session_state.current_submission_id != "new":
                submission_id_to_use = st.session_state.current_submission_id
            else:
                # Get the latest submission ID from database
                from support.submission_manager import get_all_submissions
                all_submissions = get_all_submissions()
                if all_submissions:
                    submission_id_to_use = all_submissions[-1][0]  # Get the most recent submission
                    # Update current submission ID
                    st.session_state.current_submission_id = submission_id_to_use
            
            if submission_id_to_use:
                # Generate PDFs
                from support.submission_manager import generate_pdf_from_submission, cleanup_temp_files
                cv_path, cl_path, temp_dir = generate_pdf_from_submission(submission_id_to_use)
                
                if cv_path and cl_path and os.path.exists(cv_path) and os.path.exists(cl_path):
                    # Store paths in session state for download buttons
                    st.session_state.cv_path = cv_path
                    st.session_state.cl_path = cl_path
                    st.session_state.temp_dir = temp_dir
                    st.session_state.download_generated = True
                    st.rerun()
                else:
                    st.error("❌ Failed to generate PDFs")
            else:
                st.error("❌ No submission found to generate PDFs from")
                
        except Exception as e:
            st.error(f"❌ Error generating PDFs: {e}")

# Show download buttons if PDFs are ready
if st.session_state.download_generated and "cv_path" in st.session_state:
    st.success("✅ PDFs generated and ready for download!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            with open(st.session_state.cv_path, 'rb') as f:
                st.download_button(
                    label="📥 Download CV PDF",
                    data=f.read(),
                    file_name="CV.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ Error reading CV PDF: {e}")
    
    with col2:
        try:
            with open(st.session_state.cl_path, 'rb') as f:
                st.download_button(
                    label="📥 Download Cover Letter PDF",
                    data=f.read(),
                    file_name="Cover_Letter.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ Error reading Cover Letter PDF: {e}")
    
    # Clean up button
    if st.button("🧹 Clean Up Temporary Files"):
        try:
            from support.submission_manager import cleanup_temp_files
            cleanup_temp_files(st.session_state.temp_dir)
            
            # Clear session state
            st.session_state.show_downloads = False
            st.session_state.download_generated = False
            if "cv_path" in st.session_state:
                del st.session_state.cv_path
            if "cl_path" in st.session_state:
                del st.session_state.cl_path
            if "temp_dir" in st.session_state:
                del st.session_state.temp_dir
            
            st.success("✅ Temporary files cleaned up!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error cleaning up files: {e}")
    
    # Auto-cleanup after 5 minutes
    if "download_timestamp" not in st.session_state:
        st.session_state.download_timestamp = time.time()
    
    if time.time() - st.session_state.download_timestamp > 300:  # 5 minutes
        try:
            from support.submission_manager import cleanup_temp_files
            cleanup_temp_files(st.session_state.temp_dir)
            
            # Clear session state
            st.session_state.show_downloads = False
            st.session_state.download_generated = False
            if "cv_path" in st.session_state:
                del st.session_state.cv_path
            if "cl_path" in st.session_state:
                del st.session_state.cl_path
            if "temp_dir" in st.session_state:
                del st.session_state.temp_dir
            if "download_timestamp" in st.session_state:
                del st.session_state.download_timestamp
            
            st.info("⏰ Temporary files automatically cleaned up after 5 minutes")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error during auto-cleanup: {e}")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("home.py", label="Back to Home", icon="🏠")
with col2:
    st.page_link("pages/portfolio.py", label="Portfolio", icon="📁")
with col3:
    st.page_link("pages/my_submissions.py", label="My Submissions", icon="📁")
