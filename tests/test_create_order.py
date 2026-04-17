import allure
import pytest
from api_client import ScooterApiClient
from data import ORDER_DATA


class TestCreateOrder:

    @allure.title("Создание заказа с различными цветами")
    @pytest.mark.parametrize(
        "first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color",
        ORDER_DATA
    )
    def test_create_order_with_color_variations(
        self, api_client, first_name, last_name, address, metro_station, phone,
        rent_time, delivery_date, comment, color
    ):
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment,
            "color": color
        }

        response = api_client.create_order(payload)

        assert response.status_code == 201
        assert "track" in response.json()