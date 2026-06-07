from database import engine, Base
from models import User    # Import User specifically


# Magic line - User table create karega
Base.metadata.create_all(bind=engine)

print("✅ User table created successfully!")