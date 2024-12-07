import streamlit as st
import pandas as pd
from models.transactions import get_all_transactions
from models.accounts import get_all_accounts

st.subheader("Buku Besar")

transactions = pd.DataFrame(get_all_transactions(), columns=["ID","ID Transaksi", "Tanggal", "Deskripsi", "Akun", "Debit","Kredit"])
groupedData = transactions.groupby("Akun")
summary = groupedData.agg(
  Debit=("Debit", "sum"),
  Kredit=("Kredit","sum")
)
summary["Balance"] = summary["Debit"] - summary["Kredit"]

for account, group in groupedData:
  st.subheader(account)
  group_reset = group.reset_index(drop=True)
  st.table(group_reset.style.hide(axis="index"))

st.subheader("Ringkasan")
st.table(summary)
