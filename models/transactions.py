from database import create_connection

def create_transaction(account_id, amount, date, description):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO transactions (account_id, amount, date, description) 
                      VALUES (?, ?, ?, ?)''', (account_id, amount, date, description))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM transactions''')
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_transactions(account_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM transactions WHERE account_id = ?''', (account_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_total_balance(account_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(amount) FROM transactions WHERE account_id = ?''', (account_id,))
    total_balance = cursor.fetchone()[0]
    conn.close()
    return total_balance

def get_all_balances():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT account_id, SUM(amount) FROM transactions GROUP BY account_id''')
    balances = cursor.fetchall()
    conn.close()
    return balances

def update_transaction(transaction_id, amount, date, description):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE transactions SET amount = ?, date = ?, description = ? 
                      WHERE id = ?''', (amount, date, description, transaction_id))
    conn.commit()
    conn.close()

def delete_transaction(transaction_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM transactions WHERE id = ?''', (transaction_id,))
    conn.commit()
    conn.close()