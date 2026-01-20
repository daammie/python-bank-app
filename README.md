# python-bank-app
A CLI banking application built with Python and SQLite

This app allows users to sign up, log in, deposit, withdraw, transfer money, and view transaction history.


## Features

- User signup with unique username and secure password (hashed using SHA-256)
- Automatic generation of a unique account number
- Deposit and withdrawal with validation
- Transfer funds to other users with confirmation
- Display current account balance
- View detailed transaction history
- Account details viewing
- Cancel operations at any step


## Installation & Usage
## Installation & Usage

1. Clone the repository
   ```bash
   git clone https://github.com/daammie/python-bank-app.git
   ```
   
2. Navigate to the project folder
   cd python-bank-app
   
3. Run the app
   python BankAPP.py



## Requirements

- Python 3.x
- SQLite (comes pre-installed with Python)
- Modules used: re, time, random, sqlite3, hashlib, getpass



## Usage Instructions

Sign Up: Create a new account with a minimum initial deposit of 2000.

Log In: Access your account using username and password.

Deposit/Withdraw: Enter amount or type C to cancel.

Transfer: Enter recipient account number, confirm the recipient’s name, and enter the amount.

Balance Inquiry: Check your current balance.

Transaction History: View all past transactions including deposits, withdrawals, and transfers.

Account Details: View full name, username, and account number.
 
