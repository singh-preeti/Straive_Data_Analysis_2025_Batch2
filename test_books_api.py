import json

def test_get_all_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_add_book(client):
    response = client.post(
        "/api/books",
        data=json.dumps({"title": "pytest-book"}),
        content_type="application/json"
    )
    assert response.status_code == 201
    assert "id" in response.json


def test_add_book_without_title(client):
    response = client.post(
        "/api/books",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_book_not_found(client):
    response = client.get("/api/books/999999")
    assert response.status_code == 404


def test_update_book(client):
    # First create a book
    post = client.post(
        "/api/books",
        data=json.dumps({"title": "Old Title"}),
        content_type="application/json"
    )
    book_id = post.json["id"]

    # Update
    response = client.put(
        f"/api/books/{book_id}",
        data=json.dumps({"title": "New Title"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json["title"] == "New Title"


def test_delete_book(client):
    post = client.post(
        "/api/books",
        data=json.dumps({"title": "To Delete"}),
        content_type="application/json"
    )
    book_id = post.json["id"]

    response = client.delete(f"/api/books/{book_id}")
    assert response.status_code == 204
