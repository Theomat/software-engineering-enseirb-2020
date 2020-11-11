import pytest
import requests


API_ENDPOINT = 'http://ec2-35-180-41-68.eu-west-3.compute.amazonaws.com:8080/api/intent'

def test_capital_case():
    assert 'Semaphore' == 'Semaphore'


def test_capital_case_diff():
    assert 'Semaphore' != 'semaphore'

def test_api_up():
    r = requests.get(API_ENDPOINT + '?sentence=hello')
    assert r.status_code == 200
