from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, func, text
from typing import Optional
from ..models import Borrow, Book
from datetime import date
from ..schemes import BorrowScheme
from sqlalchemy.future import select
import logging

logging.basicConfig(level=logging.INFO)


async def create_borrow(book_id: int, reader_name: str, borrow_date: date, db: AsyncSession, return_date: Optional[date] = None) -> Optional[BorrowScheme]:
    try:
        book = await db.execute(select(Book).filter(Book.id == book_id))
        book = book.scalars().first()
        logging.info("Данные о книге", book)

        if not book:
            return None
        
        if book.available_copies == 0:
            return False
        
        book.available_copies -= 1
        
        await db.commit()
        await db.refresh(book)

        result = await db.execute(select(func.count()).select_from(Borrow))
        count = result.scalar()

        if count == 0:
            await db.execute(text("SELECT setval(pg_get_serial_sequence('borrow', 'id'), 1, false);"))
            await db.commit()

        new_borrow = Borrow(book_id=book_id, reader_name=reader_name, borrow_date=borrow_date, return_date=return_date)
        db.add(new_borrow)
        await db.commit()
        await db.refresh(new_borrow)
        return BorrowScheme(
            id=new_borrow.id, 
            book_id=new_borrow.book_id,
            reader_name=new_borrow.reader_name, 
            borrow_date=new_borrow.borrow_date, 
            return_date=new_borrow.return_date,
        )
    except Exception:
        await db.rollback()
        raise
    
async def get_all_borrows(db: AsyncSession) -> list[BorrowScheme]:
    try: 
        result = await db.execute(select(Borrow).order_by(asc(Borrow.id)))
        borrows = result.scalars().all()
        if not borrows:
            return None
        return borrows
    except Exception:
        raise

async def get_borrow(id: int, db: AsyncSession) -> BorrowScheme:
    try:
        result = await db.execute(select(Borrow).filter(Borrow.id == id))
        borrow = result.scalars().first()
        if not borrow:
            return None
        
        return BorrowScheme(
            id=borrow.id, 
            book_id=borrow.book_id,
            reader_name=borrow.reader_name, 
            borrow_date=borrow.borrow_date, 
            return_date=borrow.return_date,
        )
    except Exception:
        raise

async def finished_borrow(id: int, return_date: date, db: AsyncSession) -> BorrowScheme:
    try:
        result = await db.execute(select(Borrow).filter(Borrow.id == id))
        current_borrow = result.scalars().first()

        if not current_borrow:
            return None
        
        current_borrow.return_date = return_date
        current_borrow.book.available_copies += 1
        
        await db.commit()
        await db.refresh(current_borrow)
        return BorrowScheme(
            id=current_borrow.id, 
            book_id=current_borrow.book_id,
            reader_name=current_borrow.reader_name, 
            borrow_date=current_borrow.borrow_date, 
            return_date=current_borrow.return_date,
        )

    except Exception:
        await db.rollback()
        raise

