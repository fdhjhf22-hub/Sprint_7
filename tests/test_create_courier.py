import allure
import pytest
import requests
from helpers import generate_random_string
from api_client import ScooterApiClient
from urls import BASE_URL, ENDPOINT_COURIER


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, api_client):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = api_client.register_courier(login, password, first_name)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Получаем ID созданного курьера и удаляем его через фикстуру не можем, поэтому удаляем явно.
        login_resp = api_client.login_courier(login, password)
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            if courier_id:
                api_client.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, api_client, registered_courier):
        login, password, first_name, courier_id = registered_courier

        # Попытка создать курьера с тем же логином
        response = api_client.register_courier(login, password, first_name)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json().get("message", "")

    @allure.title("Создание курьера без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_fails(self, missing_field):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}{ENDPOINT_COURIER}", data=payload)

        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json().get("message", "")