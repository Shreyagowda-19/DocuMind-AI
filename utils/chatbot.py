import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0
)

def ask_question(retriever, question):

    if "summary" in question.lower() or "summarize" in question.lower():
        docs = retriever.invoke("main topics of the document")
    else:
        docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an intelligent Research Assistant.

Use ONLY the information from the retrieved context.

If the question asks for a summary, provide a concise summary using all relevant context.

If the answer is not present in the context, reply exactly:

"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content