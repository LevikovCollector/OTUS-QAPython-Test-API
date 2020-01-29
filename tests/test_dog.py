import pytest
import requests

from jsonschema import validate


def test_singl_req(dog_host):
    '''Проверяем запрос на получение одной фотографии. Проверяем схему json'''
    respons = requests.get('{}{}'.format(dog_host, 'breeds/image/random'))
    shema = {
        'type': 'object',
        'property':
            {
                'message': {"type": "string"},
                'status': {"type": "string"}
            },
        "required": ['message', 'status']
    }
    validate(instance=respons.json(), schema=shema)


@pytest.mark.parametrize('dog_count', [2, 4, 6])
def test_random_req(dog_host, dog_count):
    '''Проверяем запрос на получение нескольких фотографий. Проверяем количество фотографий в поле message'''
    respons = requests.get('{}{}'.format(dog_host, 'breeds/image/random/' + str(dog_count)))
    all_message = respons.json()['message']
    assert len(all_message) == dog_count


@pytest.mark.parametrize('dog_breed', [('hound', ["afghan", "basset", "blood", "english", "ibizan", "plott", "walker"]),
                                       ('bulldog', ["boston", "english", "french"])])
def test_sub_breeds(dog_host, dog_breed):
    '''Проверяем запрос на получение списка подпород собак'''
    respons = requests.get('{}{}'.format(dog_host, 'breed/' + dog_breed[0] + '/list'))
    message = respons.json()['message']

    assert message == dog_breed[1]


def test_status_code(dog_host):
    '''Проверяем статус запроса'''
    respons = requests.get('{}{}'.format(dog_host, 'breeds/image/random'))
    assert respons.status_code == 200


def test_status_param(dog_host):
    '''Проверяем значение поля status'''
    respons = requests.get('{}{}'.format(dog_host, 'breeds/image/random'))
    assert respons.json()['status'] == 'success'
