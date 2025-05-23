import allure


@allure.epic("Получение заказов пользователя")
class TestGetOrders:
    @allure.title("Получить заказы пользователя с авторизацией")
    def test_get_user_orders_with_auth(self, api, new_user):
        with allure.step("Получить список ингредиентов"):
            ingredients = api.get_ingredients().json()["data"]
            ids = [i["_id"] for i in ingredients[:2]]
        with allure.step("Создать заказ для пользователя"):
            api.create_order(ids, new_user["token"])
        with allure.step("Получить заказы пользователя"):
            response = api.get_user_orders(new_user["token"])
        with allure.step("Проверить успешное получение заказов"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "orders" in response.json()

    @allure.title("Получить заказы пользователя без авторизации")
    def test_get_user_orders_without_auth(self, api):
        with allure.step("Попытка получить заказы без авторизации"):
            response = api.get_user_orders()
        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401
            assert response.json()["message"] == "You should be authorised"
