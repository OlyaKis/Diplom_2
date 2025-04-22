import allure


@allure.epic("Создание заказа")
class TestCreateOrder:
    def test_create_order_with_auth_and_valid_ingredients(self, api, new_user):
        ingredients = api.get_ingredients().json()["data"]
        ids = [i["_id"] for i in ingredients[:3]]
        response = api.create_order(ids, new_user["token"])
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_create_order_without_auth(self, api):
        ingredients = api.get_ingredients().json()["data"]
        ids = [i["_id"] for i in ingredients[:3]]
        response = api.create_order(ids)
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_create_order_without_ingredients(self, api, new_user):
        response = api.create_order([], new_user["token"])
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    def test_create_order_with_invalid_ingredient_hash(self, api, new_user):
        response = api.create_order(["123invalid456"], new_user["token"])
        assert response.status_code == 500 or response.status_code == 400
