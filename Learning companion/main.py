import streamlit as st
from modules.rag import RAGEngine
from modules.reasoning import generate_answer
from modules.perception import process_image, process_pdf
from modules.utils import save_uploaded_file, format_chunks

st.set_page_config(page_title="📚 AI Learning Companion", layout="wide")

st.title("📚 Interactive AI Learning Companion")

query = st.text_area("Ask a question:", height=100)
mode = st.selectbox("Choose mode:", ["explain", "quiz", "analogy"])
depth = st.radio("Choose difficulty:", ["beginner", "intermediate", "advanced"])
uploaded_file = st.file_uploader("Upload notes (optional, PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])

rag = RAGEngine()

if st.button("Get Answer"):
    extra_context = ""
    if uploaded_file:
        path = save_uploaded_file(uploaded_file)
        if uploaded_file.type == "application/pdf":
            extra_context = process_pdf(path)
        else:
            extra_context = process_image(path)

    chunks = rag.retrieve(query)
    if extra_context:
        chunks.append(extra_context)

    st.markdown("### 📌 Retrieved Context")
    st.info(format_chunks(chunks))

    answer = generate_answer(query, chunks, mode, depth)
    st.markdown("### ✨ Answer")
    st.write(answer)
