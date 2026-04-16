import allure
import pytest
import requests
from helpers import create_order_and_return_track, get_order_by_track
from urls import BASE_URL


class TestGetOrderByTrack:

    @allure.title("Успешное получение заказа по трек-номеру")
    def test_get_order_by_track_success(self):
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

        assert order is not None
        assert "id" in order
        assert "track" in order
        assert order["track"] == track

    @allure.title("Получение заказа без трек-номера")
    def test_get_order_without_track_fails(self):
        response = requests.get(f"{BASE_URL}/api/v1/orders/track")
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.json().get("message", "")

    @allure.title("Получение заказа с несуществующим трек-номером")
    def test_get_order_nonexistent_track_fails(self):
        response = requests.get(f"{BASE_URL}/api/v1/orders/track", params={"t": 999999})
        assert response.status_code == 404
        assert "Заказ не найден" in response.json().get("message", "")