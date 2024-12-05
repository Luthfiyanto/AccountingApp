import streamlit as st
# def ReportPage():
st.title("Laporan Laba Rugi")

        # Laporan Laba Rugi
pendapatan = st.session_state["accounts"]["Pendapatan"]
beban = st.session_state["accounts"]["Beban"]
laba_rugi = pendapatan - beban

st.write("Pendapatan:", pendapatan)
st.write("Beban:", beban)
st.write("Laba (Rugi):", laba_rugi)