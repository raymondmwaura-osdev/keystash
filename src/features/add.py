"""
Add credentials to the vault.
"""

from getpass import getpass
from src.utils import storage
import secrets, string

def build_cli(subparsers):
    """
    Define the command-line interface options for the
    'add' command.
    """
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

def add(service: str, username: str, email: str) -> None:
    """
    Add credential to the vault.

    This function takes the service, password, username, and
    email, and writes them to the vault. The service, username
    and email are passed as parameters. The user is securely
    prompted for the password.
    """
    password = get_password()
    candidate = {
        "service": service,
        "password": password,
        "username": username,
        "email": email
    }

    vault_contents = storage.read_vault()
    vault_contents.append(candidate)
    storage.write_vault(vault_contents)

def get_password() -> str:
    """
    Get the password to store from the user or generate one.
    Return the password as a string.
    """
    print("Enter the password to store.")
    print("Leave blank to generate a random password.")
    password = getpass("Password: ")

    if not password:
        password = generate_password()
        print("Generated a strong password.")

    return password

def generate_password():
    """
    Generate and return a strong password.

    Properties:
        Length: 16 characters
        Characters: uppercase and lowercase letters, digits, symbols.
        Avoids the following symbols: `'"\\|<>
        Has at least one uppercase letter and one lowercase letter.
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
