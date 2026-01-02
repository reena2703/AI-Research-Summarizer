from dotenv import load_dotenv
import gradio as gr

# Import modules
from modules.retrieval import download_papers
from modules.extract import extract_all_papers
from modules.analyze import analyze_all
from modules.draft import generate_draft
from modules.review import review_draft

# Load environment variables
load_dotenv()


def full_pipeline(topic):
    """
    Runs the entire ONLINE research summarization pipeline
    based on USER TOPIC input.
    """
    try:
        if not topic or topic.strip() == "":
            return "❌ Please enter a research topic."

        print(f"\n🔍 USER SELECTED TOPIC → {topic}\n")

        # Step 1: Retrieve papers
        print("📥 Fetching research papers...")
        papers = download_papers(topic)
        if not papers:
            return "❌ No papers found. Try another topic."

        # Step 2: Extract PDF text
        print("📄 Extracting paper content...")
        extracted = extract_all_papers()
        if not extracted:
            return "❌ Text extraction failed."

        # Step 3: Analyze papers
        print("🧠 Generating AI paper summaries...")
        summaries = analyze_all()
        if not summaries:
            return "❌ Paper analysis failed."

        # Step 4: Generate research draft
        print("📝 Creating structured research draft...")
        draft = generate_draft()
        if not draft:
            return "❌ Draft generation failed."

        # Step 5: Review draft
        print("🤖 Improving academic quality...")
        reviewed = review_draft(draft)

        print("✅ Pipeline Completed Successfully!")
        return reviewed

    except Exception as e:
        return f"❌ Pipeline Error: {e}"


def launch_app():
    with gr.Blocks() as demo:

        gr.Markdown("## 🧠 AI Research Paper Summarizer (Online Mode)")

        gr.Markdown("""
### ✅ Updated Pipeline  

1️⃣ User enters ANY research topic  
2️⃣ System searches Semantic Scholar  
3️⃣ Downloads available research papers  
4️⃣ Extracts text from PDFs  
5️⃣ Summarizes using HuggingFace  
6️⃣ Generates structured research draft  
7️⃣ Refines and reviews final output  
""")

        topic_input = gr.Textbox(
            label="Enter Research Topic",
            placeholder="Example: Deep Learning in Healthcare"
        )

        output_box = gr.Textbox(
            label="Final Reviewed Research Draft",
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
