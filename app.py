import streamlit as st
from utils.file_parser import parse_resume, parse_job_desc
from utils.gemini_analysis import get_resume_match_analysis
from utils.result_parser import parse_analysis_markdown

st.set_page_config(page_title="Resume Match AI Assistant", layout="centered")
st.title("Resume & Job Match Assistant")

st.markdown("""
Upload your **Resume** and **Job Description**, and this AI tool will:
- 🔍 Analyze both documents
- 📊 Give a match score
- 💡 Suggest targeted resume improvements
""")

# File Uploads
resume_file = st.file_uploader("📎 Upload Your Resume", type=["pdf", "docx", "txt"])

job_file = st.file_uploader("📋 Upload Job Description (optional)", type=["pdf", "docx", "txt"])
job_text_input = st.text_area("Or paste the job description below:", height=200)


# Main Trigger Button
if resume_file and (job_file or job_text_input.strip()):
    if st.button("🔍 Analyze Now"):
        with st.spinner("Extracting and analyzing..."):
            resume_text = parse_resume(resume_file)

            # Prioritize uploaded file over pasted text
            if job_file:
                job_text = parse_job_desc(job_file)
            else:
                job_text = job_text_input.strip()
            
            raw_analysis_markdown = get_resume_match_analysis(resume_text, job_text)
            
            analyze_dict = parse_analysis_markdown(raw_analysis_markdown)

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

        # Full analysis result
        with st.expander("📎 Full Raw AI Analysis"):
            st.markdown(raw_analysis_markdown)

else:
    st.info("⬆️ Please upload a resume and either upload or paste the job description.")