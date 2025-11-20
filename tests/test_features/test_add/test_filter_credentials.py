from src.features import add

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

    def test_empty_parameters(self):
        """
        Validate that `add.filter_credentials` returns all credentials
        when no filter field is provided.
        """
        input_cred = [cred1, cred2]
        output_cred = add.filter_credentials(input_cred)

        assert output_cred == input_cred

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
        assert output_cred == [cred1]

    def test_same_everything_different_password(self):
        """
        Test that `add.filter_credentials` returns credentials matching all
        specified fields except the password when the password argument is
        not provided.
        """
        input_cred = [cred1, cred2]
        output_cred = add.filter_credentials(
            input_cred,
            service=cred1["service"],
            username=cred1["username"],
            email=cred1["email"]
        )
        assert output_cred == [cred1]
