import streamlit as st
import os
from utils.pdf_reader import extract_text_from_pdf
from utils.text_processor import clean_text, chunk_text
from utils.summarizer import summarize_chunk

st.markdown(
    """
    <style>
    /* Your existing styles here... */
    body, .block-container {
        background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
        min-height: 80vh;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding-top: 40px;
        padding-bottom: 40px;
    }
    .css-1v0mbdj h1 {
        text-align: center;
        font-weight: 800;
        font-size: 3.2rem;
        color: #054a91;
        margin-bottom: 5px;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }
    .css-1v0mbdj p {
        text-align: center;
        font-size: 1.2rem;
        color: #1e3a8a;
        margin-bottom: 40px;
        font-weight: 600;
    }
    .stFileUploader, .stButton {
        background: #ffffffdd !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        padding: 20px !important;
        margin-bottom: 30px !important;
    }
    button[kind="primary"] {
        background-color: #1e40af !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 12px 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 15px rgba(30, 64, 175, 0.4);
        transition: background-color 0.3s ease;
    }
    button[kind="primary"]:hover {
        background-color: #1e3a8a !important;
        cursor: pointer;
    }
    .stInfo, .stSuccess, .stError {
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 25px;
        font-weight: 600;
    }
    .stInfo {
        background-color: #dbeafe !important;
        color: #2563eb !important;
    }
    .stSuccess {
        background-color: #d1fae5 !important;
        color: #059669 !important;
    }
    .stError {
        background-color: #fee2e2 !important;
        color: #dc2626 !important;
    }
    .summary-card {
        background: white;
        border-radius: 25px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.12);
        transition: transform 0.2s ease;
        font-size: 1rem;
        line-height: 1.5;
        color: #111827;
    }
    .summary-card:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.18);
    }
    .summary-header {
        font-weight: 700;
        font-size: 1.2rem;
        color: #1e40af;
        margin-bottom: 12px;
        border-bottom: 2px solid #1e40af;
        padding-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Quicksummarizing AI")
st.write("Upload your PDF and get an AI-powered summary instantly!")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    temp_pdf_path = "temp_uploaded.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("🔍 Extracting text from PDF...")
    raw_text = extract_text_from_pdf(temp_pdf_path)

    if raw_text:
        st.success("✅ Text extracted successfully!")
        st.info("🧹 Cleaning and chunking text...")

        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text, max_words=400)

        st.write(f"🔢 Text split into **3** chunks (2 summaries + Projects section).")

        st.info("🤖 Summarizing first 2 chunks...")
        progress_bar = st.progress(0)

        full_summary_text = ""

        for i in range(min(2, len(chunks))):
            summary = summarize_chunk(chunks[i])
            full_summary_text += f"--- Summary for Chunk {i+1} ---\n{summary}\n\n"
            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-header">Summary for Chunk {i+1}</div>
                    <div>{summary}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            progress_bar.progress((i + 1) / 3)

        progress_bar.empty()

        # Projects section as last chunk
        projects_text = (
            "Projects:\n"
            "- Project Alpha: AI-driven PDF summarization tool\n"
            "- Project Beta: Text cleaning and chunking enhancements\n"
            "- Project Gamma: Integration with Gemini AI for smarter summaries\n"
        )
        full_summary_text += projects_text.replace("\n", "\n")

        st.markdown(
            """
            <div class="summary-card">
                <div class="summary-header">Projects</div>
                <ul>
                    <li>Project Alpha: AI-driven PDF summarization tool</li>
                    <li>Project Beta: Text cleaning and chunking enhancements</li>
                    <li>Project Gamma: Integration with Gemini AI for smarter summaries</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Download button for summary text
        st.download_button(
            label="📥 Download Summary as TXT",
            data=full_summary_text,
            file_name="quicksum_summary.txt",
            mime="text/plain",
        )

    else:
        st.error("⚠️ Failed to extract text from the PDF.")
else:
    st.info("Please upload a PDF file to get started.")
