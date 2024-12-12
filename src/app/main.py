from fastapi import FastAPI
from .routers.author_routers import author_router
from .routers.book_routers import book_router

app = FastAPI()
app.include_router(author_router, prefix="/api_library/authors", tags=["authors"])
app.include_router(book_router, prefix="/api_library/books", tags=["books"])
