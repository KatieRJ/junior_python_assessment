from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///customer_orders.db"  #connection to the sqlite database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)  #session object for running queries
Base = declarative_base()