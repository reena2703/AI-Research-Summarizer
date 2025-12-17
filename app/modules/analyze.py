import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEXT_DIR = "app/papers/text"
OUTPUT_DIR = "app/output"


def ensure_output_folder():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def extract_abstract(text):
    """
    Extract abstract section heuristically.
    """
    lower = text.lower()

    if "abstract" in lower:
        start = lower.find("abstract")
        end = lower.find("introduction")

        if end != -1:
            return text[start:end].strip()
        return text[start:].strip()

    return text[:1500]  # fallback


def summarize_abstract(title, abstract):
    prompt = f"""
You are an expert AI research assistant.

Summarize the following research paper abstract into EXACTLY these sections:

1. Background
2. Objective
3. Methods
4. Results
5. Conclusion

Use concise academic language.

TITLE: {title}

ABSTRACT:
{abstract}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Summary generation failed: {e}"


def analyze_all():
    """
    Milestone 2 complete analysis:
    - Extract abstracts
    - Generate structured summaries
    - Save per-paper JSON
    - Save combined comparison-ready JSON
    """
    ensure_output_folder()

    combined_results = []

    files = [f for f in os.listdir(TEXT_DIR) if f.endswith(".txt")]

    if not files:
        print("❌ No extracted text files found.")
        return

    for file in files:
        path = os.path.join(TEXT_DIR, file)
        print(f"\n📘 Analyzing: {file}")

        with open(path, "r", encoding="utf-8") as f:
            full_text = f.read()

        abstract = extract_abstract(full_text)
        title = file.replace(".txt", "").replace("_", " ").title()

        summary = summarize_abstract(title, abstract)

        paper_result = {
            "title": title,
            "source_file": file,
            "summary": summary
        }

        # Save individual summary
        output_path = os.path.join(
            OUTPUT_DIR,
            file.replace(".txt", "_summary.json")
        )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(paper_result, f, indent=4)

        print(f"✅ Saved summary → {output_path}")

        combined_results.append(paper_result)

    # Save combined file for comparison
    combined_path = os.path.join(OUTPUT_DIR, "combined_abstracts.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined_results, f, indent=4)

    print(f"\n📊 Combined dataset ready → {combined_path}")
