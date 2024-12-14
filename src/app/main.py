from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from .routers.author_routers import author_router
from .routers.book_routers import book_router
from .routers.borrow_routers import borrow_router

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка сервера"}
    )

app.include_router(author_router, prefix="/api_library/authors", tags=["authors"])
app.include_router(book_router, prefix="/api_library/books", tags=["books"])
app.include_router(borrow_router, prefix="/api_library/borrows", tags=["borrows"])