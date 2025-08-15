import streamlit as st
from support.submission_manager import get_all_submissions, generate_pdf_from_submission, cleanup_temp_files
from support.html_builder import render_submissions_html
import os

st.set_page_config(page_title="My Submissions", layout="wide")

st.title("📁 My Submissions")

submissions = get_all_submissions()

if not submissions:
    st.info("No applications yet. Once you generate CVs and cover letters, they will appear here.")
    st.stop()

# Search filter
search_query = st.text_input("🔍 Search by company or job title")
if search_query:
    filtered_submissions = [
        s for s in submissions 
        if (search_query.lower() in s[1].lower() or 
            search_query.lower() in s[2].lower())
    ]
    submissions = filtered_submissions

# Handle download requests
if "download_cv_id" not in st.session_state:
    st.session_state.download_cv_id = None
if "download_cl_id" not in st.session_state:
    st.session_state.download_cl_id = None

# Display table
html_content = render_submissions_html(submissions)
st.components.v1.html(html_content, height=500, scrolling=True)

# Add download buttons below the table
st.subheader("⬇️ Download Documents")
st.info("Select a submission from the dropdown below to download your documents.")

# Create a dropdown for submission selection
if submissions:
    # Create a list of submission options for the dropdown
    submission_options = []
    for submission in submissions:
        submission_id, company, position, date = submission
        date_str = date.split("T")[0]
        submission_options.append(f"{company} - {position} ({date_str})")
    
    # Add a "Select submission" option at the beginning
    submission_options.insert(0, "Select a submission...")
    
    # Create the dropdown
    selected_submission_label = st.selectbox(
        "Choose a submission to download:",
        options=submission_options,
        key="submission_selector"
    )
    
    # Handle download when a submission is selected
    if selected_submission_label != "Select a submission...":
        # Find the selected submission
        selected_index = submission_options.index(selected_submission_label) - 1  # -1 because we added the placeholder
        selected_submission = submissions[selected_index]
        submission_id, company, position, date = selected_submission
        
        st.success(f"✅ Selected: {company} - {position}")
        
        # Create download buttons for the selected submission
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Download CV", key=f"cv_download_{submission_id}"):
                st.session_state.download_cv_id = submission_id
                st.rerun()
        
        with col2:
            if st.button("📄 Download Cover Letter", key=f"cl_download_{submission_id}"):
                st.session_state.download_cl_id = submission_id
                st.rerun()
else:
    st.warning("No submissions available for download.")

# Handle downloads using session state
if st.session_state.download_cv_id:
    submission_id = st.session_state.download_cv_id
    with st.spinner("Generating CV PDF..."):
        try:
            cv_path, cl_path, temp_dir = generate_pdf_from_submission(submission_id)
            if cv_path and os.path.exists(cv_path):
                # Get submission details for filename
                submission_details = [s for s in submissions if s[0] == submission_id][0]
                company, position = submission_details[1], submission_details[2]
                
                with open(cv_path, 'rb') as f:
                    st.download_button(
                        label="📥 Download CV PDF",
                        data=f.read(),
                        file_name=f"CV_{company}_{position}.pdf",
                        mime="application/pdf"
                    )
                
                # Clean up temp files
                cleanup_temp_files(temp_dir)
                st.success("✅ CV PDF ready for download!")
            else:
                st.error("❌ Failed to generate CV PDF")
        except Exception as e:
            st.error(f"❌ Error generating CV: {e}")
    
    # Clear the download request
    st.session_state.download_cv_id = None

# Handle Cover Letter download
if st.session_state.download_cl_id:
    submission_id = st.session_state.download_cl_id
    with st.spinner("Generating Cover Letter PDF..."):
        try:
            cv_path, cl_path, temp_dir = generate_pdf_from_submission(submission_id)
            if cl_path and os.path.exists(cl_path):
                # Get submission details for filename
                submission_details = [s for s in submissions if s[0] == submission_id][0]
                company, position = submission_details[1], submission_details[2]
                
                with open(cl_path, 'rb') as f:
                    st.download_button(
                        label="📥 Download Cover Letter PDF",
                        data=f.read(),
                        file_name=f"Cover_Letter_{company}_{position}.pdf",
                        mime="application/pdf"
                    )
                
                # Clean up temp files
                cleanup_temp_files(temp_dir)
                st.success("✅ Cover Letter PDF ready for download!")
            else:
                st.error("❌ Failed to generate Cover Letter PDF")
        except Exception as e:
            st.error(f"❌ Error generating Cover Letter: {e}")
    
    # Clear the download request
    st.session_state.download_cl_id = None

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("home.py", label="⬅️ Back to Home", icon="🏠")
with col2:
    st.page_link("pages/portfolio.py", label="Portfolio", icon="📁")
with col3:
    st.page_link("pages/new_submission.py", label="New Submission", icon="📝")
