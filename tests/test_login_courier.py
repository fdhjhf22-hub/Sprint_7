import allure
import pytest
import requests
from api_client import ScooterApiClient
from urls import BASE_URL, ENDPOINT_LOGIN


class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    def test_login_courier_success(self, api_client, registered_courier):
        login, password, first_name, courier_id = registered_courier
        response = api_client.login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Авторизация с неверным логином")
    def test_login_invalid_login_fails(self, api_client, registered_courier):
        login, password, first_name, courier_id = registered_courier
        response = api_client.login_courier("invalid_login", password)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

    @allure.title("Авторизация с неверным паролем")
    def test_login_invalid_password_fails(self, api_client, registered_courier):
        login, password, first_name, courier_id = registered_courier
        response = api_client.login_courier(login, "wrong_password")

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

    @allure.title("Авторизация без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_fails(self, missing_field):
        payload = {"login": "some_login", "password": "some_password"}
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}{ENDPOINT_LOGIN}", data=payload)

        assert response.status_code in [400, 504]

    @allure.title("Авторизация под несуществующим пользователем")
    def test_login_nonexistent_courier_fails(self, api_client):
        response = api_client.login_courier("nonexistent_user_12345", "any_password")
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")