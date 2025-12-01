from src.utils import constants, storage
from datetime import date
import pathlib, json, sys

def build_cli(subparsers):
    """
    Build the CLI for the 'add' command.
    """
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("-s", "--service", dest="service", required=True)

    username_group = add_parser.add_mutually_exclusive_group(required=False)
    username_group.add_argument("-u", "--username", dest="username")
    username_group.add_argument("--nousername", dest="no_username", action="store_true")

    email_group = add_parser.add_mutually_exclusive_group(required=False)
    email_group.add_argument("-e", "--email", dest="email")
    email_group.add_argument("--noemail", dest="no_email", action="store_true")

class AddCredentials:
    def __init__(
        self,
        service: str,
        password: str,
        username: str,
        email: str
    ):
        vault_encrypted = True
        self.service = service
        self.password = password
        self.username = username
        self.email = email
        self.credentials = {
            "service": self.service,
            "password": self.password,
            "username": self.username,
            "email": self.email,
            "date": date.today().strftime("%Y-%m-%d")
        }

        if not constants.VAULT.exists():
            # Initialize VAULT with an empty list (not encrypted).
            vault_encrypted = False
            constants.VAULT.parent.mkdir(parents=True, exist_ok=True)
            constants.VAULT.write_text(
                json.dumps([])
            )

        self.vault_contents = storage.read_json(
            file=constants.VAULT,
            encrypted=vault_encrypted,
            master_password=constants.MASTER_PASSWORD
        )

        # Scan the vault for duplicates.
        duplicate_scans = [
            self.check_exact_duplicate,
            self.check_same_everything_different_password
        ]
        if any(
            scan()
            for scan in duplicate_scans
        ):
            sys.exit()
        
        # Write if no duplicates are found.
        storage.write_json(
            contents=self.credentials,
            file=constants.VAULT,
            encrypted=True,
            master_password=constants.MASTER_PASSWORD
        )

    def check_exact_duplicate(self) -> bool:
        """
        Determine whether an identical credential entry already exists in the vault.

        
        This method evaluates the vault’s stored credentials against
        the candidate credential set (`self.credentials`). If one or
        more exact duplicates are identified, the method reports the
        condition and returns `True`; otherwise, it returns `False`.

        Returns:
            bool: `True` if an exact duplicate exists.
                  `False` if no identical credential entry is present.
        """
        duplicate_credentials = filter_credentials(
            self.vault_contents,
            self.service,
            self.password,
            self.username,
            self.email
        )

        if not duplicate_credentials: return False

        print("Identical credentials already exist. No changes made.")
        return True

    def check_same_everything_different_password(self) -> bool:
        """
        Check whether the vault contains a credential matching the input
        attributes but using a different password.

        The lookup keys are: service, username, and email from `self.credentials`.
        If a match is identified, the user is prompted to authorize an overwrite.

        Return False when the user approves the overwrite or when no matching
        credential exists. Return True when the user declines the overwrite.
        """
        similar_credentials = filter_credentials(
            self.vault_contents,
            service=self.service,
            username=self.username,
            email=self.email
        )
        
        if not similar_credentials: return False

        # Prompt the user.
        if self.username and self.email:
            output = f"A credential for '{self.service}' with username '{self.username}' and email '{self.email}' already exist."
        elif self.username:
            output = f"A credential for '{self.service}' with username '{self.username}' already exists."
        elif self.email:
            output = f"A credential for '{self.service}' with email '{self.email}' already exists."
        else:
            output = f"A credential for '{self.service}' already exists."
        
        print(output)
        while True:
            user_instruction = input("Overwrite existing pasword? (y/n): ")
            if user_instruction.lower() == 'y': return False
            elif user_instruction.lower() == 'n': return True

def filter_credentials(
    credentials: list[dict],
    service: str | None = None,
    password: str | None = None,
    username: str | None = None,
    email: str | None = None
    ) -> list[dict]:
    """
    Return all credentials from `credentials` that match
    all non-None provided fields.

    Parameters:
        credentials (list[dict]): A list of credential dictionaries.
        service (str, optional): Service name to match.
        password (str, optional): Password to match.
        username (str, optional): Username to match.
        email (str, optional): Email to match.

    Returns:
        list[dict]: A list of all credential dictionaries matching
        the given search criteria. Returns 'credentials' if no match is found.
    """
    filters = {
        "service": service,
        "password": password,
        "username": username,
        "email": email,
    }

    return [
        cred
        for cred in credentials
        if all(
            value is None or cred.get(field) == value
            for field, value in filters.items()
        )
    ]
