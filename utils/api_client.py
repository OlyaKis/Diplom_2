import requests
import random
import string
import allure

BASE_URL = "https://stellarburgers.nomoreparties.site/api"


def generate_random_email():
    return "".join(random.choices(string.ascii_lowercase, k=10)) + "@gmail.com"


class StellarBurgersAPI:
    def __init__(self):
        self.session = requests.Session()

    @allure.step("Регистрация пользователя")
    def register_user(self, email, password, name):
        return self.session.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "name": name
        })

    @allure.step("Логин пользователя")
    def login_user(self, email, password):
        return self.session.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })

    @allure.step("Удаление пользователя по токену")
    def delete_user(self, token):
        return self.session.delete(f"{BASE_URL}/auth/user", headers={
            "Authorization": token
        })

    @allure.step("Изменение данных пользователя с токеном")
    def change_user_data(self, token, data):
        return self.session.patch(f"{BASE_URL}/auth/user", headers={
            "Authorization": token
        }, json=data)

    @allure.step("Создание заказа")
    def create_order(self, ingredients, token=None):
        headers = {"Authorization": token} if token else {}
        return self.session.post(f"{BASE_URL}/orders", json={"ingredients": ingredients}, headers=headers)

    @allure.step("Получение заказов пользователя")
    def get_user_orders(self, token=None):
        headers = {"Authorization": token} if token else {}
        return self.session.get(f"{BASE_URL}/orders", headers=headers)

    @allure.step("Получение ингредиентов")
    def get_ingredients(self):
        return self.session.get(f"{BASE_URL}/ingredients")
