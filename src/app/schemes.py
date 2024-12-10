from pydantic import BaseModel
from datetime import date
from typing import Optional
class Author(BaseModel):
    id: int
    name: str
    surname: str
    date_of_birth: Optional[date]

class Book(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author_id: int
    available_copies: int

class Borrow(BaseModel):
    id: int
    book_id: int
    reader_name: str
    borrow_date: date
    return_date: Optional[date]
