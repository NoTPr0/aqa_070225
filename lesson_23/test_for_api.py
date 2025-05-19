from hillel_api import API as api
import logging
import requests
import pytest

s = requests.Session()

# Конфігурація логера
logging.basicConfig(level=logging.INFO)  # Встановлення рівня логування

# Тестова функція
def test_example():
    logging.info("Початок виконання тесту")
    # Робота тесту
    assert 1 + 1 == 2
    logging.info("Тест пройшов успішно")

def after_processsing(r: requests.Response):
    try:
        return r.json()
    except requests.JSONDecodeError as e:
        print(e)
        return {"nonjson": r.text}


def test_sigin_positive(get_regisered_user):
    email, password = get_regisered_user
    user_data = {
    "email": email,
    "password": password,
    "remember": False
    }
    r = api.auth.signin(s, user_data)
    r_json = after_processsing(r)    
    assert r.status_code == 200, "Wrong status code"
    assert r_json["status"] == "ok", "Key 'status' is not ok"


def test_reset_password(get_regisered_user):
    email, password = get_regisered_user
    user_data = {"email": email}
    r = api.auth.resetpassword(s, user_data)
    r_json = after_processsing(r)    
    assert r.status_code == 200, "Wrong status code"
    assert r_json["status"] == "ok", "Key 'status' is not ok"


def test_sigin_delete_and_cant_resign():
    """E2E test example"""
    # Створення даних користувача для тестування
    email = "alex22222@gmail.com"
    password = "AA12aa!@"
    user_data = {
        "name": "name",
        "lastName": "lastname",
        "email": email,
        "password": password,
        "repeatPassword": password
    }
    s = requests.Session()
    r = api.auth.signup(s, user_data)
    r_json = r.json()
    # Перевірка успішності реєстрації
    assert r.status_code == 201, "Wrong status code"
    assert r_json["status"] == "ok", "Key 'status' is not ok"

    r = api.auth.logout(s)
    r_json = r.json()
    assert r.status_code == 200, "Wrong status code"
    assert r_json["status"] == "ok", "Key 'status' is not ok"

    user_data_2 = {
    "email": email,
    "password": password,
    "remember": False
    }
    # Автентифікація користувача
    r = api.auth.signin(s, user_data_2)
    r_json = r.json()
    # Перевірка успішності автентифікації
    assert r.status_code == 200, "Wrong status code"
    assert r_json["status"] == "ok", "Key 'status' is not ok"

    # Видалення користувача
    r = api.users.users(s)
    r_json = r.json()
    
    # Перевірка успішності видалення користувача
    assert r.status_code == 200, "Wrong status code"
    assert r_json["status"] == "ok", "Key 'status' is not ok"

    # Спроба повторного входу після видалення користувача (має бути помилка)
    r = api.auth.signin(s, user_data)
    r_json = r.json() 
    # Перевірка невдалої спроби входу після видалення користувача
    assert r.status_code == 400, "Wrong status code"
    assert r_json["status"] == "error", "Key 'error' expected"
