ORDERS = {
    "ORD1001": {
        "order_id": "ORD1001",
        "product": "Leather Jacket",
        "category": "Clothing",
        "purchase_date": "2026-09-01",
        "price": 4999,
        "customer": "Rahul",
        "final_sale": False
    },

    "ORD1002": {
        "order_id": "ORD1002",
        "product": "Wireless Headphones",
        "category": "Electronics",
        "purchase_date": "2026-08-15",
        "price": 2999,
        "customer": "Aisha",
        "final_sale": False
    },

    "ORD1003": {
        "order_id": "ORD1003",
        "product": "Smart Watch",
        "category": "Electronics",
        "purchase_date": "2026-07-10",
        "price": 6999,
        "customer": "Arjun",
        "final_sale": False
    },

    "ORD1004": {
        "order_id": "ORD1004",
        "product": "Running Shoes",
        "category": "Clothing",
        "purchase_date": "2026-08-25",
        "price": 3499,
        "customer": "Sameer",
        "final_sale": False
    }
}


def find_order(order_id):
    return ORDERS.get(order_id)