import time
import streamlit as st
from utils.file_parser import parse_resume, parse_job_desc
from utils.gemini_analysis import get_resume_match_analysis
from utils.result_parser import parse_analysis_markdown
from utils.save_to_pdf import save_analysis_to_pdf

# Resets all session states and increments the reset counter
def reset_app():
    st.session_state.reset_counter += 1
    st.session_state.analysis = None
    st.session_state.last_resume = None
    st.session_state.last_jd = None
    st.session_state.show_clear_message = False

# Streamlit app configuration
st.set_page_config(page_title="Resume Match AI Assistant", layout="centered")
st.title("Resume & Job Match Assistant")

st.markdown("""
Upload your **Resume** and **Job Description**, and this AI tool will:
- 🔍 Analyze both documents
- 📊 Give a match score
- 💡 Suggest targeted resume improvements
""")

# Session state initialization
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "last_resume" not in st.session_state:
    st.session_state.last_resume = None
if "last_jd" not in st.session_state:
    st.session_state.last_jd = None
if "show_clear_message" not in st.session_state:
    st.session_state.show_clear_message = False

# Prepare variables for messages
saved_path = None
error_msg = None

# File uploads
resume_file = st.file_uploader("📎 Upload Your Resume", type=["pdf", "docx", "txt"],
                               key=f"resume_file_{st.session_state.reset_counter}")

job_file = st.file_uploader("📋 Upload Job Description", type=["pdf", "docx", "txt"],
                            key=f"job_file_{st.session_state.reset_counter}")
job_text_input = st.text_area("Or paste the job description below (optional):", height=150,
                              key=f"job_text_{st.session_state.reset_counter}")

# Auto-clear analysis if input changes
def clear_analysis():
    st.session_state.analysis = None
    st.session_state.last_resume = None
    st.session_state.last_jd = None
    st.session_state.show_clear_message = True

if st.session_state.analysis:
    if (
        (resume_file and resume_file != st.session_state.last_resume) or
        (job_file and job_file != st.session_state.last_jd) or
        (job_text_input.strip() and st.session_state.last_jd == "pasted")
    ):
        clear_analysis()

# Show 'Previous result cleared' message
if st.session_state.show_clear_message:
    st.warning("⚠️ Previous result cleared")
    time.sleep(2)
    st.session_state.show_clear_message = False
    st.rerun()

# File name collision check
duplicate_filename = False
user_confirmed_duplicate = False

if resume_file and job_file:
    if resume_file.name == job_file.name:
        duplicate_filename = True
        st.warning(f"⚠️ Both uploaded files are named **{resume_file.name}**. This may indicate you've uploaded the same file twice.")

        user_confirmed_duplicate = st.checkbox("Yes, I confirm these are two different files with the same name.")

# Buttons: Analyze + Save + Reset
if resume_file and (job_file or job_text_input.strip()):
    if not duplicate_filename or user_confirmed_duplicate:
        col1, col2, col3 = st.columns([5, 1, 1])
        # Analyze
        with col1:
            if st.button("🔍 Analyze Now"):
                with st.spinner("Extracting and analyzing..."):
                    resume_text = parse_resume(resume_file)

                    # Prioritize uploaded file over pasted text
                    job_text = parse_job_desc(job_file) if job_file else job_text_input.strip()

                    raw_analysis_markdown = get_resume_match_analysis(resume_text, job_text)

                    analyze_dict = parse_analysis_markdown(raw_analysis_markdown)

                    # Save result to session state
                    st.session_state.analysis = {
                        "raw": raw_analysis_markdown,
                        "parsed": analyze_dict
                    }
                    st.session_state.last_resume = resume_file
                    st.session_state.last_jd = job_file if job_file else "pasted"
        
        # Save
        with col2:
            if st.session_state.analysis:
                if st.button("💾 Save"):
                    result = save_analysis_to_pdf(st.session_state.analysis["raw"])
                    if result.startswith("output"):
                        saved_path = result
                    else:
                        error_msg = result
        
        # Reset
        with col3:
            st.button("🔄 Reset", on_click=reset_app)

# Display save message
if saved_path:
    st.success(f"✅ Saved to `{result}`")
elif error_msg:
    st.error(f"❌ {error_msg}")

# Display results
if st.session_state.analysis:
    analyze_dict = st.session_state.analysis["parsed"]
    raw_analysis_markdown = st.session_state.analysis["raw"]

    st.success("✅ Analysis Complete!")

    # Show match score
    score = analyze_dict['score']
    emoji = "🔥" if score > 90 else "✅" if score > 80 else "⚠️"
    st.subheader(f"{emoji} Resume Match Score")
    st.markdown(f"{score}/100")

    # Show summary
    st.subheader("📋 Match Summary")
    st.markdown(analyze_dict['summary'])

    # Show requirements
    st.subheader("📌 Top Job Requirements")
    st.markdown(analyze_dict['top_requirements'])

    # Show suggestions
    st.subheader("💡 Resume Improvement Suggestions")
    st.markdown(analyze_dict['suggestions'])

# Prompt if no complete user inputs
elif not (resume_file and (job_file or job_text_input)):
    st.info("⬆️ Please upload a resume and either upload or paste the job description.")