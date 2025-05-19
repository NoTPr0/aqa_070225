import pytest
import requests

PORT = 7070
BASE_URL = f"http://127.0.0.1:{PORT}"


def test_get_content():
    response = requests.get(f"{BASE_URL}/content")
    assert response.status_code == 200
    assert response.json() == {"content": []}


def test_create_content():
    data = {"title": "Test", "body": "Test body", "img": "https://i.imgur.com/Y5D7ew7.png"}
    response = requests.post(f"{BASE_URL}/content", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Content created successfully!"}

    # Verify the content was added
    response = requests.get(f"{BASE_URL}/content")
    assert response.status_code == 200
    assert response.json() == {"content": [data]}


def test_update_content():
    data = {"title": "Updated", "body": "Updated body"}
    response = requests.put(f"{BASE_URL}/content/0", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Content updated successfully!"}


def test_delete_content():
    response = requests.delete(f"{BASE_URL}/content/0")
    assert response.status_code == 200
    assert response.json() == {"message": "Content deleted successfully!"}

    # Verify the content was deleted
    response = requests.get(f"{BASE_URL}/content")
    assert response.status_code == 200
    assert response.json() == {"content": []}