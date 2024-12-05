import streamlit as st
import datetime
import pandas as pd

# def TransactionPage():
st.title("Jurnal Umum")

        # Form untuk menambahkan transaksi
col1, col2 = st.columns(2)
with col1:
            date = st.date_input("Tanggal", datetime.date.today())
            description = st.text_input("Deskripsi")
with col2:
            # Pilih lebih dari satu akun untuk debit dan kredit
            debit_accounts = st.multiselect("Akun Debit", list(st.session_state["accounts"].keys()))
            debit_amounts1 = [st.number_input(f"Jumlah Debit 1 untuk {account}", min_value=0.0) for account in debit_accounts]
            debit_amounts2 = [st.number_input(f"Jumlah Debit 2 untuk {account}", min_value=0.0) for account in debit_accounts]
        
            credit_accounts = st.multiselect("Akun Kredit", list(st.session_state["accounts"].keys()))
            credit_amounts1 = [st.number_input(f"Jumlah Kredit 1 untuk {account}", min_value=0.0) for account in credit_accounts]
            credit_amounts2 = [st.number_input(f"Jumlah Kredit 2 untuk {account}", min_value=0.0) for account in credit_accounts]

if st.button("Simpan Transaksi"):
            total_debit = sum(debit_amounts1) 
            total_credit = sum(credit_amounts1)

            if total_debit == total_credit:
                # Simpan transaksi ke dalam sesi
                for i, account in enumerate(debit_accounts):
                    st.session_state["transactions"].append({
                    "Tanggal": date,
                    "Deskripsi": description,
                    "Akun": account,
                    "Debit": debit_amounts1[i] + debit_amounts2[i],
                    "Kredit": 0.0
                })
                # Update saldo akun
                st.session_state["accounts"][account] += (debit_amounts1[i] + debit_amounts2[i])

            for i, account in enumerate(credit_accounts):
                st.session_state["transactions"].append({
                    "Tanggal": date,
                    "Deskripsi": description,
                    "Akun": account,
                    "Debit": 0.0,
                    "Kredit": credit_amounts1[i] + credit_amounts2[i]
                })
                # Update saldo akun
                st.session_state["accounts"][account] -= (credit_amounts1[i] + credit_amounts2[i])

            st.success("Transaksi berhasil disimpan.")
else:
            st.error("Total Jumlah Debit dan Kredit harus sama.")

        # Tabel Jurnal umum
st.write("### Daftar Transaksi")
transaction_df = pd.DataFrame(st.session_state["transactions"])
st.write(transaction_df)