# Unit tests for `src.features.remove`.
from src.features import remove
from io import StringIO
import pytest
import sys

class TestRemoveCredential:
    """Unit tests for `remove.remove`."""
    @pytest.fixture
    def sample_credentials(self):
        return [
            {"id": 111, "username": "user1", "password": "pass1", "service": "email"},
            {"id": 222, "username": "user2", "password": "pass2", "service": "github"},
            {"id": 333, "username": "user3", "password": "pass3", "service": "aws"},
        ]

    @pytest.fixture
    def mock_storage(self, mocker, sample_credentials):
        storage_mock = mocker.patch("src.features.remove.storage")
        storage_mock.read_vault.return_value = sample_credentials

        return storage_mock

    def test_successful_removal_with_y_confirmation(
        self, mocker, mock_storage, capsys, sample_credentials
    ):
        """Test successful credential removal when user confirms with 'y'"""
        mocker.patch("builtins.input", return_value="y")

        remove.remove(222)

        assert len(sample_credentials) == 2
        assert not any(cred["id"] == 222 for cred in sample_credentials)

        mock_storage.write_vault.assert_called_once_with(sample_credentials)

        captured = capsys.readouterr()
        assert "Removing the following credential:" in captured.out
        assert "Username: user2" in captured.out
        assert "Service: github" in captured.out
        assert "password" not in captured.out.lower() or "Password:" not in captured.out
        assert "Credential removed successfully." in captured.out

    def test_successful_removal_with_Y_confirmation(
        self, mocker, sample_credentials, mock_storage
    ):
        """Test successful removal with uppercase 'Y' confirmation"""
        mocker.patch("builtins.input", return_value="Y")

        remove.remove(111)

        assert len(sample_credentials) == 2
        assert not any(cred["id"] == 111 for cred in sample_credentials)
        mock_storage.write_vault.assert_called_once()

    def test_cancellation_with_n_confirmation(
        self, mocker, sample_credentials, mock_storage, capsys
    ):
        """Test that removal is cancelled when user enters 'n'"""
        mocker.patch("builtins.input", return_value="n")

        with pytest.raises(SystemExit):
            remove.remove(222)

        assert len(sample_credentials) == 3
        assert any(cred["id"] == 222 for cred in sample_credentials)

        mock_storage.write_vault.assert_not_called()

        captured = capsys.readouterr()
        assert "Not removing credential." in captured.out

    def test_cancellation_with_N_confirmation(
        self, mocker, sample_credentials, mock_storage
    ):
        """Test cancellation with uppercase 'N'"""
        mocker.patch("builtins.input", return_value="N")

        with pytest.raises(SystemExit):
            remove.remove(222)

        assert len(sample_credentials) == 3
        mock_storage.write_vault.assert_not_called()

    def test_invalid_confirmation_three_times(
        self, mocker, sample_credentials, mock_storage, capsys
    ):
        """Test that invalid input three times results in failure"""
        input_mock = mocker.patch("builtins.input", side_effect=["invalid", "x", "maybe"])

        with pytest.raises(SystemExit):
            remove.remove(222)

        assert len(sample_credentials) == 3
        mock_storage.write_vault.assert_not_called()
        assert input_mock.call_count == 3

        captured = capsys.readouterr()
        assert "Confirmation failed. Not removing credential." in captured.out

    def test_invalid_then_valid_confirmation(
        self, mocker, sample_credentials, mock_storage
    ):
        """Test that valid input after invalid input works"""
        mocker.patch("builtins.input", side_effect=["invalid", "y"])

        remove.remove(222)

        assert len(sample_credentials) == 2
        mock_storage.write_vault.assert_called_once()

    def test_credential_not_found(
        self, mocker, sample_credentials, mock_storage, capsys
    ):
        """Test behavior when credential ID doesn't exist"""
        with pytest.raises(SystemExit):
            remove.remove(9)

        assert len(sample_credentials) == 3
        mock_storage.write_vault.assert_not_called()

        captured = capsys.readouterr()
        assert "No credential with id 9 found!" in captured.out

    def test_empty_credentials_list(self, capsys, mock_storage):
        """Test behavior with empty credentials list"""
        mock_storage.read_vault.return_value = []

        with pytest.raises(SystemExit):
            remove.remove(111)

        captured = capsys.readouterr()
        assert "No credential with id 111 found!" in captured.out
