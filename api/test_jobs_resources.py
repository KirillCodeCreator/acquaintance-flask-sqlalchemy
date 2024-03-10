import datetime

from requests import get, post, put, delete

BASE_URL = "http://127.0.0.1:8080"
API_VERSION = "api/v2"

print(get(f"{BASE_URL}/{API_VERSION}/jobs").json())  # Тест - Корректное получение всех работ
print(get(f"{BASE_URL}/{API_VERSION}/jobs/1").json())  # Тест - Корректное получение работы по id
print(get(f"{BASE_URL}/{API_VERSION}/jobs/0").json())  # Тест - Ошибочный запрос - несуществующй id
#print(get(f"{BASE_URL}/{API_VERSION}/jobs/s").json())  # Тест - Ошибочный запрос - неверный тип id

print(
    post(f"{BASE_URL}/{API_VERSION}/jobs", json={}).json())  # Тест - Ошибочный запрос создания работы - неполный запрос

dt = datetime.datetime.now().isoformat()
data = {
    "team_leader_id": 1,
    "job": "developer",
    "work_size": "100",
    "collaborators": "2, 3",
    "start_date": dt
}
print(post(f"{BASE_URL}/{API_VERSION}/jobs", json=data).json())  # Тест - корректное создание работы. В ответе id работы
print(get(f"{BASE_URL}/{API_VERSION}/jobs").json())  # Тест - Корректное получение всех работ для проверки создания

data2 = {
    "team_leader_id": 1,
    "job": "developer",
    "work_size": "100",
    "collaborators": "2, 3",
    "start_date": dt,
    "end_date": datetime.datetime.now().isoformat(),
    "is_finished": True
}
print(put(f"{BASE_URL}/{API_VERSION}/jobs/0", json={}).json())  # Тест - Ошибочный запрос - редактирование несуществующей работы
print(put(f"{BASE_URL}/{API_VERSION}/jobs/5", json={}).json())  # Тест - Ошибочный запрос - редактирование работы с неполным запросом
print(put(f"{BASE_URL}/{API_VERSION}/jobs/5", json=data2).json())  # Тест - корректное редактирование работы (изменено end_date и is_finished)
print(get(f"{BASE_URL}/{API_VERSION}/jobs").json()) # Тест - Корректное получение всех работ для проверки редактирования

print(delete(
    f"{BASE_URL}/{API_VERSION}/jobs/999").json())  # Тест - Ошибочный запрос на удаление работы — несуществующий id
print(delete(f"{BASE_URL}/{API_VERSION}/jobs/5").json())  # Тест - Корректный запрос на удаление работы
print(delete(f"{BASE_URL}/{API_VERSION}/jobs/s").json())  # Тест - Ошибочный запрос на удаление работы — неверный id
print(get(f"{BASE_URL}/{API_VERSION}/jobs").json())  # Тест - Корректное получение всех работ для проверки удаления
