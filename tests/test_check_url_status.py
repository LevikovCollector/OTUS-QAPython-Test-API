import requests


def test_check_status_code(param_from_user):
    '''Проверяем статус запроса по заданному url'''
    respons = requests.get(param_from_user[0])
    assert str(respons.status_code) == param_from_user[1]
