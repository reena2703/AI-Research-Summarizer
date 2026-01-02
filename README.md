Md
# AI Research Paper Summarizer (Online Mode)

This project was developed as part of the *Infosys Virtual Internship 6.0 – AI Domain*.  
It focuses on applying Artificial Intelligence and Natural Language Processing (NLP) techniques to automate the process of research paper analysis and summarization.

The system helps users quickly understand multiple research papers by generating structured summaries and insights from open-access academic publications.

---

## Internship Details

- *Program*: Infosys Virtual Internship 6.0  
- *Domain*: Artificial Intelligence (AI)  
- *Project Type*: Academic & Skill-Based Internship Project  
- *Duration*: 8 Weeks  
- *Focus Areas*: NLP, AI Automation, Research Summarization  

---

## Problem Statement

During academic research, reviewing multiple papers is time-consuming and complex.  
Each paper follows a different structure, making comparison difficult.

This project addresses that problem by:
- Automatically collecting research papers  
- Extracting relevant sections  
- Generating AI-based summaries  
- Producing a consolidated research draft  

---

## Project Objectives

- Automate research paper discovery using APIs  
- Extract and validate important sections from PDFs  
- Generate AI-driven summaries and key findings  
- Create a structured research review draft  
- Provide a simple and interactive UI for users  

---

## Project Workflow

1. User enters a research topic  
2. Papers are fetched from Semantic Scholar  
3. Open-access PDFs are downloaded  
4. Text is extracted and sectioned  
5. AI models summarize content and extract insights  
6. Cross-paper synthesis is generated  
7. Final research draft is reviewed and refined  

---

## Folder Structure
AI-Research-Summarizer/ 
│ ├── app/ │   ├── main.py     # Main pipeline + Gradio UI
│   ├── modules/ │   │   ├── retrieval.py      # Paper search & download 
│   │   ├── extract.py        # PDF text extraction & validation 
│   │   ├── analyze.py        # Summarization & key findings 
│   │   ├── draft.py          # Research draft generation 
│   │   └── review.py         # Review & refinement 
│   │ │   ├── papers/         # Downloaded PDFs (ignored in GitHub) 
│   └── output/               # Generated outputs (ignored) 
│ ├── requirements.txt 
├── .gitignore 
├── README.md 
└── .env                      # API keys (ignored)
 
---

## Technology Stack

### Programming Language
- Python 3.x

### Libraries & Tools Used
- *Gradio* – Interactive UI  
- *Requests* – API communication  
- *Semantic Scholar API* – Paper retrieval  
- *PyMuPDF* – PDF text extraction  
- *HuggingFace Hub* – AI summarization models  
- *python-dotenv* – Environment variables  

---

## Milestone Completion Status

### Milestone 1 (Week 1–2)
✔ Environment setup  
✔ Paper search and download  
✔ Dataset preparation  

### Milestone 2 (Week 3–4)
✔ PDF text extraction  
✔ Section-wise parsing  
✔ Key findings extraction  
✔ Validation checks  

### Milestone 3 (Week 5–6)
✔ Structured draft generation  
✔ Multi-paper synthesis  

### Milestone 4 (Week 7–8)
✔ Review and refinement  
✔ UI integration  
✔ Final report preparation  

---

## Author

*Reena M*  
B.E. Computer Science Engineering  
Infosys Virtual Internship 6.0 – AI Domain  

---

## Disclaimer

This project is developed as part of the *Infosys Virtual Internship 6.0 Program* for learning and academic evaluation purposes.