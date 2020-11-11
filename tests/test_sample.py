import pytest
import requests


def test_capital_case():
    assert 'Semaphore' == 'Semaphore'


def test_capital_case_diff():
    assert 'Semaphore' != 'semaphore'

def test_api_up():
    r = requests.get('http://localhost:8080/api/intent?sentence=trouve des toilettes')
    assert r.status_code == 200
