import pytest
import requests
from urls import BASE_URL


@pytest.fixture(scope="function")
def api_session():
    """Фикстура для HTTP-сессии."""
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def base_url():
    """Фикстура возвращает базовый URL API."""
    return BASE_URL