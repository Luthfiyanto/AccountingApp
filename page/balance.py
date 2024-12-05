import streamlit as st
import pandas as pd
from models.balance import getBalance
st.title("Neraca Saldo")

# Menampilkan neraca saldo
st.subheader("Neraca Saldo")
# balance_df = pd.DataFrame()
balance_data = getBalance()
print(balance_data)
# st.write(balance_df)