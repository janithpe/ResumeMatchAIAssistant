import streamlit as st
from google import genai

# Initializes the Gemini API client using the secret API key.
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --------------------------------
# Prompt Builder for Resume Match
# --------------------------------
# Constructs a structured prompt for Gemini API to analyze resume-job compatibility.
# Args:
#   - resume_text: Extracted text from resume file.
#   - job_text: Extracted text or input from job description.
# Returns:
#   - Formatted prompt for the Gemini model.

def build_analysis_prompt(resume_text: str, job_text: str) -> str:
    return """
You are a career advisor AI.

Analyze the following job description and resume to help a job seeker tailor their resume better.

Job Description:
\"\"\"{job_text}\"\"\"

Resume:
\"\"\"{resume_text}\"\"\"

Your tasks:
1. Extract the top 10 job requirements from the job description.
2. Evaluate how well the resume matches these requirements.
3. Give a compatibility score out of 100.
4. Provide a short summary (one para) about the compatibility and the resume.
5. Suggest 5 concrete improvements the candidate can make to the resume to better align with the job.

Respond in the markdown format:

**Score: <number>/100**

**Match Summary:**
...

**Top Requirements:**
- requirement 1
- requirement 2
...

**Suggestions:**
- suggestion 1
- suggestion 2
...
""".format(job_text=job_text, resume_text=resume_text)


# --------------------------------
# Main Gemini Analysis Function
# --------------------------------
# Sends prompt with resume and job description to Gemini API and returns response in markdown format.

def get_resume_match_analysis(resume_text: str, job_text: str) -> str:
    try:
        prompt = build_analysis_prompt(resume_text, job_text)

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt
        )

        return response.text
    
    except Exception as e:
        return f"ERROR: Failed to get response from Gemini API - {e}"