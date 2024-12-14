from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..crud.borrow import get_all_borrows, get_borrow, finished_borrow, create_borrow
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemes import BorrowScheme, BorrowUpdateScheme
from datetime import date

borrow_router = APIRouter()


@borrow_router.post(
    "/",
    response_model=BorrowScheme,
    responses={
        404: {"description": "Книга с указанным айди не найдена."},
        400: {"description": "Нет доступных экземпляров книги с указанным айди."},
        422: {"description": "Дата возврата не может быть раньше даты взятия книги."},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
async def api_create_borrow(
    book_id: int,
    reader_name: str,
    borrow_date: date,
    db: Annotated[AsyncSession, Depends(get_db)],
    return_date: Optional[date] = None,
):
    borrow = await create_borrow(
        book_id=book_id,
        reader_name=reader_name,
        borrow_date=borrow_date,
        return_date=return_date,
        db=db,
    )

    if borrow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга с указанным айди не найдена.",
        )
    elif borrow is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет доступных экземпляров книги с указанным айди.",
        )
    elif borrow == "Invalid return_date":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Дата возврата не может быть раньше даты взятия книги.",
        )

    return borrow


@borrow_router.get(
    "/",
    response_model=list[BorrowScheme],
    responses={
        404: {"description": "Записи о выдаче книг не найдены."},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
async def api_get_all_borrows(db: Annotated[AsyncSession, Depends(get_db)]):
    borrows = await get_all_borrows(db)
    if not borrows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Записи о выдаче книг не найдены.",
        )
    return borrows


@borrow_router.get(
    "/{id}",
    response_model=BorrowScheme,
    responses={
        404: {"description": "Запись о выдаче по указанному айди не найдена."},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
async def api_get_borrow(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    borrow = await get_borrow(id=id, db=db)
    if not borrow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о выдаче по указанному айди не найдена.",
        )

    return borrow


@borrow_router.patch(
    "/{id}/response",
    response_model=BorrowUpdateScheme,
    responses={
        404: {"description": "Запись о выдаче по указанному айди не найдена."},
        400: {"description": "Книга уже сдана."},
        422: {"description": "Дата возврата не может быть раньше даты взятия книги."},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
async def api_finished_borrow(
    id: int, return_date: date, db: Annotated[AsyncSession, Depends(get_db)]
):
    borrow = await finished_borrow(id=id, return_date=return_date, db=db)
    if borrow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о выдаче по указанному айди не найдена.",
        )
    elif borrow is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Книга уже сдана."
        )
    elif borrow == "Invalid return_date":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Дата возврата не может быть раньше даты взятия книги.",
        )

    return borrow
