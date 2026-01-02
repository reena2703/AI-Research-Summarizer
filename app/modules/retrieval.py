import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SEMANTIC_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

PAPERS_DIR = "app/papers"
RATE_LIMIT_SECONDS = 1  # Semantic Scholar guideline


def ensure_papers_folder():
    if not os.path.exists(PAPERS_DIR):
        os.makedirs(PAPERS_DIR)


def search_semantic_scholar(query, limit=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": limit,
        "fields": "paperId,title,year,authors,openAccessPdf,url"
    }

    headers = {}
    if SEMANTIC_API_KEY:
        headers["x-api-key"] = SEMANTIC_API_KEY

    for attempt in range(3):
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
    path = os.path.join(PAPERS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def download_papers(topic):
    ensure_papers_folder()
    papers = search_semantic_scholar(topic)

    if not papers:
        print("❌ No papers found.")
        return []

    saved_files = []

    headers = {}
    if SEMANTIC_API_KEY:
        headers["x-api-key"] = SEMANTIC_API_KEY

    for idx, paper in enumerate(papers, start=1):
        pdf_info = paper.get("openAccessPdf")

        if not pdf_info or not pdf_info.get("url"):
            print("⏭ Skipping paywalled paper")
            continue

        pdf_url = pdf_info["url"]
        pdf_name = f"paper_{idx}.pdf"
        json_name = f"paper_{idx}.json"

        success = False

        for attempt in range(3):   # <-- retry logic
            try:
                print(f"⬇ Downloading attempt {attempt+1}: {pdf_name}")

                response = requests.get(
                    pdf_url,
                    headers=headers,
                    timeout=60,      # <-- longer time
                    stream=True
                )
                response.raise_for_status()

                # Validate PDF
                if "pdf" not in response.headers.get("Content-Type", ""):
                    print("⏭ Not a valid PDF, skipping")
                    break

                # Stream save
                with open(os.path.join(PAPERS_DIR, pdf_name), "wb") as f:
                    for chunk in response.iter_content(chunk_size=2048):
                        if chunk:
                            f.write(chunk)

                success = True
                break

            except Exception as e:
                print(f"⚠ Retry {attempt+1} failed: {e}")
                time.sleep(3)

        if not success:
            print("❌ Failed after 3 attempts — skipping")
            continue

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

    print(f"\n📁 Dataset ready → {len(saved_files)} papers downloaded.")
    return saved_files
