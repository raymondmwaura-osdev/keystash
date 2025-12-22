"""
This module provides functions for reading and writing files with support
for symmetric encryption and decryption.

Encrypted data is stored in a text-safe format using Base64 encoding to
ensure compatibility across different storage systems.
The file contents are stored as a single Base64-encoded record
in the following format:

    <base64(salt)>:<base64(ciphertext)>
"""
from src.utils import crypto_utils, constants
import base64, json, pathlib

# Ensure the vault directory exists.
vault_dir = pathlib.Path.home() / ".local/share/keystash"
vault_dir.mkdir(parents=True, exist_ok=True)

def read_vault() -> list:
    """
    Read, decrypt, and return vault contents. Return an empty list if the vault
    doesn't exist.

    The function expects the vault contents to follow the format produced by
    `write_vault()`:

        <base64(salt)>:<base64(ciphertext)>
    """
    try:
        contents = constants.VAULT.read_text()
        salt, encrypted_content = contents.split(":")
    # Return an empty list if the vault doesn't exist.
    except FileNotFoundError:
        return []

    # Convert salt and contents from printable ASCII string to
    # their original binary form.
    # `str.encode` changes the string to a bytes object and
    # `base64.b64decode` changes the bytes object from a printable
    # bytes string to the original binary.
    salt = base64.b64decode(
        salt.encode("utf-8")
    )
    encrypted_content = base64.b64decode(
        encrypted_content.encode("utf-8")
    )

    contents = crypto_utils.decrypt(
        encrypted_content, salt
    ).decode("utf-8")

    return json.loads(contents)

def write_vault(contents: list) -> None:
    """
    Encrypt, then write the given contents to the vault file.

    Parameters:
        contents:
            A list optionally containing credential dictionaries.

    Format:
        <base64(salt)>:<base64(ciphertext)>
    """
    # Encrypt.
    contents = json.dumps(contents)
    salt, encrypted_contents = crypto_utils.encrypt(contents.encode("utf-8"))

    # Make salt and encrypted data safe for writing to file.
    salt = base64.b64encode(salt).decode("utf-8")
    encrypted_contents = base64.b64encode(encrypted_contents).decode("utf-8")

    final_content = f"{salt}:{encrypted_contents}"
    constants.VAULT.write_text(final_content)
