from fastapi.testclient import TestClient
from main import app 
# Test client setup 
client = TestClient(app)
#FastAPI app ko in-memory test karne ke liye client banata (no real server needed)
def test_root_endpoint(): 
    """ Test: Root endpoints should return welcome message"""
    # Action :  Get request to root 
    response = client.get("/")
    # Assertions Verify Responce 
    assert response.status_code==200
    assert response.json()=={"message": "Welcome to Library Management API"}

def test_login_with_wrong_password(): 
    """Test : Wrong password should return 401"""
    response = client.post(
        "/auth/login",
        data={
             "username": "saeed@library.com",
             "password": "wrong_password"
        }
    )

    assert response.status_code == 401

def test_protected_endpoints_without_token(): 
   response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Test",
            "category": "Test",
            "total_copies": 1,
            "available_copies": 1
        }
    )

   assert response.status_code == 401

def test_get_nonexistent_book():
    """Test: Non-existent book should return 404 with custom error"""
    
    response = client.get("/books/99999")
    
    assert response.status_code == 404
    # Verify custom error structure
    data = response.json()
    assert "error" in data
    assert "book_id" in data
    assert data["book_id"] == 99999