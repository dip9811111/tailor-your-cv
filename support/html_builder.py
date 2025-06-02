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
                <strong>{proj.title or ''}</strong> {convert_date(proj)}
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

    with open("output/cv.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    return html_template
