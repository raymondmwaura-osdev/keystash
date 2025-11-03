
from toolbox import crypto_utils
import pathlib, base64, json

def read_json(file: pathlib.Path, encrypted: bool = True, master_password: bytes = None) -> list | dict:
    """
    Read the given JSON file.
    The function converts the contents from a string to a Python object.
    The return value can be a list or a dictionary depending on the JSON file.
    The 'encrypted' parameter indicates if the contents of the JSON file are encrypted or not.
    If the contents are encrypted, 'master_password' must be provided. It will be used
    to decrypt the contents of the file. If the file is not encrypted, 'master_password' should be
    None.
    """
    pass

def write_json(
    contents: list | dict,
    file: pathlib.Path,
    encrypt: bool = True,
    master_password: bytes = None
):
    """
    Serialize and write JSON data to a file, optionally encrypting the contents.

    This function converts the given Python object (a list or dictionary) into
    a JSON-formatted string and writes it to the specified file. If encryption
    is enabled, the JSON string is first encrypted using a key derived from the
    provided master password. The salt and ciphertext are Base64-encoded and
    written to the file as a single text record in the format:

        <base64(salt)>:<base64(ciphertext)>

    Parameters:
        contents (list | dict): The data to serialize as JSON.
        file (pathlib.Path): The path to the target JSON file.
        encrypt (bool, optional): Whether to encrypt the data before writing.
            Defaults to True.
        master_password (bytes, optional): The master password used to derive
            the encryption key when `encrypt` is True. Must be provided if
            encryption is enabled; should be None otherwise.

    Raises:
        ValueError: If `encrypt` is True but no master password is provided.
        TypeError: If `contents` is not serializable as JSON.

    Notes:
        - When encryption is disabled, the JSON text is written in plaintext.
        - When encryption is enabled, the resulting file is not valid JSON
          but a text-encoded cryptographic container that must be decrypted
          before parsing as JSON.
    """
    contents = json.dumps(contents)

    if encrypt and master_password:
        salt, encrypted_contents = crypto_utils.encrypt(contents.encode("utf-8"), master_password)

        # Make salt and encrypted data safe for writing to file.
        # This is done by base64 encoding then converting to string.
        salt = base64.b64encode(salt).decode("utf-8")
        encrypted_contents = base64.b64encode(encrypted_contents).decode("utf-8")

        final = f"{salt}:{encrypted_contents}"
        file.write_text(final)

    elif encrypt and not master_password:
        raise ValueError("'master_password' is required when 'encrypt == True'.")

    else:
        file.write_text(contents)
