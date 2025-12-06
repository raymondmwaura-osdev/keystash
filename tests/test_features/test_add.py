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
