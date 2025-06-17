import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"

]
import json
creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open the Google Sheet and use the 'Request Log' tab
SHEET_ID = "1JkgaBwbmy7iT8iuEaekEIhWMyc4Su35GnFiRqw2pS9Y"
worksheet = client.open_by_key(SHEET_ID).worksheet("Request Log")

# Streamlit UI
st.title("🎶 Vibe Que Song Request Form")
st.markdown("Welcome to the Vibe Zone! Drop your favorite song or line dance request below.")

# Form inputs
song = st.text_input("🎵 Song Title")
artist = st.text_input("🎤 Artist")
dance_name = st.text_input("🕺🏾 Line Dance Name (if any)")
version = st.radio("🎚️ Version", ["Original", "Remix"])
mood = st.selectbox("🧠 Mood/Vibe", ["🔥 Hype", "💃🏾 Dance", "🎉 Party", "🎶 Chill", "🎯 Smooth", "🎭 Unknown"])
tempo = st.selectbox("⏱️ Tempo", ["Slow", "Moderate", "Fast", "Unknown"])
level = st.selectbox("📘 Dance Level", ["Beginner", "Intermediate", "Trailride", "Sexy/Slow"])
occasion = st.text_input("📅 Occasion or Dedication (optional)")
user = st.text_input("🧍🏽 Your Name or Nickname")
unlisted = st.text_input("📝 If not listed, type full song + artist here")
rating = st.slider("How much are you vibin'? 🎧", 0, 5, 5)
need_music = st.radio("Do we need to find the track?", ["No", "Yes"])

if st.button("✅ Submit Request"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    unique_id = f"VQ{int(datetime.now().timestamp())}"
    new_row = [
        timestamp, song, artist, dance_name, "", version, mood, level,
        user, occasion, rating, "Pending", "App", tempo, "", "", "",
        need_music, "", "", "", unique_id
    ]
    worksheet.append_row(new_row)
    st.success("🎉 Your request was submitted successfully!")
