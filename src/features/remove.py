"""
Remove a credential from the vault.
"""
from src.utils import storage
import sys

def build_cli(subparsers):
    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument(
        dest="id",
        help="ID of the credential to remove. Use 'keystash search' to get it."
    )

def remove(id: int) -> None:
    """
    Remove the credential with the given ID from the vault. Do nothing
    if no credential with the given ID exists.

    Parameters:
        id: An integer ID of the credential to remove.
    """
    credentials = storage.read_vault()
    for cred in credentials:
        if cred["id"] == id:
            target = cred
            break
    else:
        print(f"No credential with id {id} found!")
        sys.exit()

    print("Removing the following credential:")
    print()
    for key, value in target.items():
        if key == "password":
            continue

        print(f"{key.capitalize()}: {value}")
    
    for _ in range(3):
        confirmation = input("Confirm (y/n): ")
        if confirmation.lower() in ["y", "n"]:
            break
    else:
        print("Confirmation failed. Not removing credential.")
        sys.exit()

    if confirmation.lower() == "n":
        print("Not removing credential.")
        sys.exit()

    credentials.remove(target)
    storage.write_vault(credentials)
    print("Credential removed successfully.")

