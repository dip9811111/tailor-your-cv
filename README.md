

https://github.com/user-attachments/assets/e023e563-8e6b-4cd4-8958-7df612605c4a

# 🎯 tailor-your-CV: AI-Powered Job-Tailored Resume Generator

tailor-your-CV is a powerful tool that helps users craft customized, high-impact resumes based on job descriptions using OpenAI GPT-4.1. Simply upload your professional experience, paste a job description, and let the LLM generate a tailored curriculum vitae aligned with your target role — all based on your chosen template.

## 🚀 Features

- 📁 **Experience Upload**: Upload a file containing:
  - Work experience
  - Additional personal or freelance projects
  - Hard & soft skills
  - Academic achievements
  - Personal information (mail, phone, linkedin profile, etc)

  > ✅ *Tip: A simple file format (like a plain `.txt` file) with all the details is preferred—avoid complex or heavily structured formats.*



- 🖋️ **Markdown Conversion**: Uses `MarkItDown` to convert your uploaded file to clean markdown, which is then injected into the LLM for optimized processing.

- 🧠 **AI-Powered Tailoring**: Paste a job description and automatically generate a resume tailored to match it, using GPT-4.1's advanced understanding of language and relevance.

- 🎨 **Template-Based Output**: Resumes are created using an html template that is then converted to PDF.


## 🧩 How It Works

1. **Document Ingestion**: The user's resume or experience file is processed and converted into clean Markdown — a structured, LLM-friendly format. Once completed, two files are generated: `structured_cv.pkl` (a serialized structured representation) and `user_curriculum.md` (the Markdown version). These are cached for future use, so this step can be skipped on subsequent runs unless the input document changes.

2. **Structured CV Generation**: Leveraging the structured output capabilities of modern LLMs, the system transforms the Markdown content into a standardized format, referred to as the *structured CV*. This ensures consistency and clarity in how experiences, skills, and achievements are represented.

3. **AI-Powered Tailoring — With Boundaries**: The *structured CV* and the job description are provided to the LLM. Using controlled prompts and structured output constraints, the model enhances and prioritizes relevant experiences that align with the job requirements — without hallucinating or inventing content. The focus is on intelligent rephrasing and emphasis, not fabrication.

4. **HTML & PDF Generation**: The tailored content is dynamically injected into an HTML template, which is then rendered and exported as a polished, ready-to-send PDF resume.


## 🪜 Steps to Use

1. **Install requirements**
2. **Run** `streamlit run app.py`
3. **Set up your OpenAI API key** (copy-paste it into the app, or create a `config.ini` file with an `[OPENAI]` section and `API_KEY` variable).
4. **Upload your base resume** (supported formats: `.pdf`, `.txt`, `.docx`, `.md`).
5. **Paste the target job description** into the provided input field.
6. **Generate your tailored resume** — the output is a professional PDF, optimized for the job and ready to send.

## 🛠️ Tech Stack

- **GPT-4.1** via OpenAI API – for content generation and tailoring
- **MarkItDown** – to convert user files to structured Markdown
- **Streamlit** for the UI

