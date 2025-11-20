# Functional Requirements

## Credential Management

### Add Credentials

**Goal:** Allow the user to create new credential records.
**Requirements:**
The system shall allow the user to add a new credential containing:

* service (required)
* password (required)
* username (optional)
* email (optional)

+ The system shall validate that required fields are provided before accepting the credential.
+ The system shall support future extensibility by allowing new optional fields without breaking existing records.

### Update Credentials

**Goal:** Allow the user to modify existing credentials.
**Requirements:**

+ The system shall allow the user to update the password, username, or email of an existing credential.
+ The system shall validate that the target credential exists before performing any updates.
+ The system shall maintain referential consistency by replacing the previous encrypted record with the modified encrypted record.

### View Credentials

**Goal:** Allow the user to view stored credentials securely.
**Requirements:**

+ The system shall display all non-sensitive fields (service, username, email).
+ The system shall not display passwords in plaintext unless explicitly requested.
+ The system shall support copying the password directly to the system clipboard instead of displaying it.
+ The system shall decrypt credentials only for the time required to read or copy them.

### Remove Credentials

**Goal:** Allow the user to permanently delete stored credentials.
**Requirements:**

+ The system shall allow the user to delete a credential record by specifying the service name.
+ The system shall require explicit confirmation by having the user retype the service name before deletion proceeds.
+ The system shall remove the credential such that it is unrecoverable from the vault file.
+ The system shall rewrite and re-encrypt the vault file after deletion to ensure no remnants remain.

---

## Secure Storage and Encryption

### Encryption

**Goal:** Ensure all stored credential data is protected at rest.
**Requirements:**

+ The system shall encrypt all credential data using AES.
+ The system shall derive the encryption key from a user-provided password using a secure key-derivation function.
+ The system shall require the user to enter the master password for both encryption and decryption operations.
+ The system shall never store the master password or raw encryption key in plaintext.
+ The system shall encrypt the entire vault file, not individual fields.

### Decryption

**Goal:** Restrict access to stored credentials.
**Requirements:**

+ The system shall decrypt the vault file only when the correct master password is provided.
+ The system shall fail safely and not reveal any decrypted content if the password is incorrect.
+ The system shall minimize the time decrypted data remains in memory.

### Vault File Management

**Goal:** Provide a single secure storage container.
**Requirements:**

+ The system shall store all credentials in a single encrypted vault file.
+ The system shall ensure file-level integrity when writing, updating, or deleting entries.
+ The system shall use file permissions that restrict access to the OS user account.

---

## User Interaction

### Input Handling

**Goal:** Ensure predictable and safe user input.
**Requirements:**

+ The system shall provide cli options to enter required fields during credential creation.
+ The system shall allow the user to enter the password without displaying it in plain text.
+ The system shall prompt the user for confirmation during destructive operations.
+ The system shall prompt the user for the master password on every operation requiring access to encrypted content.

### CLI Experience

**Goal:** Provide a simple, command-driven interface.
**Requirements:**

+ The system shall expose commands for add, update, view, remove, and other core functions.
+ The system shall provide clear success and error messages.
+ The system shall fail gracefully on invalid input.

---

## Future Features (Non-essential but planned)

### Backup

**Requirements:**

+ The system shall support generating a backup copy of the vault file.
+ The system shall allow the user to select the backup destination.
+ The system shall update the backup after each modification to the vault.
+ The system shall support cloud backup integrations beginning with Google Drive.

### Password Age Reminder

**Requirements:**

+ The system shall track timestamps for when each credential is added or last updated.
+ The system shall notify the user when a credential exceeds a configurable age threshold.
+ The system shall support future policies (e.g., forced rotation) without breaking existing data.

### Password Generation

**Requirements:**

+ The system shall provide a built-in password generator capable of producing strong, random passwords.
+ The system shall allow the user to configure password length.
+ The system shall allow the user to select character classes (uppercase letters, lowercase letters, digits, symbols).
+ The system shall ensure all generated passwords meet modern entropy standards for secure credentials.

---
