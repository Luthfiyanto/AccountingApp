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
                    account_name TEXT
                    )''')
    
    # Create table for transactions
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    date TEXT, 
                    description TEXT)''')

    # Create table for transaction_detail
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions_detail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id INTEGER,
                    account_type TEXT CHECK(account_type IN ('debit','credit')),
                    account,
                    amount INTEGER,
                    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
                    )''')
    
    # Create table for inventory
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id STRING PRIMARY KEY, 
                    nama_barang TEXT, 
                    unit INTEGER, 
                    harga_satuan INTEGER, 
                    jumlah INTEGER
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

    seed_users = [
        (10002,"admin", hash_password("admin123")),
        (10003,"user", hash_password("user123"))
    ]

    seed_accounts = [
        (1101,"Kas"),
        (1102,"Persediaan"),
        (4101,"Penjualan"),
        (5101,"Harga Pokok Penjualan"),
        (6201,"Beban Listrik, Air, dan Sampah"),
        (6202,"Beban Gaji"),
    ]

    cursor.execute("SELECT COUNT(*) FROM inventory")
    if(cursor.fetchone()[0] == 0):
        cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", seed_inventory)

    cursor.execute("SELECT COUNT(*) FROM users")
    if(cursor.fetchone()[0] == 0):
        cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", seed_users)
    
    cursor.execute("SELECT COUNT(*) FROM accounts")
    if(cursor.fetchone()[0] == 0):
        cursor.executemany("INSERT INTO accounts VALUES (?, ?)", seed_accounts)
    
    conn.commit()
    conn.close()