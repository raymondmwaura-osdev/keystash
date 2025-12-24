# Unit tests for `src.features.get`.
from src.features import get
import pytest

class TestGet:
    """Unit tests for 'get.get'."""
    def test_empty_credentials(self, mocker, capsys):
        """
        Verify that 'get' exits when an invalid ID is given or
        when the credentials list is empty.
        """
        storage_read_mock = mocker.patch(
            "src.features.get.storage.read_vault",
            return_value = []
        )

        with pytest.raises(SystemExit):
            get.get(328)

        output = capsys.readouterr()
        assert "No credential with ID 328 found!" in output.out

    def test_valid_input(self, mocker, capsys):
        """
        Verify that 'get' copies the password to clipboard when a valid
        ID is given.
        """
        copy_mock = mocker.patch("src.features.get.pyperclip.copy")
        storage_read_mock = mocker.patch(
            "src.features.get.storage.read_vault",
            return_value = [{
                "service": "service1",
                "password": "StrongPassword123",
                "username": None,
                "email": None,
                "id": 123
            }]
        )

        get.get(123)

        copy_mock.assert_called_with("StrongPassword123")

        output = capsys.readouterr()
        assert "Password copied to clipboard." in output.out
