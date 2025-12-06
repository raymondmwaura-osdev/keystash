# Unit tests for `src.features.add.py`.
from src.features import add
import string

def test_generate_password():
    """
    Assert that `add.generate_password` returns a strong password.
    The password must have:
        + Not less than 16 characters.
        + At least one uppercase and one lowercase letter.
        + At least 3 numbers.
    """
    password = add.generate_password()
    
    assert (
        len(password) >= 16 and
        any(char.isupper() for char in password) and
        any(char.islower() for char in password) and
        sum(char.isdigit() for char in password) >= 3
    )

class TestFilterCredentials:
    # Unit tests for 'add.filter_credentials'.
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
        Assert that 'add.filter_credentials' returns exact duplicates
        of the candidate, found in the credentials list.
        """
        candidate = self.credentials[0]
        duplicate = add.filter_credentials(self.credentials, **candidate)
        assert duplicate[0] == candidate

    def test_no_fields(self):
        """
        Assert that 'add.filter_credentials' returns all the credentials
        when none of the filter fields (service, password, username, or email)
        are provided.
        """
        duplicates = add.filter_credentials(self.credentials)
        assert duplicates == self.credentials
