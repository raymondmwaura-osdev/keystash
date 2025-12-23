import pathlib

MASTER_PASSWORD = None	# Will contain the master password provided by the user.

DATA_DIR = pathlib.Path().home() / ".local/share/keystash"
VAULT = DATA_DIR / "vault"
HASH = DATA_DIR / "hash"
