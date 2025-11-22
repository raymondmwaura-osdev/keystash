# Duplicate Detection Scenarios for Credential Addition

## Primary Identifier Assumption

Each credential entry is represented as a dictionary containing:

```python
{
    "service": str,
    "username": str | None,
    "email": str | None,
    "password": str
}
```

The `service` field acts as the primary identifier, while `username` and `email` further disambiguate individual accounts under the same service.

---

## Exact Duplicate

**Condition:**
An entry already exists with identical values for `service`, `username`, `email`, and `password`.

**Behavior:**

* The new credential is reported as an existing entry.
* Recommended action: Display a message such as

  ```
  [i] Identical credentials already exist. No changes made.
  ```
* No modification to the vault is necessary.

---

## Same Service, Same Username/Email, Different Password

**Condition:**
The service name matches an existing entry, and either the username or email also matches, but the password differs.

**Behavior:**

* This indicates that the user may have changed the password for the same account.
* Prompt the user to confirm whether to overwrite the old password:

  ```
  [!] A credential for 'github.com' with username 'johndoe' already exists.
  Overwrite existing password? (y/n):
  ```
* If confirmed, update the password field of the existing entry.
* If declined, abort the addition.

---

## Same Service, Different Username or Email

**Condition:**
The `service` matches an existing entry, but both the `username` and `email` differ.

**Behavior:**

* Multiple accounts for the same service are permitted.
* Append the new credential to the vault without modification to existing entries.
* Example message:

  ```
  [✓] Added another account for 'github.com'.
  ```

---

## Same Service, No Username or Email Provided

**Condition:**
The user provides only the `service` and `password`, and an entry for the same service already exists (with or without username/email).

**Behavior:**

* Ambiguous case: It is unclear whether this is a new account or an update.
* The program should prompt:

  ```
  [!] A credential for 'github.com' already exists.
  Add as a new entry or overwrite existing? (new/overwrite/cancel):
  ```
* If `overwrite`, replace the entire entry.
* If `new`, append the new one as a separate record.
* If `cancel`, do nothing.

---

## Same Service, Same Username, Different Email

**Condition:**
`service` and `username` match, but the `email` differs.

**Behavior:**

* Treat this as a possible alternate contact email for the same account.
* Optionally prompt the user to:

  * Update the existing record with the new email.
  * Store the credential with both emails.

---

## Same Service, Same Email, Different Username

**Condition:**
`service` and `email` match, but the `username` differs.

**Behavior:**

* May indicate that the user changed the username for the same service.
* Prompt the user on whether to update the existing credential, or cancel the operation.

---

## Same Service, Different Email and Username, Same Password

**Condition:**
Only `service` and `password` match.

**Behavior:**

* Likely coincidental or reused password.
* No action required; add as a new entry.

---


## New Service

**Condition:**
No existing entry for the specified `service`.

**Behavior:**

* Add the new entry without prompt.
* Confirm success:

  ```
  [✓] Credentials for 'example.com' added successfully.
  ```

---
