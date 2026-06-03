# 📚 Library Management API

A production-grade REST API for managing books, members, and borrowing operations in a library system. Built with FastAPI and PostgreSQL.

## 🚀 Tech Stack

- **Backend:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Server:** Uvicorn

## ✨ Features

- 14 RESTful API endpoints
- PostgreSQL database integration with SQLAlchemy ORM
- Pydantic data validation
- Business logic for borrowing/returning books
- Atomic transactions for data consistency
- Cross-resource queries (books ↔ members ↔ borrows)
- Auto-generated API documentation (Swagger UI)

## 📋 API Endpoints

### Books (`/books`)
- `POST /books/` — Add new book
- `GET /books/` — Get all books (filters: category, available_only)
- `GET /books/{id}` — Get specific book
- `PUT /books/{id}` — Update book
- `DELETE /books/{id}` — Delete book

### Members (`/members`)
- `POST /members/` — Register new member
- `GET /members/` — Get all members
- `GET /members/{id}` — Get specific member
- `PUT /members/{id}` — Update member
- `DELETE /members/{id}` — Delete member

### Borrows (`/borrows`)
- `POST /borrows/` — Borrow a book
- `GET /borrows/` — Get all borrows (filters: member_id, status)
- `GET /borrows/{id}` — Get specific borrow
- `PUT /borrows/{id}/return` — Return a book

## 🛠️ Installation

```bash
# Clone repo
git clone https://github.com/RaiSaeed8182/library_project.git
cd library_project

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL
# Create database named 'library_db' in PostgreSQL
# Update DATABASE_URL in database.py with your credentials

# Run server
uvicorn main:app --reload
```

API will run at `http://127.0.0.1:8000`

Documentation: `http://127.0.0.1:8000/docs`

## 🗂️ Project Structure