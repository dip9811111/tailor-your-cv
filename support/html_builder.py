import base64
import os
import streamlit as st

from string import Formatter
from support.html_templates.html_templates import CVTemplates, CoverLetterTemplates
from typing import Optional


class CVBuilder:
    """Main CV builder class that handles template injection"""

    def __init__(self):
        self.templates = CVTemplates()

    def find_template_placeholders(self, template_string):
        """Find all placeholders in a template string"""
        formatter = Formatter()
        placeholders = [field_name for _, field_name, _, _ in formatter.parse(template_string) if field_name]
        return set(placeholders)

    def convert_date(self, element):
        """Convert date elements to formatted string"""
        date_string = ""
        start_date = element.start_date if element.start_date not in [None, "", "null"] else ""
        end_date = element.end_date if element.end_date not in [None, "", "null"] else ""

        if start_date and end_date:
            date_string = f"({start_date} - {end_date})"
        elif start_date:
            date_string = f"({start_date})"
        elif end_date:
            date_string = f"({end_date})"

        return date_string

    def format_experience(self, exp):
        """Format experience entry"""
        title = exp.title or ''
        company = f" - {exp.company}" if exp.company else ''
        return f"""
        <div class="entry">
            <strong>{title}{company}</strong> <span class="cv-date">{self.convert_date(exp)}</span>
            <p>{exp.description or ''}</p>
        </div>
        """

    def format_education(self, edu):
        """Format education entry"""
        title = edu.title or ''
        school = f", {edu.school_name}" if edu.school_name else ''
        return f"""
        <div class="entry">
            <strong>{title}{school}</strong> <span class="cv-date">{self.convert_date(edu)}</span>
            <p>{edu.description or ''}</p>
        </div>
        """

    def format_projects(self, proj):
        """Format project entry"""
        title = proj.title or ''
        company = f" - {proj.company}" if proj.company else ''
        return f"""
        <div class="entry">
            <strong>{title}{company}</strong> <span class="cv-date">{self.convert_date(proj)}</span>
            <p>{proj.description or ''}</p>
        </div>
        """

    def format_contact_info(self, cv):
        """Format contact information"""
        contact_parts = []

        if cv.personality.address:
            contact_parts.append(f'📍 {cv.personality.address}')
        if cv.personality.telephone:
            contact_parts.append(f'📞 {cv.personality.telephone}')
        if cv.personality.e_mail:
            contact_parts.append(f'✉️ {cv.personality.e_mail}')
        if cv.personality.linkedin_link:
            contact_parts.append(f'💼 {cv.personality.linkedin_link}')

        return " | ".join(contact_parts)

    def format_skills_list(self, skills):
        """Format skills list"""
        all_skills = []
        if skills:
            all_skills.extend(skills)
        return " • ".join(all_skills)

    def build_html_from_cv(self, cv, template_id="1", dest_dir="./"):
        """
        Build HTML from CV data using specified template

        Args:
            cv: CV data object
            template_id: ID of template to use ('1', '2', '3')
            dest_dir: Destination directory for output
        """

        # Get the template
        template_method = getattr(self.templates, f"template_{template_id}", None)
        if not template_method:
            raise ValueError(f"Template '{template_id}' not found. Available: modern, classic, minimalist")

        template = template_method()

        # Prepare data for injection
        template_data = {
            'name': cv.personality.name or '',
            'surname': cv.personality.surname or '',
            'job_title': cv.job_title or '',
            'experiences': ''.join(self.format_experience(exp) for exp in cv.experiences or []),
            'education': ''.join(self.format_education(edu) for edu in cv.education or []),
            'projects': ''.join(self.format_projects(proj) for proj in cv.projects or []),
            'contact_info': self.format_contact_info(cv),
            'hard_skills': self.format_skills_list(cv.hard_skills),
            'soft_skills': self.format_skills_list(cv.soft_skills),
            'summary': cv.summary or '',
        }

        # Inject data into template
        html_content = template.format(**template_data)

        # Write to file
        output_path = f"{dest_dir}/cv.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return html_content

    def get_available_templates(self):
        """Get list of available template names"""
        return ['modern', 'classic', 'minimalist']


class CoverLetterBuilder:
    """Main Cover Letter builder class that handles template injection"""

    def __init__(self):
        self.templates = CoverLetterTemplates()

    def format_contact_info(self, cover_letter):
        """Format contact information"""
        contact_parts = {}

        contact_parts['email'] = f"{cover_letter.email} |" or ''
        contact_parts['phone'] = f"{cover_letter.phone} |" or ''
        contact_parts['linkedin'] = f'<a href="{cover_letter.linkedin}">{cover_letter.linkedin} |</a>' if cover_letter.linkedin else ''
        contact_parts['github'] = f'<a href="{cover_letter.github}">{cover_letter.github} |</a>' if cover_letter.github else ''

        return contact_parts

    def format_body_content(self, paragraphs):
        """Format body content paragraphs"""
        if not paragraphs:
            return ""

        formatted_paragraphs = []
        for paragraph in paragraphs:
            if paragraph.strip():
                formatted_paragraphs.append(f"<p>{paragraph.strip()}</p>")

        return "\n".join(formatted_paragraphs)

    def build_html_from_cover_letter(self, cover_letter, template_id="1", dest_dir="./"):
        """
        Build HTML from Cover Letter data using specified template

        Args:
            cover_letter: Cover Letter data object
            template_id: ID of template to use ('1', '2', '3')
            dest_dir: Destination directory for output
        """

        # Get the template
        template_method = getattr(self.templates, f"template_{template_id}", None)
        if not template_method:
            raise ValueError(f"Template '{template_id}' not found.")

        template = template_method()

        # Format contact info
        contact_info = self.format_contact_info(cover_letter)

        # Prepare data for injection
        template_data = {
            'name': cover_letter.name or '',
            'surname': cover_letter.surname or '',
            'current_position': cover_letter.current_position or '',
            'email': contact_info['email'],
            'phone': contact_info['phone'],
            'linkedin': contact_info['linkedin'],
            'github': contact_info['github'],
            'date': cover_letter.date,
            # 'company_name': cover_letter.company_name or '',
            # 'company_address': cover_letter.company_address or '',
            'position_title': cover_letter.position_title or '',
            'salutation': cover_letter.salutation or 'Dear Hiring Manager,',
            'body_content': self.format_body_content(cover_letter.body_paragraphs or []),
            'closing': cover_letter.closing or 'Thank you for considering my application. I look forward to hearing from you.',
        }

        # Inject data into template
        html_content = template.format(**template_data)

        # Write to file
        output_path = f"{dest_dir}/cover_letter.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return html_content

    def get_available_templates(self):
        """Get list of available template names"""
        return ['professional', 'modern', 'classic']


def create_pdf_download_link(pdf_bytes: bytes, filename: str) -> str:
    """Create a data URI for PDF download."""
    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    return f'data:application/pdf;base64,{b64_pdf}'


def create_auto_download_html(href: str, filename: str) -> str:
    """Generate HTML that triggers automatic download."""
    return f"""
    <html>
    <body>
        <a id="autoDownload" href="{href}" download="{filename}"></a>
        <script>
            document.getElementById('autoDownload').click();
        </script>
    </body>
    </html>
    """


def read_pdf_file(file_path: str) -> Optional[bytes]:
    """Safely read PDF file and return bytes, or None if file doesn't exist."""
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "rb") as f:
            return f.read()
    except (IOError, OSError) as e:
        st.error(f"Error reading file {file_path}: {e}")
        return None


def trigger_pdf_downloads():
    """Main function to handle PDF downloads."""
    # Get file paths from session state
    cv_path = st.session_state.information_extractor.generated_pdf_path
    cover_letter_path = st.session_state.information_extractor.generated_cover_letter_pdf_path

    # Define download configurations
    downloads = [
        {"path": cv_path, "filename": "CV.pdf"},
        {"path": cover_letter_path, "filename": "Cover_Letter.pdf"}
    ]

    # Read and validate all files first
    pdf_data = []
    for config in downloads:
        pdf_bytes = read_pdf_file(config["path"])
        if pdf_bytes is None:
            st.error("❌ Failed to generate PDF.")
            return

        pdf_data.append({
            "bytes": pdf_bytes,
            "filename": config["filename"]
        })

    # All files exist, proceed with downloads
    st.success("✅ PDFs generated. Download should start automatically.")

    for data in pdf_data:
        href = create_pdf_download_link(data["bytes"], data["filename"])
        download_html = create_auto_download_html(href, data["filename"])
        st.components.v1.html(download_html, height=0)


def render_editable_cv(final_cv):
    # Ensure session lists are initialized
    if "exps" not in st.session_state:
        st.session_state.exps = final_cv.experiences or []
    if "projs" not in st.session_state:
        st.session_state.projs = final_cv.projects or []
    if "edus" not in st.session_state:
        st.session_state.edus = final_cv.education or []

    # Callback to add new empty entry
    def add_entry(entry_type):
        if entry_type == "exp":
            st.session_state.exps.append(type(final_cv.experiences[0])())  # or empty dataclass
        elif entry_type == "proj":
            st.session_state.projs.append(type(final_cv.projects[0])())
        else:
            st.session_state.edus.append(type(final_cv.education[0])())

    # Callback to delete entry at index
    def delete_entry(entry_type, idx):
        if entry_type == "exp":
            st.session_state.exps.pop(idx)
        elif entry_type == "proj":
            st.session_state.projs.pop(idx)
        else:
            st.session_state.edus.pop(idx)

    with st.expander("🧍‍♂️ Personality"):
        final_cv.personality.name = st.text_input("Name", value=final_cv.personality.name or "")
        final_cv.personality.surname = st.text_input("Surname", value=final_cv.personality.surname or "")
        final_cv.job_title = st.text_input("Job Title", value=final_cv.job_title or "")
        final_cv.personality.e_mail = st.text_input("Email", value=final_cv.personality.e_mail or "")
        final_cv.personality.telephone = st.text_input("Telephone", value=final_cv.personality.telephone or "")
        final_cv.personality.linkedin_link = st.text_input("LinkedIn", value=final_cv.personality.linkedin_link or "")
        final_cv.personality.address = st.text_input("Address", value=final_cv.personality.address or "")

    with st.expander("📝 Summary"):
        final_cv.summary = st.text_area("Summary", value=final_cv.summary or "", height=100)

    with st.expander("💼 Work Experience"):
        for i, exp in enumerate(st.session_state.exps):
            with st.container():
                st.markdown(f"**Experience #{i+1}**")
                exp.title = st.text_input("Title", exp.title or "", key=f"exp_title_{i}")
                exp.company = st.text_input("Company", exp.company or "", key=f"exp_company_{i}")
                exp.start_date = st.text_input("Start Date", exp.start_date or "", key=f"exp_start_{i}")
                exp.end_date = st.text_input("End Date", exp.end_date or "", key=f"exp_end_{i}")
                exp.description = st.text_area("Description", exp.description or "", key=f"exp_desc_{i}")
                st.button("❌ Remove Experience", key=f"del_exp_{i}", on_click=delete_entry, args=("exp", i))
                st.markdown("---")  # Horizontal line separator

        st.button("➕ Add Experience", on_click=add_entry, args=("exp",), key="add_exp_btn")

    with st.expander("🛠️ Projects"):
        for i, proj in enumerate(st.session_state.projs):
            with st.container():
                st.markdown(f"**Project #{i+1}**")
                proj.title = st.text_input("Title", proj.title or "", key=f"proj_title_{i}")
                proj.company = st.text_input("Company", proj.company or "", key=f"proj_company_{i}")
                proj.start_date = st.text_input("Start Date", proj.start_date or "", key=f"proj_start_{i}")
                proj.end_date = st.text_input("End Date", proj.end_date or "", key=f"proj_end_{i}")
                proj.description = st.text_area("Description", proj.description or "", key=f"proj_desc_{i}")
                st.button("❌ Remove Project", key=f"del_proj_{i}", on_click=delete_entry, args=("proj", i))
                st.markdown("---")
        st.button("➕ Add Project", on_click=add_entry, args=("proj",))

    with st.expander("🎓 Education"):
        for i, edu in enumerate(st.session_state.edus):
            with st.container():
                st.markdown(f"**Experience #{i+1}**")
                edu.title = st.text_input("Title", edu.title or "", key=f"edu_title_{i}")
                edu.school_name = st.text_input("School", edu.school_name or "", key=f"edu_school_{i}")
                edu.start_date = st.text_input("Start Date", edu.start_date or "", key=f"edu_start_{i}")
                edu.end_date = st.text_input("End Date", edu.end_date or "", key=f"edu_end_{i}")
                edu.description = st.text_area("Description", edu.description or "", key=f"edu_desc_{i}")
                st.button("❌ Remove Education", key=f"del_edu_{i}", on_click=delete_entry, args=("edu", i))
                st.markdown("---")
        st.button("➕ Add Education", on_click=add_entry, args=("edu",))

    with st.expander("🧩 Skills"):
        hard_skills_input = st.text_area(
            "Hard Skills (comma-separated)",
            value=", ".join(final_cv.hard_skills or []),
            key="hard_skills_input"
        )
        soft_skills_input = st.text_area(
            "Soft Skills (comma-separated)",
            value=", ".join(final_cv.soft_skills or []),
            key="soft_skills_input"
        )

    with st.expander("🧾 Template Selection", expanded=True):
        template_options = {
            "Template 1": "1",
            "Template 2": "2",
            # Add new templates
        }
        selected_template_label = st.selectbox("Choose a template", list(template_options.keys()))
        st.session_state.template_id = template_options[selected_template_label]

    if st.button("✅ Apply Modifications"):
        final_cv.hard_skills = [s.strip() for s in hard_skills_input.split(",") if s.strip()]
        final_cv.soft_skills = [s.strip() for s in soft_skills_input.split(",") if s.strip()]

        st.success("Changes applied. CV updated.")
        st.session_state.information_extractor.final_cv = final_cv
        st.session_state.generated_html = st.session_state.information_extractor.build_final_cv(
            update_final_cv=True,
            template_id=st.session_state.template_id
        )
        
        # Update database if submission exists
        if hasattr(st.session_state, 'current_submission_id') and st.session_state.current_submission_id:
            try:
                from support.submission_manager import update_submission, get_all_submissions
                # Get the latest submission to update
                all_submissions = get_all_submissions()
                if all_submissions:
                    latest_submission_id = all_submissions[-1][0]
                    # Update the submission with new CV data
                    update_submission(
                        latest_submission_id,
                        st.session_state.information_extractor.final_cv,
                        st.session_state.information_extractor.final_cover_letter,
                        st.session_state.information_extractor.jd_information
                    )
                    st.success("✅ Database updated with CV changes!")
            except Exception as e:
                st.warning(f"⚠️ Database update failed: {e}")

    if st.button("📄 Generate PDF"):
        with st.spinner("Generating PDF..."):
            st.session_state.information_extractor.create_pdf()

        trigger_pdf_downloads()


def render_editable_cover_letter(final_cover_letter):
    """Render editable cover letter interface"""
    # Ensure session state is initialized
    if "cover_letter_paragraphs" not in st.session_state:
        st.session_state.cover_letter_paragraphs = final_cover_letter.body_paragraphs or []
    
    # Callback to add new paragraph
    def add_paragraph():
        st.session_state.cover_letter_paragraphs.append("")
    
    # Callback to delete paragraph at index
    def delete_paragraph(idx):
        st.session_state.cover_letter_paragraphs.pop(idx)
    
    # Personal Information
    with st.expander("👤 Personal Information", expanded=True):
        final_cover_letter.name = st.text_input(
            "Name", 
            value=final_cover_letter.name or "",
            key="cl_name"
        )
        final_cover_letter.surname = st.text_input(
            "Surname", 
            value=final_cover_letter.surname or "",
            key="cl_surname"
        )
        final_cover_letter.current_position = st.text_input(
            "Current Position", 
            value=final_cover_letter.current_position or "",
            key="cl_position"
        )
        final_cover_letter.email = st.text_input(
            "Email", 
            value=final_cover_letter.email or "",
            key="cl_email"
        )
        final_cover_letter.phone = st.text_input(
            "Phone", 
            value=final_cover_letter.phone or "",
            key="cl_phone"
        )
        final_cover_letter.linkedin = st.text_input(
            "LinkedIn", 
            value=final_cover_letter.linkedin or "",
            key="cl_linkedin"
        )
        final_cover_letter.github = st.text_input(
            "GitHub", 
            value=final_cover_letter.github or "",
            key="cl_github"
        )
    
    # Cover Letter Content
    with st.expander("✉️ Cover Letter Content", expanded=True):
        final_cover_letter.salutation = st.text_input(
            "Salutation", 
            value=final_cover_letter.salutation or "Dear Hiring Manager,",
            key="cl_salutation"
        )
        
        st.markdown("**Body Paragraphs:**")
        for i, paragraph in enumerate(st.session_state.cover_letter_paragraphs):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.session_state.cover_letter_paragraphs[i] = st.text_area(
                    f"Paragraph {i+1}", 
                    paragraph, 
                    key=f"cl_para_{i}",
                    height=100
                )
            with col2:
                st.button("❌", key=f"cl_del_para_{i}", on_click=delete_paragraph, args=(i,))
        
        st.button("➕ Add Paragraph", on_click=add_paragraph, key="cl_add_para_btn")
        
        final_cover_letter.closing = st.text_input(
            "Closing", 
            value=final_cover_letter.closing or "Thank you for considering my application. I look forward to hearing from you.",
            key="cl_closing"
        )
    
    # Job Information
    with st.expander("💼 Job Information", expanded=True):
        final_cover_letter.position_title = st.text_input(
            "Position Title", 
            value=final_cover_letter.position_title or "",
            key="cl_job_title"
        )
        final_cover_letter.company_name = st.text_input(
            "Company Name", 
            value=final_cover_letter.company_name or "",
            key="cl_company"
        )
        final_cover_letter.recipient_name = st.text_input(
            "Recipient Name (optional)", 
            value=final_cover_letter.recipient_name or "",
            key="cl_recipient"
        )
        final_cover_letter.company_address = st.text_input(
            "Company Address (optional)", 
            value=final_cover_letter.company_address or "",
            key="cl_address"
        )
    
    # Template Selection
    with st.expander("🎨 Template Selection", expanded=True):
        template_options = {
            "Template 1": "1",
            #"Template 2": "2",
            # Add more templates as needed
        }
        selected_template_label = st.selectbox(
            "Choose a template", 
            list(template_options.keys()),
            key="cl_template_select"
        )
        st.session_state.cover_letter_template_id = template_options[selected_template_label]
    
    # Apply Changes Button
    if st.button("✅ Apply Cover Letter Changes", key="cl_apply_btn"):
        # Update body paragraphs
        final_cover_letter.body_paragraphs = st.session_state.cover_letter_paragraphs
        
        # Update job description information to match cover letter
        if "information_extractor" in st.session_state:
            # Use the new method to update job description information
            success = st.session_state.information_extractor.update_jd_from_cover_letter(final_cover_letter)
            if success:
                st.success("✅ Job description information also updated!")
            else:
                st.warning("⚠️ Job description information update failed, but cover letter changes were applied.")
        
        st.success("✅ Cover letter changes applied!")
        
        # Update session state
        if "information_extractor" in st.session_state:
            st.session_state.information_extractor.final_cover_letter = final_cover_letter
            st.session_state.generated_html_cover_letter = st.session_state.information_extractor.build_final_cover_letter(
                update_final_cover_letter=True,
                template_id=st.session_state.cover_letter_template_id
            )
            
            # Update database if submission exists
            if hasattr(st.session_state, 'current_submission_id') and st.session_state.current_submission_id:
                try:
                    from support.submission_manager import update_submission, get_all_submissions
                    # Get the latest submission to update
                    all_submissions = get_all_submissions()
                    if all_submissions:
                        latest_submission_id = all_submissions[-1][0]
                        # Update the submission with new cover letter data
                        update_submission(
                            latest_submission_id,
                            st.session_state.information_extractor.final_cv,
                            st.session_state.information_extractor.final_cover_letter,
                            st.session_state.information_extractor.jd_information
                        )
                        st.success("✅ Database updated with cover letter changes!")
                except Exception as e:
                    st.warning(f"⚠️ Database update failed: {e}")


a4_style = """
<div style="
    width: 794px;
    height: 1123px;
    margin: 10px 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2), 0 -5px 10px rgba(0, 0, 0, 0.4), 0 5px 10px rgba(0, 0, 0, 0.4);
    padding: 40px;
    background-color: white;
    overflow: hidden;
">
    {}
</div>
"""


def render_submissions_html(submissions):
    # Start HTML
    html = """
    <html>
      <head>
        <style>
          body {
            font-family: 'Segoe UI', sans-serif;
            padding: 0;
            margin: 0;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          }
          thead {
            background-color: #f3f4f6;
            font-weight: bold;
            text-align: left;
          }
          th, td {
            padding: 12px 16px;
            border-bottom: 1px solid #e5e7eb;
          }
          tr:hover {
            background-color: #f9fafb;
          }
          .download-btn {
            display: inline-block;
            background-color: #2563eb;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 14px;
            border: none;
            cursor: pointer;
            margin: 2px;
            transition: background-color 0.2s;
          }
          .download-btn:hover {
            background-color: #1e40af;
          }
          .download-btn:active {
            background-color: #1e3a8a;
          }
          .download-btn:disabled {
            background-color: #9ca3af;
            cursor: not-allowed;
          }
        </style>
      </head>
      <body>
        <table>
          <thead>
            <tr>
              <th>🏢 Company</th>
              <th>💼 Job Title</th>
              <th>📅 Generation Date</th>
            </tr>
          </thead>
          <tbody>
    """

    for id_, company, pos, date in submissions:
        date_str = date.split("T")[0]
        # Create visual download buttons (these will be replaced by Streamlit buttons)
        html += f"""
            <tr>
              <td>{company}</td>
              <td>{pos}</td>
              <td>{date_str}</td>
            </tr>
        """

    return html
