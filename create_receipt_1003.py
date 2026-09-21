from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

os.makedirs("data/receipts", exist_ok=True)

pdf_path = "data/receipts/receipt_1003.pdf"

c = canvas.Canvas(pdf_path, pagesize=A4)

c.setFont("Helvetica-Bold", 18)
c.drawString(200, 800, "STORE RECEIPT")

c.setFont("Helvetica", 12)
c.drawString(100, 750, "Order ID: ORD1003")
c.drawString(100, 720, "Product: Smart Watch")
c.drawString(100, 690, "Category: Electronics")
c.drawString(100, 660, "Purchase Date: 2026-07-10")
c.drawString(100, 630, "Price: 6999")
c.drawString(100, 600, "Customer: Arjun")

c.save()

print(f"Receipt created: {pdf_path}")
