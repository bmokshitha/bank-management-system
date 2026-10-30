# Bank Management System - IBPS SO Project 2026
# Author: 2026 Graduate

import sqlite3

conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
               (acc_no INTEGER PRIMARY KEY, name TEXT, balance REAL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
               (id INTEGER PRIMARY KEY AUTOINCREMENT, acc_no INTEGER, type TEXT, amount REAL)''')
conn.commit()

def create_account():
    name = input("Enter Name: ")
    balance = float(input("Enter Initial Balance: "))
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
    conn.commit()
    print(f"Account Created! Account No: {cursor.lastrowid}")

def deposit():
    acc_no = int(input("Enter Account No: "))
    amt = float(input("Enter Amount: "))
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no = ?", (amt, acc_no))
    cursor.execute("INSERT INTO transactions (acc_no, type, amount) VALUES (?, 'DEPOSIT', ?)", (acc_no, amt))
    conn.commit()
    print("Deposited Successfully")

def withdraw():
    acc_no = int(input("Enter Account No: "))
    amt = float(input("Enter Amount: "))
    cursor.execute("SELECT balance FROM accounts WHERE acc_no = ?", (acc_no,))
    result = cursor.fetchone()
    if result and result[0] >= amt:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE acc_no = ?", (amt, acc_no))
        cursor.execute("INSERT INTO transactions (acc_no, type, amount) VALUES (?, 'WITHDRAW', ?)", (acc_no, amt))
        conn.commit()
        print("Withdrawn Successfully")
    else:
        print("Insufficient Balance or Account Not Found")

def mini_statement():
    acc_no = int(input("Enter Account No: "))
    cursor.execute("SELECT * FROM transactions WHERE acc_no = ? ORDER BY id DESC LIMIT 5", (acc_no,))
    rows = cursor.fetchall()
    print("--- Last 5 Transactions ---")
    for r in rows:
        print(r)
    cursor.execute("SELECT balance FROM accounts WHERE acc_no = ?", (acc_no,))
    bal = cursor.fetchone()
    if bal:
        print(f"Current Balance: {bal[0]}")

while True:
    print("\n1.Create Account 2.Deposit 3.Withdraw 4.Mini Statement 5.Exit")
    ch = input("Choice: ")
    if ch == '1':
        create_account()
    elif ch == '2':
        deposit()
    elif ch == '3':
        withdraw()
    elif ch == '4':
        mini_statement()
    else:
        break

conn.close()
