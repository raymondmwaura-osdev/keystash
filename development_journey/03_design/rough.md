
## Features

Add, update, view, delete.

+ Only one feature can run at a time.
+ Each feature will have its own cli options.

### Add

The add feature shall have the following CLI options:

+ `-s` / `--service`: Specify the service/website.
+ `-u` / `--username`: Enter the username.
+ `-e` / `--email`: Enter the email.
+ Other fields will be added when the need arises.

After pressing enter, the program will prompt the user to enter the password for the website. The program should not echo the password entered. The password should not be displayed on the terminal.

The program shall then prompt the user for the master password, which will be used to decrypt and encrypt the vault.

Before the credential is added to the vault, the program shall scan the vault for any credentials matching the given credential.  
Below are some conflicting scenarios:

#### Exact duplicate

+ If a credential is found, matching all fields (service, password, username, and email), the program shall inform the user that a duplicate credential already exists, and exit without modifying the vault.

#### Service

+ **Same service**:
    - If the username and email are different, the program shall save the credential, assuming the user has multiple accounts for the same service.
    - If the username and email are similar, or only the service and password are provided, the program shall prompt the user on whether to preserve or overwrite the existing credential.


If a credential is found with:

+ **The same everything (service, username, email, password).** The program shall display a message informing the user that a duplicate credential exists. The program shall then exit without modifying the vault.
+ **The same everything but different password.** The program shall inform the user that a similar credential exists, but with a different password. The program should then prompt the user on whether to overwrite the existing credential or not.
    - If the user decides to overwrite the existing credential, the program should delete the credential from the vault, and add then new credential in its place.
    - If the user decides to preserve the existing credential, the program should exit without modifying the vault.
+ **The same password.** The program shall inform the user that the password is already used, and offer to generate a different password for this credential. If the user refuses to use a different password, the program shall save the credential, with the used password, and warn the user of the security flaw.
+ **The same service.** If a credential with the same service is found, the program shall check the other fields (username and email). If the fields differ, the program shall save the credential. If the fields match, the program shall prompt the user on whether to preserve or overwrite the existing credential.
