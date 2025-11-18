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

def test_check_exact_duplicate(monkeypatch, mocker, tmp_path, capsys):
    """
    Validate that `add.AddCredentials` exits without modifying the vault, when the
    vault contains a credential record exactly matching the new credential.
    """
    # Mocks.
    storage_read_mock = mocker.Mock()
    storage_read_mock.return_value = [cred1, cred2]
    mocker.patch("src.features.add.storage.read_json", storage_read_mock)

    storage_write_mock = mocker.Mock()
    mocker.patch("src.features.add.storage.write_json", storage_write_mock)

    vault = tmp_path / "vault.json"
    vault.touch()
    monkeypatch.setattr("src.features.add.constants.VAULT", vault)

    ##
    with pytest.raises(SystemExit):
        add.AddCredentials(**cred1)

    output = capsys.readouterr()
    assert output.out == "Identical credentials already exist. No changes made.\n"
    assert not storage_write_mock.called

