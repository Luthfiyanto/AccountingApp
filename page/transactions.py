import streamlit as st
import datetime
import pandas as pd
from models.transactions import get_all_transactions, save_transactions, get_transactions, get_transaction_detail, update_transaction, delete_transaction

# inisialisasi state
if "transactions" not in st.session_state:
    st.session_state["transactions"] = []
    st.session_state["transactions"] = get_all_transactions()

st.session_state["transactions"] = get_all_transactions()
# def TransactionPage():
st.subheader("Jurnal Umum")

tab_add, tab_edit, tab_delete = st.tabs(["Add Transaction", "Edit Transaction", "Delete Transaction"])

with tab_add:
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
                debit_amounts = [st.number_input(f"Jumlah Debit untuk {account}", min_value=0) for account in debit_accounts]
            
                credit_accounts = st.multiselect("Akun Kredit", options=(st.session_state["accounts"]))
                credit_amounts = [st.number_input(f"Jumlah Kredit untuk {account}", min_value=0) for account in credit_accounts]

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

    total_debit = transaction_df["Debit"].sum()
    total_credit = transaction_df["Kredit"].sum()
    total_balance = total_debit - total_credit

    summary = {
        "Total Debit": total_debit,
        "Total Kredit": total_credit,
        "Total Balance": total_balance
    }

    st.table(transaction_df)

    st.table(summary)

# Edit transaction
with tab_edit:
    trans_data = pd.DataFrame(get_transactions(), columns=["ID Transaksi", "Tanggal", "Deskripsi"])
    transaction_id = st.selectbox("Pilih Transaksi", options=(trans_data["ID Transaksi"]))

    if transaction_id:
        recent_t_detail = get_transaction_detail(transaction_id)

        newDate = st.date_input("Tanggal Baru", value=datetime.datetime.strptime(trans_data.loc[trans_data["ID Transaksi"] == transaction_id, "Tanggal"].values[0], "%Y-%m-%d"))
        newDescription = st.selectbox("Deskripsi Baru", [
            "Penjualan barang dagang",
            "Pembelian barang dagang",
            "Pembayaran gaji karyawan",
            "Pembayaran listrik, air & sampah"
        ])
        
        debit_entries = [(d[3], d[4]) for d in recent_t_detail if d[2] == "debit"]
        credit_entries = [(d[3], d[4]) for d in recent_t_detail if d[2] == "credit"]

        new_debit_accounts = st.multiselect("Akun Debit",options=(st.session_state["accounts"]), default=([d[0] for d in debit_entries]) )
        new_debit_amounts = [st.number_input(f"Jumlah Debit untuk {account}", min_value=0, value=amount) for account, amount in debit_entries]

        new_credit_accounts = st.multiselect("Akun Kredit", options=(st.session_state["accounts"]), default=([d[0] for d in credit_entries]))
        new_credit_amounts = [st.number_input(f"Jumlah Kredit untuk {account}", min_value=0, value=amount) for account, amount in credit_entries]

        if st.button("Simpan Perubahan"):
            total_debit = sum(new_debit_amounts) 
            total_credit = sum(new_credit_amounts)

            debit_data = list(zip(new_debit_accounts,new_debit_amounts))
            credit_data = list(zip(new_credit_accounts,new_credit_amounts))

            if total_debit == total_credit:
                update_transaction(transaction_id, newDate, newDescription, debit_data, credit_data)
                st.success("Transaksi berhasil diubah.")
                st.session_state["transactions"] = get_all_transactions()
            else:
                st.error("Total Jumlah Debit dan Kredit harus sama.")
    
with tab_delete:
    trans_data = pd.DataFrame(get_transactions(), columns=["ID Transaksi", "Tanggal", "Deskripsi"])
    transaction_id = st.selectbox("Pilih Transaksi yang akan dihapus", options=trans_data["ID Transaksi"])

    if transaction_id:
        selected_transaction = trans_data.loc[trans_data["ID Transaksi"] == transaction_id]
        detail_transaction = pd.DataFrame(get_transaction_detail(transaction_id), columns=["ID", "ID Transaksi", "Tipe", "Akun", "Jumlah"])
        st.write("### Transaksi")
        st.table(selected_transaction)
        st.write("### Detail Transaksi")
        st.table(detail_transaction)

        if st.button("Hapus Transaksi"):
            delete_transaction(transaction_id)
            st.success("Transaksi berhasil dihapus.")
            st.session_state["transactions"] = get_all_transactions()
            st.rerun()