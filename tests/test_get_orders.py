import allure


@allure.epic("Получение заказов пользователя")
class TestGetOrders:
    def test_get_user_orders_with_auth(self, api, new_user):
        ingredients = api.get_ingredients().json()["data"]
        ids = [i["_id"] for i in ingredients[:2]]
        api.create_order(ids, new_user["token"])
        response = api.get_user_orders(new_user["token"])
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()

    def test_get_user_orders_without_auth(self, api):
        response = api.get_user_orders()
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"
