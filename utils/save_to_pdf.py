import os
import markdown2
from xhtml2pdf import pisa
from datetime import datetime

# --------------------------------
# Save AI Analysis to PDF
# --------------------------------
# Converts markdown text to PDF using pure-Python libraries and saves to /output
# Returns: saved file path or error message

def save_analysis_to_pdf(markdown_text: str, output_dir="output") -> str:
    try:
        # Ensure output folder exists
        os.makedirs(output_dir, exist_ok=True)

        # Convert Markdown → HTML
        html = markdown2.markdown(markdown_text)

        # Define filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.pdf"
        file_path = os.path.join(output_dir, filename)

        # Convert HTML → PDF
        with open(file_path, "w+b") as f:
            pisa_status = pisa.CreatePDF(html, dest=f)

        if pisa_status.err:
            return "❌ Error while generating PDF."
        return file_path

    except Exception as e:
        return f"❌ Failed to save analysis: {e}"