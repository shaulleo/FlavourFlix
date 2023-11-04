import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Peter Parker", "Rebeca Miller"]
usernames = ["ppparker", "rmiller"]
passwords = ['abc123', 'def456']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent.parent / "data" / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)