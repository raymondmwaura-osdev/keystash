from src.utils import constants
from src.features import add
import argparse, getpass

# Build CLI.
parser = argparse.ArgumentParser(prog="KeyStash")
subparsers = parser.add_subparsers(dest="cmd")

build_cli_functions = [add.build_cli]
for build_cli in build_cli_functions:
    build_cli(subparsers)

cli_args = parser.parse_args()

# Get master password.
constants.MASTER_PASSWORD = getpass.getpass("Enter master password: "
    ).encode(encoding="utf-8")

# Features.
if cli_args.cmd == "add":
    add.Add(
        service=cli_args.service,
        username=cli_args.username,
        email=cli_args.email
    )
