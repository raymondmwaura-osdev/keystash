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
import secrets, string
import storage

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

## Classes.
class Add:
    def __init__(self, service: str, username: str, email: str) -> None:
        self.service = service
        self.username = username
        self.email = email
        self.password = self.get_password()

        self.vault_contents = storage.read_vault()

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
