import allure


@allure.epic("Создание заказа")
class TestCreateOrder:
    @allure.title("Создать заказ с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_valid_ingredients(self, api, new_user):
        with allure.step("Получить ингредиенты и создать заказ"):
            ingredients = api.get_ingredients().json()["data"]
            ids = [i["_id"] for i in ingredients[:3]]
            response = api.create_order(ids, new_user["token"])
        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создать заказ без авторизации")
    def test_create_order_without_auth(self, api):
        with allure.step("Получить ингредиенты и создать заказ без авторизации"):
            ingredients = api.get_ingredients().json()["data"]
            ids = [i["_id"] for i in ingredients[:3]]
            response = api.create_order(ids)
        with allure.step("Проверить успешное создание заказа без авторизации"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self, api, new_user):
        with allure.step("Попытка создать заказ без ингредиентов"):
            response = api.create_order([], new_user["token"])
        with allure.step("Проверить ошибку валидации ингредиентов"):
            assert response.status_code == 400
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создать заказ с невалидным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self, api, new_user):
        with allure.step("Попытка создать заказ с невалидным ингредиентом"):
            response = api.create_order(["123invalid456"], new_user["token"])
        with allure.step("Проверить ошибку при создании заказа с невалидным ингредиентом"):
            assert response.status_code == 500 or response.status_code == 400
