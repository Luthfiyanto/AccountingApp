from database import create_connection

def getBalance():
  conn = create_connection()
  cursor = conn.cursor()

  cursor.execute('''
      SELECT 
        a.account_name,
        SUM(CASE WHEN td.account_type = 'debit' THEN td.amount ELSE 0 END) AS total_debit,
        SUM(CASE WHEN td.account_type = 'credit' THEN td.amount ELSE 0 END) AS total_credit
      FROM accounts a
      LEFT JOIN transactions_detail td ON a.account_name = td.account
      GROUP BY a.account_name
      ORDER BY a.account_name
  ''')

  conn.commit()
  conn.close()