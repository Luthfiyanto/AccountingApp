import sqlite3
import csv
from pathlib import Path
from libs import hash_password

def create_connection():
    conn = sqlite3.connect('accounting.db')
    return conn

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Create table for user
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY, 
                    username TEXT, 
                    password TEXT
                    )''')
                    
    # Create table for accounts
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY, 
                    account_name TEXT, 
                    balance REAL)''')
    
    # Create table for transactions
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY, 
                    account_name TEXT, 
                    debit REAL,
                    credit REAL, 
                    date TEXT, 
                    description TEXT)''')
    
    # Create table for inventory
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id STRING PRIMARY KEY, 
                    nama_barang TEXT, 
                    unit INTEGER, 
                    harga_satuan REAL, 
                    jumlah REAL
                    )''')
    conn.commit()
    conn.close()
def csv_to_array(csv_file):
    data = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            data.append(tuple(row))  # Convert each row to a tuple
    return data

def seed_database():
    conn = create_connection()
    cursor = conn.cursor()

    # read file csv
    csv_file = Path("inventory.csv")
    seed_inventory = csv_to_array(csv_file)
    print(seed_inventory)

    seed_users = [
        (10002,"admin", hash_password("admin123")),
        (10003,"user", hash_password("user123"))
    ]

    seed_accounts = [
        (1101,"Kas", 0),
        (1102,"Persediaan", 0),
        (4101,"Penjualan", 0),
        (5101,"Harga Pokok Penjualan", 0),
        (6201,"Beban Listrik, Air, dan Sampah", 0),
        (6202,"Beban Gaji", 0),
    ]

    seed_transactions = [
        ("Kas", 1000000, 0, "2021-01-01", "Modal awal"),
        ("Perlengkapan", 200000, 0, "2021-01-01", "Modal awal"),
        ("Peralatan", 1000000, 0, "2021-01-01", "Modal awal"),
        ("Modal", 0, 2000000, "2021-01-01", "Modal awal"),
        ("Kas", 0, 500000, "2021-01-01", "Utang awal"),
        ("Utang", 500000, 0, "2021-01-01", "Utang awal")
    ]

    cursor.execute("SELECT COUNT(*) FROM inventory")
    if(cursor.fetchone()[0] == 0):
        cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", seed_inventory)

    cursor.execute("SELECT COUNT(*) FROM users")
    if(cursor.fetchone()[0] == 0):
        cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", seed_users)
    
    cursor.execute("SELECT COUNT(*) FROM accounts")
    if(cursor.fetchone()[0] == 0):
        cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?)", seed_accounts)

    cursor.execute("SELECT COUNT(*) FROM transactions")
    if(cursor.fetchone()[0] == 0):
        cursor.executemany("INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?, ?)", seed_transactions)
    
    conn.commit()
    conn.close()