from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, func, text
from ..models import Book, Author
from sqlalchemy.future import select


async def create_book(
    title: str,
    description: str,
    author_id: int,
    available_copies: int,
    db: AsyncSession,
) -> Book:
    try:

        author = await db.execute(select(Author).filter(Author.id == author_id))
        author = author.scalars().first()

        if not author:
            return None

        result = await db.execute(select(func.count()).select_from(Book))
        count = result.scalar()

        if count == 0:
            await db.execute(
                text("SELECT setval(pg_get_serial_sequence('book', 'id'), 1, false);")
            )

        new_book = Book(
            title=title,
            description=description,
            author_id=author_id,
            available_copies=available_copies,
        )
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)

        return new_book
    except Exception:
        await db.rollback()
        raise


async def get_all_books(db: AsyncSession) -> list[Book]:
    try:
        result = await db.execute(select(Book).order_by(asc(Book.id)))
        books = result.scalars().all()
        if not books:
            return None

        return books
    except Exception:
        raise


async def get_book(id: int, db: AsyncSession) -> Book:
    try:
        result = await db.execute(select(Book).filter(Book.id == id))
        book = result.scalars().first()
        if not book:
            return None
        return book
    except Exception:
        raise


async def update_book(
    id: int,
    title: str,
    description: str,
    author_id: int,
    available_copies: int,
    db: AsyncSession,
) -> Book:
    try:
        result = await db.execute(select(Book).filter(Book.id == id))
        current_book = result.scalars().first()

        if not current_book:
            return None

        current_book.title = title
        current_book.description = description
        current_book.author_id = author_id
        current_book.available_copies = available_copies
        await db.commit()
        await db.refresh(current_book)

        
        return current_book

    except Exception:
        await db.rollback()
        raise


async def delete_book(id: int, db: AsyncSession) -> bool:
    try:
        result = await db.execute(select(Book).filter(Book.id == id))
        current_book = result.scalars().first()
        if not current_book:
            return False
        
        await db.delete(current_book)
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise
