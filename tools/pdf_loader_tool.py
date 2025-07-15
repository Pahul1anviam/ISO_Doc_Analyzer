from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf_text(file_path: str) -> str:
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    return " ".join([doc.page_content for doc in documents])

