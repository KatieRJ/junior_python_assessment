from fastapi import FastAPI, HTTPException
from app.db import SessionLocal
from app.models import Customer
from pydantic import BaseModel
from typing import List

class Order_Response(BaseModel):
    id: int
    product: str
    quantity: int
    unit_price: float

class Customer_Response(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    country: str
    status: str
    orders: List[Order_Response]

app = FastAPI()

# this is the endpoint to get customer info by ID
@app.get("/customers/{customer_id}",
         response_model=Customer_Response,
         summary="Getting a customer information and their orders",
         description="This returns customer details and all orders associated with the customer.")


def get_customer(customer_id: int):
    session = SessionLocal()
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer was not found")
    
    result = {
        "id": customer.id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone_number": customer.phone_number,
        "country": customer.country,
        "status": customer.status,
        "orders": []
    }
    for order in customer.orders:
        result["orders"].append({
            "id": order.id,
            "product": order.product,
            "quantity": order.quantity,
            "unit_price": order.unit_price
        })

    session.close()

    return result