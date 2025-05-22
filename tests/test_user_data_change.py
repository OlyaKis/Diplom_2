import allure


@allure.epic("Изменение данных пользователя")
class TestChangeUserData:
    @allure.title("Изменить данные пользователя с авторизацией")
    def test_change_user_data_with_auth(self, api, new_user):
        new_name = "NewName"
        with allure.step("Отправить запрос на изменение имени пользователя"):
            response = api.change_user_data(new_user["token"], {"name": new_name})
        with allure.step("Проверить успешное изменение имени"):
            assert response.status_code == 200
            assert response.json()["user"]["name"] == new_name

    @allure.title("Изменить данные пользователя без авторизации")
    def test_change_user_data_without_auth(self, api):
        with allure.step("Попытка изменить имя пользователя без авторизации"):
            response = api.change_user_data("", {"name": "HackerName"})
        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401
            assert response.json()["message"] == "You should be authorised"
