# 📚 Library Management API

A production-grade REST API for managing books, members, and borrowing operations in a library system. Built with FastAPI, PostgreSQL, JWT Authentication, and comprehensive testing.

## 🚀 Tech Stack

- **Backend:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose + bcrypt)
- **Validation:** Pydantic
- **Testing:** pytest + httpx
- **Server:** Uvicorn

## ✨ Features

- 14 RESTful API endpoints
- JWT-based authentication with bcrypt password hashing
- Role-Based Access Control (RBAC) — Admin/User roles
- Background tasks for audit logging
- Custom exception handlers with structured error responses
- PostgreSQL database integration with SQLAlchemy ORM
- Comprehensive pytest test suite
- Pydantic data validation with EmailStr
- Auto-generated API documentation (Swagger UI)

## 🔐 Authentication

- `POST /auth/signup` — Register new user
- `POST /auth/login` — Login and receive JWT token (OAuth2 password flow)

**Protected endpoints** require `Authorization: Bearer <token>` header.

**Admin-only endpoints** (POST/PUT/DELETE on books) require admin role.

## 📋 API Endpoints

### Books (`/books`)
- `POST /books/` — 🔒 Admin: Add new book
- `GET /books/` — 🔓 Public: Get all books (filters: category, available_only)
- `GET /books/{id}` — 🔓 Public: Get specific book
- `PUT /books/{id}` — 🔒 Admin: Update book
- `DELETE /books/{id}` — 🔒 Admin: Delete book

### Members (`/members`)
- All endpoints 🔒 Protected (privacy reasons)

### Borrows (`/borrows`)
- All endpoints 🔒 Protected

## 🛠️ Installation

```bash
# Clone repo
git clone https://github.com/RaiSaeed8182/library_project.git
cd library_project

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL
# Create database 'library_db' with role column in user table

# Run server
uvicorn main:app --reload
```

API: `http://127.0.0.1:8000`
Docs: `http://127.0.0.1:8000/docs`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
```

**Test suite:**
- Root endpoint check
- Authentication (wrong password)
- Protected route (no token = 401)
- Custom exception (404 with structured response)

## 🗂️ Project Structure