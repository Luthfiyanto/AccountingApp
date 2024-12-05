import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
from database import create_connection, initialize_database
from models.auth import register, login, getUser

def AuthPage():
  tab_login, tab_register = st.tabs(['Login', 'Register'])

  with tab_login:
        st.subheader('Login')
        username = st.text_input('Username', key='login_username')
        password = st.text_input('Password', type='password', key='login_password')

        if st.button('Login'):
            user = login(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
                
            else:
                st.error('Username or password is incorrect.')
    
  with tab_register:
        st.subheader('Register')
        username = st.text_input('Username', key='register_username')
        password = st.text_input('Password', type='password', key='register_password')

        if st.button('Register'):
            user = getUser(username)
            if user:
                st.error('Username already exists.')
            else:
                register(username, password)
                