from database import engine
from models import Book,Member,Borrow
from database import Base

Base.metadata.create_all(bind=engine)

print("All Tables are created")