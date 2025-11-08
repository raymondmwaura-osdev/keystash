import pathlib

MASTER_PASSWORD = None	# Will contain user input.
VAULT = pathlib.Path().home() / ".local/share/keystash/vault.json"