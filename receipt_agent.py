from receipt_parser import extract_receipt
from agent import ask_agent


def ask_about_receipt(pdf_path, question):

    # Extract information from receipt
    receipt = extract_receipt(pdf_path)

    order_id = receipt["order_id"]
    product = receipt["product"]
    purchase_date = receipt["purchase_date"]

    # Make sure the receipt contains the required information
    if not order_id:
        return "I could not find an Order ID in the receipt."

    # Give the agent the receipt information
    agent_question = f"""
The user uploaded a receipt.

Receipt information:
Order ID: {order_id}
Product: {product}
Purchase Date: {purchase_date}

User's question:
{question}

Use the Order ID to look up the order and use the
available tools to answer the user's question.
"""

    response = ask_agent(agent_question)

    return response.content
    