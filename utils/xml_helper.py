import re

def extract_xml(text: str, tag: str) -> str:
    """Extract content between XML-style tags."""
    pattern = rf"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""