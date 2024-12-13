from sqlalchemy import String, Text, ForeignKey,Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    surname: Mapped[str] = mapped_column(String(20), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id", ondelete='CASCADE'), nullable=False)
    available_copies: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    author: Mapped["Author"] = relationship(back_populates="books")
    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="book")

class Borrow(Base):
    __tablename__ = "borrow"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id", ondelete='CASCADE'), nullable=False)
    reader_name: Mapped[str] = mapped_column(String(20), nullable=False)
    borrow_date: Mapped[date] = mapped_column(nullable=False)
    return_date: Mapped[date] = mapped_column(nullable=True)

    book: Mapped["Book"] = relationship("Book", back_populates="borrows")

