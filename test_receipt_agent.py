from receipt_agent import ask_about_receipt


pdf_path = "data/receipts/receipt_1004.pdf"

question = input("\nAsk about your receipt: ")

answer = ask_about_receipt(
    pdf_path,
    question
)

print("\n===== FINAL ANSWER =====\n")
print(answer)
