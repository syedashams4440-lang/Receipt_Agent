from rag import create_retriever
from datetime import datetime, timedelta
from langchain.tools import tool

from database import find_order


@tool
def lookup_order(order_id: str) -> str:
    """
    Look up an order using its order ID.
    Use this when the user provides an order ID.
    """

    order = find_order(order_id)

    if not order:
        return f"Order {order_id} was not found in the database."

    return (
        f"Order ID: {order['order_id']}\n"
        f"Product: {order['product']}\n"
        f"Category: {order['category']}\n"
        f"Purchase date: {order['purchase_date']}\n"
        f"Price: ₹{order['price']}\n"
        f"Customer: {order['customer']}\n"
        f"Final sale: {'Yes' if order['final_sale'] else 'No'}\n"
    )


@tool
def calculate_return_deadline(purchase_date: str) -> str:
    """
    Calculate the return deadline.
    Return period is 30 days from purchase.
    """

    purchase = datetime.strptime(
        purchase_date,
        "%Y-%m-%d"
    )

    deadline = purchase + timedelta(days=30)

    today = datetime.now()

    days_remaining = (deadline - today).days

    result = (
        f"Return deadline: {deadline.strftime('%Y-%m-%d')}\n"
        f"Approximate days remaining: {days_remaining}"
    )

    if 0 <= days_remaining < 7:
        result += "\nWARNING: Less than 7 days remain for the return."

    elif days_remaining < 0:
        result += "\nThe return deadline has already passed."

    return result


@tool
def calculate_warranty_deadline(purchase_date: str) -> str:
    """
    Calculate the warranty deadline.
    Warranty period is 365 days from purchase.
    """

    purchase = datetime.strptime(
        purchase_date,
        "%Y-%m-%d"
    )

    deadline = purchase + timedelta(days=365)

    today = datetime.now().date()

    days_remaining = (deadline.date() - today).days

    result = (
        f"Warranty deadline: {deadline.strftime('%Y-%m-%d')}\n"
        f"Approximate days remaining: {days_remaining}"
    )

    if days_remaining < 0:
        result += "\nThe warranty has expired."

    return result

@tool
def policy_search(question: str) -> str:
    """
    Search the store's return and warranty policies.

    Use this tool when the user asks about:
    - return eligibility
    - return rules
    - warranty coverage
    - warranty rules
    - final sale products
    - conditions for returns or warranty
    """

    retriever = create_retriever()

    documents = retriever.invoke(question)

    if not documents:
        return "No relevant policy information was found."

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context
