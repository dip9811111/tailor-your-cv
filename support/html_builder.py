import base64
import os
import streamlit as st

from string import Formatter
from support.settings import dest_dir
from support.html_templates.html_templates import CVTemplates


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
            'job_title': cv.job_title,
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
            "Template 3": "3"
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

    if st.button("📄 Generate PDF"):
        with st.spinner("Generating PDF..."):
            st.session_state.information_extractor.create_pdf()

        pdf_path = st.session_state.information_extractor.generated_pdf_path
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            # Encode PDF to base64
            b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            href = f'data:application/pdf;base64,{b64_pdf}'

            download_html = f"""
            <html>
            <body>
                <a id="autoDownload" href="{href}" download="my_new_cv.pdf"></a>
                <script>
                    document.getElementById('autoDownload').click();
                </script>
            </body>
            </html>
            """
            st.success("✅ PDF generated. Download should start automatically.")
            st.components.v1.html(download_html, height=0)
        else:
            st.error("❌ Failed to generate PDF.")


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