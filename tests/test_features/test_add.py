# Unit tests for `src.features.add.py`.
from src.features import add
import pytest

def test_generate_password():
    """
    Assert that `add.generate_password` returns a strong password.
    The password must have:
        + Not less than 16 characters.
        + At least one uppercase and one lowercase letter.
        + At least 3 numbers.
    """
    password = add.generate_password()
    
    assert (
        len(password) >= 16 and
        any(char.isupper() for char in password) and
        any(char.islower() for char in password) and
        sum(char.isdigit() for char in password) >= 3
    )

class TestGetPassword:
    # Unit tests for 'add.get_password'.
    @pytest.fixture
    def get_password_mock(self, mocker):
        """
        Setup mocks for methods in this class.
        """
        getpass_mock = mocker.patch("src.features.add.getpass")
        generate_password_mock = mocker.patch(
            "src.features.add.generate_password",
            return_value="StrongPassword123"
        )
        
        return getpass_mock, generate_password_mock

    def test_get_password_without_input(self, get_password_mock):
        """
        Assert that 'add.get_password' generates and returns a strong
        password when no password is entered by the user.
        """
        getpass_mock, generate_password_mock = get_password_mock
        getpass_mock.return_value = ""

        password = add.get_password()
        assert password == "StrongPassword123"
        generate_password_mock.assert_called_once()

    def test_get_password_with_input(self, get_password_mock):
        """
        Assert that 'add.get_password' returns the password
        entered by the user.
        """
        getpass_mock, generate_password_mock = get_password_mock
        getpass_mock.return_value = "password123"

        password = add.get_password()
        assert password == "password123"
        assert not generate_password_mock.called

class TestFilterCredentials:
    # Unit tests for 'add.filter_credentials'.
    credentials = [
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
    def test_exact_duplicate(self):
        """
        Assert that 'add.filter_credentials' returns exact duplicates
        of the candidate, found in the credentials list.
        """
        candidate = self.credentials[0]
        duplicate = add.filter_credentials(self.credentials, **candidate)
        assert duplicate[0] == candidate

    def test_no_fields(self):
        """
        Assert that 'add.filter_credentials' returns all the credentials
        when none of the filter fields (service, password, username, or email)
        are provided.
        """
        duplicates = add.filter_credentials(self.credentials)
        assert duplicates == self.credentials
