"""
This module provides functions for reading and writing files with support
for symmetric encryption and decryption.

Encrypted data is stored in a text-safe format using Base64 encoding to
ensure compatibility across different storage systems.
The file contents are stored as a single Base64-encoded record
in the following format:

    <base64(salt)>:<base64(ciphertext)>

Functions:
    - read_vault():
        Read, decrypt, and return vault contents.
"""

from src.utils import crypto_utils, constants
import base64, json

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
        encrypted_content,
        constants.MASTER_PASSWORD,
        salt
    ).decode("utf-8")

    return json.loads(contents)
