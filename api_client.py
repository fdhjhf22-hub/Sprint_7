import allure
import requests
from urls import BASE_URL, ENDPOINT_COURIER, ENDPOINT_LOGIN, ENDPOINT_ORDERS, ENDPOINT_ORDERS_TRACK, ENDPOINT_ORDERS_ACCEPT, ENDPOINT_COURIER_DELETE


class ScooterApiClient:
    """Клиент для взаимодействия с API сервиса Яндекс.Самокат."""

    @staticmethod
    @allure.step("Регистрация курьера с логином {login}")
    def register_courier(login: str, password: str, first_name: str) -> requests.Response:
        payload = {"login": login, "password": password, "firstName": first_name}
        return requests.post(f"{BASE_URL}{ENDPOINT_COURIER}", data=payload)

    @staticmethod
    @allure.step("Авторизация курьера с логином {login}")
    def login_courier(login: str, password: str) -> requests.Response:
        payload = {"login": login, "password": password}
        return requests.post(f"{BASE_URL}{ENDPOINT_LOGIN}", data=payload)

    @staticmethod
    @allure.step("Удаление курьера с ID {courier_id}")
    def delete_courier(courier_id: int) -> requests.Response:
        return requests.delete(f"{BASE_URL}{ENDPOINT_COURIER_DELETE.format(courier_id=courier_id)}")

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(order_data: dict) -> requests.Response:
        return requests.post(f"{BASE_URL}{ENDPOINT_ORDERS}", json=order_data)

    @staticmethod
    @allure.step("Получение списка заказов")
    def get_orders_list() -> requests.Response:
        return requests.get(f"{BASE_URL}{ENDPOINT_ORDERS}")

    @staticmethod
    @allure.step("Получение заказа по трек-номеру {track}")
    def get_order_by_track(track: int) -> requests.Response:
        return requests.get(f"{BASE_URL}{ENDPOINT_ORDERS_TRACK}", params={"t": track})

    @staticmethod
    @allure.step("Принятие заказа {order_id} курьером {courier_id}")
    def accept_order(order_id: int, courier_id: int) -> requests.Response:
        return requests.put(
            f"{BASE_URL}{ENDPOINT_ORDERS_ACCEPT.format(order_id=order_id)}",
            params={"courierId": courier_id}
        )