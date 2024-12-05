import streamlit as st
import pandas as pd
from models.inventory import get_inventory, add_inventory, delete_inventory, update_inventory

#Inisialisasi persediaan
if "inventory" not in st.session_state:
    st.session_state["inventory"] = []
    st.session_state["inventory"] = get_inventory()

st.subheader("Inventory")

tab_display, tab_edit = st.tabs(['Overview', 'Edit'])

with tab_display:
     # Tabel persediaan
     st.write("### Daftar Persediaan")
     inventory_df = pd.DataFrame(st.session_state["inventory"], columns=["Kode Item", "Nama Barang", "Unit", "Harga Satuan", "Jumlah"])
     st.write(inventory_df)

     # # Jika inventory memiliki data, tampilkan tabel dan tombol hapus
     if st.session_state["inventory"]:
          inventory_df = pd.DataFrame(st.session_state["inventory"])

with tab_edit:
     st.subheader("Edit Data")
     # Input untuk menambahkan persediaan baru
     col1, col2, col3, col4, col5 = st.columns(5)
     with col1:
          item_code = st.text_input("Kode Item")
     with col2:
          item_name = st.text_input("Nama Barang")
     with col3:
          item_unit = st.number_input("Unit", min_value=0)
     with col4:
          item_price = st.number_input("Harga Satuan", min_value=0, step=100)
     with col5:
          item_total = item_unit * item_price

     if st.button("Tambah Persediaan"):
          result = add_inventory(
                    item_code,
                    item_name,
                    item_unit,
                    item_price,
                    item_total
               )
               
          st.session_state["inventory"] = get_inventory()
          st.success("Data berhasil disimpan.")
          
     # # Menampilkan tabel data persediaan
     header_col1, header_col2, header_col3, header_col4, header_col5, header_col6 = st.columns(6)
     with header_col1:
          st.write("ID")
     with header_col2:
          st.write("Nama")
     with header_col3:
          st.write("Kategori")
     with header_col4:
          st.write("Stok")
     with header_col5:
          st.write("Harga")
     with header_col6:
          st.write("Aksi")
     for i, row in inventory_df.iterrows():
          col1, col2, col3, col4, col5, col6 = st.columns(6)
          with col1:
               st.write(row[0])
          with col2:
               st.write(row[1])
          with col3:
               st.write(row[2])
          with col4:
               st.write(row[3])
          with col5:
               st.write(row[4])
          with col6:
               # Tombol hapus untuk setiap baris
               if st.button(f"Hapus", key=f"hapus_{row[0]}"):
                    delete_inventory(row[0])
                    st.session_state["inventory"] = get_inventory()

     else:
          st.write("Tidak ada data persediaan.")