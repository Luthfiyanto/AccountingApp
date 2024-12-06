import streamlit as st
import pandas as pd
from models.transactions import get_all_transactions
from models.accounts import get_all_accounts

st.subheader("Buku Besar")

transactions = pd.DataFrame(get_all_transactions(), columns=["ID","ID Transaksi", "Tanggal", "Deskripsi", "Akun", "Debit","Kredit"])
groupedData = transactions.groupby("Akun")
summary = groupedData.agg(
  total_debit=("Debit", "sum"),
  total_credit=("Kredit","sum")
)
summary["balance"] = summary["total_debit"] - summary["total_credit"]

for account, group in groupedData:
  st.subheader(account)
  st.table(group)

st.subheader("Ringkasan")
st.table(summary)
