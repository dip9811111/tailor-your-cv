# 🚀 AI CV Builder

Your smart assistant for creating, editing, and customizing professional CVs and cover letters using AI.

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

## 🚀 Getting Started

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

## 🎯 Workflow

1. **Setup** → Configure API keys and model preferences
2. **Portfolio** → Upload and process your CV, create persistent portfolio
3. **Application** → Generate tailored documents for specific jobs
4. **Review** → Edit and refine generated documents
5. **Export** → Download PDFs or save to database
6. **Track** → Monitor application history and progress

## 🔑 API Keys

The application supports two AI models:

- **OpenAI GPT-4**: Requires OpenAI API key
- **Google Gemini**: Requires Google API key

Configure your preferred model in the "Manage Settings" page.

## 📝 Supported File Formats

- **Input**: PDF, TXT, DOCX, MD
- **Output**: HTML preview, PDF download

## 🎨 Templates

- **CV Templates**: Modern, Classic, Minimalist
- **Cover Letter Templates**: Professional, Modern, Classic

## 🚀 Running the Application

```bash
streamlit run home.py
```

## 📊 Features

- **Persistent Portfolio**: Your CV data is saved and can be reused
- **AI Tailoring**: Documents are automatically customized for specific job requirements
- **Real-time Editing**: Edit both CV and cover letter with live preview
- **Professional Output**: Generate high-quality PDFs for job applications
- **Application Tracking**: Keep organized records of all submissions

## 🤝 Contributing

Feel free to contribute to improve the application! Areas for enhancement:

- Additional CV and cover letter templates
- More AI model integrations
- Enhanced editing capabilities
- Better mobile responsiveness
- Additional export formats

## 📄 License

This project is open source and available under the MIT License.
