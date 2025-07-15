# ISO Document Analyzer

This project is a document analysis tool designed to automatically extract ISO standard references from uploaded PDF documents, identify their version and amendment details, and structure the output in a readable format. It uses OCR (Optical Character Recognition) as a fallback if the PDF contains scanned images instead of actual text.

# Features

- Upload PDF documents (ISO certificates, compliance reports, etc.)
- Automatically extract ISO standards (e.g., ISO 9001:2015, ISO 45001:2018)
- Uses OCR if the PDF contains no readable text
- Identifies latest version and amendment of each ISO standard
- Powered by:
  - LangChain Agent
  - Google Gemini API
  - Serper API (for web-based ISO info)

# Directory Structure

ISO_Doc_Analyzer/
│
├── agents/
│   └── iso_agent.py
│
├── tools/
│   ├── pdf_loader_tool.py
│   ├── ocr_pdf_loader.py
│   ├── iso_extractor_tool.py
│   └── serper_search_tool.py
│
├── utils/
│   └── config.py
│
├── outputs/
│   └── output.json
│
├── main.py
├── streamlit_app.py
├── requirements.txt
└── README.md

# Installation

1. Clone the repository

   git clone https://github.com/your-username/ISO_Doc_Analyzer.git
   cd ISO_Doc_Analyzer

2. Create a virtual environment

   python -m venv venv
   venv\Scripts\activate   # On Windows

3. Install dependencies

   pip install -r requirements.txt

4. Install Tesseract OCR

   - Download from: https://github.com/tesseract-ocr/tesseract
   - Set this in your Python code:
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

5. Install Poppler (for pdf2image)

   - Download: https://blog.alivate.com.au/poppler-windows/
   - Extract and set the path like:
     poppler_path = r"C:\poppler\poppler-24.08.0\Library\bin"

6. Create a `.env` file in the root folder and add:

   GOOGLE_API_KEY=your_google_gemini_api_key
   SERPER_API_KEY=your_serper_api_key

# Running the Project

To run the project from CLI:

   python main.py

To launch the Streamlit UI:

   streamlit run streamlit_app.py

# Output

- In CLI mode, the result will be saved to `outputs/output.json`
- In Streamlit mode, results are displayed on screen and can be downloaded as JSON

# Notes

- If the uploaded PDF is image-only, OCR will extract text before processing
- The Gemini model may return quota errors if usage exceeds the free tier
- Serper API is used to fetch amendment/version info from the web
- If no ISO standard is found in the document, a message will be returned


