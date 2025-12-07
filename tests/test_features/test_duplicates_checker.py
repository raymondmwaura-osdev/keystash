# Unit tests for 'add.DuplicatesChecker'.
from src.features.add import DuplicatesChecker
import pytest

@pytest.fixture
def credentials():
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

def test_check_exact_duplicate(credentials):
    """
    Assert that 'DuplicatesChecker.check_exact_duplicate' returns True
    when an exact duplicate is found, and False otherwise.
    """
    candidate = credentials[0]
    return_value = DuplicatesChecker(
        credentials, candidate).check_exact_duplicate()
    assert return_value

    candidate = {
        "service": "service3",
        "password": "password3",
        "username": "username3",
        "email": "email3"
    }
    return_value = DuplicatesChecker(
        credentials, candidate).check_exact_duplicate()
    assert not return_value

def test_check_same_everything_different_password(credentials):
    """
    Assert that 'DuplicatesChecker.check_same_everything_different_password':
        + Returns False when no duplicate is found.
        + Returns True, without editing 'self.new_credentials' when the user
            decides to preserve the existing credential.
        + Returns True when the user enters invalid input 3 times.
        + Returns False, and correctly edits 'self.new_credentials' when the
            user decides to overwrite the existing credential.
    """
    # Return False when no duplicate is found.
    candidate = credentials[0].copy() # Create shallow copy to preserve 'credentials'.
    candidate["service"] = "different service"
    return_value = DuplicatesChecker(
        credentials, candidate).check_same_everything_different_password()
    assert not return_value
