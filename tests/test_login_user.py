import allure


@allure.epic("Логин пользователя")
class TestLoginUser:
    @allure.title("Логин под существующим пользователем")
    def test_login_with_valid_credentials(self, api, new_user):
        with allure.step("Отправить запрос на логин"):
            response = api.login_user(new_user["email"], new_user["password"])
        with allure.step("Проверить успешную авторизацию"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_invalid_credentials(self, api):
        with allure.step("Попытка войти с неверными данными"):
            response = api.login_user("wrong@mail.com", "wrongpass")
        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401
            assert response.json()["message"] == "email or password are incorrect"
