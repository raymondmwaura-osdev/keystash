# Specification

This is how the program should work.

## Essential Features

+ **Save credentials**: The user should be able to add credentials to save. For now, the credentials will have the following fields:
  - **service** (required): The name of the website the credential is for.
  - **password** (required): The password used to log in to the site.
  - **username** (optional): Your username in the website.
  - **email** (optional): The email used to log in to the website.

  Other fields may be added in the future, when the need arises.
+ **Secure storage**: The credentials will encrypted and saved in a file. The contents should be encrypted using AES encryption with a key derived from a password provided by the user. The user will be prompted for the password while both encrypting and decrypting. This ensures that only the user can read the credentials.
+ **View saved credentials**: The user should be able to view the saved credentials. Optionally, for added security, instead of showing the password, the program should instead copy the password to the clipboard. This ensures that the password will not be in plain text at any given time.
+ **Remove credentials**: The user should also be able to completely remove credentials from the vault. The program should ensure that the credentials are removed and unrecoverable, for added security. Since this action is not reversible, ask the user to do something like write the name of the service whose password is being deleted, to make sure that the user wants to proceed with the removal of the credentials.
+ **Change master password**: Allow the user to change the password used to encrypt and decrypt the vault.

---

## Future Features

+ **Backup**: The program should have a copy of the vault file backed up somewhere. The file should be updated every time the vault is modified. The user can select where to backup the file; it can be on a secondary drive, google drive, onedrive, or any other location the user wants. Support for saving the file on the cloud will be added when the need arises. The program should support google drive initially.
+ **Password generation**: The program should be able to generate strong passwords.
