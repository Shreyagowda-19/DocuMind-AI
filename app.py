import streamlit as st

from utils.pdf_reader import extract_text
from utils.text_splitter import split_text
from utils.vector_store import create_vector_store
from utils.retriever import get_retriever
from utils.chatbot import ask_question


# --------------------------------------------------
# Load CSS
# --------------------------------------------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="GenAI Research Assistant",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:

    st.title("Research Assistant")

    st.markdown("---")

    st.info("""
Upload any PDF

Ask unlimited questions

Powered by:

• Gemini 2.5 Flash

• FAISS

• LangChain
""")

    st.markdown("---")

    st.success("🟢 Ready")


# --------------------------------------------------
# Title
# --------------------------------------------------
st.title(" GenAI Research Assistant")

st.caption("Chat with your PDF using Gemini + LangChain + FAISS")


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


# --------------------------------------------------
# Process PDF
# --------------------------------------------------
if uploaded_file:

    st.success(f"Uploaded: **{uploaded_file.name}**")

    # -----------------------------
    # Extract Text
    # -----------------------------
    pdf_text = extract_text(uploaded_file)

    if not pdf_text.strip():
        st.error("Could not extract text.")
        st.stop()

    # -----------------------------
    # Split
    # -----------------------------
    chunks = split_text(pdf_text)

    # -----------------------------
    # Vector Store
    # -----------------------------
    vector_store = create_vector_store(chunks)

    retriever = get_retriever(vector_store)

    # -----------------------------
    # Statistics
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📦 Chunks",
        len(chunks)
    )

    col2.metric(
        "🧠 Documents",
        vector_store.index.ntotal
    )

    col3.metric(
        "📄 File Size",
        f"{uploaded_file.size//1024} KB"
    )

    st.divider()

    # -----------------------------
    # Text Preview
    # -----------------------------
    with st.expander("📄 Preview Extracted Text"):

        st.write(pdf_text[:2000])

    st.divider()

    # -----------------------------
    # Suggested Questions
    # -----------------------------
    st.subheader("💡 Suggested Questions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("📑 Summarize"):
            st.session_state["question"] = "Summarize the document"

        if st.button("📝 Important Topics"):
            st.session_state["question"] = "List all important topics"

    with col2:

        if st.button("🌐 Explain DOM"):
            st.session_state["question"] = "Explain DOM"

        if st.button("🎯 Quiz Me"):
            st.session_state["question"] = "Create 5 quiz questions"

    st.divider()

    # -----------------------------
    # Ask Question
    # -----------------------------
    question = st.text_input(
        "Ask anything about your PDF",
        value=st.session_state.get("question", ""),
        placeholder="Example: Explain DOM"
    )

    if st.button("🚀 Ask AI"):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Thinking..."):

                answer = ask_question(
                    retriever,
                    question
                )

            st.divider()

            st.markdown("## 🤖 AI Answer")

            st.success(answer)

            st.divider()

            st.info(
                "Answer generated using the uploaded PDF."
            )