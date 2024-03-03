import datetime

import requests
from werkzeug.security import generate_password_hash

BASE_URL = "http://127.0.0.1:8080"

test_result = 'тест пройден'


def test_get_all_users():
    resp = requests.get(f"{BASE_URL}/api/users")
    users = resp.json()["users"]
    assert "address" in users[-1]
    return test_result


print(f'Получение всех пользователей - {test_get_all_users()}')


def test_get_user():
    resp = requests.get(f"{BASE_URL}/api/users/1")
    user = resp.json()["users"][0]
    assert "address" in user
    return test_result


print(f'Получение заданного пользователя  - {test_get_user()}')


def test_wrong_get_user():
    resp = requests.get(f"{BASE_URL}/api/users/0")
    assert resp.status_code == 404 and "Not found" in resp.json()["error"]
    return test_result


print(f'Получение несуществующего пользователя  - {test_wrong_get_user()}')


def test_wrong_type_get_user():
    resp = requests.get(f"{BASE_URL}/api/users/string")
    assert resp.status_code == 404
    return test_result


print(f'Получение пользователя с неверным типом id - {test_wrong_type_get_user()}')


def test_user_post_empty():
    # пустой запрос на создание
    data = {}
    resp = requests.post(f"{BASE_URL}/api/users", json=data)
    assert resp.status_code == 400 and "Empty request" in resp.json()["error"]
    return test_result


print(f'Создание пользователя с пустым запросом - {test_user_post_empty()}')


def test_user_post_with_missing_fields():
    # Поле modified_date отсутсвует
    data = {
        "surname": "Sanders",
        "name": "Teddy",
        "age": 27,
        "position": "programmer",
        "speciality": "IT specialist",
        "address": "module_2",
        "email": "sanders@mars.org",
        "hashed_password": generate_password_hash("teddy_bear27"),
    }
    resp = requests.post(f"{BASE_URL}/api/users", json=data)
    assert resp.status_code == 400 and "Missing fields" in resp.json()["error"]
    return test_result


print(f'Создание пользователя с неполным запросом - {test_user_post_with_missing_fields()}')


def test_user_post_wrong_type_hash():
    data = {
        "surname": "Sanders",
        "name": "Teddy",
        "age": 27,
        "position": "programmer",
        "speciality": "IT specialist",
        "address": "module_2",
        "email": "sanders@mars.org",
        "hashed_password": generate_password_hash("teddy_bear27", method="pbkdf2:sha256"),
        "modified_date": datetime.datetime.now().isoformat(),
    }
    resp = requests.post(f"{BASE_URL}/api/users", json=data)
    assert resp.status_code == 400 and "Wrong type hash" in resp.json()["error"]
    return test_result


print(f'Создание пользователя с неверным паролем - {test_user_post_wrong_type_hash()}')


def test_user_post_with_existing_email():
    # существующий пользователь
    data = {
        "surname": "Sanders",
        "name": "Teddy",
        "age": 27,
        "position": "programmer",
        "speciality": "IT specialist",
        "address": "module_2",
        "email": "andy_story@mars.org",
        "hashed_password": generate_password_hash("teddy_bear27"),
        "modified_date": datetime.datetime.now().isoformat(),
    }
    resp = requests.post(f"{BASE_URL}/api/users", json=data)
    assert resp.status_code == 400 and "Email already exists" in resp.json()["error"]
    return test_result


print(f'Создание пользователя с использованным email - {test_user_post_with_existing_email()}')


def test_user_post():
    data = {
        "surname": "Sanders",
        "name": "Teddy",
        "age": 27,
        "position": "programmer",
        "speciality": "IT specialist",
        "address": "module_2",
        "email": "sanders@mars.org",
        "hashed_password": generate_password_hash("teddy_bear27"),
        "modified_date": datetime.datetime.now().isoformat(),
    }
    resp = requests.post(f"{BASE_URL}/api/users", json=data)
    resp.raise_for_status()
    resp = requests.get(f"{BASE_URL}/api/users")
    users = resp.json()["users"]
    assert users[-1]["name"] == "Teddy"
    return test_result


print(f'Создание пользователя с проверкой - {test_user_post()}')


def test_wrong_type_edit_user():
    resp = requests.put(f"{BASE_URL}/api/users/string")
    assert resp.status_code == 404
    return test_result


print(f'Редактирование пользователя с неверным типом id - {test_wrong_type_edit_user()}')


def test_missing_user_edit():
    # Редактирование несуществующего пользователя
    user_id = 0
    data = {}
    resp = requests.put(f"{BASE_URL}/api/users/{user_id}", json=data)
    assert resp.status_code == 404 and "Not found" in resp.json()["error"]
    return test_result


print(f'Редактирование несуществующего пользователя - {test_missing_user_edit()}')


def test_user_empty_edit():
    user_id = 6
    data = {}
    resp = requests.put(f"{BASE_URL}/api/users/{user_id}", json=data)
    assert resp.status_code == 400 and "Empty request" in resp.json()["error"]
    return test_result


print(f'Редактирование пользователя пустым запросом - {test_user_empty_edit()}')


def test_user_edit_with_missing_fields():
    # Поле modified_date отсутсвует
    user_id = 6
    data = {
        "surname": "Sanders",
        "name": "Teddy",
        "age": 27,
        "position": "programmer",
        "speciality": "IT specialist",
        "address": "module_2",
        "email": "sanders@mars.org",
        "hashed_password": generate_password_hash("teddy_bear27"),
    }
    resp = requests.put(f"{BASE_URL}/api/users/{user_id}", json=data)
    assert resp.status_code == 400 and "Missing fields" in resp.json()["error"]
    return test_result


print(f'Редактирование пользователя неполным запросом - {test_user_edit_with_missing_fields()}')


def test_user_edit_wrong_type_hash():
    user_id = 6
    data = {
        "surname": "Sanders",
        "name": "Teddy",
        "age": 27,
        "position": "programmer",
        "speciality": "IT specialist",
        "address": "module_2",
        "email": "sanders@mars.org",
        "hashed_password": generate_password_hash("teddy_bear27", method="pbkdf2:sha256"),
        "modified_date": datetime.datetime.now().isoformat(),
    }
    resp = requests.put(f"{BASE_URL}/api/users/{user_id}", json=data)
    assert resp.status_code == 400 and "Wrong type hash" in resp.json()["error"]
    return test_result


print(f'Редактирование пользователя с неверным паролем - {test_user_edit_wrong_type_hash()}')


def test_user_edit():
    user_id = 6
    data = {
        "surname": "Sanders",
        "name": "Teddy",
        "age": 27,
        "position": "programmer",
        "speciality": "IT specialist",
        "address": "module_2",
        "email": "sanders_manders@mars.org",  # уникальная почта из-за предыдущих тестов
        "hashed_password": generate_password_hash("teddy_bear27"),
        "modified_date": datetime.datetime.now().isoformat(),
    }
    resp = requests.put(f"{BASE_URL}/api/users/{user_id}", json=data)
    resp.raise_for_status()
    resp = requests.get(f"{BASE_URL}/api/users/{user_id}")
    users = resp.json()["users"][0]
    assert users["name"] == "Teddy"
    return test_result


print(f'Редактирование пользователя с проверкой - {test_user_edit_wrong_type_hash()}')


def test_missing_user_delete():
    user_id = 0
    resp = requests.delete(f"{BASE_URL}/api/users/{user_id}")  # несуществующий пользователь
    assert resp.status_code == 404 and "Not found" in resp.json()["error"]
    return test_result


print(f'Удаление несуществующего пользователя - {test_missing_user_delete()}')


def test_wrong_type_delete_user():
    resp = requests.delete(f"{BASE_URL}/api/users/string")
    assert resp.status_code == 404
    return test_result


print(f'Удаление пользователя с неверным типом id - {test_wrong_type_delete_user()}')


def test_user_delete():
    resp = requests.get(f"{BASE_URL}/api/users")
    users = resp.json()["users"]
    user = users[-1]
    user_id = user['id']
    resp = requests.delete(f"{BASE_URL}/api/users/{user_id}")
    resp.raise_for_status()
    resp = requests.get(f"{BASE_URL}/api/users/{user_id}")  # проверяем что такого пользователя
    # уже нет
    assert resp.status_code == 404 and "Not found" in resp.json()["error"]
    return test_result


print(f'Удаление пользователя с проверкой - {test_user_delete()}')
