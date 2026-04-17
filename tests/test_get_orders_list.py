import allure
from api_client import ScooterApiClient


class TestGetOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list_returns_list(self, api_client):
        response = api_client.get_orders_list()

        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)