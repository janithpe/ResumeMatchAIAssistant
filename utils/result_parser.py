import re

# --------------------------------
# Gemini Markdown Result Parser
# --------------------------------
# Parses structured markdown text from Gemini API to extract key sections.
# Returns:
#   - 'score': Compatibility score out of 100,
#   - 'summary': Summary paragraph about resume fit,
#   - 'top_requirements': Bullet list of job requirements,
#   - 'suggestions': Bullet list of resume improvement tips in a dictionary format.

def parse_analysis_markdown(markdown_text: str) -> dict:
    # Extract score using flexible pattern matching
    score_match = re.search(r"[**]*Score:\s*(\d+)[/]\d+[**]*", markdown_text)
    score = int(score_match.group(1)) if score_match else None

    # Define headings pattern (using markdown-style or plain)
    pattern = re.compile(
        r"\*\*?(Match Summary|Top Requirements|Suggestions):\*\*?", re.IGNORECASE
    )

    # Find all matches for headers
    matches = list(pattern.finditer(markdown_text))
    sections = {}

    for i, match in enumerate(matches):
        section_name = match.group(1).lower()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown_text)
        section_text = markdown_text[start:end].strip()
        sections[section_name] = section_text

    return {
        "score": score,
        "summary": sections.get("match summary", ""),
        "top_requirements": sections.get("top requirements", ""),
        "suggestions": sections.get("suggestions", "")
    }