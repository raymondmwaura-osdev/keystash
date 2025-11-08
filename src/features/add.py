from src.utils import constants, storage
from datetime import date
import pathlib, json

def add_password(service: str, password: str, username: str, email: str):
    vault_encrypted = True
    credentials = {
        "service": service,
        "password": password,
        "username": username,
        "email": email
    }

    if not constants.VAULT.exists():
        # Initialize with an empty dictionary.
        vault_encrypted = False

        constants.VAULT.parent.mkdir(parents=True, exist_ok=True)
        constants.VAULT.write_text(
            json.dumps({})
        )

    vault_contents = storage.read_json(
        file=constants.VAULT,
        encrypted=vault_encrypted,
        master_password=constants.MASTER_PASSWORD
    )

    # TODO: Check if duplicates exist.

    today_date = date.today().strftime("%Y-%m-%d")
    vault_contents[today_date] = credentials
    storage.write_json(
        contents=vault_contents,
        file=constants.VAULT,
        encrypt=True,
        master_password=constants.MASTER_PASSWORD
    )