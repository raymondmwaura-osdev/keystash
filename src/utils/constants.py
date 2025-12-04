import pathlib

MASTER_PASSWORD = None	# Will contain the master password provided by the user.
VAULT = pathlib.Path().home() / ".local/share/keystash/vault.json"
