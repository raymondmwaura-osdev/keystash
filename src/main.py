"""
Interactive mode plans:
    If cli_args.cmd == None, enter interactive mode.
    If the user runs keystash with a specific command, run the command and exit.
    If the user runs a specific command and uses the `-i/--interactive` flag, execute the command then enter interactive mode.
    The `-i/--interactive` flag should only be on the main parser, not in every command's subparser.
"""
from src.features import add, search, passwd, remove, get
from src.utils import constants, storage
from getpass import getpass
import argparse, sys, bcrypt

def build_cli():
    """
    Setup all CLI commands and options.

    Return the top level parser got by `argparse.ArgumentParser()`.
    """
    parser = argparse.ArgumentParser(prog="KeyStash")
    subparsers = parser.add_subparsers(dest="cmd")

    build_cli_functions = [
        add.build_cli,
        search.build_cli,
        passwd.build_cli,
        remove.build_cli,
        get.build_cli
    ]
    for build_cli in build_cli_functions:
        build_cli(subparsers)

    return parser

def verify_identity(cmd: None | str) -> str:
    """
    Verify user identity by prompting for the master password.

    Parameters:
        cmd:
            The cli command passed in by the user.

    Return the password if the user is verified, exit otherwise.
    Exit if the master password is not set and 'cmd' != "passwd".
    """
    if constants.HASH.exists():
        password_hash = constants.HASH.read_text().strip()
        for _ in range(3):
            password = getpass("Enter master password: ").strip()

            if bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8")
            ):
                return password

            print("Incorrect master password!")

        sys.exit()

    elif cmd != "passwd": # Allow the user to use only 'passwd' when constants.HASH doesn't exist.
        print("Master password not set.")
        print("Use 'keystash passwd' to set the master password.")
        sys.exit()

def main():
    parser = build_cli()
    cli_args = parser.parse_args()
    constants.MASTER_PASSWORD = verify_identity(cli_args.cmd)

    if cli_args.cmd == None:
        # Call interactive mode function.
        pass

    else:
        # Call a function that handles only one command.
        handle_one_command(cli_args.cmd)

def handle_one_command(cmd):
    """
    Run one command passed in from the user and exit.
    """
    if cmd == "add":
        add.add(
            service=cli_args.service,
            username=cli_args.username,
            email=cli_args.email
        )

    elif cmd == "search":
        search.search(
            service=cli_args.service,
            username=cli_args.username,
            email=cli_args.email
        )

    elif cmd == "passwd":
        passwd.passwd()

    elif cmd == "remove":
        remove.remove(int(cli_args.id))

    elif cmd == "get":
        get.get(int(cli_args.id))

if __name__ == "__main__":
    main()
