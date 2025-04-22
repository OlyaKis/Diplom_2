import allure
import pytest
from utils.api_client import generate_random_email


@allure.epic("Создание пользователя")
class TestCreateUser:
    def test_create_unique_user(self, api):
        email = generate_random_email()
        response = api.register_user(email, "123456", "Tester")
        assert response.status_code == 200
        assert response.json()["success"] is True
        api.delete_user("Bearer " + response.json()["accessToken"])

    def test_create_existing_user(self, api, new_user):
        response = api.register_user(new_user["email"], new_user["password"], "Tester")
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_with_missing_field(self, api, missing_field):
        user_data = {
            "email": generate_random_email(),
            "password": "123456",
            "name": "Tester"
        }
        user_data.pop(missing_field)
        response = api.session.post("https://stellarburgers.nomoreparties.site/api/auth/register", json=user_data)
        assert response.status_code == 403 or response.status_code == 400
        assert response.json()["success"] is False
