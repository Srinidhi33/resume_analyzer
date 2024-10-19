📄 AI-Powered Resume Analyzer
# AI-Powered Resume Analyzer

Welcome to the AI-Powered Resume Analyzer! This project helps users analyze their resumes by matching their qualifications, skills, and experience to the requirements of specific job titles. By leveraging FastAPI for the backend and Streamlit for the frontend, this tool provides detailed feedback on how well a resume fits a job, including a match score and AI-generated suggestions to improve the resume.

## 🛠️ Key Features

- **Job Title Input**: Enter any job title (e.g., "Data Analyst," "Software Engineer") to customize the analysis.
- **Resume File Upload**: Supports resume uploads in both PDF and DOCX formats.
- **Keyword Matching**: Matches resume content with job-related keywords.
- **Match Score**: Provides a percentage score of how well the resume fits the job.
- **AI-Generated Feedback**: Generates personalized suggestions to improve the resume based on identified gaps.
- **User-Friendly UI**: Streamlit provides an easy-to-use interface with clear and concise results.

## 🚀 How It Works

1. **Upload Your Resume**: Upload your resume in PDF or DOCX format.
2. **Enter a Job Title**: Specify the job you're targeting.
3. **Analyze**: The tool will analyze your resume and job title against predefined job-related keywords (from a CSV file) and return:
    - Matched Keywords
    - Missing Keywords
    - Match Score (displayed via a progress bar)
    - Concise AI Feedback for improving your resume.
4. **Feedback**: Use the AI's suggestions to enhance your resume and increase your chances of landing your dream job!

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI**: OpenAI GPT-based feedback generation (or similar API-based model)

## 📦 File Structure

- `app.py`: Contains the Streamlit frontend and logic to interact with the FastAPI backend.
- `main.py`: FastAPI backend for handling file uploads, processing resumes, and providing the analysis.
- `job_keywords.csv`: CSV file containing job-specific keywords that are used to match the resume content.

## 🔧 Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/resume-analyzer.git
    cd resume-analyzer
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Backend (FastAPI)**:
    ```bash
    uvicorn main:app --reload
    ```

4. **Run the Frontend (Streamlit)**:
    ```bash
    streamlit run app.py
    ```

5. **Access the App**: Open your browser and go to `http://localhost:8501` to access the Streamlit frontend.

## 💡 Usage Tips

- Make sure your resume is in PDF or DOCX format.
- The job title you input should closely match the position you're applying for.
- Pay attention to the AI-generated feedback—it provides key improvements based on real gaps in your resume.

## 🤖 AI-Generated Feedback

The resume analyzer uses advanced AI models to generate actionable, concise feedback on how to improve your resume. It looks at missing qualifications, experience, and skills based on the provided job title and suggests improvements that can help you stand out to recruiters.

## 📊 Example Output

- **Matched Keywords**: Python, Data Analysis, SQL
- **Missing Keywords**: Machine Learning, Data Visualization
- **Match Score**: 75%
- **AI Feedback**: "To improve your resume, consider adding experience with Machine Learning techniques, as it is highly relevant to Data Analyst roles."

## ❤️ Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you have suggestions to improve this tool.