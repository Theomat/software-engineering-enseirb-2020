import requests


API_ENDPOINT = 'http://localhost:8080/api/intent'


def test_capital_case():
    assert 'Semaphore' == 'Semaphore'


def test_capital_case_diff():
    assert 'Semaphore' != 'semaphore'


def test_api_up():
    r = requests.get(API_ENDPOINT + '?sentence=hello')
    assert r.status_code == 200
