import allure
import pytest
import requests
from helpers import (
    register_new_courier_and_return_login_password,
    login_courier_and_return_id,
    delete_courier,
    create_order_and_return_track,
    get_order_by_track
)
from urls import BASE_URL


class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось создать курьера"
        login, password, first_name = courier_data
        courier_id = login_courier_and_return_id(login, password)
        assert courier_id is not None, "Не удалось получить ID курьера"

        order_payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": 1,
            "phone": "+79991234567",
            "rentTime": 3,
            "deliveryDate": "2026-05-01",
            "comment": "",
            "color": ["BLACK"]
        }
        track = create_order_and_return_track(order_payload)
        assert track is not None, "Не удалось создать заказ"

        order = get_order_by_track(track)
        assert order is not None, "Не удалось получить заказ по треку"
        order_id = order.get("id")

        response = requests.put(
            f"{BASE_URL}/api/v1/orders/accept/{order_id}",
            params={"courierId": courier_id}
        )

        assert response.status_code == 200
        assert response.json() == {"ok": True}

        delete_courier(courier_id)

    @allure.title("Принятие заказа без ID курьера")
    def test_accept_order_without_courier_id_fails(self):
        response = requests.put(f"{BASE_URL}/api/v1/orders/accept/1")
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")

    @allure.title("Принятие заказа с неверным ID курьера")
    def test_accept_order_invalid_courier_id_fails(self):
        response = requests.put(
            f"{BASE_URL}/api/v1/orders/accept/1",
            params={"courierId": 999999}
        )
        assert response.status_code == 404
        assert "Курьера с таким id не существует" in response.json().get("message", "")

    @allure.title("Принятие заказа без ID заказа")
    def test_accept_order_without_order_id_fails(self):
        response = requests.put(
            f"{BASE_URL}/api/v1/orders/accept/",
            params={"courierId": 1}
        )
        assert response.status_code in [400, 404]

    @allure.title("Принятие заказа с неверным ID заказа")
    def test_accept_order_invalid_order_id_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось создать курьера"
        login, password, first_name = courier_data
        courier_id = login_courier_and_return_id(login, password)
        assert courier_id is not None, "Не удалось получить ID курьера"

        response = requests.put(
            f"{BASE_URL}/api/v1/orders/accept/999999",
            params={"courierId": courier_id}
        )
        assert response.status_code == 404
        assert "Заказа с таким id не существует" in response.json().get("message", "")

        delete_courier(courier_id)