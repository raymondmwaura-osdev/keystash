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

class TestAddCredentials:
    """Unit tests for `add.AddCredentials`."""
    def test_check_exact_duplicate(self, monkeypatch, mocker, tmp_path, capsys):
        """
        Validate that `add.AddCredentials` triggers a termination path when the vault
        contains a credential record matching all primary key fields.
        """
        storage_read_mock = mocker.Mock()
        storage_read_mock.return_value = [cred1, cred2]
        mocker.patch("src.features.add.storage.read_json", storage_read_mock)

        vault = tmp_path / "vault.json"
        vault.touch()
        monkeypatch.setattr("src.features.add.constants.VAULT", vault)

        sys_exit_mock = mocker.Mock()
        sys_exit_mock.side_effect = SystemExit
        mocker.patch("src.features.add.sys.exit", sys_exit_mock)
        
        with pytest.raises(SystemExit):
            add.AddCredentials(**cred1)
        sys_exit_mock.assert_called_once()

        output = capsys.readouterr()
        assert output.out == "Identical credentials already exist. No changes made.\n"

class TestFilterCredentials:
    """Unit tests for `add.filter_credentials`."""
    def test_empty_credentials(self):
        """
        Validate that `add.filter_credentials` provides an empty list
        when the input credential set contains no records.
        """
        input_cred = []
        output_cred = add.filter_credentials(
            input_cred,
            **cred1
        )

        assert output_cred == []

    def test_exact_duplicate(self):
        """
        Confirm that `add.filter_credentials` isolates and returns only
        the credential entry that matches all supplied fields.
        """
        input_cred = [cred1, cred2]
        output_cred = add.filter_credentials(
            input_cred,
            **cred1
        )
        expected_output = [cred1]

        assert output_cred == expected_output
