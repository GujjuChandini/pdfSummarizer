import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error opening or reading PDF file '{pdf_path}': {e}")
        return None # Or raise the exception if you want to stop execution
    return text