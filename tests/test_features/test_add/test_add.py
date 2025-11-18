"""
Unit tests for `src.features.add.AddCredentials`.
"""
from src.features import add
import pytest

cred1 = {
    "service": "service1",
    "password": "password1",
    "username": "username1",
    "email": "email1"
    }
cred2 = {
    "service": "service2",
    "password": "password2",
    "username": "username2",
    "email": "email2"
}

## FIXTURES.
@pytest.fixture
def my_mocks(mocker, tmp_path, monkeypatch):
    """
    Create mocks of functions and objects used in `AddCredentials`.
    """
    storage_read_mock = mocker.Mock(
        return_value = [cred1, cred2]
    )
    mocker.patch("src.features.add.storage.read_json", storage_read_mock)

    storage_write_mock = mocker.Mock()
    mocker.patch("src.features.add.storage.write_json", storage_write_mock)

    vault = tmp_path / "vault.json"
    vault.touch()
    monkeypatch.setattr("src.features.add.constants.VAULT", vault)

    return storage_read_mock, storage_write_mock, vault

@pytest.fixture
def storage_write_mock(my_mocks):
    """
    Set up mocks and return only the mock for 'storage.write_json'.
    """
    return my_mocks[1]

## Test Functions
def test_check_exact_duplicate(storage_write_mock, capsys):
    """
    Validate that `add.AddCredentials` exits without modifying the vault, when the
    vault contains a credential record exactly matching the new credential.
    """
    with pytest.raises(SystemExit):
        add.AddCredentials(**cred1)

    output = capsys.readouterr()
    assert output.out == "Identical credentials already exist. No changes made.\n"
    assert not storage_write_mock.called
