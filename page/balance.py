import streamlit as st
import pandas as pd
from models.transactions import get_all_transactions
from models.accounts import get_all_accounts

st.subheader("Neraca Saldo")

transactions = pd.DataFrame(get_all_transactions(), columns=["ID","ID Transaksi", "Tanggal", "Deskripsi", "Akun", "Debit","Kredit"])
groupedData = transactions.groupby("Akun")
summary = groupedData.agg(
  Debit=("Debit", "sum"),
  Kredit=("Kredit","sum")
)
summary["Balance"] = (summary["Debit"] - summary["Kredit"]).abs()

st.table(summary)

total_debit = transactions["Debit"].sum()
total_credit = transactions["Kredit"].sum()
total_balance = abs(total_debit - total_credit)

# Filter transactions sales & non sales
sales_transactions = transactions[transactions["Akun"] == "Penjualan"]
non_sales_transactions = transactions[transactions["Akun"] != "Penjualan"]

# Calculate total sales & non sales
total_sales_credit = sales_transactions["Kredit"].sum()
total_non_sales_debit = non_sales_transactions["Debit"].sum()

summary = {
    "Total Debit": total_non_sales_debit,
    "Total Kredit": total_sales_credit,
    "Total Balance": total_balance
}

st.table(summary)