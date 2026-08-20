from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from app.polling import fetch_supplier_inventory
from app.inventory import inventory_ledger, processed_events


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
            for product in inventory_ledger.values()
        ]

    @strawberry.field
    def product(self, sku: str) -> Product | None:
        product = inventory_ledger.get(sku)

        if product:
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

    event_id = data.get("event_id")

    # Check if this event was already processed
    if event_id in processed_events:
        return {
            "message": "Duplicate event ignored"
        }

    sku = data.get("sku")
    new_status = data.get("status")
    new_quantity = data.get("quantity")

    # Find the product in the central inventory ledger
    product = inventory_ledger.get(sku)

    if product:
        # Update the shared inventory ledger
        product["status"] = new_status
        product["quantity"] = new_quantity

        # Remember the processed event
        processed_events.add(event_id)

        return {
            "message": "Inventory updated successfully",
            "sku": sku,
            "status": new_status,
            "quantity": new_quantity
        }

    return {
        "message": "Product not found",
        "sku": sku
    }