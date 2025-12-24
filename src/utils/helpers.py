def filter_credentials(
    credentials: list[dict],
    *,
    service: str | None = "any",
    password: str | None = "any",
    username: str | None = "any",
    email: str | None = "any"
) -> list[dict]:
    """
    Filter credential records based on explicit matching rules.

    Each record is a dict with keys: 'service', 'password', 'username', and 'email'.

    For each filter field (service, password, username, email), you may provide:
        - An actual value: only credentials with the same value will match.
        - None: only credentials where the field is None will match.
        - "any": the field is ignored and all values match.

    Parameters:
        credentials:
            A list of credential dictionaries with the following keys:
                service, password, username, and email.

        service, password, username, email:
            The rule for each field. Each must be either:
            - A concrete value (string)
            - None
            - "any"

    Returns:
        A list of all credentials that satisfy all provided rules.
    """
    filters = {
        "service": service,
        "password": password,
        "username": username,
        "email": email
    }

    def matches(cred: dict) -> bool:
        """
        Return True if the given credential matches the
        filter fields. False if they differ.
        """
        return all(
            True if value == "any"
            else cred[key] == value
            for key, value in filters.items()
        )

    return [
        cred
        for cred in credentials
        if matches(cred)
    ]

