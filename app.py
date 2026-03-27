import streamlit as st
import os

# SECURITY WARNING: DO NOT HARDCODE API KEYS. 
# Use environment variables or UI input to provide keys.
import sys

# 1. IMMEDIATE UI RENDER (This MUST be first)
st.set_page_config(page_title="AI DDR Generator", layout="wide")

st.title("🏗️ AI Detailed Diagnostic Report (DDR) Generator")
st.success("✅ App Interface Loaded Successfully.")
st.markdown("Generate professional property diagnostic reports using RAG and Groq AI.")

# 2. Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 3. Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    
    # Try to get key from environment first
    env_key = os.getenv("GROQ_API_KEY", "")
    groq_api_key = st.text_input("Enter Groq API Key", value=env_key, type="password")
    
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key
    
    st.header("Upload Documents")
    inspection_file = st.file_uploader("Upload Inspection Report (PDF)", type="pdf")
    thermal_file = st.file_uploader("Upload Thermal Report (PDF)", type="pdf")

    if st.button("Clear Vector Store"):
        if os.path.exists("data/chroma_db"):
            import shutil
            shutil.rmtree("data/chroma_db")
            st.success("Vector store cleared!")

# 4. Main logic (Imports inside the button block for stability)
if groq_api_key and inspection_file and thermal_file:
    if st.button("🚀 Process Reports & Generate DDR"):
        if not groq_api_key.startswith("gsk_"):
            st.error("Invalid Groq API Key format. It should start with 'gsk_'.")
        else:
            try:
                # DEFERRED IMPORTS (Prevents startup crash)
                with st.spinner("📦 Loading AI Engines (HuggingFace, Torch, LangChain)..."):
                    from loader import PDFLoader
                    from splitter import TextSplitter
                    from embeddings import EmbeddingModel
                    from vector_store import VectorStore
                    from retriever import Retriever
                    from report_generator import ReportGenerator
                
                with st.spinner("📄 Processing documents..."):
                    # Step 1: Save uploaded files
                    if not os.path.exists("data"):
                        os.makedirs("data")
                    
                    inspection_path = os.path.join("data", "inspection.pdf")
                    thermal_path = os.path.join("data", "thermal.pdf")
                    
                    with open(inspection_path, "wb") as f:
                        f.write(inspection_file.getbuffer())
                    with open(thermal_path, "wb") as f:
                        f.write(thermal_file.getbuffer())
                    
                    # Step 2: Extract and chunk
                    st.info("🔍 Extracting text and images...")
                    loader = PDFLoader()
                    inspection_data = loader.extract_text_and_images(inspection_path, "inspection")
                    thermal_data = loader.extract_text_and_images(thermal_path, "thermal")
                    
                    st.write(f"✅ Loaded {len(inspection_data)} pages from inspection.")
                    st.write(f"✅ Loaded {len(thermal_data)} pages from thermal.")
                    
                    all_extracted_data = inspection_data + thermal_data
                    
                    splitter = TextSplitter()
                    documents = splitter.split_data(all_extracted_data)
                    st.write(f"✅ Created {len(documents)} text chunks.")
                    
                    # Step 3: Embeddings and Vector Store
                    st.info("📦 Creating vector store...")
                    emb_model = EmbeddingModel().get_embeddings()
                    vs = VectorStore(emb_model)
                    vector_db = vs.create_store(documents)
                    
                    # Step 4: Retrieval and Generation
                    st.info("🤖 Generating report...")
                    retriever = Retriever(vector_db)
                    
                    general_query = "Summarize all property issues, dampness, thermal hotspots, leakage in rooms, root causes, and recommended actions."
                    context, image_paths = retriever.get_context_for_ddr(general_query)
                    
                    st.write(f"✅ Retrieved context size: {len(context)} chars.")
                    
                    generator = ReportGenerator(groq_api_key=groq_api_key)
                    ddr_report = generator.generate_ddr(context)
                    
                    # Store in session state
                    st.session_state["ddr_report"] = ddr_report
                    st.session_state["image_paths"] = image_paths
                    st.success("🎉 Report generated successfully!")
            
            except Exception as e:
                st.error(f"❌ PIPELINE ERROR: {e}")
                st.exception(e)

# 5. Display Report
if "ddr_report" in st.session_state:
    st.divider()
    st.header("📄 Generated Detailed Diagnostic Report")
    st.markdown(st.session_state["ddr_report"])
    
    st.header("📸 Evidence Gallery")
    if st.session_state["image_paths"]:
        unique_images = list(set(st.session_state["image_paths"]))
        cols = st.columns(3)
        for i, img_path in enumerate(unique_images):
            with cols[i % 3]:
                if os.path.exists(img_path):
                    st.image(img_path, caption=os.path.basename(img_path), use_container_width=True)
    else:
        st.info("No relevant images found.")

elif not groq_api_key:
    st.warning("Please enter your Groq API Key in the sidebar.")
elif not (inspection_file and thermal_file):
    st.info("Please upload both reports to begin.")
