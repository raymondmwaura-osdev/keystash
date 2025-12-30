+ In `keystash search`, don't just search for an exact match:
    - Make the search case insensitive.
    - Search for substrings.
    - In the output, print the closest matches first and partial matches later.

+ Enter the master password once, then maybe enter interactive mode so that the user can enter multiple consecutive commands without having to enter the master password everytime.
+ **Update Credentials**: Allow the user to update/modify saved credentials.
+ **Backup**: The program should have a copy of the vault file backed up somewhere. The file should be updated every time the vault is modified. The user can select where to backup the file; it can be on a secondary drive, google drive, onedrive, or any other location the user wants. Support for saving the file on the cloud will be added when the need arises. The program should support google drive initially.
+ Remove all `print` statements and use `logger` instead.
+ Copy the password to the clipboard when it is automatically generated in the `add` feature.
