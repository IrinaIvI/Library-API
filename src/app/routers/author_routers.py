from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..crud.author import get_all_authors, get_author, update_author, delete_author, create_author
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemes import AuthorScheme
from datetime import date

author_router = APIRouter()

@author_router.post("/", response_model=AuthorScheme, responses={
    500: {"description": "Внутренняя ошибка сервера"},
})
async def api_create_author(name: str, surname: str, date_of_birth: date, db: Annotated[AsyncSession, Depends(get_db)]):
    author = await create_author(name=name, surname=surname, date_of_birth=date_of_birth, db=db)
    return author

@author_router.get("/", response_model=list[AuthorScheme], responses={
        404: {"description": "Авторы не найдены."},
        500: {"description": "Внутренняя ошибка сервера."},
    })
async def api_get_all_authors(db: Annotated[AsyncSession, Depends(get_db)]):
    authors = await get_all_authors(db)
    if not authors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Авторы не найдены.")
    return authors
    
@author_router.get("/{id}", response_model=AuthorScheme, responses={
        404: {"description": "Автор по указанному айди не найден."},
        500: {"description": "Внутренняя ошибка сервера."},
})
async def api_get_author(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    author = await get_author(id=id, db=db)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автор по указанному айди не найден.")
    
    return author
    
@author_router.put("/{id}", response_model=AuthorScheme, responses={
        404: {"description": "Автор по указанному айди не найден."},
        500: {"description": "Внутренняя ошибка сервера."},
})
async def api_update_author(id: int, name: str, surname: str, date_of_birth: date, db: Annotated[AsyncSession, Depends(get_db)]):
    current_author = await update_author(id, name, surname, date_of_birth, db)

    if not current_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автор по указанному айди не найден.")
    return current_author
    
@author_router.delete("/{id}", responses={
        404: {"description": "Автор по указанному айди не найден."},
        500: {"description": "Внутренняя ошибка сервера."},
})
async def api_delete_author(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    deleted_author = await delete_author(id=id, db=db)
    if not deleted_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автор по указанному айди не найден.")
    return {"detail": "Автор успешно удален."}