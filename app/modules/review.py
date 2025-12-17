import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def review_draft(draft_text):
    """
    Uses GPT to review and refine the generated research draft.

    Output Format:
    1. Improvements Needed (bullet points)
    2. Revised Draft (clean, improved academic writing)
    """

    prompt = f"""
You are an expert academic editor.

Review and improve the following research draft:

DRAFT:
{draft_text}

Your response must follow EXACTLY this structure:

1. **Improvements Needed**
Provide 6–8 bullet points focusing on:
- clarity
- academic tone
- structure/organization
- logical flow
- coherence
- grammar & vocabulary
- completeness of arguments
- citation consistency

2. **Revised Draft**
Provide a polished, fully improved version of the draft.
Rules:
- Maintain the original meaning.
- Improve academic tone.
- Fix grammar and flow.
- Do NOT invent new research data.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            temperature=0.3
        )

        # Return cleaned content
        return response.choices[0].message["content"]

    except Exception as e:
        print(f"❌ Error reviewing draft: {e}")
        return "Review process failed due to an unexpected error."
