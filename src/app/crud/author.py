from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, func, text
from ..models import Author
from datetime import date
from ..schemes import AuthorScheme
from sqlalchemy.future import select


async def create_author(name: str, surname: str, date_of_birth: date, db: AsyncSession) -> AuthorScheme:
    try:

        result = await db.execute(select(func.count()).select_from(Author))
        count = result.scalar()

        if count == 0:
            await db.execute(text("SELECT setval(pg_get_serial_sequence('author', 'id'), 1, false);"))
            await db.commit()

        new_author = Author(name=name, surname=surname, date_of_birth=date_of_birth)
        db.add(new_author)
        await db.commit()
        await db.refresh(new_author)

        return AuthorScheme(
            id=new_author.id,
            name=new_author.name,
            surname=new_author.surname,
            date_of_birth=new_author.date_of_birth,
        )
    except Exception:
        await db.rollback()
        raise
    
async def get_all_authors(db: AsyncSession) -> list[AuthorScheme]:
    try: 
        result = await db.execute(select(Author).order_by(asc(Author.id)))
        authors = result.scalars().all()
        if not authors:
            return None
        
        return authors
    except Exception:
        raise

async def get_author(id: int, db: AsyncSession) -> AuthorScheme:
    try:
        result = await db.execute(select(Author).filter(Author.id == id))
        author = result.scalars().first()
        if not author:
            return None
        
        return AuthorScheme(
            id=author.id,
            name=author.name,
            surname=author.surname,
            date_of_birth=author.date_of_birth,
        )
        
    except Exception:
        raise
    
async def update_author(id: int, name: str, surname: str, date_of_birth: date, db: AsyncSession) -> Author:
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

        return AuthorScheme(
            id=current_author.id,
            name=current_author.name,
            surname=current_author.surname,
            date_of_birth=current_author.date_of_birth,
        )
    
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

