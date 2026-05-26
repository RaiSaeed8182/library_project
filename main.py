from fastapi import FastAPI
from routes import books, members, borrows


app = FastAPI(title="Library Management API")


# Connect all routers
app.include_router(books.route)
app.include_router(members.route)
app.include_router(borrows.route)


@app.get("/")
async def root():
    return {"message": "Welcome to Library Management API"}