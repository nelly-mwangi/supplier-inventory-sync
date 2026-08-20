# Central inventory ledger

inventory_ledger = {
    "SKU001": {
        "sku": "SKU001",
        "name": "Wireless Mouse",
        "quantity": 25,
        "status": "in_stock"
    },
    "SKU002": {
        "sku": "SKU002",
        "name": "Laptop Stand",
        "quantity": 5,
        "status": "in_stock"
    },
    "SKU003": {
        "sku": "SKU003",
        "name": "Keyboard",
        "quantity": 0,
        "status": "out_of_stock"
    }
}

# Track webhook events that have already been processed
processed_events = set()