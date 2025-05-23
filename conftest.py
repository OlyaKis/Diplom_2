import pytest
from utils.api_client import StellarBurgersAPI
from utils.helpers import generate_random_email
import allure


@pytest.fixture(scope="function")
def api():
    return StellarBurgersAPI()


@pytest.fixture(scope="function")
def new_user(api):
    email = generate_random_email()
    password = "123456"
    name = "TestName"
    with allure.step("Зарегистрировать нового пользователя"):
        resp = api.register_user(email, password, name)
        if resp.status_code != 200:
            raise RuntimeError(f"Не удалось создать пользователя: {resp.status_code}, {resp.text}")
        token = resp.json()["accessToken"]
    yield {"email": email, "password": password, "token": token}
    with allure.step("Удалить пользователя после теста"):
        api.delete_user(token)
