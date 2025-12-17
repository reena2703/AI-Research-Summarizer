import fitz  # PyMuPDF
import os

PAPERS_DIR = "app/papers"
TEXT_DIR = "app/papers/text"


def ensure_text_folder():
    """
    Create text folder (app/papers/text) if it does not exist.
    """
    if not os.path.exists(TEXT_DIR):
        os.makedirs(TEXT_DIR)
        print(f"Created folder: {TEXT_DIR}")


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF using PyMuPDF.
    Returns extracted text as a single large string.
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page_num, page in enumerate(doc, start=1):
            try:
                text = page.get_text("text")
            except Exception:
                text = ""

            full_text += f"\n\n--- Page {page_num} ---\n{text}"

        doc.close()
        return full_text

    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return ""


def extract_all_papers():
    """
    Extract text from ALL PDFs stored in app/papers/
    Save them as .txt files inside app/papers/text/
    Returns a list of the created .txt file paths.
    """
    ensure_text_folder()
    extracted_files = []

    if not os.path.exists(PAPERS_DIR):
        print(f"❌ Papers folder does not exist: {PAPERS_DIR}")
        return extracted_files

    pdf_files = [f for f in os.listdir(PAPERS_DIR) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("❌ No PDFs found in app/papers/")
        return extracted_files

    for filename in pdf_files:
        pdf_path = os.path.join(PAPERS_DIR, filename)
        print(f"📄 Extracting text from: {pdf_path}")

        text = extract_text_from_pdf(pdf_path)

        if text.strip():
            txt_filename = filename.replace(".pdf", ".txt")
            txt_path = os.path.join(TEXT_DIR, txt_filename)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"✅ Saved extracted text → {txt_path}")
            extracted_files.append(txt_path)
        else:
            print(f"⚠ Extraction failed or PDF contained no readable text: {filename}")

    return extracted_files
