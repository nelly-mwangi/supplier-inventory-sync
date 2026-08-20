import json
from pathlib import Path


def fetch_supplier_inventory():
    data_file = Path(__file__).parent.parent / "data" / "supplier_inventory.json"

    with open(data_file, "r") as file:
        inventory = json.load(file)

    return inventory