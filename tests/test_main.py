# Unit tests for `src.main`.
from src import main
import pytest, bcrypt

class TestVerifyIdentity:
    """Unit tests for 'main.verify_identity'."""
    @pytest.fixture
    def password_fixture(self):
        """Return a password string and its hash."""
        password = "StrongPassword123"
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        return password, password_hash

    @pytest.fixture
    def hash_file_mock(self, mocker, password_fixture):
        """Mock and return 'src.main.constants.HASH'."""
        password, password_hash = password_fixture
        
        mock = mocker.patch("src.main.constants.HASH")
        mock.exists.return_value = True
        mock.read_text.return_value = password_hash.decode("utf-8")

        return mock

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
        
    def test_verify_identity_success_first_attempt(self, mocker, password_fixture, hash_file_mock):
        """Test successful verification on first password attempt."""
        # Setup
        password = password_fixture[0]
        mocker.patch("src.main.getpass", return_value=password)
        
        # Execute
        result = main.verify_identity(None)
        
        # Assert
        assert result == password
        hash_file_mock.exists.assert_called_once()
        hash_file_mock.read_text.assert_called_once()

    def test_verify_identity_success_third_attempt(self, mocker, password_fixture, hash_file_mock):
        """Test successful verification on third password attempt."""
        # Setup
        password = password_fixture[0]
        mocker.patch("src.main.getpass", side_effect=["wrong1", "wrong2", password])
        mock_print = mocker.patch("builtins.print")
        
        # Execute
        result = main.verify_identity(None)
        
        # Assert
        assert result == password
        assert mock_print.call_count == 2
        mock_print.assert_any_call("Incorrect master password!")
