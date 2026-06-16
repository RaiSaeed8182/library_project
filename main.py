from fastapi import FastAPI, Request
from routes import books, members, borrows, auth
from exceptions import BookNotFoundException
from fastapi.responses import JSONResponse


app = FastAPI(title="Library Management API")
# Global Exception Handler — BookNotFoundException
@app.exception_handler(BookNotFoundException)
async def book_not_found_handler(request: Request, exc: BookNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Book Not Found",
            "detail": exc.message,
            "book_id": exc.book_id,
            "suggestion": "Check GET /books/ for available book IDs",
            "path": str(request.url)
        }
    )


# Connect all routers
app.include_router(books.route)
app.include_router(members.route)
app.include_router(borrows.route)
app.include_router(auth.route)  


@app.get("/")
async def root():
    return {"message": "Welcome to Library Management API"}