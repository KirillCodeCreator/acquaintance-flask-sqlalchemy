import requests

BASE_URL = "http://127.0.0.1:8080"


def test_get_all_jobs():
    """получение всех работ"""
    resp = requests.get(f"{BASE_URL}/api/jobs")
    jobs = resp.json()["jobs"]
    assert "is_finished" in jobs[-1]
    return 'тест завершен'


def test_get_job():
    """получение одной работы"""
    resp = requests.get(f"{BASE_URL}/api/jobs/1")
    job = resp.json()["jobs"][0]
    assert "is_finished" in job
    return 'тест завершен'


def test_wrong_get_job():
    """получение несуществующей работы"""
    resp = requests.get(f"{BASE_URL}/api/jobs/0")
    assert resp.status_code == 404 and "Not found" in resp.json()["error"]
    return 'тест завершен'


def test_wrong_type_get_job():
    """Получение работы с неверным типом id"""
    resp = requests.get(f"{BASE_URL}/api/jobs/string")
    assert resp.status_code == 404
    return 'тест завершен'


print(f'Получение всех работ - {test_get_all_jobs()}')
print(f'Получение одной работы - {test_get_job()}')
print(f'Получение несуществующей работы - {test_wrong_get_job()}')
print(f'Получение работы с неверным типом id - {test_wrong_type_get_job()}')
