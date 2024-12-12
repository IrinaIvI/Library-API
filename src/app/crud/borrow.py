from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, func, text
from ..models import Borrow
from datetime import date
from ..schemes import BorrowScheme
from sqlalchemy.future import select


async def create_borrow(book_id: int, reader_name: str, borrow_date: date, return_date: int, db: AsyncSession) -> BorrowScheme:
    try:

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
    
async def update_borrow(id: int, book_id: int, reader_name: str, borrow_date: date, return_date: int, db: AsyncSession) -> BorrowScheme:
    try:
        result = await db.execute(select(Borrow).filter(Borrow.id == id))
        current_borrow = result.scalars().first()

        if not current_borrow:
            return None

        current_borrow.book_id = book_id
        current_borrow.reader_name = reader_name
        current_borrow.borrow_date = borrow_date
        current_borrow.return_date = return_date
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

async def delete_borrow(id: int, db: AsyncSession) -> bool:
    try:
        result = await db.execute(select(Borrow).filter(Borrow.id == id))
        current_borrow = result.scalars().first()
        if not current_borrow:
            return False
        
        await db.delete(current_borrow)
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise

