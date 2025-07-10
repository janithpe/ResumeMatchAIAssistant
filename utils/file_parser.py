import docx
import pymupdf
from io import BytesIO

# --------------------------------
# Core Text Extraction Function
# --------------------------------
# Extracts text from supported file types: PDF, DOCX, or TXT.
# Returns the text content as a string. Handles decoding and parsing.

def extract_text(uploaded_file) -> str:
    try:
        file_name = uploaded_file.name.lower()

        # Read PDF using PyMuPDF
        if file_name.endswith(".pdf"):
            pdf_stream = BytesIO(uploaded_file.read())
            doc = pymupdf.open(stream=pdf_stream, filetype="pdf")
            return "\n".join([page.get_text() for page in doc])
        
        # Read DOCX using python-docx
        elif file_name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
        
        # Decode plain text
        elif file_name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")
        
        else:
            return "ERROR: Unsupported file format."
    
    except Exception as e:
        return f"ERROR: Unable to read file: {e}"


# --------------------------------
# Resume File Parser
# --------------------------------
# Extracts and returns resume content from the uploaded file.

def parse_resume(uploaded_file) -> str:
    return extract_text(uploaded_file)


# --------------------------------
# Job Description File Parser
# --------------------------------
# Extracts and returns job description text from the uploaded file.

def parse_job_desc(uploaded_file) -> str:
    return extract_text(uploaded_file)