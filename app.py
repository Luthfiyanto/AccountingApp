import streamlit as st
from database import initialize_database, seed_database
# from models.auth import logout
from models.accounts import get_all_accounts
from page import auth

# Initialize the database
initialize_database()
seed_database()

# Streamlit app
st.title('Sistem Informasi Akuntansi')

# Initialize the session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None


if "accounts" not in st.session_state:
    st.session_state["accounts"] = []
    account_data = get_all_accounts()
    st.session_state["accounts"] = [row [1] for row in account_data]

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

if not st.session_state.logged_in:
    auth.AuthPage()
else:
    authPage = st.Page(logout, title='Auth', icon=':material/login:')
    inventoryPage = st.Page('page/inventory.py', title='Persediaan', icon=':material/store:', default=True)
    transactionPage = st.Page('page/transactions.py', title='Jurnal Umum', icon=':material/receipt_long:')
    generalLedgerPage = st.Page('page/ledger.py', title="Buku Besar", icon=":material/book:")
    trialBalancePage = st.Page('page/balance.py', title="Neraca Saldo", icon=":material/balance:")
    reportPage = st.Page('page/report.py', title='Laporan Laba Rugi', icon=':material/insights:')
    logoutPage = st.Page(logout, title='Logout', icon=':material/logout:')
    accountPage = st.Page('page/account.py', title="Akun", icon=':material/settings:')

    pages = [inventoryPage, transactionPage,generalLedgerPage, trialBalancePage, reportPage, accountPage,logoutPage]

    if st.session_state.user:
        pg = st.navigation(pages)
        st.write(f'Selamat Datang, {st.session_state.user[1]}!')
        pg.run()
    else:
        authPage = st.Page('page/auth.py', title='Auth', icon=':material/login:')
        pg = st.navigation([authPage])
        pg.run()

    
    