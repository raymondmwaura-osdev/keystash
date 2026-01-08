# KeyStash

KeyStash is a lightweight CLI password manager that securely stores your passwords locally. It stores your passwords and credentials in an encrypted vault file located at `~/.local/share/keystash`.

---

## Installation

Install directly from the repository:

```sh
pip install git+https://github.com/raymondmwaura-osdev/keystash.git@v0.1.1 # Specify your desired version
```

This will:
+ Clone the repository
+ Build the wheel
+ Install the wheel

Alternatively, you can download a prebuilt wheel for your desired version and run:

```sh
pip install keystash-[version]-py3-none-any.whl
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

**Note**: Your password will not be displayed on screen for security reasons.

The master password is used to verify your identity and generate a key for encrypting and decrypting the vault. **Don't forget this password.** There is currently no way to recover your credentials without it. Account recovery functionality will be implemented in a future release.

### Interactive Mode

Type `keystash`, `keystash -i`, or `keystash --interactive` to enter interactive mode.

```
$ keystash
Enter master password:
(keystash) 
```

Normally, KeyStash prompts for the master password every time it's run from the command line. In interactive mode, KeyStash continuously prompts for commands in a persistent session. This allows you to run multiple commands without re-entering the master password each time.

To exit interactive mode and end the session, use `exit` or `quit`.

### Add Credentials

To add credentials to the vault, use `add`:

```
(keystash) add -s github.com -u sample_username123 -e email@example.com
Enter the password to store.
Leave blank to generate a random password.
Password:
Generated a strong password.
Credential saved successfully!
```

+ `-s` specifies the service (required), `-u` specifies the username (optional), `-e` specifies the email (optional)
+ You'll be prompted for the password you want to save to the vault. Leave this field empty to have the program generate a strong password for you.

**Note**: Your password will not be displayed on screen for security reasons.

### View Credentials

To view saved credentials, use `search`:

```
(keystash) search

Service: github.com
Username: sample_username123
Email: email@example.com
Id: 699
```

The "Id" field is used to specify credentials in the `get` and `remove` commands.

With `search`, you can specify filter fields (all are optional):
+ `-s SERVICE`: Show only credentials for the specified service
+ `-u USERNAME`: Show only credentials with the specified username
+ `-e EMAIL`: Show only credentials with the specified email

If no filter fields are specified, the command will display all credentials in the vault.

### Get the Password

To retrieve the password for a specific credential, use `get`:

```
# To get the password for the credential saved above (github.com),
# use `keystash search` to find the credential's ID.
(keystash) search -s github.com

Service: github.com
Username: sample_username123
Email: email@example.com
Id: 699

# Use the ID in the `get` command.
(keystash) get 699
Password copied to clipboard.
```

`get` copies the password to your system's clipboard, allowing you to paste it wherever needed. For security reasons, the password is not displayed in the terminal.

### Remove Credentials

To delete credentials, use `remove`:

```
(keystash) remove 699
Removing the following credential:

Service: github.com
Username: sample_username123
Email: email@example.com
Id: 699
Confirm (y/n): y
Credential removed successfully.
```

`remove` requires the ID of the credential you want to delete.

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
