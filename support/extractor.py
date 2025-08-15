import pickle
import os

from datetime import datetime
from support.html_builder import CVBuilder, CoverLetterBuilder
from support.settings import dest_dir
from support.supportClasses import (
    Curriculum, FinalCurriculum, NewCurriculum, 
    JobDescriptionInformation, CoverLetter, FinalCoverLetter
)
from support.supportLLM import (
    system_prompt_data_extraction, system_prompt_curriculum_creation, 
    system_prompt_jd_extraction, system_prompt_cover_letter_creation
)


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

    def validate_model(self):
        """Validate that the model is properly initialized"""
        if self.MODEL is None:
            raise ValueError("Model is not initialized. Please set MODEL before calling methods.")
        
        print("✅ Model validation successful:")
        print(f"   - Model type: {type(self.MODEL)}")
        if hasattr(self.MODEL, 'model_name'):
            print(f"   - Model name: {self.MODEL.model_name}")
        if hasattr(self.MODEL, 'with_structured_output'):
            print("   - Supports structured output: Yes")
        else:
            print("   - Supports structured output: No")
        
        return True

    def load_existing_structured_cv(self):
        """Load existing structured CV data if available"""
        try:
            if os.path.exists(self.structured_cv_path):
                with open(self.structured_cv_path, 'rb') as file:
                    structured_cv = pickle.load(file)
                self.structured_cv = structured_cv
                return structured_cv
            return None
        except Exception as e:
            print(f"Error loading existing structured CV: {e}")
            return None

    def has_existing_structured_cv(self):
        """Check if structured CV data exists"""
        return os.path.exists(self.structured_cv_path)

    def extract_data(self, markdown_cv: str = None, is_new_cv=False):
        """
        Extract structured data from a document using a language model.
        """
        
        # Validate model before proceeding
        self.validate_model()

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

            try:
                structured_llm = self.MODEL.with_structured_output(
                    Curriculum,
                    method="function_calling"
                )

                structured_cv = structured_llm.invoke(messages)
                
                # Validate the response
                if structured_cv is None:
                    raise ValueError("LLM returned None response for CV extraction")
                
                if not hasattr(structured_cv, 'personality'):
                    raise ValueError(f"CV response missing 'personality' attribute. Response type: {type(structured_cv)}")
                
                if not hasattr(structured_cv, 'experiences'):
                    raise ValueError(f"CV response missing 'experiences' attribute. Response type: {type(structured_cv)}")
                
                if not hasattr(structured_cv, 'projects'):
                    raise ValueError(f"CV response missing 'projects' attribute. Response type: {type(structured_cv)}")
                
                if not hasattr(structured_cv, 'education'):
                    raise ValueError(f"CV response missing 'education' attribute. Response type: {type(structured_cv)}")
                
                # Log successful response for debugging
                print("✅ CV extraction successful:")
                print(f"   - Name: {structured_cv.personality.name if structured_cv.personality else 'N/A'}")
                print(f"   - Experiences count: {len(structured_cv.experiences) if structured_cv.experiences else 0}")
                print(f"   - Projects count: {len(structured_cv.projects) if structured_cv.projects else 0}")
                print(f"   - Education count: {len(structured_cv.education) if structured_cv.education else 0}")
                
            except Exception as e:
                print(f"❌ Error in CV extraction: {e}")
                print(f"   - Messages sent to LLM: {messages}")
                print(f"   - Model type: {type(self.MODEL)}")
                if hasattr(self.MODEL, 'model_name'):
                    print(f"   - Model name: {self.MODEL.model_name}")
                raise e

            with open(self.structured_cv_path, 'wb') as f:
                pickle.dump(structured_cv, f)

        else:
            with open(self.structured_cv_path, 'rb') as file:
                structured_cv = pickle.load(file)

        self.structured_cv = structured_cv

        return structured_cv

    def create_new_cover_letter(self, structured_curriculum: str, job_description: str):
        
        # Validate model before proceeding
        self.validate_model()

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

        try:
            structured_llm = self.MODEL.with_structured_output(
                CoverLetter,
                method="function_calling"
            )

            cover_letter = structured_llm.invoke(messages)
            
            # Validate the response
            if cover_letter is None:
                raise ValueError("LLM returned None response for cover letter")
            
            if not hasattr(cover_letter, 'salutation'):
                raise ValueError(f"Cover letter response missing 'salutation' attribute. Response type: {type(cover_letter)}")
            
            if not hasattr(cover_letter, 'body_paragraphs'):
                raise ValueError(f"Cover letter response missing 'body_paragraphs' attribute. Response type: {type(cover_letter)}")
            
            if not hasattr(cover_letter, 'closing'):
                raise ValueError(f"Cover letter response missing 'closing' attribute. Response type: {type(cover_letter)}")
            
            # Log successful response for debugging
            print("✅ Cover letter generation successful:")
            print(f"   - Salutation: {cover_letter.salutation}")
            print(f"   - Body paragraphs count: {len(cover_letter.body_paragraphs) if cover_letter.body_paragraphs else 0}")
            print(f"   - Closing: {cover_letter.closing}")
            
            self.cover_letter = cover_letter

        except Exception as e:
            print(f"❌ Error in create_new_cover_letter: {e}")
            print(f"   - Messages sent to LLM: {messages}")
            print(f"   - Model type: {type(self.MODEL)}")
            if hasattr(self.MODEL, 'model_name'):
                print(f"   - Model name: {self.MODEL.model_name}")
            raise e

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
        
        # Validate model before proceeding
        self.validate_model()

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

        try:
            structured_llm = self.MODEL.with_structured_output(
                NewCurriculum,
                method="function_calling"
            )

            new_structured_cv = structured_llm.invoke(messages)
            
            # Validate the response
            if new_structured_cv is None:
                raise ValueError("LLM returned None response")
            
            if not hasattr(new_structured_cv, 'summary'):
                raise ValueError(f"LLM response missing 'summary' attribute. Response type: {type(new_structured_cv)}")
            
            if not hasattr(new_structured_cv, 'experiences'):
                raise ValueError(f"LLM response missing 'experiences' attribute. Response type: {type(new_structured_cv)}")
            
            if not hasattr(new_structured_cv, 'projects'):
                raise ValueError(f"LLM response missing 'projects' attribute. Response type: {type(new_structured_cv)}")
            
            # Log successful response for debugging
            print("✅ LLM response validated successfully:")
            print(f"   - Summary length: {len(new_structured_cv.summary) if new_structured_cv.summary else 0}")
            print(f"   - Experiences count: {len(new_structured_cv.experiences) if new_structured_cv.experiences else 0}")
            print(f"   - Projects count: {len(new_structured_cv.projects) if new_structured_cv.projects else 0}")
            
            self.new_cv = new_structured_cv

        except Exception as e:
            print(f"❌ Error in create_new_cv: {e}")
            print(f"   - Messages sent to LLM: {messages}")
            print(f"   - Model type: {type(self.MODEL)}")
            if hasattr(self.MODEL, 'model_name'):
                print(f"   - Model name: {self.MODEL.model_name}")
            raise e

        # Continue with JD extraction
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

        try:
            structured_llm = self.MODEL.with_structured_output(
                JobDescriptionInformation,
                method="function_calling"
            )

            jd_information = structured_llm.invoke(messages)
            
            # Validate JD response
            if jd_information is None:
                raise ValueError("LLM returned None response for JD extraction")
            
            if not hasattr(jd_information, 'company_name'):
                raise ValueError(f"JD response missing 'company_name' attribute. Response type: {type(jd_information)}")
            
            if not hasattr(jd_information, 'job_title'):
                raise ValueError(f"JD response missing 'job_title' attribute. Response type: {type(jd_information)}")
            
            print("✅ JD extraction successful:")
            print(f"   - Company: {jd_information.company_name}")
            print(f"   - Job Title: {jd_information.job_title}")
            
            self.jd_information = jd_information

        except Exception as e:
            print(f"❌ Error in JD extraction: {e}")
            print(f"   - Messages sent to LLM: {messages}")
            raise e

        with open(self.new_cv_path, 'wb') as f:
            pickle.dump(new_structured_cv, f)

        with open(self.jd_information_path, 'wb') as f:
            pickle.dump(jd_information, f)

        return new_structured_cv

    def update_jd_from_cover_letter(self, cover_letter):
        """
        Update job description information from cover letter data.
        This ensures consistency when users modify cover letter information.
        """
        if not self.jd_information:
            from support.supportClasses import JobDescriptionInformation
            self.jd_information = JobDescriptionInformation()
        
        # Update with cover letter data
        self.jd_information.job_title = cover_letter.position_title
        self.jd_information.company_name = cover_letter.company_name
        
        # Save updated information
        try:
            with open(self.jd_information_path, 'wb') as f:
                pickle.dump(self.jd_information, f)
            
            print("✅ Job description information updated from cover letter:")
            print(f"   - Job Title: {self.jd_information.job_title}")
            print(f"   - Company: {self.jd_information.company_name}")
            
            return True
        except Exception as e:
            print(f"❌ Error saving updated jd_information: {e}")
            return False

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
        # Validate job description information before saving to database
        if not self.jd_information:
            raise ValueError("Job description information is missing. Please ensure job description was processed.")
        
        if not self.jd_information.company_name:
            raise ValueError("Company name is missing from job description. Please check the job description input.")
        
        if not self.jd_information.job_title:
            raise ValueError("Job title is missing from job description. Please check the job description input.")
        
        # Validate that we have the required objects
        if not self.final_cv:
            raise ValueError("Final CV is missing. Please generate the CV first.")
        
        if not self.final_cover_letter:
            raise ValueError("Final cover letter is missing. Please generate the cover letter first.")
        
        print("✅ Validating job information before saving:")
        print(f"   - Company: {self.jd_information.company_name}")
        print(f"   - Position: {self.jd_information.job_title}")
        
        # Save structured objects to database instead of generating PDF files
        from support.submission_manager import save_submission
        
        save_submission(
            self.jd_information.company_name,
            self.jd_information.job_title,
            self.final_cv,
            self.final_cover_letter,
            self.jd_information
        )
        
        print("✅ Submission saved to database successfully!")
        print("   - CV object saved")
        print("   - Cover letter object saved")
        print("   - Job description information saved")
