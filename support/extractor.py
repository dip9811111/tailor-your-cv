import pickle
import weasyprint

from datetime import datetime
from support.html_builder import CVBuilder, CoverLetterBuilder
from support.settings import dest_dir
from support.supportClasses import Curriculum, FinalCurriculum, NewCurriculum, JobDescriptionInformation, CoverLetter, FinalCoverLetter
from support.supportLLM import system_prompt_data_extraction, system_prompt_curriculum_creation, system_prompt_jd_extraction, system_prompt_cover_letter_creation
from support.submission_manager import save_submission


class InformationExtractor:
    def __init__(self):

        self.system_prompt_data_extraction = system_prompt_data_extraction
        self.system_prompt_curriculum_creation = system_prompt_curriculum_creation
        self.system_prompt_cover_letter_creation = system_prompt_cover_letter_creation
        self.system_prompt_jd_extraction = system_prompt_jd_extraction

        self.MODEL = None

        self.structured_cv = None
        self.new_cv = None
        self.final_cv = None
        self.jd_information = None
        self.cover_letter = None
        self.final_cover_letter = None

        self.generated_pdf_path = f"{dest_dir}/cv_output.pdf"
        self.generated_cover_letter_pdf_path = f"{dest_dir}/cover_letter_output.pdf"

        self.structured_cv_path = f"{dest_dir}/structured_cv.pkl"
        self.new_cv_path = f"{dest_dir}/new_cv.pkl"
        self.cover_letter_path = f"{dest_dir}/cover_letter.pkl"
        self.jd_information_path = f"{dest_dir}/jd_info.pkl"

        self.generated_html = None
        self.generated_html_cover_letter = None


    def extract_data(self, markdown_cv: str = None, is_new_cv=False):
        """
        Extract structured data from a document using a language model.
        """

        if is_new_cv:
            user_message = f"""
                    This is my portfolio:
                    [START PORTFOLIO]
                    {markdown_cv}
                    [END PORTFOLIO]
                    """

            messages = [
                {"role": "system", "content": self.system_prompt_data_extraction},
                {"role": "user", "content": user_message},
            ]

            structured_llm = self.MODEL.with_structured_output(
                Curriculum,
                method="function_calling"
            )

            structured_cv = structured_llm.invoke(messages)

            with open(self.structured_cv_path, 'wb') as f:
                pickle.dump(structured_cv, f)

        else:
            with open(self.structured_cv_path, 'rb') as file:
                structured_cv = pickle.load(file)

        self.structured_cv = structured_cv

        return structured_cv

    def create_new_cover_letter(self, structured_curriculum: str, job_description: str):

        user_message = f"""
            This is my portfolio:

            [START PORTFOLIO]
            {structured_curriculum}
            [END PORTFOLIO]

            This is the job description:
            [JOB DESCRIPTION]
            {job_description}
            [END JOB DESCRIPTION]
        """

        messages = [
            {"role": "system", "content": self.system_prompt_cover_letter_creation},
            {"role": "user", "content": user_message},
        ]

        structured_llm = self.MODEL.with_structured_output(
            CoverLetter,
            method="function_calling"
        )

        cover_letter = structured_llm.invoke(messages)
        self.cover_letter = cover_letter

        with open(self.cover_letter_path, 'wb') as f:
            pickle.dump(cover_letter, f)

        return cover_letter

    def build_final_cover_letter(self, update_final_cover_letter=False, template_id="1"):

        if not update_final_cover_letter:
            final_cover_letter = FinalCoverLetter(
                name=self.structured_cv.personality.name,
                surname=self.structured_cv.personality.surname,
                current_position=self.structured_cv.personality.job_title,
                email=self.structured_cv.personality.e_mail,
                phone=self.structured_cv.personality.telephone,
                linkedin=self.structured_cv.personality.linkedin_link,
                github='',
                date=datetime.now().strftime("%d/%m/%Y"),
                recipient_name='',
                company_address='',
                company_name=self.jd_information.company_name if self.jd_information else None,
                position_title=self.jd_information.job_title if self.jd_information else None,
                salutation=self.cover_letter.salutation,
                body_paragraphs=self.cover_letter.body_paragraphs,
                closing=self.cover_letter.closing
            )

            self.final_cover_letter = final_cover_letter

            with open(f'{dest_dir}/final_cover_letter.pkl', 'wb') as f:
                pickle.dump(final_cover_letter, f)

        cover_letter_builder = CoverLetterBuilder()
        html_content = cover_letter_builder.build_html_from_cover_letter(
            cover_letter=self.final_cover_letter,
            template_id=template_id,
            dest_dir=dest_dir
        )
        self.generated_html_cover_letter = html_content

        return self.generated_html_cover_letter

    def create_new_cv(self, structured_curriculum: str, job_description: str):
        """
        Modify structured data from a document using a language model.
        """

        user_message = f"""
            This is my portfolio:

            [START PORTFOLIO]
            {structured_curriculum}
            [END PORTFOLIO]

            [JOB DESCRIPTION]
            {job_description}
            [END JOB DESCRIPTION]
        """

        messages = [
            {"role": "system", "content": self.system_prompt_curriculum_creation},
            {"role": "user", "content": user_message},
        ]

        structured_llm = self.MODEL.with_structured_output(
            NewCurriculum,
            method="function_calling"
        )

        new_structured_cv = structured_llm.invoke(messages)
        self.new_cv = new_structured_cv

        with open(self.new_cv_path, 'wb') as f:
            pickle.dump(new_structured_cv, f)

        user_message = f"""
            This is the Job Description:
            [JOB DESCRIPTION]
            {job_description}
            [END JOB DESCRIPTION]
        """

        messages = [
            {"role": "system", "content": self.system_prompt_jd_extraction},
            {"role": "user", "content": user_message},
        ]

        structured_llm = self.MODEL.with_structured_output(
            JobDescriptionInformation,
            method="function_calling"
        )

        jd_information = structured_llm.invoke(messages)
        self.jd_information = jd_information

        with open(self.jd_information_path, 'wb') as f:
            pickle.dump(jd_information, f)

        return new_structured_cv

    def build_final_cv(self, update_final_cv=False, template_id="1"):

        if not update_final_cv:
            final_CV = FinalCurriculum(
                personality=self.structured_cv.personality,
                job_title=self.structured_cv.personality.job_title,  # self.new_cv.job_title,
                summary=self.new_cv.summary,
                experiences=self.new_cv.experiences,
                projects=self.new_cv.projects,
                hard_skills=self.structured_cv.hard_skills,
                soft_skills=self.structured_cv.soft_skills,
                education=self.structured_cv.education
            )

            self.final_cv = final_CV

            with open(f'{dest_dir}/final_cv.pkl', 'wb') as f:
                pickle.dump(final_CV, f)

        cv_builder = CVBuilder()
        html_content = cv_builder.build_html_from_cv(
            cv=self.final_cv,
            template_id=template_id,
            dest_dir=dest_dir
        )
        self.generated_html = html_content

        return self.generated_html

    def create_pdf(self):
        weasyprint.HTML(string=self.generated_html).write_pdf(self.generated_pdf_path)
        weasyprint.HTML(string=self.generated_html_cover_letter).write_pdf(self.generated_cover_letter_pdf_path)

        jd_information = self.jd_information
        save_submission(
            jd_information.company_name,
            jd_information.job_title,
            self.generated_pdf_path,
            self.generated_cover_letter_pdf_path
        )
