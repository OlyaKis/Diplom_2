import allure
import pytest
from utils.api_client import generate_random_email


@allure.epic("Создание пользователя")
class TestCreateUser:
    @allure.title("Создать уникального пользователя")
    def test_create_unique_user(self, api):
        email = generate_random_email()
        with allure.step("Отправить запрос на регистрацию нового пользователя"):
            response = api.register_user(email, "123456", "Tester")
        with allure.step("Проверить успешность регистрации"):
            assert response.status_code == 200
            assert response.json()["success"] is True
        with allure.step("Удалить созданного пользователя"):
            api.delete_user("Bearer " + response.json()["accessToken"])

    @allure.title("Создать пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, api, new_user):
        with allure.step("Попытка зарегистрировать уже существующего пользователя"):
            response = api.register_user(new_user["email"], new_user["password"], "Tester")
        with allure.step("Проверить ответ о существующем пользователе"):
            assert response.status_code == 403
            assert response.json()["message"] == "User already exists"

    @allure.title("Создать пользователя с пропущенным обязательным полем")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_with_missing_field(self, api, missing_field):
        user_data = {
            "email": generate_random_email(),
            "password": "123456",
            "name": "Tester"
        }
        user_data.pop(missing_field)
        with allure.step(f"Регистрация с отсутствующим полем: {missing_field}"):
            response = api.session.post(
                "https://stellarburgers.nomoreparties.site/api/auth/register", json=user_data
            )
        with allure.step("Проверить неуспешную регистрацию"):
            assert response.status_code == 403 or response.status_code == 400
            assert response.json()["success"] is False
