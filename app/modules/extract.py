import fitz  # PyMuPDF
import os

PAPERS_DIR = "app/papers"
TEXT_DIR = "app/papers/text"

# Section headers to detect
SECTIONS = ["abstract", "methods", "methodology", "results", "conclusion"]


def ensure_text_folder():
    """
    Create text folder (app/papers/text) if it does not exist.
    """
    if not os.path.exists(TEXT_DIR):
        os.makedirs(TEXT_DIR)
        print(f"📁 Created folder: {TEXT_DIR}")


def extract_text_from_pdf(pdf_path):
    """
    Extracts raw text from a PDF using PyMuPDF.
    Returns extracted text as a single string.
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page in doc:
            try:
                full_text += page.get_text("text")
            except Exception:
                pass

        doc.close()
        return full_text

    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return ""


def extract_sections(text):
    """
    Extract section-wise text (Abstract, Methods, Results).
    """
    text_lower = text.lower()
    sections_data = {}

    for i, section in enumerate(SECTIONS):
        if section in text_lower:
            start = text_lower.find(section)
            end = len(text_lower)

            for next_section in SECTIONS[i + 1:]:
                pos = text_lower.find(next_section)
                if pos != -1:
                    end = pos
                    break

            sections_data[section] = text[start:end].strip()

    return sections_data


def validate_sections(sections):
    """
    Simple validation to check required sections.
    """
    required = ["abstract", "methods", "results"]
    missing = [sec for sec in required if sec not in sections]

    if missing:
        print(f"⚠ Missing sections: {missing}")
        return False

    return True


def extract_all_papers():
    """
    Extract text from ALL PDFs stored in app/papers/
    Save section-wise text into app/papers/text/
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

        full_text = extract_text_from_pdf(pdf_path)

        if not full_text.strip():
            print(f"⚠ No readable text found in {filename}")
            continue

        sections = extract_sections(full_text)

        # ✅ VALIDATION USED CORRECTLY
        if not validate_sections(sections):
            print("⚠ Incomplete paper — still saved for reference")

        txt_filename = filename.replace(".pdf", "_sections.txt")
        txt_path = os.path.join(TEXT_DIR, txt_filename)

        with open(txt_path, "w", encoding="utf-8") as f:
            for sec, content in sections.items():
                f.write(f"\n\n===== {sec.upper()} =====\n")
                f.write(content)

        print(f"✅ Section-wise text saved → {txt_path}")
        extracted_files.append(txt_path)

    return extracted_files
