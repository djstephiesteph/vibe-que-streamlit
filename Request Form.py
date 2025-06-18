import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# ---- Google Sheets Auth Setup ----
creds_dict = st.secrets["GOOGLE_CREDS"]
creds = Credentials.from_service_account_info(creds_dict, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])
gc = gspread.authorize(creds)

# 🔗 Open the sheet
worksheet = gc.open_by_key("1JkgaBwbmy7iT8iuEaekEIhWMyc4Su35GnFiRqw2pS9Y").worksheet("Request Log")

# ---- Streamlit Request Form ----
st.title("🎧 VibeQue Request Form")

st.markdown("""
Use the form below to request up to 4 songs or line dances for tonight’s event! 💃🏾🕺🏽
""")

with st.form("request_form"):
    name = st.text_input("Your Name")
    song1 = st.text_input("Song or Line Dance #1")
    song2 = st.text_input("Song or Line Dance #2")
    song3 = st.text_input("Song or Line Dance #3")
    song4 = st.text_input("Song or Line Dance #4")
    submit = st.form_submit_button("Submit")

if submit:
    worksheet.append_row([name, song1, song2, song3, song4])
    st.success(f"Thanks {name}! Your request has been submitted. 🎶")
