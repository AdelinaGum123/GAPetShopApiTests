from operator import truediv

import allure
import requests
import jsonschema
import pytest

from .schemas.inventory_schema import INVENTORY_SCHEMA
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_add_store(self):
        with allure.step("Подготовка данных для добавление нового заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на добавление нового заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_data = response.json()

        with allure.step("Проверка статуса ответа и валидация json схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_data, STORE_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_data['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_data['petId'] == payload['petId'], "petId питомца не совпадает с ожидаемым"
            assert response_data['quantity'] == payload['quantity'], "quantity питомца не совпадает с ожидаемым"
            assert response_data['status'] == payload['status'], "status питомца не совпадает с ожидаемым"
            assert response_data['complete'] == payload['complete'], "complete питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_store_id(self, create_store):
        with allure.step("Получение ID заказа"):
            store_id = create_store["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{store_id}")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == store_id, "ID не совпал с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_delete_store_id(self, create_store):
        with allure.step("Получение ID заказа"):
            store_id = create_store["id"]

        with allure.step("Отправка запроса на удаление информации о заказе по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{store_id}")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка что заказ действительно удален"):
            response = requests.get(f"{BASE_URL}/store/order/{store_id}")
            assert response.status_code == 404, "Заказ не был удален, статус не 404"

    @allure.title("Попытка получить информацию о несуществуещем заказе")
    def test_get_information_nonexistent_store(self):
        with allure.step("Отправка запроса на получение информации о несуществуещем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка структуры ответа"):
            inventory_data = response.json()
            jsonschema.validate(instance=inventory_data, schema=INVENTORY_SCHEMA)
