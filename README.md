

https://github.com/user-attachments/assets/e1bcc8dc-0d8c-46b5-aca1-9963898d2bdc

# 🎯 tailor-your-CV: AI-Powered Job-Tailored Resume Generator

tailor-your-CV is a powerful tool that helps users craft customized, high-impact resumes and cover letter based on job descriptions using
LLMs. Simply upload your professional experience, paste a job description,
and let the LLM generate a tailored curriculum vitae aligned with your target role — all based on your chosen template.

## ✨ Features

- **AI-Powered CV Processing**: Upload your existing CV and let AI extract and structure your information
- **Portfolio Management**: Maintain a persistent portfolio of your experiences, skills, and education
- **Tailored Applications**: Generate job-specific CVs and cover letters based on job descriptions
- **Multiple AI Models**: Support for both OpenAI GPT-4 and Google Gemini models
- **Professional Templates**: Multiple CV and cover letter templates to choose from
- **PDF Generation**: Download your documents as professional PDFs
- **Application Tracking**: Keep track of all your job applications

## 🏗️ Architecture

The application is built with a modular, multi-page structure:

### Core Pages

1. **🏠 Home** (`home.py`) - Dashboard and navigation hub
2. **⚙️ Manage Settings** (`pages/manage_settings.py`) - API key configuration and model selection
3. **📁 Portfolio** (`pages/portfolio.py`) - CV upload, processing, and editing
4. **📝 New Submission** (`pages/new_submission.py`) - Job-specific CV and cover letter generation
5. **📬 My Submissions** (`pages/my_submissions.py`) - Application history and downloads

### Support Modules

- **`support/extractor.py`** - AI-powered data extraction and document generation
- **`support/html_builder.py`** - HTML generation and editing interfaces
- **`support/supportClasses.py`** - Data models and structures
- **`support/html_templates/`** - CV and cover letter templates
- **`support/submission_manager.py`** - Database operations for submissions

## 🚀 Workflow

### 1. Setup & Configuration
- Navigate to "Manage Settings"
- Configure your OpenAI or Gemini API key
- Select your preferred AI model

### 2. Portfolio Creation
- Go to "Portfolio" page
- Upload your existing CV (PDF, TXT, DOCX, MD)
- AI will extract and structure your information
- Edit and refine your experiences, skills, and education
- Save your portfolio for future use

### 3. Job Application
- Navigate to "New Submission"
- Paste the job description
- AI generates tailored CV and cover letter
- Edit both documents to your preference
- Download PDFs or save to database

### 4. Track Applications
- View all submissions in "My Submissions"
- Download previous applications
- Monitor your job search progress

## 🔧 Technical Requirements

- Python 3.8+
- Streamlit
- Required packages: see `requirements.txt`

## 📁 File Structure

```
tailor-cv/
├── home.py                          # Main dashboard
├── pages/
│   ├── manage_settings.py           # API configuration
│   ├── portfolio.py                 # Portfolio management
│   ├── new_submission.py            # Job application creation
│   └── my_submissions.py            # Application history
├── support/
│   ├── extractor.py                 # AI processing engine
│   ├── html_builder.py              # Document generation
│   ├── supportClasses.py            # Data models
│   ├── html_templates/              # Document templates
│   └── submission_manager.py        # Database operations
└── requirements.txt                  # Dependencies
```

## 🔑 API Keys

The application supports two AI models:

- **OpenAI GPT-4**: Requires OpenAI API key
- **Google Gemini**: Requires Google API key

Create a `config.ini` file with an `[OPENAI]` or `[GEMINI]` section and `API_KEY` variable, or copy-paste them in the "Manage Settings" page.

## 🚀 Running the Application

```bash
streamlit run home.py
```

## 🤝 Contributing

Feel free to contribute to improve the application! Areas for enhancement:

- Additional CV and cover letter templates
- More AI model integrations
- Enhanced editing capabilities
- Better mobile responsiveness
- Additional export formats

## 📄 License

This project is open source and available under the MIT License.
