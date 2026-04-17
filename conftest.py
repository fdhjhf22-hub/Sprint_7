import pytest
from helpers import generate_random_string
from api_client import ScooterApiClient
from data import BASE_ORDER_PAYLOAD


@pytest.fixture(scope="function")
def api_client():
    """Фикстура возвращает экземпляр API-клиента."""
    return ScooterApiClient()


@pytest.fixture(scope="function")
def test_courier_credentials():
    """Генерирует случайные данные для курьера и возвращает (login, password, first_name)."""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return login, password, first_name


@pytest.fixture(scope="function")
def registered_courier(api_client, test_courier_credentials):
    """
    Создаёт курьера с помощью API и возвращает (login, password, first_name, courier_id).
    Если создание не удалось, возвращает None.
    """
    login, password, first_name = test_courier_credentials
    response = api_client.register_courier(login, password, first_name)
    if response.status_code != 201:
        return None
    # Получаем ID через логин
    login_resp = api_client.login_courier(login, password)
    if login_resp.status_code != 200:
        return None
    courier_id = login_resp.json().get("id")
    return login, password, first_name, courier_id


@pytest.fixture(scope="function")
def created_order(api_client):
    """
    Создаёт заказ и возвращает (track, order_id).
    Если создание не удалось, возвращает (None, None).
    """
    response = api_client.create_order(BASE_ORDER_PAYLOAD)
    if response.status_code != 201:
        return None, None
    track = response.json().get("track")
    order_resp = api_client.get_order_by_track(track)
    if order_resp.status_code != 200:
        return None, None
    order = order_resp.json().get("order")
    order_id = order.get("id")
    return track, order_id