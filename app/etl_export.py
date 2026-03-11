import csv
from app.db import SessionLocal
from app.models import Customer
from datetime import datetime
import os

os.makedirs("output", exist_ok=True)
date_str = datetime.now().strftime("%Y-%m-%d")
OUTPUT_FILE = f"output/Active_Customer_Orders_{date_str}.csv" # output file name + date when generated

#gets only customers that are active
def export_active_customers():
    session = SessionLocal()
    customers = (session.query(Customer).filter(Customer.status == "active").all())
    export_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = []

    for customer in customers:
        full_name = f"{customer.first_name} {customer.last_name}"

        for order in customer.orders:
            rows.append({
                "export_date": export_date,
                "customer_id": customer.id,
                "name": full_name,
                "email": customer.email,
                "phone_number": customer.phone_number,
                "country": customer.country,
                "order_id": order.id,
                "product": order.product,
                "quantity": order.quantity,
                "unit_price": order.unit_price,
                "total_value": order.quantity * order.unit_price

            })
    session.close()
    #creates the output csv file
    with open(OUTPUT_FILE, "w", newline = "") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exporting completed: {OUTPUT_FILE}")

if __name__ == "__main__":

    export_active_customers()
