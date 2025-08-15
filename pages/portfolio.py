import os
import streamlit as st
from support.extractor import InformationExtractor
from support.manage_ingestion import process_file
from support.load_models import load_openAI_model, load_gemini_model
from support.file_manager import FileManager

st.set_page_config(page_title="Portfolio", layout="wide")

st.title("📁 Portfolio Management")
st.markdown("Manage your CV data and uploaded files.")

# Initialize file manager
file_manager = FileManager()

# Check if API keys are configured
if "selected_model" not in st.session_state:
    st.warning("⚠️ Please configure your API keys in 'Manage Settings' first.")
    st.page_link("pages/manage_settings.py", label="Go to Manage Settings", icon="🔑")
    st.stop()

# Get API keys from session state
openai_api_key = st.session_state.get("openai_api_key", "")
gemini_api_key = st.session_state.get("gemini_api_key", "")
selected_model = st.session_state.get("selected_model", "openai")

# Set environment variables
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
if gemini_api_key:
    os.environ["GOOGLE_API_KEY"] = gemini_api_key

# Check for existing portfolio data
existing_portfolio = file_manager.load_portfolio_data()

# Auto-load existing portfolio if available
if existing_portfolio and "structured_cv" not in st.session_state:
    st.session_state.structured_cv = existing_portfolio
    st.session_state.final_cv = existing_portfolio
    st.session_state.exps = existing_portfolio.experiences or []
    st.session_state.projs = existing_portfolio.projects or []
    st.session_state.edus = existing_portfolio.education or []
    st.success("✅ Existing portfolio loaded automatically!")

# Portfolio Status Section
st.subheader("📊 Portfolio Status")
col1, col2, col3 = st.columns(3)

with col1:
    if "structured_cv" in st.session_state:
        st.success("✅ Portfolio Ready")
        portfolio_files = file_manager.get_portfolio_files()
        if portfolio_files:
            last_updated = portfolio_files[0]['modified'].strftime('%Y-%m-%d %H:%M')
            st.markdown(f"**Last Updated:** {last_updated}")
        else:
            st.markdown("**Last Updated:** Unknown")
    else:
        st.warning("⚠️ No Portfolio")
        st.markdown("*Upload a CV to get started*")

with col2:
    uploaded_files = file_manager.get_uploaded_files()
    st.info(f"📁 {len(uploaded_files)} Uploaded Files")
    if uploaded_files:
        st.markdown(f"**Latest:** {uploaded_files[0]['original_name']}")

with col3:
    if "structured_cv" in st.session_state:
        exp_count = len(st.session_state.structured_cv.experiences or [])
        proj_count = len(st.session_state.structured_cv.projects or [])
        edu_count = len(st.session_state.structured_cv.education or [])
        st.metric("Total Entries", exp_count + proj_count + edu_count)

st.markdown("---")

# Main Content Tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "✏️ Edit Portfolio", "📁 File Management"])

with tab1:
    st.subheader("📤 Upload New CV File")
    
    # Show existing portfolio info if available
    if "structured_cv" in st.session_state:
        st.info("💡 You already have a portfolio. Uploading a new file will replace the current one.")
        
        # Show current portfolio summary
        cv = st.session_state.structured_cv
        col1, col2 = st.columns(2)
        with col1:
            name = cv.personality.name or 'N/A'
            surname = cv.personality.surname or 'N/A'
            st.markdown(f"**Current CV:** {name} {surname}")
            st.markdown(f"**Job Title:** {cv.personality.job_title or 'N/A'}")
        with col2:
            st.markdown(f"**Experiences:** {len(cv.experiences or [])}")
            st.markdown(f"**Projects:** {len(cv.projects or [])}")
            st.markdown(f"**Education:** {len(cv.education or [])}")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CV file", 
        type=["pdf", "txt", "docx", "md"],
        help="Supported formats: PDF, TXT, DOCX, MD"
    )
    
    if uploaded_file:
        # Show file info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**File:** {uploaded_file.name}")
            st.markdown(f"**Size:** {uploaded_file.size} bytes")
        with col2:
            st.markdown(f"**Type:** {uploaded_file.type}")
        
        # Process button
        if st.button("🔄 Process CV", type="primary"):
            with st.spinner("Processing your CV..."):
                try:
                    # Save uploaded file
                    file_path, safe_filename = file_manager.save_uploaded_file(
                        uploaded_file, uploaded_file.name
                    )
                    
                    # Process the file
                    markdown_cv = process_file(uploaded_file)
                    
                    if markdown_cv:
                        # Initialize information extractor
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
                        
                        # Extract structured data
                        structured_cv = st.session_state.information_extractor.extract_data(
                            markdown_cv=markdown_cv, is_new_cv=True
                        )
                        
                        # Store in session state
                        st.session_state.structured_cv = structured_cv
                        st.session_state.final_cv = structured_cv
                        
                        # Initialize editable lists
                        st.session_state.exps = structured_cv.experiences or []
                        st.session_state.projs = structured_cv.projects or []
                        st.session_state.edus = structured_cv.education or []
                        
                        # Save to portfolio directory
                        file_manager.save_portfolio_data(structured_cv)
                        
                        st.success("✅ CV processed successfully!")
                        st.rerun()
                        
                    else:
                        st.error("❌ Failed to process file. Please check the file format.")
                        
                except Exception as e:
                    st.error(f"❌ Error processing CV: {str(e)}")

with tab2:
    if "structured_cv" in st.session_state:
        st.subheader("✏️ Edit Your Portfolio")
        
        # Load from session state
        if "final_cv" not in st.session_state:
            st.session_state.final_cv = st.session_state.structured_cv
        
        # Initialize session lists if not present
        if "exps" not in st.session_state:
            st.session_state.exps = st.session_state.final_cv.experiences or []
        if "projs" not in st.session_state:
            st.session_state.projs = st.session_state.final_cv.projects or []
        if "edus" not in st.session_state:
            st.session_state.edus = st.session_state.final_cv.education or []
        
        # Callback functions
        def add_entry(entry_type):
            if entry_type == "exp":
                if st.session_state.exps:
                    st.session_state.exps.append(type(st.session_state.exps[0])())
                else:
                    from support.supportClasses import Experience
                    st.session_state.exps.append(Experience())
            elif entry_type == "proj":
                if st.session_state.projs:
                    st.session_state.projs.append(type(st.session_state.projs[0])())
                else:
                    from support.supportClasses import Experience
                    st.session_state.projs.append(Experience())
            elif entry_type == "edu":
                if st.session_state.edus:
                    st.session_state.edus.append(type(st.session_state.edus[0])())
                else:
                    from support.supportClasses import EducationExperience
                    st.session_state.edus.append(EducationExperience())
        
        def delete_entry(entry_type, idx):
            if entry_type == "exp":
                st.session_state.exps.pop(idx)
            elif entry_type == "proj":
                st.session_state.projs.pop(idx)
            elif entry_type == "edu":
                st.session_state.edus.pop(idx)
        
        # Portfolio Editor Interface
        col1, col2 = st.columns([0.6, 0.4])
        
        with col1:
            # Personal Information
            with st.expander("👤 Personal Information", expanded=True):
                st.session_state.final_cv.personality.name = st.text_input(
                    "Name", 
                    value=st.session_state.final_cv.personality.name or "",
                    key="portfolio_name"
                )
                st.session_state.final_cv.personality.surname = st.text_input(
                    "Surname", 
                    value=st.session_state.final_cv.personality.surname or "",
                    key="portfolio_surname"
                )
                st.session_state.final_cv.personality.job_title = st.text_input(
                    "Current Job Title", 
                    value=st.session_state.final_cv.personality.job_title or "",
                    key="portfolio_job_title"
                )
                st.session_state.final_cv.personality.e_mail = st.text_input(
                    "Email", 
                    value=st.session_state.final_cv.personality.e_mail or "",
                    key="portfolio_email"
                )
                st.session_state.final_cv.personality.telephone = st.text_input(
                    "Telephone", 
                    value=st.session_state.final_cv.personality.telephone or "",
                    key="portfolio_phone"
                )
                st.session_state.final_cv.personality.linkedin_link = st.text_input(
                    "LinkedIn", 
                    value=st.session_state.final_cv.personality.linkedin_link or "",
                    key="portfolio_linkedin"
                )
                st.session_state.final_cv.personality.address = st.text_input(
                    "Address", 
                    value=st.session_state.final_cv.personality.address or "",
                    key="portfolio_address"
                )
            
            # Summary
            with st.expander("📝 Summary", expanded=True):
                st.session_state.final_cv.summary = st.text_area(
                    "Professional Summary", 
                    value=st.session_state.final_cv.summary or "",
                    height=100,
                    key="portfolio_summary"
                )
            
            # Skills
            with st.expander("🧩 Skills", expanded=True):
                hard_skills_input = st.text_area(
                    "Hard Skills (comma-separated)",
                    value=", ".join(st.session_state.final_cv.hard_skills or []),
                    key="portfolio_hard_skills"
                )
                soft_skills_input = st.text_area(
                    "Soft Skills (comma-separated)",
                    value=", ".join(st.session_state.final_cv.soft_skills or []),
                    key="portfolio_soft_skills"
                )
        
        with col2:
            # Work Experience
            with st.expander("💼 Work Experience", expanded=True):
                for i, exp in enumerate(st.session_state.exps):
                    with st.container():
                        st.markdown(f"**Experience #{i+1}**")
                        exp.title = st.text_input("Title", exp.title or "", key=f"portfolio_exp_title_{i}")
                        exp.company = st.text_input("Company", exp.company or "", key=f"portfolio_exp_company_{i}")
                        exp.start_date = st.text_input("Start Date", exp.start_date or "", key=f"portfolio_exp_start_{i}")
                        exp.end_date = st.text_input("End Date", exp.end_date or "", key=f"portfolio_exp_end_{i}")
                        exp.description = st.text_area("Description", exp.description or "", key=f"portfolio_exp_desc_{i}", height=80)
                        st.button("❌ Remove", key=f"portfolio_del_exp_{i}", on_click=delete_entry, args=("exp", i))
                        st.markdown("---")
                
                st.button("➕ Add Experience", on_click=add_entry, args=("exp",), key="portfolio_add_exp_btn")
            
            # Projects
            with st.expander("🛠️ Projects", expanded=True):
                for i, proj in enumerate(st.session_state.projs):
                    with st.container():
                        st.markdown(f"**Project #{i+1}**")
                        proj.title = st.text_input("Title", proj.title or "", key=f"portfolio_proj_title_{i}")
                        proj.company = st.text_input("Company/Organization", proj.company or "", key=f"portfolio_proj_company_{i}")
                        proj.start_date = st.text_input("Start Date", proj.start_date or "", key=f"portfolio_proj_start_{i}")
                        proj.end_date = st.text_input("End Date", proj.end_date or "", key=f"portfolio_proj_end_{i}")
                        proj.description = st.text_area("Description", proj.description or "", key=f"portfolio_proj_desc_{i}", height=80)
                        st.button("❌ Remove", key=f"portfolio_del_proj_{i}", on_click=delete_entry, args=("proj", i))
                        st.markdown("---")
                
                st.button("➕ Add Project", on_click=add_entry, args=("proj",))
            
            # Education
            with st.expander("🎓 Education", expanded=True):
                for i, edu in enumerate(st.session_state.edus):
                    with st.container():
                        st.markdown(f"**Education #{i+1}**")
                        edu.title = st.text_input("Degree/Title", edu.title or "", key=f"portfolio_edu_title_{i}")
                        edu.school_name = st.text_input("School/University", edu.school_name or "", key=f"portfolio_edu_school_{i}")
                        edu.start_date = st.text_input("Start Date", edu.start_date or "", key=f"portfolio_edu_start_{i}")
                        edu.end_date = st.text_input("End Date", edu.end_date or "", key=f"portfolio_edu_end_{i}")
                        edu.description = st.text_area("Description", edu.description or "", key=f"portfolio_edu_desc_{i}", height=80)
                        st.button("❌ Remove", key=f"portfolio_del_edu_{i}", on_click=delete_entry, args=("edu", i))
                        st.markdown("---")
                
                st.button("➕ Add Education", on_click=add_entry, args=("edu",))
        
        # Save Portfolio Button
        if st.button("💾 Save Portfolio", type="primary"):
            # Update skills
            st.session_state.final_cv.hard_skills = [s.strip() for s in hard_skills_input.split(",") if s.strip()]
            st.session_state.final_cv.soft_skills = [s.strip() for s in soft_skills_input.split(",") if s.strip()]
            
            # Update experiences, projects, and education
            st.session_state.final_cv.experiences = st.session_state.exps
            st.session_state.final_cv.projects = st.session_state.projs
            st.session_state.final_cv.education = st.session_state.edus
            
            # Save to file
            file_manager.save_portfolio_data(st.session_state.final_cv)
            
            st.success("✅ Portfolio saved successfully!")
            
            # Update session state
            st.session_state.structured_cv = st.session_state.final_cv
    else:
        st.info("📁 No portfolio found. Please upload a CV file first.")

with tab3:
    st.subheader("📁 File Management")
    
    # Uploaded Files Section
    st.markdown("**📤 Uploaded CV Files**")
    uploaded_files = file_manager.get_uploaded_files()
    
    if uploaded_files:
        for file_info in uploaded_files:
            col1, col2, col3, col4 = st.columns([0.4, 0.2, 0.2, 0.2])
            with col1:
                st.markdown(f"**{file_info['original_name']}**")
                st.caption(f"Uploaded: {file_info['modified'].strftime('%Y-%m-%d %H:%M')}")
            with col2:
                st.markdown(f"{file_info['size']:,} bytes")
            with col3:
                if st.button("🗑️", key=f"del_{file_info['filename']}", help="Delete file"):
                    if file_manager.delete_uploaded_file(file_info['filename']):
                        st.success("File deleted!")
                        st.rerun()
            with col4:
                if st.button("📥", key=f"download_{file_info['filename']}", help="Download file"):
                    with open(file_info['path'], 'rb') as f:
                        st.download_button(
                            label="Download",
                            data=f.read(),
                            file_name=file_info['original_name'],
                            mime="application/octet-stream"
                        )
            st.markdown("---")
    else:
        st.info("No uploaded files yet.")
    
    # Portfolio Files Section
    st.markdown("**💾 Portfolio Data Files**")
    portfolio_files = file_manager.get_portfolio_files()
    
    if portfolio_files:
        for file_info in portfolio_files:
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            with col1:
                st.markdown(f"**{file_info['filename']}**")
                st.caption(f"Last modified: {file_info['modified'].strftime('%Y-%m-%d %H:%M')}")
            with col2:
                st.markdown(f"{file_info['size']:,} bytes")
            with col3:
                if st.button("📥", key=f"download_portfolio_{file_info['filename']}", help="Download portfolio data"):
                    with open(file_info['path'], 'rb') as f:
                        st.download_button(
                            label="Download",
                            data=f.read(),
                            file_name=file_info['filename'],
                            mime="application/octet-stream"
                        )
            st.markdown("---")
    else:
        st.info("No portfolio data files yet.")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("home.py", label="Back to Home", icon="🏠")
with col2:
    st.page_link("pages/manage_settings.py", label="Manage Settings", icon="⚙️")
with col3:
    st.page_link("pages/new_submission.py", label="New Submission", icon="📝")
