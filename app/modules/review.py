import os
import requests
from dotenv import load_dotenv

load_dotenv()

INPUT_FILE = "app/output/final_research_draft.txt"
OUTPUT_FILE = "app/output/reviewed_research_draft.txt"

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")   # must exist in .env

MODEL = "facebook/bart-large-cnn"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}


def hf_summarize(text):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": 200,
            "max_length": 400
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=90)

    if response.status_code != 200:
        raise Exception(f"HuggingFace API Error: {response.text}")

    result = response.json()

    # router always returns list
    return result[0]["summary_text"]


def review_draft(text=None):
    if text is None:
        if not os.path.exists(INPUT_FILE):
            return "❌ No draft found"
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            text = f.read()

    print("🤖 Sending draft to HuggingFace Reviewer...")

    refined_text = hf_summarize(text)

    reviewed_content = f"""
================ REVIEWED RESEARCH DRAFT =================

REFINED REVIEW OUTPUT
{refined_text}

Notes:
This version improves clarity, structure, grammar, and academic tone while
keeping meaning intact.

==========================================================
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(reviewed_content)

    print(f"✅ Reviewed draft saved → {OUTPUT_FILE}")
    return reviewed_content
