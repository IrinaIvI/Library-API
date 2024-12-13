from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..database import get_db
from ..crud.borrow import get_all_borrows, get_borrow, finished_borrow, create_borrow
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemes import BorrowScheme
from datetime import date

borrow_router = APIRouter()

@borrow_router.post("/", response_model=BorrowScheme)
async def api_create_borrow(book_id: int, reader_name: str, borrow_date: date, db: Annotated[AsyncSession, Depends(get_db)], return_date: Optional[date] = None):
   try:
       borrow = await create_borrow(book_id=book_id, reader_name=reader_name, borrow_date=borrow_date, return_date=return_date, db=db)

       if borrow is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Книга с указанным айди {book_id} не найдена."
            )
       elif borrow == False:
           raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Нет доступных экземпляров книги с указанным айди {book_id}."
            )
       
       return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Новая запись о выдаче успешно создана!",
                "borrow": {
                    "id": borrow.id,
                    "title": borrow.title,
                    "desctiption": borrow.description,
                    "author": borrow.author_id,
                    "available_copies": borrow.available_copies,
                }
            }
        )
   except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")

@borrow_router.get("/", response_model=list[BorrowScheme])
async def api_get_all_borrows(db: Annotated[AsyncSession, Depends(get_db)]):
    try: 
        borrows = await get_all_borrows(db)
        if not borrows:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Записи о выдаче книг не найдены")
        return borrows
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
@borrow_router.get("/{id}")
async def api_get_borrow(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        borrow = await get_borrow(id=id, db=db)
        if not borrow:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись о выдаче по указанному айди не найдена")
        return borrow
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
@borrow_router.patch("/{id}/return")
async def api_finished_borrow(id: int, return_date: date, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        borrow = await finished_borrow(id=id, return_date=return_date, db=db)
        if not borrow:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись о выдаче книги по указанному айди не найдена")
        return borrow
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    