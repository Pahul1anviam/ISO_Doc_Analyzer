import streamlit as st
from tools.pdf_loader_tool import load_pdf_text
from tools.iso_extractor_tool import extract_iso_codes
from tools.serper_search_tool import search_iso_update
from utils.config import GOOGLE_API_KEY
import google.generativeai as genai
import json, re
import tempfile

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")  # Or "gemini-2.5-flash"

st.title("📄 ISO Document Analyzer (Gemini + Serper)")

uploaded_file = st.file_uploader("Upload your ISO certificate PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with st.spinner("🔍 Extracting text..."):
        text = load_pdf_text(tmp_path)
        iso_codes = extract_iso_codes(text)

    st.success(f"✅ Found ISO Standards: {', '.join(iso_codes) if iso_codes else 'None'}")

    if iso_codes:
        results = {}
        for code in iso_codes:
            st.markdown(f"### 🔎 Checking: `{code}`")

            search_result = search_iso_update(code)

            prompt = f"""
            ISO Standard: {code}
            Search Results:
            {search_result}

            Provide structured analysis:
            {{
              "status": "...",
              "latest_version": "...",
              "amendment": "..."
            }}
            """
            response = model.generate_content(prompt)
            cleaned = re.sub(r"```json|```", "", response.text).strip()

            try:
                structured = json.loads(cleaned)
            except json.JSONDecodeError:
                structured = {"raw_response": response.text}

            results[code] = structured
            st.json(structured)

        # Allow download
        st.download_button("📥 Download Result as JSON", json.dumps(results, indent=2), file_name="iso_analysis.json", mime="application/json")
