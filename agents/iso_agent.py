import google.generativeai as genai
from tools.pdf_loader_tool import load_pdf_text
from tools.ocr_pdf_loader import load_pdf_text_with_ocr
from tools.iso_extractor_tool import extract_iso_codes
from tools.serper_search_tool import search_iso_update
from utils.config import GOOGLE_API_KEY
from google.api_core.exceptions import ResourceExhausted
import time, json, re

# ✅ Configure Gemini model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")  # Fast & quota-efficient

def analyze_iso_from_pdf(pdf_path: str, use_gemini=True) -> dict:
    # Step 1: Load text from PDF
    text = load_pdf_text(pdf_path)

    # Step 2: Fallback to OCR if no text
    if not text.strip():
        print("⚠️ PDF is empty. Using OCR fallback...")
        text = load_pdf_text_with_ocr(pdf_path)
        print("✅ OCR text (first 300 chars):\n", text[:300])

    # Step 3: Extract ISO codes using regex
    iso_codes = extract_iso_codes(text)
    output_data = {}

    # Step 4: Handle case where no ISO-related content is found
    if not iso_codes:
        output_data["result"] = {
            "status": "No ISO-related content found in the document."
        }
        return output_data

    # Step 5: Loop through detected ISO codes
    for code in iso_codes:
        search_result = search_iso_update(code)

        prompt = f"""
        You are an ISO versioning assistant. Based on the ISO code and the search results below, provide structured information.

        ISO Standard: {code}
        Search Results:
        {search_result}

        Return a clean JSON:
        {{
          "status": "...",
          "latest_version": "...",
          "amendment": "..."
        }}
        """

        # Step 6: Choose model or simulated response
        if not use_gemini:
            structured = {
                "status": "Simulated output (Gemini disabled)",
                "latest_version": code,
                "amendment": "No amendment (test mode)"
            }
        else:
            try:
                response = model.generate_content(prompt)
            except ResourceExhausted:
                print("⚠️ Gemini quota exhausted. Retrying in 60s...")
                time.sleep(60)
                response = model.generate_content(prompt)

            # Step 7: Clean up response
            cleaned = re.sub(r"```json|```", "", response.text).strip()
            try:
                structured = json.loads(cleaned)
            except json.JSONDecodeError:
                structured = {
                    "raw_response": response.text,
                    "status": "Failed to parse JSON"
                }

        output_data[code] = structured

    return output_data
