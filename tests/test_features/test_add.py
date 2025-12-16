# Unit tests for `src.features.add`.
from src.features import add
import pytest

def test_add(mocker):
    """
    Assert that `add.add` adds the new credentials to the vault.
    """
    vault_contents = [
        {
            "service": "service1",
            "username": "username1",
            "email": "email1",
            "password": "password1"
        }
    ]
    new_credential = {
        "service": "service2",
        "username": "username2",
        "email": "email2",
        "password": "password2"
    }
    expected_output = vault_contents[:]
    expected_output.append(new_credential)

    mocker.patch("src.features.add.get_password", return_value=new_credential["password"])
    mocker.patch("src.features.add.storage.read_vault", return_value=vault_contents)
    write_vault_mock = mocker.patch("src.features.add.storage.write_vault")

    add.add(
        new_credential["service"],
        new_credential["username"],
        new_credential["email"]
    )

    write_vault_mock.assert_called_with(expected_output)

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

