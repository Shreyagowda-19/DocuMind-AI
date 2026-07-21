import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",   # or gemini-3.5-flash if your package supports it
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0
)


def ask_question(retriever, question):

    if "summary" in question.lower() or "summarize" in question.lower():
        docs = retriever.invoke("main topics of the document")
    else:
        docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an intelligent Research Assistant.

Answer ONLY from the context below.

Return ONLY the answer.
Do NOT return JSON.
Do NOT return Python objects.
Do NOT return metadata.
Do NOT return signatures.
Do NOT return extras.

If the answer is not available say:

"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    st.write("TYPE OF RESPONSE:", type(response))
    st.write("RESPONSE OBJECT:")
    st.write(response)

    st.stop()

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        final_answer = ""

        for item in content:

            if isinstance(item, dict):
                final_answer += item.get("text", "")

            elif hasattr(item, "text"):
                final_answer += item.text

            else:
                final_answer += str(item)

        return final_answer.strip()

    return str(content)