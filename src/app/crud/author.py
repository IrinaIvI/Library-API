from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, func, text
from ..models import Author
from datetime import date
from sqlalchemy.future import select


async def create_author(
    name: str, surname: str, date_of_birth: date, db: AsyncSession
) -> Author:
    try:

        result = await db.execute(select(func.count()).select_from(Author))
        count = result.scalar()

        if count == 0:
            await db.execute(
                text("SELECT setval(pg_get_serial_sequence('author', 'id'), 1, false);")
            )

        new_author = Author(name=name, surname=surname, date_of_birth=date_of_birth)
        db.add(new_author)
        await db.commit()
        await db.refresh(new_author)

        return new_author
    
    except Exception:
        await db.rollback()
        raise


async def get_all_authors(db: AsyncSession) -> list[Author]:
    try:
        result = await db.execute(select(Author).order_by(asc(Author.id)))
        authors = result.scalars().all()
        if not authors:
            return None

        return authors
    except Exception:
        raise


async def get_author(id: int, db: AsyncSession) -> Author:
    try:
        result = await db.execute(select(Author).filter(Author.id == id))
        author = result.scalars().first()
        if not author:
            return None
        
        return author

    except Exception:
        raise


async def update_author(
    id: int, name: str, surname: str, date_of_birth: date, db: AsyncSession
) -> Author:
    try:
        result = await db.execute(select(Author).filter(Author.id == id))
        current_author = result.scalars().first()

        if not current_author:
            return None

        current_author.name = name
        current_author.surname = surname
        current_author.date_of_birth = date_of_birth
        await db.commit()
        await db.refresh(current_author)

        return current_author

    except Exception:
        await db.rollback()
        raise


async def delete_author(id: int, db: AsyncSession) -> bool:
    try:
        result = await db.execute(select(Author).filter(Author.id == id))
        current_author = result.scalars().first()
        if not current_author:
            return False

        await db.delete(current_author)
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise
