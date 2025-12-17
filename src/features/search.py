from src.utils import storage, helpers

def build_cli(subparsers):
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument(
        "-s", "--service",
        dest="service", required=False, default="any",
        help="Only show credentials with the specified service."
    )
    search_parser.add_argument(
        "-u", "--username",
        dest="username", required=False, default="any",
        help="Only show credentials with the specified username."
    )
    search_parser.add_argument(
        "-e", "--email",
        dest="email", required=False, default="any",
        help="Only show credentials with the specified email."
    )

def search(service: str, username: str, email: str) -> None:
    credentials = storage.read_vault()
    matching_credentials = helpers.filter_credentials(
        credentials, service=service,
        username=username, email=email
    )

    if not matching_credentials:
        print("No matching credentials found!")

    for credential in matching_credentials:
        print()
        for key, value in credential.items():
            if key == "password": continue

            print(f"{key.capitalize()}: {value}")
