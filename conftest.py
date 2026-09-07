import os
import uuid

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


@pytest.fixture
def courier():
    """
    Фикстура создаёт уникального курьера перед тестом
    и удаляет его после завершения.
    """
    # Генерация уникальных данных
    unique_login = f"courier_{uuid.uuid4().hex[:8]}"
    data = {
        "login": unique_login,
        "password": "1234",
        "firstName": "Test"
    }

    # Создание курьера через API
    create_response = requests.post(f"{BASE_URL}/api/v1/courier", json=data)
    assert create_response.status_code == 201, "Не удалось создать курьера"

    yield data  # передаем данные в тест

    # Удаление курьера после теста
    login_response = requests.post(
        f"{BASE_URL}/api/v1/courier/login",
        json={"login": data["login"], "password": data["password"]}
    )

    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")
