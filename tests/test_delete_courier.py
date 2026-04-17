import allure
import requests
from api_client import ScooterApiClient
from urls import BASE_URL, ENDPOINT_COURIER_DELETE


class TestDeleteCourier:

    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, api_client, registered_courier):
        login, password, first_name, courier_id = registered_courier

        response = api_client.delete_courier(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление курьера без ID")
    def test_delete_courier_without_id_fails(self):
        response = requests.delete(f"{BASE_URL}{ENDPOINT_COURIER_DELETE.format(courier_id='')}")
        assert response.status_code == 404

    @allure.title("Удаление курьера с несуществующим ID")
    def test_delete_courier_nonexistent_id_fails(self, api_client):
        response = api_client.delete_courier(999999)
        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.json().get("message", "")