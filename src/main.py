from src.features import add, search, passwd
from src.utils import constants, storage
from getpass import getpass
import argparse, sys, bcrypt

# Build CLI.
parser = argparse.ArgumentParser(prog="KeyStash")
subparsers = parser.add_subparsers(dest="cmd")

build_cli_functions = [
    add.build_cli,
    search.build_cli,
    passwd.build_cli
]
for build_cli in build_cli_functions:
    build_cli(subparsers)

cli_args = parser.parse_args()

# Verify user identity.
if constants.HASH.exists():
    password_hash = constants.HASH.read_bytes()
    for _ in range(3):
        password = getpass("Enter master password: ")
        
        if bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash
        ):
            constants.MASTER_PASSWORD = password
            break

        print("Incorrect master password!")

    else: sys.exit()

elif cli_args.cmd != "passwd": # Allow the user to use only 'passwd' when constants.HASH doesn't exist.
    print("Master password not set.")
    print("Use 'keystash passwd' to set the master password.")
    sys.exit()

# Features.
if cli_args.cmd == "add":
    add.add(
        service=cli_args.service,
        username=cli_args.username,
        email=cli_args.email
    )

elif cli_args.cmd == "search":
    search.search(
        service=cli_args.service,
        username=cli_args.username,
        email=cli_args.email
    )

elif cli_args.cmd == "passwd":
    passwd.passwd()
