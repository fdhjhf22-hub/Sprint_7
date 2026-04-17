import allure
import requests
from api_client import ScooterApiClient
from urls import BASE_URL, ENDPOINT_ORDERS_TRACK


class TestGetOrderByTrack:

    @allure.title("Успешное получение заказа по трек-номеру")
    def test_get_order_by_track_success(self, api_client, created_order):
        track, order_id = created_order

        response = api_client.get_order_by_track(track)

        assert response.status_code == 200
        order = response.json().get("order")
        assert order is not None
        assert order["track"] == track
        assert "id" in order

    @allure.title("Получение заказа без трек-номера")
    def test_get_order_without_track_fails(self):
        response = requests.get(f"{BASE_URL}{ENDPOINT_ORDERS_TRACK}")
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.json().get("message", "")

    @allure.title("Получение заказа с несуществующим трек-номером")
    def test_get_order_nonexistent_track_fails(self, api_client):
        response = api_client.get_order_by_track(999999)
        assert response.status_code == 404
        assert "Заказ не найден" in response.json().get("message", "")