from database import create_connection

def save_transactions(date, description, debit_accounts, credit_accounts):
    conn = create_connection()
    cursor = conn.cursor()

    # Simpan data ke tabel transaksi
    cursor.execute(
        "INSERT INTO transactions (date, description) VALUES (?,?)",
        (date,description)
    )

    transaction_id = cursor.lastrowid

    # Simpan data debit ke tabel transactions_detail
    for account, amount in debit_accounts:
        cursor.execute(
            "INSERT INTO transactions_detail (transaction_id, account_type, account, amount) VALUES (?,?,?,?)",
            (transaction_id, 'debit', account, amount)
        )

    # Simpan data kredit ke tabel transactions_detail
    for account, amount in credit_accounts:
        cursor.execute(
            "INSERT INTO transactions_detail (transaction_id, account_type, account, amount) VALUES (?,?,?,?)",
            (transaction_id, 'credit', account, amount)
        )
    
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            td.id AS id,
            td.transaction_id AS transaction_id,
            t.date AS date,
            t.description AS description,
            td.account AS account,
            CASE WHEN td.account_type = 'debit' THEN td.amount ELSE 0 END AS debit,
            CASE WHEN td.account_type = 'credit' THEN td.amount ELSE 0 END AS credit
        FROM
            transactions_detail td
        JOIN
            transactions t ON td.transaction_id = t.id
        LEFT JOIN
            accounts a ON td.account = a.account_name

    ''')
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