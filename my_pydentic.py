from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Book API with Pydantic")


class BookSchema(BaseModel):
    id: int = Field(default=None, gt=0, description="Book ID")
    name: str = Field(min_length=5, max_length=50, description="Book name")
    author: str = Field(min_length=5, max_length=50, description="Book author")


class ResponseSchema(BaseModel):
    success: bool
    message: str
    data: list


books: List[BookSchema] = [
    BookSchema(id=1, name="Programm by C", author="Sergey Chernikov"),
    BookSchema(id=2, name="Programm using OOP", author="Nikita Novozhen"),
]


@app.get(
    "/books",
    response_model=ResponseSchema,
    tags=["Books"],
    summary="Получить все книги",
)
def read_books() -> ResponseSchema:
    return {
        "success": True,
        "message": f"Found {len(books)} book(s)",
        "data": books,
    }


@app.get(
    "/books/{book_id}",
    response_model=ResponseSchema,
    tags=["Books"],
    summary="Получить кигу по ID",
)
def read_book(book_id: int) -> ResponseSchema:
    for book in books:
        if book.id == book_id:
            return {
                "success": True,
                "message": f"Book with id={book_id} found",
                "data": book,
            }
    raise HTTPException(
        status_code=404, detail=f"Book with id={book_id} not found"
    )


@app.post(
    "/books",
    response_model=ResponseSchema,
    tags=["Books"],
    summary="Создать новую книгу",
)
def create_book(new_book: BookSchema):
    new_book.id = len(books) + 1
    books.append(new_book)
    return {
        "success": True,
        "message": f"Book created successfully (id={new_book.id})",
        "data": new_book,
    }


# нужно поправить логику передачи null
@app.put(
    "/books/{book_id}",
    response_model=ResponseSchema,
    tags=["Books"],
    summary="Заменить уществующую книгу(если ID занят) или создать новую",
)
def update_book(book_id: int, updated: BookSchema):
    for index, book in enumerate(books):
        if book.id == book_id:
            updated.id = book_id
            books[index] = updated
            return {
                "success": True,
                "message": f"Book with id={book_id} updated successfully",
                "data": updated,
            }
    raise HTTPException(
        status_code=404, detail=f"Book with id={book_id} not found"
    )


@app.patch(
    "/books/{book_id}",
    response_model=ResponseSchema,
    tags=["Books"],
    summary="Частично или полность изменить книгу",
)
def patch_book(book_id: int, data: BookSchema):
    for index, book in enumerate(books):
        if book.id == book_id:
            updated_data = book.model_dump()
            incoming_data = data.model_dump(exclude_unset=True)
            updated_data.update(incoming_data)
            books[index] = BookSchema(**updated_data)
            return {
                "success": True,
                "message": f"Book with id={book_id} partially updated",
                "data": books[index],
            }
    raise HTTPException(
        status_code=404, detail=f"Book with id={book_id} not found"
    )


@app.delete(
    "/books/{book_id}",
    response_model=ResponseSchema,
    tags=["Books"],
    summary="Удалить книгу по ID",
)
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted = books.pop(index)
            return {
                "success": True,
                "message": f"Book with id={book_id} deleted successfully",
                "data": deleted,
            }
    raise HTTPException(
        status_code=404, detail=f"Book with id={book_id} not found"
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)