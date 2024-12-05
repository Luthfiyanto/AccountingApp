from database import create_connection

def add_inventory(id, nama_barang, unit, harga_satuan, jumlah):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM inventory WHERE id = ?''', (id,))
    inventory = cursor.fetchall()
    if inventory:
        update_inventory(id, nama_barang, unit, harga_satuan, jumlah)
    elif not inventory:
        cursor.execute('''INSERT INTO inventory (id, nama_barang, unit, harga_satuan, jumlah) 
                      VALUES (?, ?, ?, ?, ?)''', (id, nama_barang, unit, harga_satuan, jumlah))
    conn.commit()
    conn.close()

def get_inventory():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM inventory''')
    inventory = cursor.fetchall()
    conn.close()
    return inventory

def get_inventory_by_id(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM inventory WHERE id = ?''', (id,))
    inventory = cursor.fetchone()
    conn.close()
    return inventory

def update_inventory(id, nama_barang, unit, harga_satuan, jumlah):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE inventory SET nama_barang = ?, unit = ?, harga_satuan = ?, jumlah = ? 
                      WHERE id = ?''', (nama_barang, unit, harga_satuan, jumlah, id))
    conn.commit()
    conn.close()

def delete_inventory(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM inventory WHERE id = ?''', (id,))
    conn.commit()
    conn.close()