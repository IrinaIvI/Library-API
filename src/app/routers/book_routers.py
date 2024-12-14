from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..database import get_db
from ..crud.book import get_all_books, get_book, create_book, delete_book, update_book
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemes import BookScheme

book_router = APIRouter()

@book_router.post("/", response_model=BookScheme)
async def api_create_book(title: str, description: str, author_id: int, available_copies: int, db: Annotated[AsyncSession, Depends(get_db)]):
   try:
       book = await create_book(title=title, description=description, author_id=author_id, available_copies=available_copies, db=db)

       if not book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Автор с указанным айди {author_id} не найден."
            )
       return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=book
        )
   except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")

@book_router.get("/", response_model=list[BookScheme])
async def api_get_all_books(db: Annotated[AsyncSession, Depends(get_db)]):
    try: 
        books = await get_all_books(db)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книги не найдены")
        return books
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
@book_router.get("/{id}", response_model=BookScheme)
async def api_get_book(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        book = await get_book(id, db)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга по указанному айди не найдена")
        return book
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
@book_router.put("/{id}", response_model=BookScheme)
async def api_update_book(id: int, title: str, description: str, author_id: int, available_copies: int, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        current_book = await update_book(id=id, title=title, description=description, author_id=author_id, available_copies=available_copies, db=db)

        if not current_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга по указанному айди не найдена")
        
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=current_book,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
@book_router.delete("/{id}")
async def api_delete_book(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        deleted_book = await delete_book(id=id, db=db)
        if not deleted_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга по указанному айди не найдена")
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content="Книга успешно удалена")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")