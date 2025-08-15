
class CVTemplates:
    """Collection of HTML templates for CV generation"""
    
    @staticmethod
    def template_1():
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <style>
                @page {{ size: A4; margin: 0.25in; }}
                * {{ box-sizing: border-box; }}
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 11px;
                    line-height: 1.3;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    height: 100vh;
                    max-height: 10.5in;
                }}

                #container {{
                    display: flex;
                    width: 100%;
                    height: 100%;
                }}

                #main {{
                    flex: 7.5;
                    padding: 1rem;
                    overflow: hidden;
                }}
                
                aside {{
                    flex: 2.5;
                    background: #f8f8f8;
                    padding: 1rem;
                    font-size: 10px;
                    overflow: auto;
                }}
                h1 {{
                    margin: 0 0 0.5rem 0;
                    font-size: 26px;
                    line-height: 1.2;
                }}
                h2 {{
                    color: #8B0000;
                    border-bottom: 1px solid #8B0000;
                    padding-bottom: 2px;
                    margin: 0.8rem 0 0.5rem 0;
                    font-size: 18px;
                }}
                h3 {{
                    border-bottom: 1px solid #ccc;
                    margin: 0.8rem 0 0.3rem 0;
                    font-size: 12px;
                    padding-bottom: 2px;
                }}
                .job_title{{
                    font-size: 14px;
                }}
                .section-block {{
                    margin-bottom: 0.8rem;
                }}
                .entry {{
                    margin-bottom: 0.6rem;
                    page-break-inside: avoid;
                }}
                .entry-header {{
                    margin-bottom: 0.2rem;
                    line-height: 1.2;
                }}
                .entry-header strong {{
                    font-size: 16px;
                }}
                .entry strong {{
                    font-size: 14px;
                }}
                .cv-date {{
                    font-size: 12px;
                    color: #333;
                    margin-left: 0.4rem;
                    font-weight: bold;
                }}
                p {{
                    margin: 0.2rem 0;
                    line-height: 1.3;
                    font-size: 12px;
                }}
                .sidebar-section {{
                    margin-bottom: 0.8rem;
                }}
                .contact-item {{
                    margin-bottom: 0.3rem;
                    font-size: 9px;
                    line-height: 1.2;
                    word-break: break-word;
                }}
                .skills-content {{
                    font-size: 11px;
                    line-height: 1.3;
                    word-wrap: break-word;
                }}
                a {{
                    color: #8B0000;
                    text-decoration: none;
                    word-break: break-all;
                }}
            </style>
        </head>
        <body>
            <div id="container">
                <section id="main">
                    <h1>{name} {surname}</h1>
                    <div class="job_title">{job_title}</div>
                    <div class="section-block">
                        <h2>SUMMARY</h2>
                        <p>{summary}</p>
                    </div>

                    <div class="section-block">
                        <h2>EXPERIENCES</h2>
                        {experiences}
                    </div>

                    <div class="section-block">
                        <h2>MY PROJECTS</h2>
                        {projects}
                    </div>

                    <div class="section-block">
                        <h2>EDUCATION</h2>
                        {education}
                    </div>
                </section>

                <aside>
                    <div class="sidebar-section">
                        <h3>CONTACT INFO</h3>
                        {contact_info}
                    </div>
                    <div class="sidebar-section">
                        <h3>HARD SKILLS</h3>
                        <div class="skills-content">
                            {hard_skills}
                        </div>
                        <h3>SOFT SKILLS</h3>
                        <div class="skills-content">
                            {soft_skills}
                        </div>
                    </div>
                </aside>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def template_2():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{ size: A4; margin: 0.5in; }}
                * {{ box-sizing: border-box; }}

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

                .job_title{{
                    font-size: 18px;
                    font-weight: bold;
                    color: #6B46C1;
                    margin-bottom: 5px;
                    letter-spacing: 1px;
                    margin-top: auto;
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
                <div class="name">{name} {surname}</div>
                <div class="job_title">{job_title}</div>
                <div class="contact-info">
                    {contact_info}
                </div>
            </div>

            <div class="section">
                <div class="section-title">Summary</div>
                <p class="summary-text">{summary}</p>
            </div>

            <div class="section">
                <div class="section-title">Work Experience</div>
                {experiences}
            </div>

            <div class="section">
                <div class="section-title">My Projects</div>
                {projects}
            </div>

            <div class="section">
                <div class="section-title">Education</div>
                {education}
            </div>

            <div class="two-column">
                <div class="column">
                    <div class="section">
                        <div class="section-title">Hard Skills</div>
                        <div class="skills-content">{hard_skills}</div>
                    </div>
                </div>

                <div class="column">
                    <div class="section">
                        <div class="section-title">Soft Skills</div>
                        <div class="skills-content">{soft_skills}</div>
                    </div>
                </div>
            </div>

        </body>
        </html>
        """


class CoverLetterTemplates:
    """Collection of HTML templates for Cover Letter generation"""

    @staticmethod
    def template_1():
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <style>
                @page {{ size: A4; margin: 0.75in; }}
                * {{ box-sizing: border-box; }}
                body {{
                    font-family: 'Calibri', 'Arial', sans-serif;
                    font-size: 11pt;
                    line-height: 1.5;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    max-width: 8.5in;
                    margin: 0 auto;
                }}

                .header {{
                    text-align: center;
                    margin-bottom: 2rem;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 1rem;
                }}

                .name {{
                    font-size: 24pt;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 0.3rem;
                    letter-spacing: 0.5px;
                }}

                .job-title {{
                    font-size: 14pt;
                    color: #666;
                    margin-bottom: 0.8rem;
                    font-style: italic;
                }}

                .contact-info {{
                    font-size: 10pt;
                    color: #555;
                    line-height: 1.3;
                }}

                .contact-info a {{
                    color: #2980b9;
                    text-decoration: none;
                }}

                .recipient {{
                    margin-bottom: 1.5rem;
                    font-size: 11pt;
                }}

                .recipient-name {{
                    font-weight: bold;
                    margin-bottom: 0.2rem;
                }}

                .recipient-details {{
                    color: #666;
                    line-height: 1.3;
                }}

                .date {{
                    font-size: 10pt;
                    color: #666;
                }}

                .subject {{
                    font-weight: bold;
                    text-transform: uppercase;
                    font-size: 18pt;
                    color: #2c3e50;
                    letter-spacing: 1px;
                }}

                .date-subject-line {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 2rem 0 1.5rem 0;
                }}

                .salutation {{
                    margin-bottom: 1rem;
                    font-size: 11pt;
                }}

                .body-content {{
                    margin-bottom: 1.5rem;
                    text-align: justify;
                    font-size: 11pt;
                    line-height: 1.6;
                }}

                .body-content p {{
                    margin-bottom: 1rem;
                    text-indent: 0;
                }}

                .closing {{
                    margin-top: 2rem;
                    margin-bottom: 1rem;
                }}

                .signature {{
                    margin-top: 2rem;
                    font-weight: bold;
                    color: #2c3e50;
                }}

                .highlight {{
                    background-color: #f8f9fa;
                    padding: 0.1rem 0.3rem;
                    border-radius: 3px;
                }}

                .skills-mention {{
                    font-style: italic;
                    color: #2980b9;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="name">{name} {surname}</div>
                <div class="job-title">{current_position}</div>
                <div class="contact-info"> {email} {phone} {linkedin} {github}</div>
            </div>

            <div class="date-subject-line">
                <div class="subject">{position_title}</div>
                <div class="date">{date}</div>
            </div>

            <div class="salutation">{salutation}</div>

            <div class="body-content">
                {body_content}
            </div>

            <div class="closing">{closing}</div>

            <div class="signature">{name} {surname}</div>
        </body>
        </html>
        """
