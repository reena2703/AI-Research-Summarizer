import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read Semantic Scholar API key (optional but recommended)
SEMANTIC_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

PAPERS_DIR = "app/papers"
RATE_LIMIT_SECONDS = 1  # Semantic Scholar guideline (1 RPS)


def ensure_papers_folder():
    """Create papers folder if it does not exist."""
    if not os.path.exists(PAPERS_DIR):
        os.makedirs(PAPERS_DIR)


def search_semantic_scholar(query, limit=5):
    """
    Search Semantic Scholar for papers related to a topic.
    Uses API key if available, otherwise falls back to public access.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "paperId,title,year,authors,openAccessPdf,url"
    }

    headers = {}
    if SEMANTIC_API_KEY:
        headers["x-api-key"] = SEMANTIC_API_KEY

    for attempt in range(3):  # retry logic
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            return response.json().get("data", [])

        except Exception as e:
            print(f"⚠ Search attempt {attempt + 1} failed: {e}")
            time.sleep(RATE_LIMIT_SECONDS)

    return []


def save_metadata(metadata, filename):
    """Save paper metadata as JSON."""
    path = os.path.join(PAPERS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def download_papers(topic):
    """
    Downloads open-access research PDFs and stores metadata JSON.
    Prepares dataset for analysis.
    """
    ensure_papers_folder()
    papers = search_semantic_scholar(topic)

    if not papers:
        print("❌ No papers found.")
        return []

    saved_files = []

    for idx, paper in enumerate(papers, start=1):
        pdf_info = paper.get("openAccessPdf")

        if not pdf_info or not pdf_info.get("url"):
            print("⏭ Skipping paywalled paper")
            continue

        pdf_url = pdf_info["url"]
        pdf_name = f"paper_{idx}.pdf"
        json_name = f"paper_{idx}.json"

        try:
            print(f"⬇ Downloading: {pdf_name}")

            pdf_response = requests.get(pdf_url, timeout=20)
            pdf_response.raise_for_status()

            # Save PDF
            with open(os.path.join(PAPERS_DIR, pdf_name), "wb") as f:
                f.write(pdf_response.content)

            # Save metadata
            metadata = {
                "topic": topic,
                "paperId": paper.get("paperId"),
                "title": paper.get("title"),
                "year": paper.get("year"),
                "authors": [a["name"] for a in paper.get("authors", [])],
                "pdf_url": pdf_url,
                "source": "Semantic Scholar"
            }

            save_metadata(metadata, json_name)
            saved_files.append(pdf_name)

            time.sleep(RATE_LIMIT_SECONDS)

        except Exception as e:
            print(f"⚠ Failed to download {pdf_url}: {e}")

    print(f"\n📁 Dataset ready → {len(saved_files)} papers downloaded.")
    return saved_files
