# 🔐 Python Password Manager (CLI)

A secure command-line password manager built in Python using modern cryptographic standards.  
It securely stores passwords using **AES-GCM encryption**, **Argon2id key derivation**, and includes **password breach detection** via Have I Been Pwned.

---


## 🚀 Features

- 🔒 **AES-256-GCM encryption** for stored passwords
- 🔑 **Argon2id key derivation** (memory-hard, brute-force resistant)
- 🛡️ **HIBP (Have I Been Pwned) API integration**
- 📊 **Password strength checking** using `zxcvbn`
- 🎲 **Secure password generator**
- 📋 **Clipboard copy support**
- 🗄️ **MySQL-backed storage**
- 🧪 Clean CLI using `argparse` and `rich`

---

## 🧠 Security Design

- Master password is **never stored**
- Encryption key is derived at runtime
- Device secret is stored securely in DB
- Passwords are encrypted using **AES-GCM with random nonce**
- Uses **k-anonymity** for breach checking (HIBP)

---
## 📦 Requirements

- Python 3.8+
- MySQL Server

---

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/Ryan27-27/Credential-Vault.git
cd Credential-Vault
```
Install Python Requirements:
```bash
pip install -r requirements.txt
```
## 🗄️ Database Setup (MySQL / SQL)

This password manager requires an SQL database.  
Any **MySQL-compatible database** (MySQL / MariaDB) can be used.

---

### 1️⃣ Login as root

```bash
sudo mysql -u root
```
### 2️⃣ Create a database user
```bash
CREATE USER 'pm'@'localhost' IDENTIFIED BY 'Secret';
```
### 3️⃣ Grant privileges
```bash
GRANT ALL PRIVILEGES ON *.* TO 'pm'@'localhost';
FLUSH PRIVILEGES;
```
### Update database credentials

Edit the database configuration file:

```text
utils/dbconfig.py
```
Replace credentials with your own if needed.

### Run
---
### Configure

You need to first configure the password manager by choosing a MASTER PASSWORD. This config step is only required to be executed once.

```bash
python config.py make
```
The above command will make a new configuration by asking you to choose a MASTER PASSWORD. This will generate the DEVICE SECRET, create db and required tables.

```bash
python config.py delete
```

The above command will delete the existing configuration. Doing this will completely delete your device secret and all your entries and you will loose all your passwords. So be aware!

```bash
python config.py remake
```
The above command will first delete the existing configuration and create a fresh new configuration by asking you to choose a MASTER PASSWORD, generate the DEVICE SECRET, create the db and required tables.

### Usage
```text
python pm.py -h
usage: pm.py [-h] [-d DOMAIN] [-u URL] [-e EMAIL] [-l UNAME] [--length LENGTH] [-c] option

Password Manager

positional arguments:
  option               (a)dd / (e)xtract / (g)enerate

options:
  -h, --help           show this help message and exit
  -d, --domain DOMAIN  Site name
  -u, --url URL        Site URL
  -e, --email EMAIL    Email
  -l, --uname UNAME    Username
  --length LENGTH      Length of the password to generate
  -c, --copy           Copy password to clipboard
```

### Add entry
```bash
python pm.py add -d mysite -u mysite.com -e hello@email.com -l myusername
```
### Retrieve entry
```bash
python pm.py extract
```
The above command retrieves all the entries
```text
python pm.py e -d mysite
```
The above command retrieves all the entries whose site name is "mysite"
```text
python pm.py e -d mysite -l myusername
```
The above command retrieves the entry whose site name is "mysite" and username is "myusername"
```text
python pm.py e -d mysite -l myusername --copy
```
The above command copies the password of the site "mysite" and username "myusername" into the clipboard

### Generate Password
```bash
python pm.py g --length 15
```
The above command generates a password of length 15 and copies to clipboard
