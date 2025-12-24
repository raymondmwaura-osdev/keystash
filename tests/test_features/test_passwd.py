# Unit tests for `src.features.passwd`.
from src.features import passwd

class TestPasswd:
    # Unit tests for `passwd.passwd`.
    def test_unmatching_passwords(self, mocker):
        """
        Verify `passwd` will prompt for the password a maximum
        of 3 times before exiting the program.
        """
        # Mocks.
        getpass_mock = mocker.patch("src.features.passwd.getpass")
        getpass_mock.side_effect = [str(i) for i in range(6)] # Return a different password with each call.
        sys_exit_mock = mocker.patch("src.features.passwd.sys.exit")

        passwd.passwd()

        assert getpass_mock.call_count == 6
        sys_exit_mock.assert_called_once()

    def test_matching_passwords(self, mocker):
        """
        Assert that 'passwd', when given matching passwords:
            + Does not call 'sys.exit'.
            + Generates the password hash.
            + Saves the hash to disk.
        """
        getpass_mock = mocker.patch(
            "src.features.passwd.getpass",
            return_value="master_password"
        )
        sys_exit_mock = mocker.patch("src.features.passwd.sys.exit")
        hashpw_mock = mocker.patch(
            "src.features.passwd.bcrypt.hashpw",
            return_value=b"password_hash"
        )
        hash_mock = mocker.patch("src.features.passwd.constants.HASH")

        passwd.passwd()

        assert not sys_exit_mock.called
        hash_mock.write_text.assert_called_with("password_hash")
