from api import PetFriends
from settings import valid_email, valid_password, incorrect_key
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_list_of_pets(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_all_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_create_pet_simple_without_photo(name='Милена',  animal_type='Сиамская', age=1 ):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_post_add_photo_to_pet(pet_photo='images/rysch_kot.jpg'):

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_all_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][1]['id']

    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_photo_to_pet(auth_key, pet_photo, pet_id)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['id'] == pet_id
    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Негативный тест (неверный api-ключ)
def test_FAILD_get_list_of_pets_with_incorrect_key(filter=''):
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        assert auth_key == incorrect_key

# Негативный тест (пустые поля логин и пароль):
def test_FAILD_get_api_key_for_empty_user_data(email='', password=''):
        status, result = pf.get_api_key(email, password)

        if len(email or password) == 0:
            assert status == 200
        else:
            raise Exception('Data is invalid. Please use correct data for new user.')

#Проверим, что все обязательные поля для обновления информации заполнены корректно.
def test_update_pet_info(name='Боренька', animal_type='Кот', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_all_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][4]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, name,animal_type,age)
    if len(name and animal_type) > 0 and int(age):
        assert result['animal_type'] == animal_type
    else:
        raise Exception('All fields must be completed')
