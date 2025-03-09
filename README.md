# Capture the Flag (CTF) Web Application

## ⚠️ Repository Deprecated ⚠️
This repository is no longer maintained. The latest version is now available at: [CTF](https://github.com/PixelsJr/CTF) 

[![CTF](https://img.shields.io/badge/Repository-Moved-blue)](https://github.com/PixelsJr/CTF)

## Overview

This project is a submission to TalTech's ASI KARIKAS 2025 competition (https://asikarikas.ee/).

This is a vulnerable web application designed to help computer science enthuasiasts learn about potential security flaws in web applications. The goal is to provide an interactive educational experience that highlights various vulnerabilities commonly found in web apps.

UPDATE: Our submission has made it to the final round, and we’ve been invited to compete on March 15th at TTÜ's Mektory!

### Purpose

The application consists of multiple security vulnerabilities (seven to be exact) that users must find. The flags represent various attack vectors that are designed to you understand how to find and exploit vulnerabilities.

## Vulnerabilities Included

- **Username enumeration and password brute-forceability**: Some areas of the app allow you to enumerate account username's and then brute-force their passwords.
- **Cross-Site Scripting (XSS)**: Some user input fields are vulnerable to a stored XSS vulnerability, allowing attackers to execute JavaScript code on every browser that might visit the page.
- **Client-side validation bypass**: The attacker is able to break the app's front-end functionality in specific ways to do things they should not be able to do.
- **Insecure Direct Object References (IDOR)**: Users can directly token values to access unauthorized resources.
- **JWT token manipulation**: JWT tokens (that are used for authorization) can be modified and then signed in a way that the server accepts them.
- **Local file inclusion (LFI)**: The attacker is able to cleverly manipulate a poorly-coded api and use it's output to be able to read all files on the server.
- **File Upload Vulnerability**: A file upload functionality contains an RCE vulnerability, allowing the attacker to get shell access to the server hosting the webapp.

---

## How to Run the Application Locally

Follow these steps to run the application on your local machine:

### Prerequisites

- Node.js (Tested on v23.6.0)
- npm (Tested on 10.9.2)
- Python (Tested on 3.13.0)
- PHP binaries (Tested on Zend Engine v4.4.3) (Definitely see README_additional.md for more info)

### Installation Steps

1. Clone this repository to your local machine:
   ```git clone https://github.com/LellerLololol/CTF-VEEBIRAKENDUS.git```
2. Navigate to the project directory:
   ```CTF-VEEBIRAKENDUS```
3. Install the dependencies (/client folder):
   ```npm install```
4. Build the project:
   ```npm run build```
5. Install the python requirements from /server:
   ```pip install -r requirements.txt```
6. Start the /vulns/xxs_vuln/auto_bot.py script in another shell (this is required for a flag to show itself)

   ```python auto_bot.py```
7. Start the application (/server folder):
   ```python server.py```

---

## Flags

The web application contains 7 flags hidden behind the vulnerabilities. Each flag can be discovered by exploiting the corresponding vulnerability. Here are the flag locations:

1. **Flag 1**: Found by enumerating a specific username, brute-forcing their password and logging into the account.
2. **Flag 2**: Found after performing XSS on another user and retrieving their cookies.
3. **Flag 3**: Can be bought in the shop for enough money (or by changing the client-side code) and can then be viewed in /Profile.
4. **Flag 4**: Is revealed after getting access (via IDOR) to the account whose ID of 1.
5. **Flag 5**: Can be viewed after getting access to /admin via JWT token manipulation.
6. **Flag 6**: Can be found by reading the flag.txt file with a broken api.
7. **Flag 7**: Can be read at FLAG_RCE.txt (at project root dir) after getting shell access.

---

## Solution Walkthrough

The full walkthrough to find all flags can be found in the `walkthrough.md` file.

---

## License

This project is licensed under the GNU General Public License (GPL) Version 3 - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- This project was created ONLY for educational purposes.
- Thanks to ASI KARIKAS for hosting such an interesting competition.

---

## Credits / Authors

- **Developers**: LellerLololol and PixelsJr
- **Team**: LellerLololol, PixelsJr, BHGull, lfkood
