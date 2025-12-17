import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INPUT_FILE = "app/output/combined_abstracts.json"
OUTPUT_FILE = "app/output/final_research_draft.txt"


def load_combined_summaries():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError("combined_abstracts.json not found")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_research_draft(combined_data):
    prompt = f"""
You are an expert academic researcher.

Using the following structured summaries from MULTIPLE research papers,
generate a complete **Research Review Draft**.

CONTENT:
{json.dumps(combined_data, indent=2)}

Your output MUST include the following sections:

1. Abstract (100–150 words)
2. Introduction
3. Methodology Comparison
4. Results Synthesis (similarities and differences)
5. Key Findings (bullet points)
6. Limitations
7. Conclusion
8. References (APA-style, based on titles/authors provided)

Rules:
- Use academic English
- Synthesize across papers (do NOT summarize one-by-one)
- Do NOT invent new data
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0.4
    )

    return response.choices[0].message.content


def save_draft(text):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"📄 Final research draft saved → {OUTPUT_FILE}")


def generate_draft():
    print("📝 Generating research review draft...")
    combined_data = load_combined_summaries()
    draft = generate_research_draft(combined_data)
    save_draft(draft)
    return draft
