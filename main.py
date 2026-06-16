from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware     # ← NEW
from routes import books, members, borrows, auth
from exceptions import BookNotFoundException


app = FastAPI(title="Library Management API")


# NEW: CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Existing: Global Exception Handler
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


# Routers
app.include_router(books.route)
app.include_router(members.route)
app.include_router(borrows.route)
app.include_router(auth.route)


@app.get("/")
async def root():
    return {"message": "Welcome to Library Management API"}