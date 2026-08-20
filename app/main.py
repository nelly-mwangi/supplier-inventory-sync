from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from app.polling import fetch_supplier_inventory

# Track webhook events that have already been processed
processed_events = set()

# Product data
products = [
    {
        "sku": "SKU001",
        "name": "Wireless Mouse",
        "quantity": 25,
        "status": "in_stock"
    },
    {
        "sku": "SKU002",
        "name": "Laptop Stand",
        "quantity": 5,
        "status": "in_stock"
    },
    {
        "sku": "SKU003",
        "name": "Keyboard",
        "quantity": 0,
        "status": "out_of_stock"
    }
]


# GraphQL Product type
@strawberry.type
class Product:
    sku: str
    name: str
    quantity: int
    status: str


# GraphQL Query
@strawberry.type
class Query:

    @strawberry.field
    def products(self) -> list[Product]:
        return [
            Product(
                sku=product["sku"],
                name=product["name"],
                quantity=product["quantity"],
                status=product["status"]
            )
            for product in products
        ]

    @strawberry.field
    def product(self, sku: str) -> Product | None:
        for product in products:
            if product["sku"] == sku:
                return Product(
                    sku=product["sku"],
                    name=product["name"],
                    quantity=product["quantity"],
                    status=product["status"]
                )

        return None


# Create GraphQL schema
schema = strawberry.Schema(query=Query)


# Create GraphQL router
graphql_app = GraphQLRouter(schema)


# Create FastAPI application
app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def home():
    return {
        "message": "Supplier Inventory GraphQL API is running"
    }
@app.get("/poll")
def poll_supplier():
    inventory = fetch_supplier_inventory()

    return {
        "message": "Supplier inventory fetched successfully",
        "inventory": inventory
    }
# Webhook endpoint for supplier inventory updates
@app.post("/webhook/inventory")
async def inventory_webhook(data: dict):

    # Get the unique event ID
    event_id = data.get("event_id")

    # Check if this event was already processed
    if event_id in processed_events:
        return {
            "message": "Duplicate event ignored"
        }

    sku = data.get("sku")
    name = data.get("name")
    quantity = data.get("quantity")
    status = data.get("status")

    # Find the product in the current inventory
    for product in products:
        if product["sku"] == sku:
            product["name"] = name
            product["quantity"] = quantity
            product["status"] = status

            # Remember that this event has been processed
            processed_events.add(event_id)

            return {
                "message": "Inventory updated successfully",
                "sku": sku,
                "status": status
            }

    return {
        "message": "Product not found",
        "sku": sku
    }