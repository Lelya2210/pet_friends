from api import PetFriends
from settings import valid_email, valid_password
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
    #status, result = pf.post_add_photo_to_pet(auth_key, pet_photo, pet_id)
    #assert status == 200
    #assert result['id'] == pet_id

    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_photo_to_pet(auth_key, pet_photo, pet_id)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['id'] == pet_id
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")