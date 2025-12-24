"""
Copy a password to the clipboard.
"""
from src.utils import storage
import pyperclip, sys

def build_cli(subparsers):
    get_subparser = subparsers.add_parser("get")
    get_subparser.add_argument("id",
        help="The ID of the credential with the desired password."
    )

def get(id: int) -> None:
    """
    Copy the password in the credential with the given ID to the clipboard.
    Do nothing if no credential with the given ID exists or if the credentials
    list is empty.
    """
    credentials = storage.read_vault()

    for cred in credentials:
        if cred["id"] == id:
            target = cred
            break
    else:
        print(f"No credential with ID {id} found!")
        sys.exit()

    pyperclip.copy(target["password"])
    print("Password copied to clipboard.")
