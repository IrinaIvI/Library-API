from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..database import get_db
from ..crud.author import get_all_authors, get_author, update_author, delete_author, create_author
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemes import AuthorScheme
from datetime import date

author_router = APIRouter()

@author_router.post("/", response_model=AuthorScheme)
async def api_create_author(name: str, surname: str, date_of_birth: date, db: Annotated[AsyncSession, Depends(get_db)]):
   try:
       author = await create_author(name, surname, date_of_birth, db)
       return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Новый автор успешно создан!",
                "author": {
                    "id": author.id,
                    "name": author.name,
                    "surname": author.surname,
                    "date_of_birth": str(author.date_of_birth)
                }
            }
        )
   except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")

@author_router.get("/", response_model=list[AuthorScheme])
async def api_get_all_authors(db: Annotated[AsyncSession, Depends(get_db)]):
    try: 
        authors = await get_all_authors(db)
        if not authors:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Авторы не найдены")
        return authors
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
@author_router.get("/{id}")
async def api_get_author(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        author = await get_author(id, db)
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автор по указанному айди не найден")
        return author
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
@author_router.put("/{id}", response_model=AuthorScheme)
async def api_update_author(id: int, name: str, surname: str, date_of_birth: date, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        current_author = await update_author(id, name, surname, date_of_birth, db)

        if not current_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автор по указанному айди не найден")
        
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "message": "Информация об авторе обновлена",
                "author": {
                    "id": current_author.id,
                    "name": current_author.name,
                    "surname": current_author.surname,
                    "date_of_birth": str(current_author.date_of_birth)
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")
    
@author_router.delete("/{id}")
async def api_delete_author(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        deleted_author = await delete_author(id, db)
        if not deleted_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автор по указанному айди не найден")
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content="Автор успешно удален")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка сервера: {e}")