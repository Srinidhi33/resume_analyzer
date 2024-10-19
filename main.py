import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from PyPDF2 import PdfReader
from io import BytesIO
import docx2txt
import re


app = FastAPI()

#add a set of predifined keywords for different job titles
job_keywords_df = pd.read_csv("job_keywords.csv")


@app.get("/")
async def read_root():
    """Basic endpoint to check if the API is running."""
    return {"message": "Resume Analyzer API is running."}

#create a api endpoint to upload a resume and analyze it
@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), job_title: str = Form(...)):
    try:
        # create a BytesIO buffer for the uploaded file
        contents = await file.read()
        file.seek(0) 

        # extract text from the resume based on the file type - PDF or DOCX
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(BytesIO(contents))
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="File format not supported.")
        
        # Call neccessary functions to match keywords and provide feedback
        missing_keywords, matched_keywords, match_score = match_keywords(text, job_title)
        feed=feedback(job_title, missing_keywords)
        return {
            "filename": file.filename,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "match_score": match_score * 100, # conevert to % for display
            "feedback": feed
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# extract text if its a pdf
def extract_text_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

#function to extract text from a docx file
#use doct2txt lib rather than python-docx for better results
def extract_text_from_docx(file_stream):
    text = docx2txt.process(file_stream)
    return text


# func to check matching keywords
def match_keywords(text, job_title):
    # Clean the text: extract words and lower the case
    words = re.findall(r'\b\w+\b', text.lower())
    words = [word.lower() for word in words if word.isalnum()]

    # Normalize the job title to lower case for case-insensitive matching
    job_title_lower = job_title.lower().strip()

    # extract the CSV data for the specific job title
    keywords_df = job_keywords_df[job_keywords_df['Job Title'].str.lower().str.strip() == job_title_lower]

    # Check if we have any keywords for the job title
    if keywords_df.empty:
        raise HTTPException(status_code=404, detail=f"No keywords found for job title: {job_title}")

    #get keywords from the data frame and lower the case
    keywords = keywords_df['Keyword'].str.lower().tolist()

    
    matched_keywords = set(word.capitalize() for word in words if word in keywords)
    match_score = len(matched_keywords) / len(keywords) if keywords else 0

    # check for missed words that can help in feedback func
    missing_keywords = [word.capitalize() for word in keywords if word not in words]

    return missing_keywords, list(matched_keywords), match_score

#func that can get feedback from the AI
#use Rapid-api to hit the OG GPT-4 model API 
#besides its free :)
def feedback(job_title, missing_keywords):
    import requests

    url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"
    prompt = f"I am analyzing a resume for a {job_title} position. The resume is missing the following key skills: {', '.join(missing_keywords)}. Can you suggest how the candidate can improve their resume?"

    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "system_prompt": "You are a friend who analyzes resumes and provides some one-line suggestion where I can learn about the missing skills .",
        "temperature": 0.6,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "web_access": False
    }

    headers = {
        "x-rapidapi-key": "caea6e5b6cmsh034a11dca5febdap10775djsn4d16e8e92558",
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    # format the response from json to a string
    result = response_data.get('result', '')
    return result



