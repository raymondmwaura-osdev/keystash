"""
Take in the following:
    + service
    + username
    + email

Prompt the user for the password to store.
    + Don't echo the password to the terminal.
    + Give the user an option for the program to generate a strong password.

Read the vault.
    + If the vault doesn't exist, create it with an empty list.

Check if duplicate credentials exist in the vault. Act accordingly.
Write the credential to the vault/don't.
Exit.

## Code Logic

+ Have `Add` as the main class.
+ Have other classes to group related functions (e.g. have one class for checking the vault for duplicate credentials).
+ Have standalone functions.
+ The `Add` class should join all the other classes and functions together.
"""
from getpass import getpass
from src.utils import storage
import secrets, string, sys

## Functions.
def build_cli(subparsers):
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument(
        "-s", "--service",
        dest="service", required=True,
        help="Name of the service. Example: 'github.com'."
    )
    add_parser.add_argument(
        "-u", "--username",
        dest="username", required=False, default=None,
        help="Username associated with the account."
    )
    add_parser.add_argument(
        "-e", "--email",
        dest="email", required=False, default=None,
        help="Email associated with the account."
    )

def generate_password():
    """
    Generate and return a strong password.

    Properties:
        Length: 16 characters
        Characters: uppercase and lowercase letters, digits, symbols.
        Avoids the following symbols: `'"\\|<>
        Has at least one uppercase letter, one lowercase letter.
        Has at least 3 numbers.
    """
    password_length = 16
    symbols = "!@#$%^&*()-_=+[]{};:,.?/"
    characters = string.ascii_letters + string.digits + symbols

    while True:
        password = "".join(secrets.choice(characters) for _ in range(password_length))
        # Check password strength.
        if (any(char.isupper() for char in password)
        and any(char.islower() for char in password)
        and sum(char.isdigit() for char in password) >= 3):
            break

    return password

def get_password() -> str:
    """
    Get the password to store from the user or generate one.
    Return the password as a string.
    """
    print(f"Enter the password to store.")
    print("Leave blank to generate a random password.")
    password = getpass("Password: ")

    if not password:
        password = generate_password()
        print("Generated a strong password.")

    return password

def filter_credentials(
    credentials: list[dict],
    *,
    service: str | None = "any",
    password: str | None = "any",
    username: str | None = "any",
    email: str | None = "any",
) -> list[dict]:
    """
    Filter credential records based on explicit matching rules.

    Each record is a dict with keys: 'service', 'password', 'username', and 'email'.

    For each filter field (service, password, username, email), you may provide:
        - An actual value: only credentials with the same value will match.
        - None: only credentials where the field is None will match.
        - "any": the field is ignored and all values match.

    Parameters:
        service, password, username, email:
            The rule for each field. Each must be either:
            - A concrete value (string)
            - None
            - "any"

    Returns:
        A list of all credentials that satisfy all provided rules.
    """
    filters = {
        "service": service,
        "password": password,
        "username": username,
        "email": email
    }

    def matches(cred: dict) -> bool:
        """
        Return True if the given credential matches the
        filter fields. False if they differ.
        """
        return all(
            True if value == "any"
            else cred[key] == value
            for key, value in filters.items()
        )

    return [
        cred
        for cred in credentials
        if matches(cred)
    ]

## Classes.
class Add:
    def __init__(self, service: str, username: str, email: str) -> None:
        password = get_password()
        candidate = {
            "service": service,
            "password": password,
            "username": username,
            "email": email
        }

        vault_contents = storage.read_vault()
        new_contents = DuplicatesChecker(candidate, vault_contents)

class DuplicatesChecker:
    """
    Scan the given 'credentials' for credentials that are similar
    to the given 'candidate'.
    Return credentials to write to the vault.

    This class scans the given 'credentials' for credential entries
    similar to the given 'candidate'. Depending on the findings, the
    class will either exit the program or edit and return 'credentials'.

    The returned 'credentials' will contain the 'candidate' credentials
    and will be ready to be written in the vault file. This will only
    happen if either no duplicate credentials are found, or if the user
    chose to overwrite the duplicate credentials. If duplicate credentials
    exist and the user chose to preserve the already existing credentials,
    the class will exit the program.
    """
    def __init__(self, credentials: list, candidate: dict) -> list:
        self.credentials = credentials
        self.candidate = candidate
 
    def check_all(self):
        """
        Run all duplicate checks and return the final credentials to write
        to the vault.
        """
        check_duplicate_functions = [
            self.check_exact_duplicate
        ]
        if any(
            function()
            for function in check_duplicate_functions
        ):
            sys.exit(0)

        return self.credentials

    def check_exact_duplicate(self):
        """
        Return True if 'self.credentials' contain an exact duplicate of
        'self.candidate'. Otherwise, return False.
        """
        exact_duplicate = filter_credentials(self.credentials, **self.candidate)
        if exact_duplicate:
            print("Identical credentials already exist! No changes made.")
            return True
        
        return False

    def check_same_everything_different_password(self):
        """
        Handle password update when a credential exists with the same
        service, username, and email, but different password.

        If the credential exists, the user will be prompted on whether
        to update or discard the password.

        Return True and edit `self.credentials` if the user decides
        to preserve the existing password.
        Return False if the user decides to update the password.
        """
        duplicate = filter_credentials(
            self.credentials,
            service=self.candidate["service"],
            username=self.candidate["username"],
            email=self.candidate["email"]
        )
