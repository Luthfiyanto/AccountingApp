import streamlit as st
import datetime
import pandas as pd
from models.transactions import get_all_transactions, save_transactions

# inisialisasi state
if "transactions" not in st.session_state:
    st.session_state["transactions"] = []
    st.session_state["transactions"] = get_all_transactions()

# def TransactionPage():
st.subheader("Jurnal Umum")

        # Form untuk menambahkan transaksi
col1, col2 = st.columns(2)
with col1:
            date = st.date_input("Tanggal", datetime.date.today())
            description = st.selectbox("Deskripsi", [
                "Penjualan barang dagang",
                "Pembelian barang dagang",
                "Pembayaran gaji karyawan",
                "Pembayaran listrik, air & sampah"
            ])
with col2:
            # Pilih lebih dari satu akun untuk debit dan kredit
            debit_accounts = st.multiselect("Akun Debit", options=(st.session_state["accounts"]))
            # debit_amounts1 = [st.number_input(f"Jumlah Debit 1 untuk {account}", min_value=0.0) for account in debit_accounts]
            # debit_amounts2 = [st.number_input(f"Jumlah Debit 2 untuk {account}", min_value=0.0) for account in debit_accounts]
            debit_amounts = [st.number_input(f"Jumlah Debit untuk {account}", min_value=0.0) for account in debit_accounts]
        
            credit_accounts = st.multiselect("Akun Kredit", options=(st.session_state["accounts"]))
            # credit_amounts1 = [st.number_input(f"Jumlah Kredit 1 untuk {account}", min_value=0.0) for account in credit_accounts]
            # credit_amounts2 = [st.number_input(f"Jumlah Kredit 2 untuk {account}", min_value=0.0) for account in credit_accounts]
            credit_amounts = [st.number_input(f"Jumlah Kredit untuk {account}", min_value=0.0) for account in credit_accounts]

if st.button("Simpan Transaksi"):
            total_debit = sum(debit_amounts) 
            total_credit = sum(credit_amounts)

            debit_data = list(zip(debit_accounts,debit_amounts))
            credit_data = list(zip(credit_accounts,credit_amounts))

            if total_debit == total_credit:
            # Simpan transaksi ke dalam sesi
                save_transactions(date, description, debit_data, credit_data)
                st.success("Transaksi berhasil disimpan.")
                st.session_state["transactions"] = get_all_transactions()
else:
            st.error("Total Jumlah Debit dan Kredit harus sama.")

        # Tabel Jurnal umum
st.write("### Daftar Transaksi")
transaction_df = pd.DataFrame(st.session_state["transactions"], columns=["ID","ID Transaksi", "Tanggal", "Deskripsi", "Akun", "Debit","Kredit"])
st.write(transaction_df)