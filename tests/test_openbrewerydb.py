import pytest
import requests

from jsonschema import validate


def test_shema_json(fix_get_openbrewerydb_host):
    '''Проверяем структуру json'''

    respons = requests.get('{}{}'.format(fix_get_openbrewerydb_host, 'breweries?by_name=Almanac_Beer_Company'))
    shema = {'type': 'array',
             'tems': {

                 'type': 'object',
                 'property':
                     {
                         'id': {"type": "number"},
                         'brewery_type': {"type": "string"},
                         'street': {"type": "string"},
                         'city': {"type": "string"},
                         'state': {"type": "string"},
                         'postal_code': {"type": "string"},
                         'longitude': {"type": "string"},
                         'latitude': {"type": "string"},
                         'phone': {"type": "string"},
                         'website_url': {"type": "string"},
                         'updated_at': {"type": "string"},
                         'tag_list': {"type": "array"}
                     },
                 "required": ['id', 'brewery_type', 'street', 'city', 'state', 'postal_code', 'longitude', 'latitude',
                              'phone', 'website_url', 'updated_at', 'tag_list']
             }}
    validate(instance=respons.json(), schema=shema)


@pytest.mark.parametrize('state', ['Ohio', 'New_York', 'New_Mexico'])
def test_by_state_req(fix_get_openbrewerydb_host, state):
    '''Проверяем запрос, который возвращает список баров в указанном штате'''
    respons = requests.get('{}{}'.format(fix_get_openbrewerydb_host, 'breweries?by_state=' + state))
    for brewery in respons.json():
        assert brewery['state'] == state.replace('_', ' ')


@pytest.mark.parametrize('type_brewery', [('regional', 20), ('bar', 1), ('large', 20), ('contract', 20)])
def test_by_type_req(fix_get_openbrewerydb_host, type_brewery):
    '''Проверяем сколько создано баров с указанным типом'''
    respons = requests.get('{}{}'.format(fix_get_openbrewerydb_host, 'breweries?by_type=' + type_brewery[0]))
    assert len(respons.json()) == type_brewery[1]


def test_status_code(fix_get_openbrewerydb_host):
    '''Проверяем статус запроса'''
    respons = requests.get('{}{}'.format(fix_get_openbrewerydb_host, 'breweries?by_name=Almanac_Beer_Company'))
    assert respons.status_code == 200


def test_per_page(fix_get_openbrewerydb_host):
    '''Проверяем запрос на отображение заданого числа баров'''
    respons = requests.get('{}{}'.format(fix_get_openbrewerydb_host, 'breweries?per_page=5'))
    assert len(respons.json()) == 5
