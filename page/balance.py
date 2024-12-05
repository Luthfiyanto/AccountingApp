import streamlit as st
import pandas as pd
st.title("Neraca Saldo")

# Menampilkan neraca saldo
st.subheader("Neraca Saldo")
balance_df = pd.DataFrame(st.session_state["accounts"].items(), columns=["Akun", "Saldo"])
for account, balance in st.session_state["accounts"].items():
            total_debit = sum(t["Debit"] for t in st.session_state["transactions"] if t["Akun"] == account)
            total_credit = sum(t["Kredit"] for t in st.session_state["transactions"] if t["Akun"] == account)
        
        #hitung saldo akhir
st.session_state["accounts"][account] = total_debit - total_credit

balance_df = pd.DataFrame(st.session_state["accounts"].items(), columns=["Akun", "Saldo"])
st.write(balance_df)