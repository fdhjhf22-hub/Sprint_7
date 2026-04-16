import random
import string


def generate_random_string(length: int) -> str:
    """Генерирует строку из случайных букв нижнего регистра заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def register_new_courier_and_return_login_password() -> list:
    """
    Регистрирует нового курьера со случайными данными.
    Возвращает список [login, password, firstName] или пустой список при ошибке.
    """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []


def login_courier_and_return_id(login: str, password: str) -> int | None:
    """
    Авторизует курьера и возвращает его ID.
    Если авторизация не удалась, возвращает None.
    """
    payload = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

    if response.status_code == 200:
        return response.json().get("id")
    return None


def delete_courier(courier_id: int) -> bool:
    """
    Удаляет курьера по ID.
    Возвращает True, если удаление успешно (код 200 и {"ok":true}).
    """
    response = requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")
    return response.status_code == 200 and response.json().get("ok") is True


def create_order_and_return_track(order_data: dict) -> int | None:
    """
    Создаёт заказ и возвращает его трек-номер.
    Если создание не удалось, возвращает None.
    """
    response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
    if response.status_code == 201:
        return response.json().get("track")
    return None


def accept_order(order_id: int, courier_id: int) -> bool:
    """
    Принимает заказ курьером.
    Возвращает True, если принятие успешно (код 200 и {"ok":true}).
    """
    response = requests.put(
        f"{BASE_URL}/api/v1/orders/accept/{order_id}",
        params={"courierId": courier_id}
    )
    return response.status_code == 200 and response.json().get("ok") is True


def get_order_by_track(track: int) -> dict | None:
    """
    Получает заказ по трек-номеру.
    Возвращает словарь с данными заказа или None, если заказ не найден.
    """
    response = requests.get(f"{BASE_URL}/api/v1/orders/track", params={"t": track})
    if response.status_code == 200:
        return response.json().get("order")
    return None