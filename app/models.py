from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

# customer tables with respective info
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    country = Column(String)
    status = Column(String)
    orders = relationship("Order", back_populates="customer") #linking orders made by customer

# order table that has info of purchases for each customer
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    customer = relationship("Customer", back_populates="orders") # linking back to customer