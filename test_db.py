from database import engine

try:
    connection = engine.connect()
    print("✅ SUCCESS! Database connected!")
    connection.close()
except Exception as e:
    print(f"❌ ERROR: {e}")