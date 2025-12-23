"""
Change the master password.

Functions:
    build_cli: Define command-line options used by this feature.

    passwd: Prompt the user for the new master password, hash it, then save it.
"""
from src.utils import constants
from getpass import getpass
import bcrypt, sys

def build_cli(subparsers):
    subparsers.add_parser("passwd")

def passwd():
    """
    Prompt the user for the new master password, hash it, then save it.

    The user is prompted to enter the new master password twice. If the two
    inputs don't match, the user is prompted again, a maximum of 3 times.
    If the user enters unmatching passwords 3 times, the program exits and
    the new master password is not saved.

    Note: Echo is turned off. The password typed by the user will not be
    visible on the terminal.

    The password hash is stored in 'constants.HASH'.
    """
    print("Setting master password.")
    for _ in range(3):
        new_password = getpass("Enter new master password: ")
        new_password2 = getpass("Enter new master password again: ")

        if new_password == new_password2: break

        print("Passwords don't match.")

    else:
        print("New master password not saved.")
        sys.exit()

    # Save password hash.
    password_hash = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    )
    constants.HASH.write_bytes(password_hash)
