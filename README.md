# Library API

Проект представляет собой REST API для управления библиотечным каталогом с использованием FastAPI. API предоставляет возможность работы с книгами, авторами и выдачей книг читателям.

## Структура базы данных
База данных состоит из трех таблиц: `author`, `book`, `borrow`.

# API Endpoints

## Эндпоинты для авторов
- **POST /authors** — Создание нового автора.
- **GET /authors** — Получение списка всех авторов.
- **GET /authors/{id}** — Получение информации об авторе по id.
- **PUT /authors/{id}** — Обновление информации об авторе.
- **DELETE /authors/{id}** — Удаление автора.

## Эндпоинты для книг
- **POST /books** — Добавление новой книги.
- **GET /books** — Получение списка всех книг.
- **GET /books/{id}** — Получение информации о книге по id.
- **PUT /books/{id}** — Обновление информации о книге.
- **DELETE /books/{id}** — Удаление книги.

## Эндпоинты для выдач
- **POST /borrows** — Создание записи о выдаче книги.
- **GET /borrows** — Получение списка всех выдач.
- **GET /borrows/{id}** — Получение информации о выдаче по id.
- **PATCH /borrows/{id}/return** — Завершение выдачи (с указанием даты возврата).

## Требования к системе

- **Python**: 3.12 или выше.
- **PostgreSQL**
- **Docker**
