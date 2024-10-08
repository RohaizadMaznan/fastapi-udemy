from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {
        "title": "Book 1",
        "author": "Author 1",
        "genre": "Genre 1",
        "category": "Category 1",
    },
    {
        "title": "Book 2",
        "author": "Author 2",
        "genre": "Genre 2",
        "category": "Category 2",
    },
    {
        "title": "Book 3",
        "author": "Author 3",
        "genre": "Genre 3",
        "category": "Category 3",
    },
    {
        "title": "Book 4",
        "author": "Author 4",
        "genre": "Genre 4",
        "category": "Category 4",
    },
    {
        "title": "Book 5",
        "author": "Author 5",
        "genre": "Genre 5",
        "category": "Category 5",
    },
]


@app.get("/")
async def read_root():
    return {"message": "server is online"}


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}
