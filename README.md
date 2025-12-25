# KeyStash

KeyStash is a lightweight CLI password manager that securely stores your passwords locally. KeyStash stores your passwords and credentials in an encrypted vault file located at `~/.local/share/keystash`.

---

## Installation

Install directly from the repository:

```sh
pip install git+https://github.com/raymondmwaura-osdev/KeyStash.git@v0.1.0 # Specify your desired version
```

This will:
+ Clone the repository
+ Build the wheel
+ Install the wheel

Alternatively, you can download a prebuilt wheel for your desired version and run:

```sh
pip install keystash-0.1.0-py3-none-any.whl
```

---

## Usage

### Set Master Password

Immediately after installation, run `keystash passwd` to set your master password.

Expected output:

```
$ keystash passwd
Setting master password.
Enter new master password:
Enter new master password again:
Master password set successfully!
```

The master password is used to verify your identity and generate a key for encrypting and decrypting the vault. **Don't forget this password.** There is currently no way to recover your credentials without the master password. Account recovery functionality will be implemented in a future release.

### Add Credentials

To add credentials to the vault, use `keystash add`:

```
$ keystash add -s github.com -u sample_username123 -e email@example.com
Enter master password:
Enter the password to store.
Leave blank to generate a random password.
Password:
Generated a strong password.
Credential saved successfully!
```

+ `-s` specifies the service (required), `-u` specifies the username (optional), `-e` specifies the email (optional)
+ You will first be prompted for the master password you previously set with `keystash passwd`
+ You'll then be prompted for the password you want to save to the vault. You can leave this field empty and the program will generate a strong password for you

### View Credentials

To view saved credentials, use `keystash search`:

```
$ keystash search
Enter master password:

Service: github.com
Username: sample_username123
Email: email@example.com
Id: 699
```

With `search`, you can specify filter fields (all are optional):
+ `-s SERVICE`: Show only credentials for the specified service
+ `-u USERNAME`: Show only credentials with the specified username
+ `-e EMAIL`: Show only credentials with the specified email

The "Id" field is used to specify credentials in the `get` and `remove` commands.

### Get the Password

To retrieve the password for a specific credential, use `keystash get`:

```
# To get the password for the credential saved above (github.com),
# use `keystash search` to find the credential's ID.
$ keystash search -s github.com
Enter master password:

Service: github.com
Username: sample_username123
Email: email@example.com
Id: 699

# Use the ID in the `get` command.
$ keystash get 699
Enter master password:
Password copied to clipboard.
```

`keystash get` copies the password to your system's clipboard. You can then paste the password wherever needed. For security reasons, the password is not displayed in the terminal.

### Remove Credentials

To delete credentials, use `keystash remove`:

```
$ keystash remove 699
Enter master password:
Removing the following credential:

Service: github.com
Username: sample_username123
Email: email@example.com
Id: 699
Confirm (y/n): y
Credential removed successfully.
```

`keystash remove` requires the ID of the credential you want to delete.

Use `keystash -h/--help` or `keystash <command> -h/--help` for more information.

---

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository** on GitHub
2. **Create a feature branch** (`git checkout -b feature/your-feature-name`)
3. **Make your changes** and commit them with clear, descriptive messages
4. **Push to your branch** (`git push origin feature/your-feature-name`)
5. **Open a Pull Request** describing your changes

Please ensure your code follows the existing style and includes appropriate tests where applicable. If you're planning major changes, consider opening an issue first to discuss your ideas.

For bug reports and feature requests, please open an issue on the [GitHub repository](https://github.com/raymondmwaura-osdev/keystash/issues).

---
