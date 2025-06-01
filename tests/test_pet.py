import allure
import requests
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
            response.json = response.json()

        with allure.step("Проверка статуса ответа и валидация json схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response.json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response.json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

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
            response.json = response.json()

        with allure.step("Проверка статуса ответа и валидация json схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе c полными данными"):
            assert response.json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response.json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response.json['category']['id'] == payload['category']['id'], "id категории не совпадаетс ожидаемым"
            assert response.json['category']['name'] == payload['category']['name'], "Название категории не совпадает"
            assert response.json['photoUrls'] == payload['photoUrls'], "photoUrls питомца не совпадает с ожидаемым"
            assert response.json['tags'][0]['id'] == payload['tags'][0]['id'], "id тега не совпадает с ожидаемым"
            assert response.json['tags'][0]['name'] == payload['tags'][0]['name'], "Название тега категории не совпадает"
            assert response.json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"
