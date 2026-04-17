import pytest
from helpers import generate_random_string
from api_client import ScooterApiClient
from data import BASE_ORDER_PAYLOAD


@pytest.fixture(scope="function")
def api_client():
    """Фикстура возвращает экземпляр API-клиента."""
    return ScooterApiClient()


@pytest.fixture(scope="function")
def registered_courier(api_client):
    """
    Создаёт курьера со случайными данными, авторизует его и возвращает
    кортеж (login, password, first_name, courier_id).
    После теста курьер удаляется.
    """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # Предусловие: создание курьера
    response = api_client.register_courier(login, password, first_name)

    # Авторизация для получения ID
    login_resp = api_client.login_courier(login, password)
    courier_id = login_resp.json().get("id") if login_resp.status_code == 200 else None

    yield login, password, first_name, courier_id

    # Очистка после теста
    if courier_id:
        api_client.delete_courier(courier_id)


@pytest.fixture(scope="function")
def created_order(api_client):
    """
    Создаёт тестовый заказ и возвращает кортеж (track, order_id).
    Очистка не требуется.
    """
    response = api_client.create_order(BASE_ORDER_PAYLOAD)
    track = response.json().get("track") if response.status_code == 201 else None

    if track:
        order_resp = api_client.get_order_by_track(track)
        order = order_resp.json().get("order") if order_resp.status_code == 200 else {}
        order_id = order.get("id")
        return track, order_id
    return None, None