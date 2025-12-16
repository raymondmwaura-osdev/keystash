from src.utils import helpers

class TestFilterCredentials:
    # Unit tests for 'helpers.filter_credentials'.
    credentials = [
        {
            "service": "service1",
            "password": "password1",
            "username": "username1",
            "email": "email1"
        },
        {
            "service": "service2",
            "password": "password2",
            "username": "username2",
            "email": "email2"
        }
    ]
    def test_exact_duplicate(self):
        """
        Assert that 'filter_credentials' returns an exact duplicate
        of the candidate if it exists in the credentials list.
        """
        candidate = self.credentials[0]
        duplicate = helpers.filter_credentials(self.credentials, **candidate)
        assert duplicate[0] == candidate

    def test_no_fields(self):
        """
        Assert that 'filter_credentials' returns all the credentials
        when none of the filter fields (service, password, username, or email)
        are provided.

        Assert also that 'filter_credentials' returns an empty list when
        all the filter fields are set to None.
        """
        duplicates = helpers.filter_credentials(self.credentials)
        assert duplicates == self.credentials

        duplicates = helpers.filter_credentials(
            self.credentials,
            service=None,
            username=None,
            email=None,
            password=None
        )
        assert duplicates == []
