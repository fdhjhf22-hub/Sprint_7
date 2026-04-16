import allure
import pytest
import requests
from helpers import register_new_courier_and_return_login_password, login_courier_and_return_id, delete_courier
from urls import BASE_URL


class TestDeleteCourier:

    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось создать курьера"
        login, password, first_name = courier_data

        courier_id = login_courier_and_return_id(login, password)
        assert courier_id is not None, "Не удалось получить ID курьера"

        response = requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление курьера без ID")
    def test_delete_courier_without_id_fails(self):
        response = requests.delete(f"{BASE_URL}/api/v1/courier/")
        assert response.status_code == 400 or response.status_code == 404

    @allure.title("Удаление курьера с несуществующим ID")
    def test_delete_courier_nonexistent_id_fails(self):
        response = requests.delete(f"{BASE_URL}/api/v1/courier/999999")
        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.json().get("message", "")