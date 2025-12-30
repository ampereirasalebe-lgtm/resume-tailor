import os
from pypdf import PdfReader

def extract_resume_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_resumes_from_folder(folder_path="resumes"):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Resume folder '{folder_path}' does not exist")

    pdf_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise FileNotFoundError("No PDF resumes found in resumes/ folder")

    merged_text = ""

    for pdf in pdf_files:
        merged_text += "\n\n--- Resume Source ---\n\n"
        reader = PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                merged_text += page_text + "\n"

    return merged_text.strip()