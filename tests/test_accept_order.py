import allure
from api_client import ScooterApiClient


class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, api_client, registered_courier, created_order):
        login, password, first_name, courier_id = registered_courier
        track, order_id = created_order

        response = api_client.accept_order(order_id, courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Принятие заказа без ID курьера")
    def test_accept_order_without_courier_id_fails(self, api_client):
        response = api_client.accept_order(order_id=1, courier_id=None)
        assert response.status_code == 400

    @allure.title("Принятие заказа с неверным ID курьера")
    def test_accept_order_invalid_courier_id_fails(self, api_client):
        response = api_client.accept_order(order_id=1, courier_id=999999)
        assert response.status_code == 404
        assert "Курьера с таким id не существует" in response.json().get("message", "")

    @allure.title("Принятие заказа без ID заказа")
    def test_accept_order_without_order_id_fails(self, api_client):
        response = api_client.accept_order(order_id=None, courier_id=1)
        assert response.status_code in [400, 404, 500]

    @allure.title("Принятие заказа с неверным ID заказа")
    def test_accept_order_invalid_order_id_fails(self, api_client, registered_courier):
        login, password, first_name, courier_id = registered_courier
        response = api_client.accept_order(order_id=999999, courier_id=courier_id)
        assert response.status_code == 404
        assert "Заказа с таким id не существует" in response.json().get("message", "")