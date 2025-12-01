# `add`

Allow the user to add a new credential to the encrypted vault file. Each entry must include a service name and password, and may optionally include a username and email.

---

## Functional Requirements

+ Support these options:
    - `-s` / `--service` (required): Name of the service (e.g., `github.com`).
    - `-u` / `--username` (optional): Username for the service.
    - `-e` / `--email` (optional): Email associated with the account.
    - `--nousername` (default): Specify that no username is associated with the entry.
    - `--noemail` (default): Specify that no email is associated with the entry.
+ `--username` and `--nousername` are mutually exclusive. The same applies to `--email` and `--noemail`.
+ If neither `-u` nor `--nousername` is provided, assume `--nousername`. Apply the same rule for `-e` and `--noemail`.
+ Prompt the user securely for the `master_password`, which encrypts and decrypts the vault.
+ Prompt the user securely for the service password. Do not show it on the terminal.
+ Provide an option to generate a strong password automatically.
+ Check the vault for duplicate or conflicting credentials before saving. Depending on the case, reject, overwrite, or prompt the user. The scenarios are described below.
+ If the vault file does not exist, create it and store the encrypted entry.
+ Encrypt all vault contents before saving.

---

## Handling Duplicates

### Primary Identifier Assumption

Each credential entry uses this structure:

```json
{
    "service": str,
    "password": str,
    "username": str | None,
    "email": str | None,
}
```

The `service` field is the primary identifier. The `username` and `email` fields further distinguish entries under the same service.

**Note:**
If the user omits either the username or email, assume that the missing field matches any existing entry for the same service and provided fields.
For example: if the user provides a service and username but no email, and an existing entry has the same service and username, assume the email also matches.

---

### Exact Duplicate

**Condition:**
An entry already exists with identical `service`, `username`, `email`, and `password`.

**Behavior:**

* Notify the user that the credential already exists.
* Suggested message:

  ```
  [i] Identical credentials already exist. No changes made.
  ```
* Do not modify the vault.

---

### Same Everything, Different Password

**Conditions:**
One of the following holds:

* Same service, username, and email.
* Same service and username, no email.
* Same service and email, no username.
* Same service with neither username nor email.

**Behavior:**

* Treat this as a password update for an existing account.
* Prompt the user:

  ```
  [!] A credential for 'github.com' with username 'johndoe' already exists.
  Overwrite existing password? (y/n):
  ```
* If confirmed, update the password.
* If declined, cancel the operation.

---

### Same Password

**Condition:**
The same password is already used by another entry, regardless of service, username, or email.

**Behavior:**

* Warn the user that the password is reused.
* Offer to generate a new strong password:

  * If accepted, generate and apply it.
  * If refused, save the provided password and warn about the security risk.

---

### Same Service

* **Same service and username, different email**

  * This may indicate an email change.
  * Ask whether to overwrite the existing email or store both.
  * Act according to the user’s choice.

* **Same service and email, different username**

  * This may indicate a username change or multiple accounts using the same email.
  * Ask whether to overwrite the existing entry or create an additional one.
  * Act according to the user’s choice.

* **Same service, different username and email**

  * Treat this as a new account under the same service.
  * Store the new credential.

---

## New Service

**Condition:**
No entry exists for the specified service.

**Behavior:**

* Add the new credential without prompting.
* Show confirmation:

  ```
  [✓] Credentials for 'example.com' added successfully.
  ```

---
