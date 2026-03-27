# 🏗️ AI DDR Report Generator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green.svg)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com/)

An AI-powered system that generates **Detailed Diagnostic Reports (DDR)** by intelligently merging **Inspection Reports** and **Thermal Reports** using a RAG (Retrieval-Augmented Generation) pipeline.

---

## 🎯 Problem Statement

Traditional property diagnostics often involve manual review of multiple, disconnected documents like inspection logs and thermal scans. This process is time-consuming, prone to human error, and often fails to correlate visual findings with thermal data effectively. 

**AI DDR Generator** solves this by:
- Automatically extracting observations from diverse report types.
- Correlating visual defects with thermal hotspots.
- Eliminating duplicate information across documents.
- Producing a structured, professional, and client-ready diagnostic report in seconds.

---

## ✨ Features

*   **Multi-Document Synthesis:** Combines data from both standard inspection and thermal PDF reports.
*   **Intelligent Deduplication:** Identifies and merges overlapping observations found across different pages or documents.
*   **Evidence Mapping:** Automatically extracts and links relevant images from the reports to specific observations.
*   **Structured Technical Reasoning:** Classifies issues by severity (Low/Medium/High) with clear justifications.
*   **Root Cause Analysis:** Provides scientific reasoning for property defects (e.g., dampness, leakages).
*   **Actionable Remediation:** Generates tailored recommendations for each detected issue.
*   **Missing Data Handling:** Explicitly identifies gaps in information using the "Not Available" tag to ensure transparency.
*   **Modern Interactive UI:** Built with Streamlit for a fast, responsive, and user-friendly experience.

---

## 🧠 How It Works (RAG Pipeline)

The system utilizes a sophisticated RAG architecture to ensure accuracy and groundedness:

1.  **PDF Loading:** `PyMuPDF` (Fitz) extracts raw text and embeds images from uploaded reports.
2.  **Smart Chunking:** Text is split into semantically meaningful chunks using recursive character splitting.
3.  **HuggingFace Embeddings:** High-dimensional vector representations are generated for each text chunk.
4.  **ChromaDB Vector Store:** Embeddings are stored in a local vector database for ultra-fast semantic retrieval.
5.  **Context-Aware Retrieval:** The system retrieves the most relevant technical details based on the diagnostic query.
6.  **LLM Generation (Groq):** Using `Llama-3.1-8b` (via Groq API), the system synthesizes the retrieved context into a professional report following strict engineering templates.

---

## ⚙️ Tech Stack

*   **Logic:** Python 3.9+
*   **Orchestration:** LangChain
*   **LLM:** Groq API (Llama 3.1 & Gemma 2)
*   **Vector DB:** ChromaDB
*   **Embeddings:** HuggingFace (Sentence Transformers)
*   **PDF Engine:** PyMuPDF
*   **UI Framework:** Streamlit

---

## 📸 Screenshots

### 1. Home UI
![Home UI](assets/Home%20UI.png)
*Professional dashboard for report uploading and configuration.*

### 2. Generated Report
![Generated Report](assets/Generated%20Report.png)
*Structured output including area-wise observations and severity assessment.*

### 3. Case Report Details
![Continue report](assets/Continue%20report.png)
*Further details for the generated report with additional insights.*

### 4. Evidence Gallery
![Evidence images](assets/Evidence%20images%20.png)
*Visual evidence extracted directly from the source PDFs.*

### 5. Detailed Case View
![Report continue](assets/Report%20continue.png)
*Extended view of the report for more technical data.*

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9 or higher
- A Groq API Key (Get it at [console.groq.com](https://console.groq.com/))

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/ai-ddr-generator.git
    cd ai-ddr-generator
    ```

2.  **Set Up Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_gsk_xxx_key_here
    ```

5.  **Run the App**
    ```bash
    streamlit run app.py
    ```

---

## 📊 Output Format

The generated **Detailed Diagnostic Report (DDR)** follows a rigorous structure:

| Section | Description |
| :--- | :--- |
| **Property Issue Summary** | High-level overview of the property's state. |
| **Area-wise Observations** | Detailed defects grouped by room with linked evidence images. |
| **Probable Root Cause** | Scientific explanation for the observed issues. |
| **Severity Assessment** | Low/Medium/High rating with technical justification. |
| **Recommended Actions** | Step-by-step remediation plan for the client. |
| **Missing Information** | Clear list of data points not found (e.g., `Paint type → Not Available`). |

---

## 📂 Project Structure

```text
ai-ddr-generator/
├── app.py              # Main Streamlit Application
├── src/                # Core Library
│   ├── loader.py       # PDF Text/Image Extraction
│   ├── splitter.py     # Document Chunking Logic
│   ├── embeddings.py   # Vector Embeddings Configuration
│   ├── vector_store.py # ChromaDB Management
│   ├── retriever.py    # Semantic Search Logic
│   └── report_generator.py # LLM Synthesis & Fallback Handling
├── data/               # Local Storage
│   ├── chroma_db/      # Vector Database files
│   └── extracted_images/ # Cached Evidence Images
└── requirements.txt    # Python Dependencies
```

---

## ⚠️ Limitations

*   **Handwritten Text:** OCR capabilities are currently limited; printed PDFs work best.
*   **Image Resolution:** Evidence quality depends entirely on the resolution of the source PDF images.
*   **Context Window:** Large reports exceeding 50+ pages may require advanced sliding window retrieval.

---

## 🚀 Future Improvements

*   **Multi-LLM Voting:** Implementing a consensus mechanism between Llama-3 and Claude/GPT-4 for higher accuracy.
*   **Automatic PDF Export:** Direct generation of downloadable PDF/DOCX reports with branded templates.
*   **Historic Comparison:** Ability to compare new reports with previous diagnostic sessions to track repair progress.
*   **Mobile App:** A technician-facing mobile app for real-time report generation on-site.

---

## 🎥 Demo

[![Watch the Demo](https://img.shields.io/badge/Loom-Video_Demo-9254f3?style=for-the-badge&logo=loom)](https://www.loom.com/share/d46be1476e3e42f3a7121bf29f5aa89a)

---

## 🧑‍💻 Author

**Harsh Lagwal**
- [Portfolio](https://portfolio-harsh-lagwal.vercel.app/)
- [LinkedIn](https://www.linkedin.com/in/harshlagwal)
- [GitHub](https://github.com/harshlagwal)

---
Developed by Harsh Lagwal.
