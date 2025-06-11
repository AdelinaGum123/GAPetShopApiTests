from wsgiref.util import request_uri

import allure
import requests
import pytest
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществуещего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществуещего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществуещего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json = payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществуещем питомце")
    def test_get_information_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществуещем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для добавление нового питомца"):
            payload = {
                "id": 1,
                "name": "Baddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на добавление нового питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_data = response.json()

        with allure.step("Проверка статуса ответа и валидация json схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_data, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_data['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_data['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_data['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_full_info_pet(self):
        with allure.step("Подготовка данных для добавление нового питомца c полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }
        with allure.step("Отправка запроса на добавление нового питомца c полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_data = response.json()

        with allure.step("Проверка статуса ответа и валидация json схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_data, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе c полными данными"):
            assert response_data['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_data['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_data['category']['id'] == payload['category']['id'], "id категории не совпадаетс ожидаемым"
            assert response_data['category']['name'] == payload['category']['name'], "Название категории не совпадает"
            assert response_data['photoUrls'] == payload['photoUrls'], "photoUrls питомца не совпадает с ожидаемым"
            assert response_data['tags'][0]['id'] == payload['tags'][0]['id'], "id тега не совпадает с ожидаемым"
            assert response_data['tags'][0]['name'] == payload['tags'][0]['name'], "Название тега категории не совпадает"
            assert response_data['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet(self, create_pet):
        with allure.step("Получение информации о питомце"):

            pet_id = create_pet["id"]

            updated_pet = {
               "id": pet_id,
               "name": "Petty",
               "status": "sold"
           }

        with allure.step("Отправка запроса на обновление информации о питомце"):
            response = requests.put(f"{BASE_URL}/pet/", json=updated_pet)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка информации о питомце"):
            assert updated_pet["id"] == pet_id, "ID питомца изменился"
            assert updated_pet["name"] == "Petty", "Имя питомца не обновилось"
            assert updated_pet["status"] == "sold", "Статус питомца не обновился"


    @allure.title("Удаление информации о питомце")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение информации о питомце"):
            pet_id = create_pet["id"]

        with allure.step("Удаление питомца"):
            response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка сообщения о удалении питомца"):
            assert response.text == "Pet deleted", "Сообщение об удалении не соответствует ожидаемому"

        with allure.step("Проверка что питомец действительно удален"):
            get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert get_response.status_code == 404, "Питомец не был удален, статус не 404"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code, expected_response_type",
        [
            ("available", 200,list),
            ("pending", 200,list),
            ("sold", 200,list),
            ("",400,str),
            ("abracadabra",400,str),
        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code, expected_response_type):
        with allure.step(f"Отправка запроса на получение питомца по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params= {"status": status})

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == expected_status_code

        with allure.step("Проверка формата данных"):

            if response.status_code == 200:
                assert isinstance(response.json(), list)
            else:
                assert isinstance(response.text, expected_response_type)
                assert "message" in response.json()
                assert "Input error: query parameter `status value" in response.json()["message"]

