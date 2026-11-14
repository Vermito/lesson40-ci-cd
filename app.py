from fastapi import FastAPI, HTTPException

app = FastAPI(title="Online Library Demo")

BOOKS = {
    1: {"id": 1, "title": "Python для начинающих"},
    2: {"id": 2, "title": "Изучаем FastAPI"},
}


@app.get("/")
def home():
    return {"message": "Добро пожаловать в онлайн-библиотеку!"}


@app.get("/books")
def get_books():
    return list(BOOKS.values())


@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = BOOKS.get(book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    return book
