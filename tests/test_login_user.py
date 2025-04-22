import allure


@allure.epic("Логин пользователя")
class TestLoginUser:
    def test_login_with_valid_credentials(self, api, new_user):
        response = api.login_user(new_user["email"], new_user["password"])
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_login_with_invalid_credentials(self, api):
        response = api.login_user("wrong@mail.com", "wrongpass")
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
