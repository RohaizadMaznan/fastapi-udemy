from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Auto-generated ID", default=None)
    title: str = Field(..., min_length=3)
    author: str = Field(...)
    description: str = Field(..., min_length=1, max_length=100)
    rating: int = Field(..., lt=6, gt=0)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Your book title here",
                "author": "Your author name here",
                "description": "Your book description here",
                "rating": 5,
                "published_date": 2021,
            }
        }
    }


BOOKS = [
    Book(1, "Book 1", "Author 1", "Description 1", 4, 2021),
    Book(2, "Book 2", "Author 2", "Description 2", 3, 2020),
    Book(3, "Book 3", "Author 3", "Description 3", 5, 2019),
    Book(4, "Book 4", "Author 4", "Description 4", 5, 2018),
    Book(5, "Book 5", "Author 5", "Description 5", 1, 2017),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book.__dict__
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(..., gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book.__dict__)
    return books_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book.__dict__)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest = Body(...)):
    new_book = Book(**book.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book has been created successfully"}


def find_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            return {"message": "Book has been updated successfully"}


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Book has been deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")
