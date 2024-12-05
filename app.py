import streamlit as st
from database import initialize_database, seed_database
# from models.auth import logout
from page import auth

# Initialize the database
initialize_database()
seed_database()

# Streamlit app
st.title('Accounting App')

# Initialize the session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

if "accounts" not in st.session_state:
    st.session_state["accounts"] = {
        "Kas": 0,
        "Persediaan": 0,
        "Pendapatan": 0,
        "Penjualan": 0,
        "HPP": 0,
        "Beban": 0,
        "Beban listrik, air, sampah": 0,
        "Beban gaji": 0
    }

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

if not st.session_state.logged_in:
    auth.AuthPage()
else:
    authPage = st.Page(logout, title='Auth', icon=':material/login:')
    inventoryPage = st.Page('page/inventory.py', title='Inventory', icon=':material/store:', default=True)
    transactionPage = st.Page('page/transactions.py', title='Transaction', icon=':material/receipt_long:')
    reportPage = st.Page('page/report.py', title='Report', icon=':material/insights:')
    logoutPage = st.Page(logout, title='Logout', icon=':material/logout:')

    pages = [inventoryPage, transactionPage, reportPage, logoutPage]

    if st.session_state.user:
        pg = st.navigation(pages)
        st.write(f'Welcome back, {st.session_state.user[1]}!')
        pg.run()
    else:
        authPage = st.Page('page/auth.py', title='Auth', icon=':material/login:')
        pg = st.navigation([authPage])
        pg.run()

    
    