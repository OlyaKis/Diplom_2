import pytest
import random
import string
from utils.api_client import StellarBurgersAPI


@pytest.fixture(scope="function")
def api():
    return StellarBurgersAPI()


def generate_random_email():
    return "".join(random.choices(string.ascii_lowercase, k=10)) + "@gmail.com"

@pytest.fixture(scope="function")
def new_user(api):
    email = generate_random_email()
    password = "123456"
    name = "TestName"
    resp = api.register_user(email, password, name)
    assert resp.status_code == 200
    token = resp.json()["accessToken"]
    yield {"email": email, "password": password, "token": token}
    api.delete_user(token)
