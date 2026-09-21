import re
from langchain_community.document_loaders import PyPDFLoader


def extract_receipt(pdf_path):

    # Load the PDF
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    # Combine all pages
    text = "\n".join(
        document.page_content
        for document in documents
    )

    print("\n===== RECEIPT TEXT =====")
    print(text)

    # Extract Order ID
    order_match = re.search(
        r"Order\s*ID\s*[:#]?\s*(ORD\d+)",
        text,
        re.IGNORECASE
    )

    # Extract purchase date
    date_match = re.search(
        r"(?:Purchase\s*Date|Date)\s*[:#]?\s*(\d{4}-\d{2}-\d{2})",
        text,
        re.IGNORECASE
    )

    # Extract product
    product_match = re.search(
        r"(?:Product|Item)\s*[:#]?\s*(.+)",
        text,
        re.IGNORECASE
    )

    order_id = (
        order_match.group(1)
        if order_match
        else None
    )

    purchase_date = (
        date_match.group(1)
        if date_match
        else None
    )

    product = (
        product_match.group(1).strip()
        if product_match
        else None
    )

    return {
        "order_id": order_id,
        "product": product,
        "purchase_date": purchase_date,
        "raw_text": text
    }