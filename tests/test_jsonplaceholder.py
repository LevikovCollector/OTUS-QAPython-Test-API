import pytest
import requests

from jsonschema import validate


def test_shema_json(jsonplaceholder_host):
    '''Проверяем структуру json'''
    respons = requests.get('{}{}'.format(jsonplaceholder_host, 'posts/1'))
    shema = {
        'type': 'object',
        'property': {'userId': 'number',
                     'id': 'number',
                     'title': 'string',
                     'body': 'string',
                     },
        'required': ['userId', 'id', 'title', 'body']
    }
    validate(instance=respons.json(), schema=shema)


@pytest.mark.parametrize('polls', [('test1', 'body_text1', 1), ('test2', 'body_text2', 2)])
def test_create_post(jsonplaceholder_host, polls):
    '''Проверяем метод POST'''
    sent_poll = {'title': polls[0],
                 'body': polls[1],
                 'userId': polls[2]
                 }
    respons = requests.post('{}{}'.format(jsonplaceholder_host, 'posts'), json=sent_poll)
    assert respons.status_code == 201
    assert respons.json()['id'] == 101


@pytest.mark.parametrize('polls', [('test3', 'body_text3', 3, 1), ('test4', 'body_text4', 4, 2)])
def test_update_post(jsonplaceholder_host, polls):
    '''Проверяем метод PUT'''
    up_poll = {'title': polls[0],
               'body': polls[1],
               'userId': polls[2],
               'id': polls[3]
               }
    respons = requests.put('{}{}'.format(jsonplaceholder_host, 'posts/' + str(polls[3])), json=up_poll)

    assert respons.json()['id'] == polls[3]


def test_delete_post(jsonplaceholder_host):
    '''Проверяем метод DELETE'''
    respons = requests.delete('{}{}'.format(jsonplaceholder_host, 'posts/1'))

    assert respons.ok
    assert respons.json() == {}


def test_get_post_list_by_user_id(jsonplaceholder_host):
    '''Проверяем количество постов пользователя'''
    respons = requests.get('{}{}'.format(jsonplaceholder_host, 'posts?userId=1'))
    assert len(respons.json()) == 10
