# Unit tests for `src.main`.
from src import main
import pytest, bcrypt

class TestInteractiveMode:
    """Unit tests for `main.interactive_mode`."""
    def test_interactive_mode_exit_command(self, mocker):
        """Test that 'exit' command terminates the loop."""
        mock_input = mocker.patch('builtins.input', return_value='exit')
        
        with pytest.raises(SystemExit):
            parser = mocker.Mock()
            main.interactive_mode(parser)
        
        mock_input.assert_called_once_with("(keystash) ")

    def test_interactive_mode_quit_command(self, mocker):
        """Test that 'quit' command terminates the loop."""
        mock_input = mocker.patch('builtins.input', return_value='quit')
        
        with pytest.raises(SystemExit):
            parser = mocker.Mock()
            main.interactive_mode(parser)
            
        mock_input.assert_called_once_with("(keystash) ")

    def test_interactive_mode_empty_command(self, mocker):
        """Test that empty input is skipped and continues loop."""
        mock_input = mocker.patch('builtins.input', side_effect=['', 'exit'])
        
        with pytest.raises(SystemExit):
            parser = mocker.Mock()
            main.interactive_mode(parser)
        
        assert mock_input.call_count == 2

    def test_interactive_mode_whitespace_command(self, mocker):
        """Test that whitespace-only input is skipped."""
        mock_input = mocker.patch('builtins.input', side_effect=['   ', '\t', 'exit'])
        
        with pytest.raises(SystemExit):
            parser = mocker.Mock()
            main.interactive_mode(parser)
        
        assert mock_input.call_count == 3

    def test_interactive_mode_valid_command(self, mocker):
        """Test that valid commands are parsed and executed."""
        parser = mocker.Mock()
        mock_namespace = mocker.Mock()
        parser.parse_args.return_value = mock_namespace
        
        mock_input = mocker.patch('builtins.input', side_effect=['add -s service', 'exit'])
        mock_run_command = mocker.patch('src.main.run_command')
        
        with pytest.raises(SystemExit):
            main.interactive_mode(parser)
        
        parser.parse_args.assert_called_once_with(['add', '-s', 'service'])
        mock_run_command.assert_called_once_with(mock_namespace)

    def test_interactive_mode_invalid_command_continues(self, mocker):
        """Test that SystemExit from argparse is caught and loop continues."""
        parser = mocker.Mock()
        parser.parse_args.side_effect = SystemExit()
        
        mock_input = mocker.patch('builtins.input', side_effect=['invalid --bad-flag', 'exit'])
        mock_run_command = mocker.patch("src.main.run_command")
        
        with pytest.raises(SystemExit):
            main.interactive_mode(parser)
        
        assert parser.parse_args.call_count == 1
        mock_run_command.assert_not_called()
        assert mock_input.call_count == 2

    def test_interactive_mode_multiple_commands(self, mocker):
        """Test executing multiple valid commands before exit."""
        parser = mocker.Mock()
        namespace1 = mocker.Mock()
        namespace2 = mocker.Mock()
        namespace3 = mocker.Mock()
        parser.parse_args.side_effect = [namespace1, namespace2, namespace3]
        
        mock_input = mocker.patch('builtins.input', 
            side_effect=['cmd1', 'cmd2 -f value', 'cmd3 --flag value', 'exit'])
        mock_run_command = mocker.patch('src.main.run_command')
        
        with pytest.raises(SystemExit):
            main.interactive_mode(parser)
        
        assert parser.parse_args.call_count == 3
        parser.parse_args.assert_any_call(['cmd1'])
        parser.parse_args.assert_any_call(['cmd2', '-f', 'value'])
        parser.parse_args.assert_any_call(['cmd3', '--flag', 'value'])
        
        assert mock_run_command.call_count == 3
        mock_run_command.assert_any_call(namespace1)
        mock_run_command.assert_any_call(namespace2)
        mock_run_command.assert_any_call(namespace3)

    def test_interactive_mode_command_with_multiple_args(self, mocker):
        """Test that commands with multiple arguments are split correctly."""
        parser = mocker.Mock()
        mock_namespace = mocker.Mock()
        parser.parse_args.return_value = mock_namespace
        
        mock_input = mocker.patch('builtins.input', 
            side_effect=['set key value --option flag', 'exit'])
        mock_run_command = mocker.patch('src.main.run_command')
        
        with pytest.raises(SystemExit):
            main.interactive_mode(parser)
        
        parser.parse_args.assert_called_once_with(['set', 'key', 'value', '--option', 'flag'])
        mock_run_command.assert_called_once_with(mock_namespace)

    def test_interactive_mode_mixed_valid_invalid_commands(self, mocker):
        """Test handling mix of valid commands, invalid commands, and empty input."""
        parser = mocker.Mock()
        valid_namespace = mocker.Mock()
        parser.parse_args.side_effect = [valid_namespace, SystemExit, valid_namespace]
        
        mock_input = mocker.patch('builtins.input', 
            side_effect=['valid', '', 'invalid', 'valid2', 'exit'])
        mock_run_command = mocker.patch('src.main.run_command')
        
        with pytest.raises(SystemExit):
            main.interactive_mode(parser)
        
        assert mock_input.call_count == 5
        assert parser.parse_args.call_count == 3
        assert mock_run_command.call_count == 2

class TestVerifyIdentity:
    """Unit tests for 'main.verify_identity'."""
    @pytest.fixture(scope="class")
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
        password = password_fixture[0]
        mocker.patch("src.main.getpass", return_value=password)
        
        result = main.verify_identity(None)
        
        assert result == password
        hash_file_mock.exists.assert_called_once()
        hash_file_mock.read_text.assert_called_once()

    def test_verify_identity_success_third_attempt(self, mocker, password_fixture, hash_file_mock):
        """Test successful verification on third password attempt."""
        password = password_fixture[0]
        mocker.patch("src.main.getpass", side_effect=["wrong1", "wrong2", password])
        mock_print = mocker.patch("builtins.print")
        
        result = main.verify_identity(None)
        
        assert result == password
        assert mock_print.call_count == 2
        mock_print.assert_any_call("Incorrect master password!")

    def test_verify_identity_fails_after_three_attempts(self, mocker, hash_file_mock):
        """Test that system exits after three incorrect password attempts."""
        mocker.patch("src.main.getpass", return_value="wrong_password")
        mock_print = mocker.patch("builtins.print")
        
        with pytest.raises(SystemExit):
            main.verify_identity(None)
        
        assert mock_print.call_count == 3
        mock_print.assert_called_with("Incorrect master password!")

    def test_verify_identity_no_hash_file_non_passwd_command(self, mocker):
        """Test exit when hash file doesn't exist and command is not 'passwd'."""
        mock_hash = mocker.patch("src.main.constants.HASH")
        mock_hash.exists.return_value = False
        
        mock_print = mocker.patch("builtins.print")
        
        with pytest.raises(SystemExit):
            main.verify_identity(None)
        
        mock_hash.exists.assert_called_once()
        assert mock_print.call_count == 2
        mock_print.assert_any_call("Master password not set.")
        mock_print.assert_any_call("Use 'keystash passwd' to set the master password.")

    def test_verify_identity_no_hash_file_passwd_command(self, mocker):
        """Test that function returns normally when hash doesn't exist but command is 'passwd'."""
        mock_hash = mocker.patch("src.main.constants.HASH")
        mock_hash.exists.return_value = False
        
        mock_print = mocker.patch("builtins.print")
        mock_exit = mocker.patch("src.main.sys.exit")
        
        result = main.verify_identity("passwd")
        
        assert result is None
        mock_hash.exists.assert_called_once()
        mock_print.assert_not_called()
        mock_exit.assert_not_called()

    def test_verify_identity_strips_whitespace(self, mocker, password_fixture, hash_file_mock):
        """Test that password whitespace is properly stripped."""
        password, password_hash = password_fixture
        hash_file_mock.read_text.return_value = f"  {password_hash.decode('utf-8')}  \n"
        
        mocker.patch("src.main.getpass", return_value=f"  {password}  ")
        
        result = main.verify_identity(None)
        
        assert result == password

    def test_verify_identity_empty_password_input(self, mocker, password_fixture, hash_file_mock):
        """Test behavior with empty password input."""
        password, password_hash = password_fixture
        
        mocker.patch("src.main.getpass", side_effect=["", "", password])
        mock_print = mocker.patch("builtins.print")
        
        result = main.verify_identity(None)
        
        assert result == password
        assert mock_print.call_count == 2
