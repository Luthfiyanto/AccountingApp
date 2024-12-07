import streamlit as st
import pandas as pd
from models.accounts import get_all_accounts
from models.transactions import get_all_transactions
# def ReportPage():
st.subheader("Laporan Laba Rugi")

st.session_state["transactions"] = get_all_transactions()
accounts_df = pd.DataFrame(get_all_accounts(), columns=["Kode", "Akun"])

def classify_account(code):
        if 4000 <= code <= 4999:
                return "Pendapatan"
        elif 5000 <= code < 5999:
                return "HPP"
        elif 6000 <= code <= 6999:
                return "Beban Operasional"
        else:
                return "Lainnya"

accounts_df["category"] = accounts_df["Kode"].apply(classify_account)

transaction_df = pd.DataFrame(st.session_state["transactions"], columns=["ID","ID Transaksi", "Tanggal", "Deskripsi", "Akun", "Debit","Kredit"])
transaction_df = transaction_df.merge(
        accounts_df[["Akun", "category"]],
        on="Akun",
        how="left"
)

summary_debit = transaction_df.groupby("category")["Debit"].sum().reset_index()
summary_kredit = transaction_df.groupby("category")["Kredit"].sum().reset_index()

pendapatan1 = summary_debit.loc[summary_debit["category"] == "Pendapatan", "Debit"].sum()
pendapatan2 = summary_kredit.loc[summary_kredit["category"] == "Pendapatan", "Kredit"].sum()
pendapatan = pendapatan2 - pendapatan1

hpp = summary_debit.loc[summary_debit["category"] == "HPP", "Debit"].sum()
beban_operasional = summary_debit.loc[summary_debit["category"] == "Beban Operasional", "Debit"].sum()

laba_kotor = pendapatan - hpp
laba_bersih = laba_kotor - beban_operasional

summary = {
        "Pendapatan": pendapatan,
        "HPP": hpp,
        "Laba Kotor": laba_kotor,
        "Beban Operasional": beban_operasional,
        "Laba Bersih": laba_bersih
}

st.table(summary)