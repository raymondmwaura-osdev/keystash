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
        Has at least one uppercase letter, one lowercase letter, and one symbol.
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

def filter_credentials(
    credentials: list[dict],
    *,
    service: str = None,
    password: str = None,
    username: str = None,
    email: str = None,
) -> list[dict]:
    """
    Return a list of entries in 'credentials' with the same values
    as the ones provided ('service', 'password', 'username', 'email').
    Return all the credentials if none of the values are provided.
    """
    filters = {
        "service": service,
        "password": password,
        "username": username,
        "email": email
    }
    
    return [
        cred
        for cred in credentials
        if all(
            cred[key] == value or value == None
            for key, value in filters.items()
        )
    ]

## Classes.
class Add:
    def __init__(self, service: str, username: str, email: str) -> None:
        self.service = service
        password = self.get_password()

        self.candidate = {
            "service": service,
            "password": password,
            "username": username,
            "email": email
        }

        vault_contents = storage.read_vault()
        print(vault_contents)

        new_contents = DuplicatesChecker(self.candidate, vault_contents)

    def get_password(self) -> str:
        """
        Get the password to store from the user or generate one.

        Returns the password as a string.
        """
        print(f"Enter the password for \"{self.service}\".")
        print("Leave blank to generate a random password.")
        password = getpass("Password: ")

        if not password:
            password = generate_password()
            print("Generated a strong password.")

        return password

class DuplicatesChecker:
    """
    Scan the given 'credentials' for credentials that are similar
    to the given 'candidate'.
    Return credentials to write to the vault.

    This class scans the given 'credentials' for credential entries
    similar to the given 'candidate'. Depending on the findings, the
    class will either exit the program or edit and return 'credentials'.

    The returned 'credentials' is will contain the 'candidate' credentials
    and will be ready to be written in the vault file. This will only
    happen if either no duplicate credentials are found, or if the user
    chose to overwrite the duplicate credentials. If duplicate credentials
    exist and the user chose to preserve the already existing credentials,
    the class will exit the program.
    """
    def __init__(self, candidate: dict, credentials: list) -> list:
        self.credentials = credentials
        self.candidate = candidate
        self.new_credentials = []

        check_functions = [
            self.check_exact_duplicate
        ]
        if any(
            function()
            for function in check_functions
        ):
            sys.exit(0)

        return self.new_credentials

    def check_exact_duplicate(self):
        """
        Return True if 'self.credentials' contain an exact duplicate of
        'self.candidate'. Otherwise, return False.
        """
        exact_duplicates = filter_credentials(self.credentials, **self.candidate)
        if len(exact_duplicates) == 1:
            print("Identical credentials already exist! No changes made.")
            return True
        
        return False
