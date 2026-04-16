import pytest
import requests
from helpers import generate_random_string
from api_client import ScooterApiClient
from data import BASE_ORDER_PAYLOAD


@pytest.fixture(scope="function")
def api_client():
    """Фикстура возвращает экземпляр API-клиента."""
    return ScooterApiClient()


@pytest.fixture(scope="function")
def registered_courier(api_client):
    """Создаёт курьера со случайными данными, возвращает (login, password, first_name, courier_id)."""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    response = api_client.register_courier(login, password, first_name)
    assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

    login_resp = api_client.login_courier(login, password)
    assert login_resp.status_code == 200, f"Не удалось авторизоваться: {login_resp.text}"
    courier_id = login_resp.json().get("id")

    yield login, password, first_name, courier_id

    # Удаляем курьера после теста
    if courier_id:
        api_client.delete_courier(courier_id)


@pytest.fixture(scope="function")
def created_order(api_client):
    """Создаёт тестовый заказ и возвращает его track, order_id."""
    response = api_client.create_order(BASE_ORDER_PAYLOAD)
    assert response.status_code == 201, f"Не удалось создать заказ: {response.text}"
    track = response.json().get("track")

    order_resp = api_client.get_order_by_track(track)
    assert order_resp.status_code == 200
    order = order_resp.json().get("order")
    order_id = order.get("id")

    yield track, order_id

    # Заказ не удаляется (в API нет удаления), но можно отменить при необходимости.
    # Для тестов это не критично.