import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import sqlite3
from database import create_connection
import streamlit as st
from libs import hash_password


def getUser(username):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM users 
    WHERE username = ?
    ''', (username,))

    user = cursor.fetchone()
    conn.close()

    return user

def register(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO users (username, password) 
        VALUES (?, ?)
        ''', (username, hash_password(password)))

        conn.commit()
        st.success('User registered successfully')
    except sqlite3.IntegrityError:
        st.error('User already exists')
    finally:
        conn.close()

def login(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM users 
    WHERE username = ? AND password = ?
    ''', (username, hash_password(password)))

    user = cursor.fetchone()
    conn.close()

    if user:
        return user
    else:
        return False

