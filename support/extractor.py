import os
import pickle
import weasyprint

from support.html_builder import build_html_from_cv
from support.supportClasses import Curriculum, NewCurriculum, FinalCurriculum
from support.supportLLM import system_prompt_data_extraction, system_prompt_curriculum_creation


class InformationExtractor:
    def __init__(self):

        self.system_prompt_data_extraction = system_prompt_data_extraction
        self.system_prompt_curriculum_creation = system_prompt_curriculum_creation
        self.MODEL = None
        self.structured_cv = None
        self.new_cv = None
        self.generated_pdf_path = "output/cv_output.pdf"
        self.structured_cv_path = "output/structured_cv.pkl"

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

    def create_new_cv(self, structured_curriculum: str, job_description: str):
        """
        Extract structured data from a document using a language model.
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

        return new_structured_cv

    def build_final_CV(self):

        final_CV = FinalCurriculum(
            personality=self.structured_cv.personality,
            summary=self.new_cv.summary,
            experiences=self.new_cv.experiences,
            projects=self.new_cv.projects,
            hard_skills=self.structured_cv.hard_skills,
            soft_skills=self.structured_cv.soft_skills,
            education=self.structured_cv.education
        )

        with open('output/final_cv.pkl', 'wb') as f:
            pickle.dump(final_CV, f)

        html_content = build_html_from_cv(final_CV)
        weasyprint.HTML(string=html_content).write_pdf(self.generated_pdf_path)
