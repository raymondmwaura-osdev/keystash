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

def test_check_exact_duplicate(credentials, mocker):
    """
    Assert that 'DuplicatesChecker.check_exact_duplicate' exits the program
    when an exact duplicate is found, and returns None otherwise.
    """
    # Exact duplicate present.
    system_exit_mock = mocker.patch("src.features.add.sys.exit")
    candidate = credentials[0]
    DuplicatesChecker(credentials, candidate).check_exact_duplicate()
    system_exit_mock.assert_called_once()

    # Exact duplicate absent.
    system_exit_mock = mocker.patch("src.features.add.sys.exit")
    candidate = credentials[0].copy() # Create shallow copy to preserve 'credentials'.
    candidate["service"] = "different service"
    return_value = DuplicatesChecker(
        credentials, candidate).check_exact_duplicate()
    assert not return_value
    assert not system_exit_mock.called

def test_check_same_everything_different_password(credentials, mocker):
    """
    Assert that 'DuplicatesChecker.check_same_everything_different_password':
        + Returns False when no duplicate is found.
        + Returns True, without editing 'self.new_credentials' when the user
            decides to preserve the existing credential.
        + Prompts the user 3 times and returns True on invalid input.
        + Returns False, and correctly edits 'self.new_credentials' when the
            user decides to overwrite the existing credential.
    """
    # Setup.
    matching_candidate = credentials[0].copy() # Create shallow copy to preserve 'credentials'.
    matching_candidate["password"] = "different password" # Same everything, different password.

    mismatching_candidate = credentials[0].copy()
    mismatching_candidate["service"] = "different service" # Cause service mismatch.

    # Return False when no duplicate is found.
    return_value = DuplicatesChecker(
        credentials, mismatching_candidate).check_same_everything_different_password()
    assert not return_value

    # Return True when user enters "n".
    mocker.patch("src.features.add.input", return_value = "n")
    return_value = DuplicatesChecker(
        credentials, matching_candidate).check_same_everything_different_password()
    assert return_value

    # Call 'input' 3 times and return True with invalid input.
    input_mock = mocker.patch("src.features.add.input", return_value = "invalid")
    return_value = DuplicatesChecker(
        credentials, matching_candidate).check_same_everything_different_password()

    assert input_mock.call_count == 3
    assert return_value

    # Return False and correctly edit `self.new_credentials`.
    input_mock = mocker.patch("src.features.add.input", return_value = "y")
    duplicates_checker_instance = DuplicatesChecker(credentials, matching_candidate)
    return_value = duplicates_checker_instance.check_same_everything_different_password()

    expected_output = credentials[:]
    expected_output[0] = matching_candidate
    assert duplicates_checker_instance.new_credentials == expected_output
    assert not return_value
