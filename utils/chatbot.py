import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

def ask_question(retriever, question):

    # Retrieve relevant chunks
    if "summary" in question.lower() or "summarize" in question.lower():
        docs = retriever.invoke("main topics of the document")
    else:
        docs = retriever.invoke(question)

    # Combine retrieved chunks
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Prompt
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