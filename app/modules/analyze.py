import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TEXT_DIR = "app/papers/text"
OUTPUT_DIR = "app/output"

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = "facebook/bart-large-cnn"


def ensure_output_folder():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


# -------- ABSTRACT EXTRACTION --------
def extract_abstract(text: str) -> str:
    text_lower = text.lower()

    if "abstract" in text_lower:
        start = text_lower.find("abstract")
        end = text_lower.find("introduction")

        if end != -1:
            return text[start:end].strip()

        return text[start:].strip()

    return text[:1500]


# -------- KEY FINDINGS EXTRACTION --------
def extract_key_findings(results_text):
    """
    Extract key findings from Results section using HuggingFace.
    """
    prompt = (
        "Extract the key findings and results from the following research text:\n\n"
        + results_text[:2000]
    )

    return hf_summarize(prompt)


# -------- HUGGINGFACE SUMMARIZER --------
def hf_summarize(text):
    url = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

    headers = {"Content-Type": "application/json"}

    if HF_API_KEY:
        headers["Authorization"] = f"Bearer {HF_API_KEY}"

    payload = {
        "inputs": text,
        "parameters": {"min_length": 120, "max_length": 300}
    }

    for attempt in range(3):
        try:
            print(f"   🔹 HuggingFace request attempt {attempt + 1}")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()

            if isinstance(result, list) and "summary_text" in result[0]:
                return result[0]["summary_text"]

            return "Summarization failed"

        except Exception as e:
            print(f"   ⚠ HF error attempt {attempt+1}: {e}")
            time.sleep(2)

    return "❌ Failed to summarize due to repeated HF failures."


# -------- MAIN ANALYSIS PIPELINE --------
def analyze_all():
    ensure_output_folder()

    if not os.path.exists(TEXT_DIR):
        print("❌ No text folder found.")
        return None

    files = [f for f in os.listdir(TEXT_DIR) if f.endswith(".txt")]

    if not files:
        print("❌ No text files found.")
        return None

    combined = []

    for file in files:
        print(f"\n📘 Analyzing: {file}")

        path = os.path.join(TEXT_DIR, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        # Abstract summary
        abstract = extract_abstract(text)
        summary = hf_summarize(abstract)

        # Key findings from Results section
        results_section = text.lower().split("results")[-1][:3000]
        key_findings = extract_key_findings(results_section)

        title = file.replace(".txt", "").replace("_", " ").title()

        result = {
            "title": title,
            "source_file": file,
            "summary": summary,
            "key_findings": key_findings
        }

        out_path = os.path.join(
            OUTPUT_DIR,
            file.replace(".txt", "_summary.json")
        )

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print(f"✅ Saved summary → {out_path}")
        combined.append(result)

    combined_path = os.path.join(OUTPUT_DIR, "combined_abstracts.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=4)

    print(f"\n📊 Combined dataset ready → {combined_path}")
    return combined

