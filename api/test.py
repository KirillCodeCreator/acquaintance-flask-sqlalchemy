from datetime import datetime

import requests

BASE_URL = "http://127.0.0.1:8080"

test_result = 'тест пройден'


def test_get_all_jobs():
    """получение всех работ"""
    resp = requests.get(f"{BASE_URL}/api/jobs")
    jobs = resp.json()["jobs"]
    assert "is_finished" in jobs[-1]
    return test_result


def test_get_job():
    """получение одной работы"""
    resp = requests.get(f"{BASE_URL}/api/jobs/1")
    job = resp.json()["jobs"][0]
    assert job["id"] == 1
    return test_result


def test_wrong_get_job():
    """получение несуществующей работы"""
    resp = requests.get(f"{BASE_URL}/api/jobs/0")
    assert resp.status_code == 404 and "Not found" in resp.json()["error"]
    return test_result


def test_wrong_type_get_job():
    """Получение работы с неверным типом id"""
    resp = requests.get(f"{BASE_URL}/api/jobs/string")
    assert resp.status_code == 404
    return test_result


def test_job_post_empty():
    """Проверка, что метод POST для создания работы завершится с ошибкой, если будет передан пустой запрос"""
    data = {}
    resp = requests.post(f"{BASE_URL}/api/jobs", json=data)
    assert resp.status_code == 400 and "Empty request" in resp.json()["error"]
    return test_result


def test_job_post_with_missing_fields():
    """Проверка, что метод POST для создания работы завершится с ошибкой, если в запросе поле is_finished отсутствует"""
    data = {
        "team_leader_id": 4,
        "job": "Working hard",
        "work_size": 100,
        "collaborators": "1, 2, 3",
        "start_date": datetime.now().isoformat(),
    }
    resp = requests.post(f"{BASE_URL}/api/jobs", json=data)
    assert resp.status_code == 400 and "Missing fields" in resp.json()["error"]
    return test_result


def test_job_post_with_unknown_team_leader_id():
    """Проверка, что метод POST для создания работы завершится с ошибкой,
     если в запросе будет передан не существующий в БД team_leader_id"""
    data = {
        "team_leader_id": 999,
        "job": "Working hard",
        "work_size": 100,
        "collaborators": "1, 2, 3",
        "start_date": datetime.now().isoformat(),
        "end_date": None,
        "is_finished": False
    }
    resp = requests.post(f"{BASE_URL}/api/jobs", json=data)
    assert resp.status_code == 400 and "team_leader_id unknown" in resp.json()["error"]
    return test_result


def test_job_post():
    """Проверка, что метод POST для создания работы завершится успешно и
     проверка наличия работы по созданному id завершиться успешно"""
    data = {
        "team_leader_id": 4,
        "job": "Test working",
        "work_size": 100,
        "collaborators": "1, 2, 3",
        "start_date": datetime.now().isoformat(),
        "end_date": None,
        "is_finished": False,
        "categories": [1]
    }
    resp = requests.post(f"{BASE_URL}/api/jobs", json=data)
    resp.raise_for_status()
    job_id = resp.json()["id"]
    resp = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
    jobs = resp.json()["jobs"]
    assert jobs[0]["id"] == job_id
    return test_result


print(f'Получение всех работ - {test_get_all_jobs()}')
print(f'Получение одной работы - {test_get_job()}')
print(f'Получение несуществующей работы - {test_wrong_get_job()}')
print(f'Получение работы с неверным типом id - {test_wrong_type_get_job()}')

print(f'Попытка создания работы с пустым запросом - {test_job_post_empty()}')
print(f'Попытка создания работы с неполным запросом - {test_job_post_with_missing_fields()}')
print(f'Попытка создания работы с несуществующим тим лидом  - {test_job_post_with_unknown_team_leader_id()}')
print(f'Создание работы и проверка создания - {test_job_post()}')
