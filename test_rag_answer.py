from llm_config import llm
from rag import create_retriever


retriever = create_retriever()


def answer_question(question):

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are a store policy assistant.

Answer the user's question using ONLY the policy information
provided below.

If the answer is not present in the policy, say that the
policy does not provide that information.

POLICY INFORMATION:
{context}

USER QUESTION:
{question}

Give a clear and concise answer.
"""

    response = llm.invoke(prompt)

    return response.content


question = input("\nAsk a policy question: ")

answer = answer_question(question)

print("\n===== ANSWER =====\n")
print(answer)
