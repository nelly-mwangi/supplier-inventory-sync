from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from app.polling import fetch_supplier_inventory

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