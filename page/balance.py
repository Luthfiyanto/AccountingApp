import streamlit as st
import pandas as pd
from models.transactions import get_all_transactions
from models.accounts import get_all_accounts

st.subheader("Neraca Saldo")

transactions = pd.DataFrame(get_all_transactions(), columns=["ID","ID Transaksi", "Tanggal", "Deskripsi", "Akun", "Debit","Kredit"])
groupedData = transactions.groupby("Akun")
summary = groupedData.agg(
  total_debit=("Debit", "sum"),
  total_credit=("Kredit","sum")
)
summary["balance"] = summary["total_debit"] - summary["total_credit"]

st.table(summary)

total_debit = transactions["Debit"].sum()
total_credit = transactions["Kredit"].sum()
total_balance = total_debit - total_credit

summary = {
    "Total Debit": total_debit,
    "Total Kredit": total_credit,
    "Total Balance": total_balance
}

st.table(summary)