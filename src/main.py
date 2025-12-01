from src.utils import constants
from src.features import add
import argparse, getpass

# Build CLI.
parser = argparse.ArgumentParser(prog="KeyStash")
subparsers = parser.add_subparsers(dest="cmd")

features_cli = [add]
for feature in features_cli:
    feature.build_cli(subparsers)

args = parser.parse_args()
constants.MASTER_PASSWORD = getpass.getpass("Enter master password: "
    ).encode(encoding="utf-8")
if args.cmd == "add":
    AddCredentials(
        service=args.service,
        password=args.password,
        username=args.username,
        email=args.email
    )
