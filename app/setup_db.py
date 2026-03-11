import csv
from app.db import engine, Base, SessionLocal
from app.models import Customer, Order

CUSTOMERS_FILE = "data/customers.csv"
ORDERS_FILE = "data/orders.csv"

# creates tables only if they don't already exist
def create_tables():
    Base.metadata.create_all(engine)

# takes the customers.csv and inserts info into DB. Skips if the customer already exists.    
def load_customers(session):
    with open(CUSTOMERS_FILE, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            existing = session.get(Customer, int(row["id"]))
            if not existing:
                customer = Customer(
                    id=int(row["id"]),
                    first_name = row["first_name"],
                    last_name = row["last_name"],
                    email = row["email"],
                    phone_number = row["phone_number"],
                    country = row["country"],
                    status = row["status"]
                )
                session.add(customer)

# inserts order info into DB. Skips if the ID already exists.
def load_orders(session):
    with open(ORDERS_FILE, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            existing = session.get(Order, int(row["id"]))
            if not existing:
                order = Order(
                    id = int(row["id"]),
                    customer_id = int(row["customer_id"]),
                    product = row["product"],
                    quantity = int(row["quantity"]),
                    unit_price=float(row["unit_price"])
                )
                session.add(order)

# runs the full setup
def main():
    create_tables()
    session = SessionLocal()

    load_customers(session)
    load_orders(session)

    session.commit()
    session.close()

    print("Database setup completed successfully.")

if __name__ == "__main__":
    main()