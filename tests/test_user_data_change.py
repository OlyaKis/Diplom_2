import allure


@allure.epic("Изменение данных пользователя")
class TestChangeUserData:
    def test_change_user_data_with_auth(self, api, new_user):
        new_name = "NewName"
        response = api.change_user_data(new_user["token"], {"name": new_name})
        assert response.status_code == 200
        assert response.json()["user"]["name"] == new_name

    def test_change_user_data_without_auth(self, api):
        response = api.change_user_data("", {"name": "HackerName"})
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"
