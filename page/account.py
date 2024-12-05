import streamlit as st
import pandas as pd
from models.accounts import get_all_accounts, delete_account, create_account

if "accounts" not in st.session_state:
    st.session_state["accounts"] = get_all_accounts()
    
st.subheader("Manage Account")

# account_pd = pd.DataFrame(st.session_state["account"], columns=["ID", "Akun"])
account_pd = pd.DataFrame(get_all_accounts(), columns=["ID", "Akun"])

# Input akun baru
col1, col2 = st.columns(2)
with col1:
  new_account_id = st.number_input("Kode minimal 4 angka", min_value=1000)
with col2:
  new_account = st.text_input("Akun baru")

if st.button("Enter"):
  result = create_account(new_account_id,new_account)
  st.session_state["account"]= get_all_accounts()
  st.success("Data berhasil disimpan")
  st.rerun()

header_col1, header_col2, header_col3 = st.columns(3)
with header_col1:
  st.write("ID")
with header_col2:
  st.write("Akun")
with header_col3:
  st.write("Aksi")

for i, row in account_pd.iterrows():
  print()
  col1, col2, col3 = st.columns(3)
  with col1:
    st.write(row[0])
  with col2:
    st.write(row[1])
  with col3:
    if st.button(f"Hapus", key=f"hapus_akun_{row[0]}"):
      delete_account(row[0],row[1])
      st.session_state["account"]= get_all_accounts()
      st.rerun()