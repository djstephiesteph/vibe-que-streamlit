import streamlit as st
import gspread
import pandas as pd
import json
from datetime import datetime
from google.oauth2.service_account import Credentials

# ---------- 1. Page Setup ----------
st.set_page_config(page_title="VibeQue Request Zone", layout="wide")
st.title("🎧 VibeQue Request Zone")
st.markdown("Request up to 4 songs or line dances for tonight's event! 💃🏾🕺🏽")
st.markdown("---")

# ---------- 2. Google Sheets Auth ----------
creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
creds = Credentials.from_service_account_info(creds_dict)
gc = gspread.authorize(creds)

# ---------- 3. Sheet + Worksheet ----------
SHEET_ID = "1JkgaBwbmy7iT8iuEaekEIhWMyc4Su35GnFiRqw2pS9Y"
worksheet = gc.open_by_key(SHEET_ID).worksheet("Request Log")

# ---------- 4. Load + Display Current Requests ----------
data = worksheet.get_all_records()
df = pd.DataFrame(data)
st.subheader("📋 Current Request Log")
st.dataframe(df, use_container_width=True)

# ---------- 5. Submit Form ----------
st.subheader("➕ Add Your Song or Line Dance Request")

with st.form("request_form", clear_on_submit=True):
    song = st.text_input("🎵 Song Title")
    artist = st.text_input("🎤 Artist")
    line_dance = st.text_input("💃🏾 Line Dance Name (if any)")
    category = st.selectbox("🎧 Category", ["Line Dance", "Slow Jam", "Club Banger", "Throwback", "Other"])
    remix = st.radio("Remix Version?", ["Original", "Remix", "Either"])
