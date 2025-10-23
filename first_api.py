import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 1, "name_book": "Programm by C", "author": "Сергей Черников"},
    {"id": 2, "name_book": "Programm using OOP", "author": "Никита Новожен"},
]


class Book(BaseModel):
    id: int | None
    name: str
    author: str


@app.get("/books", tags=["Books"])
def read_books():
    return books


@app.get("/books/{book_id}", tags=["Books"])
def read_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book


@app.put("/books", tags=["Books"])
def update_book(new_book: Book):
    if new_book.id is not None:
        for index, book in enumerate(books):
            if book["id"] == new_book.id:
                books[index] = {
                    "id": new_book.id,
                    "name_book": new_book.name,
                    "author": new_book.author,
                }

                return {
                    "succsess": True,
                    "mesenge": f"Update book-id: {new_book.id} complited!",
                }

    if new_book.id is None:
        new_book.id = int(len(books) + 1)

    books.append(new_book)
    return {
        "succsess": True,
        "mesenge": f"Append book-id: {new_book.id} complited!",
    }


@app.post("/books", tags=["Books"])
def create_book(new_book: Book):
    new_book.id = len(books) + 1
    books.append(new_book)
    return {
        "succsess": True,
        "mesenge": f"Append book-id: {new_book.id} complited!",
    }


@app.patch("/books/{book_id}", tags=["Books"])
def patch_book(
    book_id: int,
    name_book: str | None = Query(default=None),
    author_book: str | None = Query(default=None),
):
    if name_book == None and author_book == None:
        return {
            "succsess": False,
            "mesenge": f"Not data transmitted for edit book-id: {book_id}!",
        }
    for index, book in enumerate(books):
        if book["id"] == book_id:
            if name_book is not None:
                books[index]["name_book"] = name_book
            if author_book is not None:
                books[index]["author"] = author_book
    return {"succsess": True, "mesenge": f"Edit book-id: {book_id} complited!"}


@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            del books[index]
            return {
                "succsess": True,
                "mesenge": f"Comlited delete book-id: {book_id}",
            }
    return {"succsess": False, "mesenge": f"Not found book-id: {book_id}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
