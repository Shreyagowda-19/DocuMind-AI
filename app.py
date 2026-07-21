import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   # Change to gemini-3.5-flash if your SDK supports it
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0
)


def ask_question(retriever, question):

    # Retrieve relevant chunks
    if "summary" in question.lower() or "summarize" in question.lower():
        docs = retriever.invoke("main topics of the document")
    else:
        docs = retriever.invoke(question)

    # Combine retrieved context
    context = "\n\n".join(doc.page_content for doc in docs)

    # Prompt
    prompt = f"""
You are an intelligent Research Assistant.

Answer ONLY using the information provided in the context.

Instructions:
- Give a clean, well-structured answer.
- Use bullet points where appropriate.
- Do NOT return JSON.
- Do NOT return Python objects.
- Do NOT return metadata.
- Do NOT return signatures.
- Do NOT return extras.

If the answer is not present in the context, reply exactly:

"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    content = response.content

    # -------------------------------
    # Case 1: Plain string
    # -------------------------------
    if isinstance(content, str):
        return content.strip()

    # -------------------------------
    # Case 2: List of content blocks
    # -------------------------------
    if isinstance(content, list):

        final_answer = []

        for block in content:

            # Dictionary block
            if isinstance(block, dict):
                if "text" in block:
                    final_answer.append(block["text"])

            # LangChain object block
            elif hasattr(block, "text"):
                final_answer.append(block.text)

            else:
                final_answer.append(str(block))

        return "\n".join(final_answer).strip()

    # -------------------------------
    # Case 3: Fallback
    # -------------------------------
    return str(content)