import fitz  # PyMuPDF
import pandas as pd
import os


# -------- PDF PROCESSING --------
def extract_pdf_text(file_path):
    text = ""

    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    return text


# -------- CSV PROCESSING --------
def extract_csv_text(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()


# -------- MAIN ROUTER --------
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1]

    if ext == ".pdf":
        return extract_pdf_text(file_path)

    elif ext == ".csv":
        return extract_csv_text(file_path)

    else:
        return "Unsupported file type"


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
