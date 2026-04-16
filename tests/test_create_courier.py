import allure
import pytest
import requests
from helpers import register_new_courier_and_return_login_password, generate_random_string, delete_courier, login_courier_and_return_id
from urls import BASE_URL


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        courier_id = login_courier_and_return_id(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось создать первого курьера"
        login, password, first_name = courier_data

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json().get("message", "")

        courier_id = login_courier_and_return_id(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title("Создание курьера без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_fails(self, missing_field):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json().get("message", "")