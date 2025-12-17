import os
from dotenv import load_dotenv
import gradio as gr

# Import all modules
from modules.retrieval import download_papers
from modules.extract import extract_all_papers
from modules.analyze import analyze_all
from modules.draft import generate_draft
from modules.review import review_draft

# Load API keys
load_dotenv()


def full_pipeline(topic):
    """
    Runs the entire research summarization pipeline.
    """
    try:
        # Step 1: Download Papers
        papers = download_papers(topic)
        if not papers:
            return "❌ No papers found. Try another topic."

        # Step 2: Extract text from downloaded PDFs
        extracted = extract_all_papers()
        if not extracted:
            return "❌ Could not extract text from PDFs."

        # Step 3: Analyze each paper using GPT
        summaries = analyze_all()
        if not summaries:
            return "❌ Failed to summarize papers."

        # Step 4: Generate draft of research review
        draft = generate_draft(summaries)
        if not draft:
            return "❌ Draft generation failed."

        # Step 5: Final review to improve structure & clarity
        reviewed = review_draft(draft)
        return reviewed

    except Exception as e:
        return f"❌ Pipeline Error: {e}"


def launch_app():
    # Gradio 6.x → NO theme parameter in Blocks()
    with gr.Blocks() as demo:

        gr.Markdown("## 🧠 AI Research Paper Summarizer")
        
        gr.Markdown("""
### What this system does:

1. 🔍 Searches Semantic Scholar for related papers  
2. 📥 Downloads available research PDFs  
3. 📄 Extracts text from each paper  
4. 🧠 Uses GPT to analyze & summarize each paper  
5. 📝 Generates a combined research draft  
6. ✅ Reviews & improves the final research output  
""")

        topic_input = gr.Textbox(
            label="Enter Research Topic",
            placeholder="Example: Deep Learning in Healthcare",
        )

        output_box = gr.Textbox(
            label="Final Research Draft (Reviewed)",
            lines=30
        )

        run_button = gr.Button("Run Full Pipeline 🚀")

        run_button.click(
            fn=full_pipeline,
            inputs=topic_input,
            outputs=output_box
        )

    demo.launch()


if __name__ == "__main__":
    launch_app()
