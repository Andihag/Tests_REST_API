import json

import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """api библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"
        """Магический метод __init__ присваивает всем экземплярам класса PetFriends базовый URL"""


    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API и возвращает статус запроса и результат запроса в формате JSON
        с уникальным ключом пользователя, найденного по указанным email и password"""

        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API и возвращает статус запроса и результат запроса в формате JSON
        со списком найденных питомцев по указанному фильтру"""

        headers = {"auth_key": auth_key["key"]}
        filter = {"filter": filter}

        res = requests.get(self.base_url+"api/pets", headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод добавляет нового питомца и возвращает информацию о добавленном питомце в формате JSON"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })

        headers = {"auth_key": auth_key["key"], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+"api/pets", headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса"""

        headers = {"auth_key": auth_key["key"]}
        res = requests.delete(self.base_url+"api/pets/" + pet_id, headers=headers)
        status = res.status_code
        return status


    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод изменяет информацию о питомце и возвращает обновленную информацию о питомце в формате JSON"""

        headers = {"auth_key": auth_key["key"]}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + "api/pets/" + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод позволяет добавить информацию о новом питомце и возвращает информацию о питомце в формате JSON"""

        headers = {"auth_key": auth_key["key"]}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + "/api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def set_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод позволяет добавить фото питомца к информации о существующем питомце и возвращает информацию
        о питомце в формате JSON"""

        data = MultipartEncoder(
            fields={
                "pet_photo": (pet_photo, open(pet_photo, "rb"), "image/jpg")
            })

        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}

        res = requests.post(self.base_url + "/api/pets/set_photo/" + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result





