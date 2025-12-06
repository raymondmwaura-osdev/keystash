# Unit tests for 'add.DuplicatesChecker'.
from src.features.add import DuplicatesChecker
import pytest

@pytest.fixture
def get_credentials():
    return [
        {
            "service": "service1",
            "password": "password1",
            "username": "username1",
            "email": "email1"
        },
        {
            "service": "service2",
            "password": "password2",
            "username": "username2",
            "email": "email2"
        }
    ]

def test_check_exact_duplicate(get_credentials):
    """
    Assert that 'DuplicatesChecker.check_exact_duplicate' returns True
    when an exact duplicate is found, and False otherwise.
    """
    candidate = get_credentials[0]
    return_value = DuplicatesChecker(
        get_credentials, candidate).check_exact_duplicate()
    assert return_value

    candidate = {
        "service": "service3",
        "password": "password3",
        "username": "username3",
        "email": "email3"
    }
    return_value = DuplicatesChecker(
        get_credentials, candidate).check_exact_duplicate()
    assert not return_value
