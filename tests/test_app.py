from CI_CD_ACTIONS.app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == ("Добро пожаловать в онлайн-библиотеку!")


def test_get_books():
    response = client.get("/books")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_book():
    response = client.get("/books/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Python для начинающих"


def test_book_not_found():
    response = client.get("/books/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Книга не найдена"}
