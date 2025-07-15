import streamlit as st
import tempfile
import json
from agents.iso_agent import analyze_iso_from_pdf

st.title("📄 ISO Document Analyzer (with OCR + Gemini + Serper)")

uploaded_file = st.file_uploader("Upload your ISO certificate PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with st.spinner("🔍 Analyzing document..."):
        result = analyze_iso_from_pdf(tmp_path)

    if "result" in result:
        st.warning(result["result"]["status"])
    else:
        st.success("✅ ISO codes and versioning info extracted.")
        for code, data in result.items():
            st.markdown(f"### 🔎 `{code}`")
            st.json(data)

        st.download_button("📥 Download JSON", json.dumps(result, indent=2), file_name="iso_analysis.json")
