from database import create_connection

def create_account(user_id, name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO accounts (id, account_name) VALUES (?, ?)''', (user_id, name))
    conn.commit()
    conn.close()

def get_all_accounts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, account_name FROM accounts''')
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def get_account(account_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM accounts WHERE id = ?''', (account_id,))
    account = cursor.fetchone()
    conn.close()
    return account

def delete_account(account_id, account_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM accounts WHERE id = ? AND account_name =?''', (account_id,account_name))
    conn.commit()
    conn.close()