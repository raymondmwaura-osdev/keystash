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
    Provide a mock environment for 'AddCredentials'. Includes:
        + A temporary vault file injected into the constants module.
        + A stubbed JSON reader returning known credentials.
        + A stubbed JSON writer capturing write attempts.

    Returns a tuple containing (storage_read_mock, storage_write_mock).
    """
    vault = tmp_path / "vault.json"
    vault.touch()
    monkeypatch.setattr("src.features.add.constants.VAULT", vault)

    storage_read_mock = mocker.Mock(
        return_value = [cred1, cred2]
    )
    mocker.patch("src.features.add.storage.read_json", storage_read_mock)

    storage_write_mock = mocker.Mock()
    mocker.patch("src.features.add.storage.write_json", storage_write_mock)

    return storage_read_mock, storage_write_mock

@pytest.fixture
def storage_write_mock(my_mocks):
    """
    Set up the mock environment using the 'my_mocks' fixture and return
    only the mocked JSON writer. Useful for tests that test usage of the
    JSON write function.
    """
    return my_mocks[-1]

## Test Functions
def test_check_exact_duplicate(storage_write_mock, capsys):
    """
    Validate that `add.AddCredentials` exits without modifying the vault, when the
    vault contains a credential record exactly matching the new credential.

    Validates:
        + Termination using SystemExit.
        + Correct output displayed.
        + No modifications to the vault.
    """
    with pytest.raises(SystemExit):
        add.AddCredentials(**cred1)

    output = capsys.readouterr()
    assert output.out == "Identical credentials already exist. No changes made.\n"
    assert not storage_write_mock.called

class TestSameEverythingDifferentPassword:
    """
    Unit tests for when the vault contains a credential that matches
    all the fields of the input credential except the password.
    """
    def test_overwrite(self, mocker, storage_write_mock):
        """
        Validate that confirming the overwrite ("y") results in a
        single write operation to the vault.
        """
        # Mocks.
        input_mock = mocker.Mock()
        input_mock.return_value = 'y'
        mocker.patch("src.features.add.input", input_mock)

        add.AddCredentials(
            service=cred1["service"],
            password="different password",
            username=cred1["username"],
            email=cred1["email"]
        )

        storage_write_mock.assert_called_once()

    def test_no_overwrite(self, mocker, storage_write_mock):
        """
        Validate that declining the overwrite ("n") prevents any vault
        modification and terminates the program.
        """
        # Mocks.
        input_mock = mocker.Mock()
        input_mock.return_value = 'n'
        mocker.patch("src.features.add.input", input_mock)
        
        with pytest.raises(SystemExit):
            add.AddCredentials(
                service=cred1["service"],
                password="different password",
                username=cred1["username"],
                email=cred1["email"]
            )

        assert not storage_write_mock.called
