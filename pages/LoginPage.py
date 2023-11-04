import pickle
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth



# --- User Login ---
names = ["Peter Parker", "Rebeca Miller"]
usernames = ["ppparker", "rmiller"]

file_path = Path(__file__).parent.parent / "data" / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "Home", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Something is wrong! Please try again or create an account.")

if authentication_status == None:
    st.warning("Please enter your username and password.")

if authentication_status:
    st.sucess('Logged on successfully!')
    #Código para entrar nas restantes páginas!
    
# -- SIDEBAR for log out

authenticator.logout("Logout", "Sidebar")
st.sidebar.title(f"Welcome {name}")
