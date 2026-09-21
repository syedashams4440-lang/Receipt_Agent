from tools import lookup_order


print("===== EXISTING ORDER =====")

result = lookup_order.invoke({
    "order_id": "ORD1001"
})

print(result)


print("\n===== NON-EXISTING ORDER =====")

result = lookup_order.invoke({
    "order_id": "ORD9999"
})

print(result)

from tools import calculate_return_deadline


print("\n===== RETURN DEADLINE =====")

result = calculate_return_deadline.invoke({
    "purchase_date": "2026-09-01"
})

print(result)

from tools import calculate_warranty_deadline


print("\n===== WARRANTY DEADLINE =====")

result = calculate_warranty_deadline.invoke({
    "purchase_date": "2026-08-15"
})

print(result)