from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..crud.book import get_all_books, get_book, create_book, delete_book, update_book
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemes import BookScheme

book_router = APIRouter()


@book_router.post(
    "/",
    response_model=BookScheme,
    responses={
        404: {"description": "Автор с указанным айди не найден."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def api_create_book(
    title: str,
    description: str,
    author_id: int,
    available_copies: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    new_book = await create_book(
        title=title,
        description=description,
        author_id=author_id,
        available_copies=available_copies,
        db=db,
    )

    if not new_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Автор с указанным айди не найден.",
        )
    return BookScheme(
            id=new_book.id,
            title=new_book.title,
            description=new_book.description,
            author_id=new_book.author_id,
            available_copies=new_book.available_copies,
        )


@book_router.get(
    "/",
    response_model=list[BookScheme],
    responses={
        404: {"description": "Книги не найдены."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def api_get_all_books(db: Annotated[AsyncSession, Depends(get_db)]):
    books = await get_all_books(db)
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книги не найдены."
        
        )
    
    books_response = [
        BookScheme(
            id=book.id,
            title=book.title,
            description=book.description,
            author_id=book.author_id,
            available_copies=book.available_copies,
        )
        for book in books
    ]

    return books_response


@book_router.get(
    "/{id}",
    response_model=BookScheme,
    responses={
        404: {"description": "Книга по указанному айди не найдена."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def api_get_book(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    book = await get_book(id, db)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга по указанному айди не найдена.",
        )
    return BookScheme(
            id=book.id,
            title=book.title,
            description=book.description,
            author_id=book.author_id,
            available_copies=book.available_copies,
        )


@book_router.put(
    "/{id}",
    response_model=BookScheme,
    responses={
        404: {"description": "Книга по указанному айди не найдена."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def api_update_book(
    id: int,
    title: str,
    description: str,
    author_id: int,
    available_copies: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    current_book = await update_book(
        id=id,
        title=title,
        description=description,
        author_id=author_id,
        available_copies=available_copies,
        db=db,
    )

    if not current_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга по указанному айди не найдена.",
        )

    return BookScheme(
            id=current_book.id,
            title=current_book.title,
            description=current_book.description,
            author_id=current_book.author_id,
            available_copies=current_book.available_copies,
        )


@book_router.delete(
    "/{id}",
    responses={
        404: {"description": "Книга по указанному айди не найдена."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def api_delete_book(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    deleted_book = await delete_book(id=id, db=db)
    if not deleted_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга по указанному айди не найдена.",
        )
    return {"detail": "Книга успешно удалена."}
