import re

def extract_iso_codes(text):
    pattern = r"(ISO\s*\d{4,5}\s*:?[-]?\s*\d{4})"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return list(set(match.strip().replace(" ", "") for match in matches))
