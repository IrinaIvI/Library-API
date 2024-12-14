from pydantic import BaseModel
from datetime import date
from typing import Optional
class AuthorScheme(BaseModel):
    id: int
    name: str
    surname: str
    date_of_birth: Optional[date]

class BookScheme(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author_id: int
    available_copies: int

class BorrowScheme(BaseModel):
    id: int
    book_id: int
    reader_name: str
    borrow_date: date
    return_date: Optional[date]
    is_return: bool


class BorrowUpdateScheme(BaseModel):
    id: int
    return_date: date