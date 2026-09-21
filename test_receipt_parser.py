from receipt_parser import extract_receipt


pdf_path = "data/receipts/receipt_1001.pdf"

receipt = extract_receipt(pdf_path)


print("\n===== EXTRACTED RECEIPT INFORMATION =====")

print("Order ID:", receipt["order_id"])
print("Product:", receipt["product"])
print("Purchase Date:", receipt["purchase_date"])
