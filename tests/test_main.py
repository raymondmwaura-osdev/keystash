# Unit tests for `src.main`.
from src import main
import pytest

class TestVerifyIdentity:
    """Unit tests for 'main.verify_identity'."""
    def test_no_hash(self, mocker, capsys):
        """
        Assert that 'main.verify_identity' prints a message and exits when
        'constants.HASH' doesn't exist and 'cmd' is None.

        Assert that 'main.verify_identity' does not exit when 'constants.HASH'
        doesn't exist and 'cmd' is "passwd".
        """
        sys_exit_mock = mocker.patch("src.main.sys.exit")
        hash_mock = mocker.patch("src.main.constants.HASH")
        hash_mock.exists.return_value = False

        # cmd == "passwd"
        main.verify_identity("passwd")
        assert not sys_exit_mock.called

        # cmd != "passwd"
        main.verify_identity(None)
        
        output = capsys.readouterr()
        assert "Master password not set." in output.out
        sys_exit_mock.assert_called()
        
    def test_correct_password(self, mocker):
        pass

    def test_incorrect_password_three_times(self, mocker):
        pass
