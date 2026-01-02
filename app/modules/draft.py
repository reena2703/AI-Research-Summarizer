import os
import json
import requests

INPUT_FILE = "app/output/combined_abstracts.json"
OUTPUT_FILE = "app/output/final_research_draft.txt"

HF_MODEL = "facebook/bart-large-cnn"
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


def load_combined():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError("combined_abstracts.json not found")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def hf_summarize(text):
    url = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

    headers = {"Content-Type": "application/json"}
    if HF_API_KEY:
        headers["Authorization"] = f"Bearer {HF_API_KEY}"

    payload = {
        "inputs": text,
        "parameters": {"min_length": 180, "max_length": 400}
    }

    response = requests.post(url, headers=headers, json=payload, timeout=90)
    result = response.json()

    if isinstance(result, list):
        return result[0]["summary_text"]

    return "Summary generation failed"


def generate_research_draft(data):
    summaries = "\n".join(p["summary"] for p in data)
    findings = "\n".join(p.get("key_findings", "") for p in data)

    abstract = hf_summarize(
        "Write an academic abstract based on the following research summaries:\n" + summaries
    )

    methods = hf_summarize(
        "Compare and summarize the research methods used in the following papers:\n" + summaries
    )

    results = hf_summarize(
        "Synthesize the key results and findings from these studies:\n" + findings
    )

    references = "\n".join(
        f"{i+1}. {p['title']}. Retrieved from Semantic Scholar."
        for i, p in enumerate(data)
    )

    draft = f"""
================ RESEARCH REVIEW =================

ABSTRACT
{abstract}

METHODS
{methods}

RESULTS
{results}

REFERENCES (APA Style)
{references}

=================================================
"""
    return draft


def save_draft(text):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"📄 Final research draft saved → {OUTPUT_FILE}")


def generate_draft():
    print("📝 Generating structured research draft (Milestone 3)...")
    data = load_combined()
    draft = generate_research_draft(data)
    save_draft(draft)
    return draft
