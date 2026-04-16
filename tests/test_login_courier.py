import allure
import pytest
import requests
from helpers import register_new_courier_and_return_login_password, generate_random_string, delete_courier, login_courier_and_return_id
from urls import BASE_URL


class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    def test_login_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось создать курьера"
        login, password, first_name = courier_data

        payload = {"login": login, "password": password}
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

        assert response.status_code == 200
        assert "id" in response.json()

        courier_id = response.json().get("id")
        if courier_id:
            delete_courier(courier_id)

    @allure.title("Авторизация с неверным логином")
    def test_login_invalid_login_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось создать курьера"
        login, password, first_name = courier_data

        payload = {"login": "invalid_login", "password": password}
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

        courier_id = login_courier_and_return_id(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title("Авторизация с неверным паролем")
    def test_login_invalid_password_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось создать курьера"
        login, password, first_name = courier_data

        payload = {"login": login, "password": "wrong_password"}
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

        courier_id = login_courier_and_return_id(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title("Авторизация без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_fails(self, missing_field):
        payload = {"login": "some_login", "password": "some_password"}
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

        assert response.status_code in [400, 504]
        if response.status_code == 400:
            assert "Недостаточно данных для входа" in response.json().get("message", "")

    @allure.title("Авторизация под несуществующим пользователем")
    def test_login_nonexistent_courier_fails(self):
        payload = {"login": "nonexistent_user_12345", "password": "any_password"}
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")