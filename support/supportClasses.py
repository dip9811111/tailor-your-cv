from pydantic import BaseModel, Field
from typing import List, Optional


class Experience(BaseModel):
    title: Optional[str] = Field(
        description="Title or position held in a past experience listed in the original CV."
    )
    company: Optional[str] = Field(
        description="Name of the company or organization listed in the original CV."
    )
    description: Optional[str] = Field(
        description="Brief explanation or bullet points describing the responsibilities and achievements in this experience."
    )
    start_date: Optional[str] = Field(
        description="Starting date (or year) of this experience."
    )
    end_date: Optional[str] = Field(
        description="End_date date (or year) of this experience."
    )


class EducationExperience(BaseModel):
    title: Optional[str] = Field(
        description="Title of the education experience listed in the original CV."
    )
    school_name: Optional[str] = Field(
        description="Name of the school or university listed in the original CV."
    )
    description: Optional[str] = Field(
        description="Brief explanation or bullet points describing the responsibilities and achievements in this experience, including grade and learnt skills."
    )
    start_date: Optional[str] = Field(
        description="Starting date (or year) of this experience."
    )
    end_date: Optional[str] = Field(
        description="End_date date (or year) of this experience."
    )


class NewExperience(BaseModel):
    title: Optional[str] = Field(
        description="Title or position for a proposed experience tailored to match job requirements."
    )
    company: Optional[str] = Field(
        description="Name of the company or organization listed in the original CV."
    )
    description: Optional[str] = Field(
        description="Generated description for this tailored experience, optimized to reflect alignment with the job description."
    )
    reasoning: Optional[str] = Field(
        description="Justification for including this experience in the revised CV based on relevance to the target job."
    )
    start_date: Optional[str] = Field(
        description="Starting date (or year) of this experience."
    )
    end_date: Optional[str] = Field(
        description="End_date date (or year) of this experience."
    )


class Personality(BaseModel):
    name: Optional[str] = Field(
        description="First name of the CV holder."
    )
    surname: Optional[str] = Field(
        description="Last name (surname) of the CV holder."
    )
    e_mail: Optional[str] = Field(
        description="e-mail to contact the CV holder."
    )
    telephone: Optional[str] = Field(
        description="Phone number to contact the CV holder."
    )
    linkedin_link: Optional[str] = Field(
        description="URL to the CV holder's LinkedIn profile."
    )
    address: Optional[str] = Field(
        description="Physical or mailing address of the CV holder."
    )


class Curriculum(BaseModel):
    personality: Optional[Personality] = Field(
        default=None,
        description="Personal and contact information from the original CV."
    )
    experiences: Optional[List[Experience]] = Field(
        default=None,
        description="List of professional or educational experiences extracted from the original CV."
    )
    projects: Optional[List[Experience]] = Field(
        default=None,
        description="List of projects extracted from the original CV."
    )
    hard_skills: Optional[List[str]] = Field(
        default=None,
        description="Explicit technical skills (e.g., programming, data analysis) listed in the CV."
    )
    soft_skills: Optional[List[str]] = Field(
        default=None,
        description="Interpersonal or non-technical skills (e.g., teamwork, communication) from the CV."
    )
    education: Optional[List[EducationExperience]] = Field(
        default=None,
        description="Educational information (e.g. schools, university) from the CV."
    )
    summary: Optional[str] = Field(
        default=None,
        description="Key summary statements or objective section originally included in the CV."
    )


class NewCurriculum(BaseModel):
    experiences: Optional[List[NewExperience]] = Field(
        default=None,
        description="Newly generated work-experiences curated to best align with the job requirements. Each includes reasoning for selection."
    )
    projects: Optional[List[NewExperience]] = Field(
        default=None,
        description="Newly generated projects curated to best align with the job requirements. Each includes reasoning for selection."
    )
    summary: Optional[str] = Field(
        default=None,
        description="Generated summary statements designed to closely match the target job's qualifications and tone."
    )


class FinalCurriculum:
    def __init__(self, personality, summary, experiences, projects, education, hard_skills, soft_skills):
        self.personality = personality
        self.experiences = experiences
        self.projects = projects
        self.summary = summary
        self.education = education
        self.soft_skills = soft_skills
        self.hard_skills = hard_skills
