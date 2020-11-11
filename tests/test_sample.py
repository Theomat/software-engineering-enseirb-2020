import pytest

def test_capital_case():
    assert 'Semaphore' == 'Semaphore'


def test_capital_case_diff():
    assert 'Semaphore' != 'semaphore'