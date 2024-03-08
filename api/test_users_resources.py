import datetime

from requests import get, post, put, delete
from werkzeug.security import generate_password_hash

BASE_URL = "http://127.0.0.1:8080"
API_VERSION = "api/v2"

print(get(f"{BASE_URL}/{API_VERSION}/users").json())  # Тест - Корректное получение всех пользователей
print(get(f"{BASE_URL}/{API_VERSION}/users/1").json())  # Тест - Корректное получение пользователя по id
print(get(f"{BASE_URL}/{API_VERSION}/users/0").json())  # Тест - Ошибочный запрос - несуществующй id
print(get(f"{BASE_URL}/{API_VERSION}/users/s").json())  # Тест - Ошибочный запрос - неверный тип id


print(post(f"{BASE_URL}/{API_VERSION}/users", json={}).json())  # Тест - Ошибочный запрос создания пользователя - неполный запрос
data = {
    "surname": "Ivan",
    "name": "Ivanov",
    "age": 27,
    "position": "developer",
    "speciality": "IT specialist",
    "address": "module_2",
    "email": "test@mail.ru",
    "hashed_password": generate_password_hash("1"),
    "modified_date": datetime.datetime.now().isoformat(),
}
print(post(f"{BASE_URL}/{API_VERSION}/users", json=data).json())  # Тест - корректное создание пользователя. В ответе id пользователя
print(get(f"{BASE_URL}/{API_VERSION}/users").json())  # Тест - Корректное получение всех пользователей для создания

data2 = {
    "surname": "Ivan",
    "name": "Ivanov",
    "age": 27,
    "position": "programm developer",
    "speciality": "IT specialist",
    "address": "module_2",
    "email": "test@mail.ru",
    "hashed_password": generate_password_hash("1"),
    "modified_date": datetime.datetime.now().isoformat(),
}
print(put(f"{BASE_URL}/{API_VERSION}/users/0", json={}).json())  # Тест - Ошибочный запрос - редактирование несуществующего пользователя
print(put(f"{BASE_URL}/{API_VERSION}/users/6", json=data2).json())  # Тест - корректное редактирование пользователя (изменено position и modified_date)
print(get(f"{BASE_URL}/{API_VERSION}/users").json())  # Тест - Корректное получение всех пользователей для проверки редактирования

print(delete(f"{BASE_URL}/{API_VERSION}/users/999").json())  # Тест - Ошибочный запрос на удаление пользователя — несуществующий id
print(delete(f"{BASE_URL}/{API_VERSION}/users/s").json())  # Тест - Ошибочный запрос на удаление пользователя — неверный id
print(delete(f"{BASE_URL}/{API_VERSION}/users/6").json())  # Тест - Корректный запрос на удаление пользователя
print(get(f"{BASE_URL}/{API_VERSION}/users").json())  # Тест - Корректное получение всех пользователей для проверки удаления
