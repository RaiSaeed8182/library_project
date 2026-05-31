from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Rai%404017@localhost:5432/library_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False , bind=engine)


Base = declarative_base() # it is a foundation to create tables in SQL , ak parent class jis say baki table inhert ho tay hain A

def get_db():
    db=SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
