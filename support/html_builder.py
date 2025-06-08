import base64
import os
import streamlit as st

from support.settings import dest_dir


def build_html_from_cv(cv):

    def convert_date(element):
        date_string = ""

        # Normalize None/null values to empty strings for consistent checking
        start_date = element.start_date if element.start_date not in [None, "", "null"] else ""
        end_date = element.end_date if element.end_date not in [None, "", "null"] else ""

        if start_date and end_date:
            date_string = f"({start_date} - {end_date})"
        elif start_date:
            date_string = f"({start_date})"
        elif end_date:
            date_string = f"({end_date})"  # Fixed: was assigning to element instead of date_string

        return date_string

    def format_experience(exp):
        return f"""
        <div class="experience-entry">
            <div class="entry-header">
                <strong>{exp.title or ''} - {exp.company or ''}</strong> {convert_date(exp)}
            </div>
            <p>{exp.description or ''}</p>
        </div>
        """

    def format_education(edu):
        return f"""
        <div class="education-entry">
            <div class="entry-header">
                <strong>{edu.title or ''}, {edu.school_name or ''} </strong> {convert_date(edu)}
            </div>
            <p>{edu.description or ''}</p>
        </div>
        """

    def format_projects(proj):
        return f"""
        <div class="project-entry">
            <div class="entry-header">
                <strong>{proj.title or ''} - {proj.company or ''}</strong> {convert_date(proj)}
            </div>
            <p>{proj.description or ''}</p>
        </div>
        """

    def format_contact_info(cv):
        contact_parts = []

        if cv.personality.address:
            contact_parts.append(f'<span class="contact-item">📍 {cv.personality.address}</span>')

        if cv.personality.telephone:
            contact_parts.append(f'<span class="contact-item">📞 {cv.personality.telephone}</span>')

        if cv.personality.e_mail:
            contact_parts.append(f'<span class="contact-item">✉️ {cv.personality.e_mail}</span>')

        if cv.personality.linkedin_link:
            contact_parts.append(f'<span class="contact-item">💼 <a href="{cv.personality.linkedin_link}">{cv.personality.linkedin_link}</a></span>')

        return " ".join(c for c in contact_parts)

    def format_skills_list(skills):
        if not skills:
            return ""
        return " • ".join(skills)

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                margin: 0.5cm;
                size: A4;
            }}

            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: auto;
                padding: 20px;
                line-height: 1.2;
                color: #333;
                background-color: white;
                font-size: 12px;
            }}

            .header {{
                text-align: center;
                margin-bottom: 15px;
            }}

            .name {{
                font-size: 32px;
                font-weight: bold;
                color: #6B46C1;
                margin-bottom: 5px;
                letter-spacing: 1px;
                margin-top: -20px;
            }}

            .contact-info {{
                font-size: 11px;
                color: #666;
                margin-top: 8px;
            }}

            .contact-info a {{
                color: #6B46C1;
                text-decoration: none;
            }}

            .contact-info a:hover {{
                text-decoration: underline;
            }}

            .section {{
                margin-bottom: 15px;
            }}

            .section-title {{
                font-size: 18px;
                font-weight: bold;
                color: #6B46C1;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 10px;
                padding-bottom: 2px;
                border-bottom: 1.5px solid #6B46C1;
            }}

            .experience-entry, .education-entry, .project-entry {{
                margin-bottom: 10px;
            }}

            .entry-header {{
                margin-bottom: 2px;
                color: #333;
                font-size: 12px;
            }}

            .summary-text {{
                text-align: justify;
                margin-bottom: 0;
                font-size: 11px;
                line-height: 1.3;
            }}

            .skills-content {{
                font-size: 11px;
                line-height: 1.4;
            }}

            p {{
                margin: 3px 0;
                font-size: 11px;
                text-align: justify;
                line-height: 1.3;
            }}

            .two-column {{
                display: flex;
                gap: 25px;
                margin-bottom: 15px;
            }}

            .column {{
                flex: 1;
            }}

            @media (max-width: 600px) {{
                .two-column {{
                    flex-direction: column;
                    gap: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="name">{cv.personality.name or ''} {cv.personality.surname or ''}</div>
            <div class="contact-info">
                {format_contact_info(cv)}
            </div>
        </div>

        <div class="section">
            <div class="section-title">Summary</div>
            <p class="summary-text">{cv.summary or ''}</p>
        </div>

        <div class="section">
            <div class="section-title">Work Experience</div>
            {"".join(format_experience(exp) for exp in cv.experiences or [])}
        </div>

        <div class="section">
            <div class="section-title">Projects</div>
            {"".join(format_projects(proj) for proj in cv.projects or [])}
        </div>

        <div class="section">
            <div class="section-title">Education</div>
            {"".join(format_education(edu) for edu in cv.education or [])}
        </div>

        <div class="two-column">
            <div class="column">
                <div class="section">
                    <div class="section-title">Hard Skills</div>
                    <div class="skills-content">{format_skills_list(cv.hard_skills or [])}</div>
                </div>
            </div>

            <div class="column">
                <div class="section">
                    <div class="section-title">Soft Skills</div>
                    <div class="skills-content">{format_skills_list(cv.soft_skills or [])}</div>
                </div>
            </div>
        </div>

    </body>
    </html>
    """

    with open(f"{dest_dir}/cv.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    return html_template


def render_editable_cv(final_cv):
    st.markdown("## 🧠 Final CV Editor")

    with st.expander("🧍‍♂️ Personality"):
        final_cv.personality.name = st.text_input("Name", value=final_cv.personality.name or "")
        final_cv.personality.surname = st.text_input("Surname", value=final_cv.personality.surname or "")
        final_cv.personality.e_mail = st.text_input("Email", value=final_cv.personality.e_mail or "")
        final_cv.personality.telephone = st.text_input("Telephone", value=final_cv.personality.telephone or "")
        final_cv.personality.linkedin_link = st.text_input("LinkedIn", value=final_cv.personality.linkedin_link or "")
        final_cv.personality.address = st.text_input("Address", value=final_cv.personality.address or "")

    with st.expander("📝 Summary"):
        final_cv.summary = st.text_area("Summary", value=final_cv.summary or "", height=100)

    with st.expander("💼 Work Experience"):
        for i, exp in enumerate(final_cv.experiences or []):
            with st.container():
                st.markdown(f"#### Experience #{i+1}")
                exp.title = st.text_input(f"Title #{i+1}", value=exp.title or "", key=f"title_{i}")
                exp.company = st.text_input(f"Company #{i+1}", value=exp.company or "", key=f"company_{i}")
                exp.start_date = st.text_input(f"Start Date #{i+1}", value=exp.start_date or "", key=f"start_{i}")
                exp.end_date = st.text_input(f"End Date #{i+1}", value=exp.end_date or "", key=f"end_{i}")
                exp.description = st.text_area(f"Description #{i+1}", value=exp.description or "", key=f"desc_{i}")

    with st.expander("🛠️ Projects"):
        for i, proj in enumerate(final_cv.projects or []):
            with st.container():
                st.markdown(f"#### Project #{i+1}")
                proj.title = st.text_input(f"Title #{i+1}", value=proj.title or "", key=f"proj_title_{i}")
                proj.company = st.text_input(f"Company #{i+1}", value=proj.company or "", key=f"proj_company_{i}")
                proj.start_date = st.text_input(f"Start Date #{i+1}", value=proj.start_date or "", key=f"proj_start_{i}")
                proj.end_date = st.text_input(f"End Date #{i+1}", value=proj.end_date or "", key=f"proj_end_{i}")
                proj.description = st.text_area(f"Description #{i+1}", value=proj.description or "", key=f"proj_desc_{i}")

    with st.expander("🎓 Education"):
        for i, edu in enumerate(final_cv.education or []):
            with st.container():
                st.markdown(f"#### Education #{i+1}")
                edu.title = st.text_input(f"Title #{i+1}", value=edu.title or "", key=f"edu_title_{i}")
                edu.school_name = st.text_input(f"School #{i+1}", value=edu.school_name or "", key=f"edu_school_{i}")
                edu.start_date = st.text_input(f"Start Date #{i+1}", value=edu.start_date or "", key=f"edu_start_{i}")
                edu.end_date = st.text_input(f"End Date #{i+1}", value=edu.end_date or "", key=f"edu_end_{i}")
                edu.description = st.text_area(f"Description #{i+1}", value=edu.description or "", key=f"edu_desc_{i}")

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

    if st.button("✅ Apply Modifications"):
        final_cv.hard_skills = [s.strip() for s in hard_skills_input.split(",") if s.strip()]
        final_cv.soft_skills = [s.strip() for s in soft_skills_input.split(",") if s.strip()]

        st.success("Changes applied. CV updated.")
        st.session_state.information_extractor.final_cv = final_cv
        st.session_state.generated_html = st.session_state.information_extractor.build_final_cv(update_final_cv=True)

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