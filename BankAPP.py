

import re
import time
import random        
import sqlite3
import hashlib
from getpass import getpass





conn = sqlite3.connect('BankDB.db')

cursor = conn.cursor()



cursor.execute('''
                
             create table if not exists USERS(
             id INTEGER PRIMARY KEY AUTOINCREMENT,  
             full_name TEXT NOT NULL,
             username TEXT NOT NULL UNIQUE,
             password TEXT NOT NULL,
             account_number TEXT NOT NULL UNIQUE,
             balance REAL NOT NULL,
             created_at DATETIME DEFAULT CURRENT_TIMESTAMP  
               
               )

               ''')



cursor.execute('''
               
                CREATE TABLE IF NOT EXISTS TRANSACTIONS(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id INTEGER NOT NULL, 
             transaction_type TEXT NOT NULL,
             amount REAL NOT NULL,
             balance REAL NOT NULL,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
             recipient_account TEXT,
             FOREIGN KEY(user_id) REFERENCES USERS(id)

               )
               
               ''')




def sign_up():
   print('---Sign UP---')
   while True:
      first_name = input('Please enter your first name : ').strip()
      if not first_name:
         print('First name field cannot be empty')
         continue

      last_name = input('Please enter your last name : ').strip()
      if not last_name:
         print('Last name field cannot be empty')
         continue
      
      full_name = first_name + " " + last_name
      if len(full_name) < 4:
         print('Full name must be at least 4 characters.')
         continue
      
      if full_name.isdigit():
         print('Name must contain only letters')
         continue

      if len(full_name) > 225:
         print('Full name cannot exceed 255 characters.')
         continue
      break

   while True:
      username = input('Please enter your username: ').strip()
      if not username:
         print('Username field cannot be empty')
         continue
      
      if len(username) < 3:
         print('Minimum length for username is 3 characters')
         continue
       
      if len(username) > 20:
         print('Maximum length for username is 20 characters')
         continue
       
      pattern = r'^[a-zA-Z0-9_]+$'
      if not re.match(pattern, username):
         print('Enter a valid username that contains only letters, numbers and underscores')
         print(re.match)
         continue
      break


   while True:
      password = getpass('Please enter your password : ')
      if not password:
         print('Password field cannot be empty')
         continue

      if len(password) < 8:
        print('Minimum length for password is 8 characters')
        continue

      if len(password) > 20:
        print('Maximum length for password is 20 characters')
        continue

      pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,20}$'
      if not re.match(pattern, password):
         print('Enter a valid password that contains at least one uppercase, one lowercase, numbers and special characters')
         continue
      

      confirm_password = getpass('Please confirm password: ')
      if not confirm_password:
        print('Password field cannot be empty')
        continue

      if password != confirm_password:
        print('Password doesn\'t match, please try again')
        continue
      break
    
   hashed_password = hashlib.sha256(password.encode()).hexdigest()
   account_number = gen_acnt_num()

    
   #compulsory deposit for account creation
   while True:
      try:
         initial_deposit = int(input('initial deposit required (minimum of 2000.00):'))
      except ValueError:
         print('Please enter a numeric value.')
         continue
       
      if initial_deposit < 2000.00:
         print('You can not deposit below 2000.00')
         continue
      balance = initial_deposit
      break
    
       
   while True:
      try:
          cursor.execute('''
        insert into USERS (full_name, username, password, account_number, balance) VALUES
        (?,?,?,?,?)
        ''',(full_name, username, hashed_password, account_number, balance))
       
      except sqlite3.IntegrityError:
         print('Username already exists')
         continue
      else:
        conn.commit()
        time.sleep(2)
        print(f'''Signup successful!
              Your account number is {account_number}''')

        time.sleep(3)
        log_in()
        break
        

def gen_acnt_num():
   num = random.randint(100000000, 900000000)
   return f"0{num}"


def log_in():
    print('---Log in---')

    while True:
        username = input('Enter your username : ').strip()
        if not username:
            print('Username field cannot be empty')
            continue
        break
    
    while True:
        password = getpass('Enter your password : ').strip()
        if not password:
            print('Password field cannot be empty')
            continue
        break
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute('''
    select * from users where username = ? and password = ?''',(username,hashed_password))
    user = cursor.fetchone()
    if user is None:
        print('Invalid username or password')
        return
    print('Procesing....')
    time.sleep(3)
    print('Log in Successful!')
    submenu(username)
    



def submenu(username):
   while True:
      
      print('''
         Please select an action:
         1. Deposit
         2. Withdrawal
         3. Balance Inquiry
         4. Transaction History
         5. Transfer
         6. Account Details:
         7. Exit
         ''')

      user = input('Enter an option:').strip()

      if user == '1':
         time.sleep(2)
         deposit(username)
      elif user == '2':
         time.sleep(2)
         withdrawal(username)
      elif user == '3':
         time.sleep(2)
         display_bal(username)
      elif user == '4':
         time.sleep(2)
         transaction_history(username)
      elif user == '5':
         time.sleep(2)
         transfer(username)
      elif user == '6':
         time.sleep(2)
         account_details(username)
      elif user == '7':
         print('Exitting...')
         break
      else:
         print("Invalid choice, please select again.")






# Banking_Transactions


def deposit(username):
   cursor.execute('SELECT id, balance FROM USERS WHERE username=?', (username,) )
   user_id, new_balance = cursor.fetchone()
 
   while True:
      deposit_input = input('Enter amount to deposit (or type C to cancel): ').strip()
      if deposit_input.lower() == 'c':
         print('Deposit cancelled.')
         return
      
      try:
         deposit_amount = float(deposit_input)
      except ValueError:
         print('Please enter a numeric value.')
         continue 

      if deposit_amount <= 0:
          print('Please enter a valid amount')
          continue

      new_balance += deposit_amount

      cursor.execute('UPDATE USERS SET balance=? WHERE username=?', (new_balance, username))

      cursor.execute('''INSERT INTO TRANSACTIONS (user_id, transaction_type, amount, balance)
                     VALUES (?, ?, ?, ?)''',
                     (user_id, 'deposit', deposit_amount, new_balance))
      conn.commit()

      print(f'Deposit successful! Your new balance is {new_balance:.2f}')
      break

  


def withdrawal(username):
   
   cursor.execute('SELECT id, balance FROM USERS WHERE username=?', (username,))
   user_id, new_balance= cursor.fetchone()

   while True:
      amount_input = input('Enter amount to withdraw (or type C to cancel): ').strip()

      if amount_input.lower() == 'c':
         print('Withdrawal cancelled.')
         return
      
      try:
         withdrawal_amount = float(amount_input)
      except ValueError:
         print('Please enter a numeric value.')
         continue

      if withdrawal_amount < 1000:
         print('please enter a valid amount(minimum of 1000)')
         continue

      if withdrawal_amount > new_balance:
         print('Insufficient Funds!')
         continue

      new_balance -= withdrawal_amount

      cursor.execute('UPDATE USERS SET balance = ? WHERE username = ?', (new_balance, username))
      
      cursor.execute('''INSERT INTO TRANSACTIONS(user_id, transaction_type, amount, balance)
                     VALUES (?, ?, ?, ?)''',
                     (user_id, 'withdrawal', withdrawal_amount, new_balance))
      conn.commit()
      
      print(f'Withdrawal successful! Your new balance is {new_balance:.2f}')
      break
      
                     



def display_bal(username):

   cursor.execute('SELECT balance FROM USERS WHERE username=?', (username,))
   result = cursor.fetchone()

   if not result:
      print('user not found.')
      return
   
   balance = result[0]
   
   print(f'Your current balance is #{balance}')
    




def transaction_history(username):
   cursor.execute('''
                  SELECT id FROM USERS WHERE username = ?
                  ''', (username,),)
   user_id = cursor.fetchone()[0]

   cursor.execute('''
                  SELECT transaction_type, amount, balance, timestamp, 
                  recipient_account FROM TRANSACTIONS WHERE user_id = ?''',
                  (user_id,))
   records = cursor.fetchall()
   if not records:
      print('No transaction history found.')
      return
   
   print('TRANSACTION HISTORY\n')
   for i, record in enumerate(records, start=1):
      transaction_type, amount, balance, timestamp, recipient_account = record
      if transaction_type == 'transfer':
         print(f"{i}. {transaction_type} of {amount:.2f} to account {recipient_account}\n Balance: {balance:.2f} | {timestamp}")
      elif transaction_type == 'credit':
         print(f"{i}. Received {amount:.2f} | Balance: {balance:.2f} | {timestamp}")
      else:
         print(f"{i}. {transaction_type} of {amount:.2f} | Balance: {balance:.2f} | {timestamp}")



      
   

def transfer(username):
   
   cursor.execute('''SELECT id, account_number, balance FROM USERS 
                     WHERE username = ?''',(username,))
   sender_id, sender_account, sender_balance = cursor.fetchone()


   while True:
      recipient_account = input('Enter recipient account number(or type C to cancel): ').strip()
      if recipient_account.lower() == 'c':
         print('Transfer cancelled.')
         return
      
      if not recipient_account:
         print('Account number field cannot be empty')
         continue

      if not recipient_account.isdigit():
         print('Account number must contain only digits.')
         continue

      if len(recipient_account) != 10:
         print('Invalid account number, 10 digits expected.')
         continue

      if recipient_account ==  sender_account:
         print('self-transfer is not allowed')
         continue
         
      
      cursor.execute('SELECT id, full_name, balance FROM USERS WHERE account_number=?',
                     (recipient_account,))
      recipient = cursor.fetchone()

      if not recipient:
         print('Recipient not found')
         continue

      recipient_id, recipient_name, recipient_balance = recipient

      confirm = input(f'Are you sure you want to transfer to {recipient_name}. Continue? (Y/N): '
                      ).strip().lower()

      if confirm != 'y':
         print('Transfer cancelled.')
         continue

      while True:
         amount_input = input('Enter amount to transfer(or type C to cancel): ').strip()
         
         if amount_input.lower() == 'c':
            print('Transfer cancelled.')
            return
      
         try: 
            amount = float(amount_input)

         except ValueError:
            print('Please enter a numeric value.')
            continue

         if amount < 1:
            print('please enter a valid amount.')
            continue

         if amount > sender_balance:
            print('Insufficient Funds!')
            continue

      
   
         new_sender_balance = sender_balance - amount
         new_recipient_balance = recipient_balance + amount


         cursor.execute('''UPDATE USERS SET balance = ? 
                     WHERE id= ?''', (new_sender_balance, sender_id))
      
         cursor.execute('''UPDATE USERS SET balance = ? 
                     WHERE id= ?''', (new_recipient_balance, recipient_id))
      

         cursor.execute('''INSERT INTO TRANSACTIONS 
                     (user_id, transaction_type, amount, balance, recipient_account)
                      VALUES (?,?,?,?,?)''',
               (sender_id, 'transfer', amount, new_sender_balance, recipient_account)) 
              
         cursor.execute('''INSERT INTO TRANSACTIONS
                     (user_id, transaction_type, amount, balance)
                     VALUES(?,?,?,?)''', 
                     (recipient_id, 'credit', amount, new_recipient_balance))
      
         conn.commit()
         print('Transfer successful')
         print(f'Your current balance is {new_sender_balance}')
         break      




def account_details(username):
   cursor.execute('''
                  SELECT full_name, username, account_number
                  FROM USERS
                  WHERE username = ?
                  ''', (username,))
   user = cursor.fetchone()

   if not user:
      print('User not found.')
   else:
      print(f'''
            ACCOUNT DETAILS:
            Name: {user[0]} 
            Username: {user[1]}
            Account Number: {user[2]}
            ''')



def menu():
   print('''WELCOME!
         Please select an option from the menu below:
         1. Sign Up
         2. Log In
         3. Quit
         ''')

try:
    while True:
        menu()
        choice = input('Choose an option from the menu above: ').strip()
        if choice == '3':
            print('Thank you for banking with us')
            break
        elif choice == '1':
            sign_up()
        elif choice == '2':
            log_in()
        else:
            print('Invalid choice, select from the menu')
except Exception as e:
    print(f'Something went wrong: {e}')
finally:
    conn.close()






### after getting your data
## clean
## split (detect: the features, then the target )

variance
co variance
standard deviation
mean
learn in relation to model development
        







   
   
 








































































