
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Google Sheets authentication using secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open Google Sheet and load Master and Request Log tabs
SHEET_ID = "1JkgaBwbmy7iT8iuEaekEIhWMyc4Su35GnFiRqw2pS9Y"
master_ws = client.open_by_key(SHEET_ID).worksheet("Master Song List")
request_log_ws = client.open_by_key(SHEET_ID).worksheet("Request Log")

# Load Master Song List into DataFrame
master_data = master_ws.get_all_records()
master_df = pd.DataFrame(master_data)

# Streamlit UI setup
st.title("🎶 Vibe Que Song Request Form")
st.markdown("Welcome to the Vibe Zone! Drop your favorite song or line dance request below.")

# Dropdowns populated from Master
song_options = master_df["Song"].dropna().unique()
song = st.selectbox("🎵 Song Title", [""] + list(song_options))

# Auto-fill Artist and Dance based on song selection
if song:
    selected_row = master_df[master_df["Song"] == song].iloc[0]
    artist = selected_row["Artist"]
    line_dance_name = selected_row["Line Dance Name"]
else:
    artist = st.text_input("🎤 Artist")
    line_dance_name = st.text_input("🕺🏾 Line Dance Name (if any)")

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
        timestamp, song, artist, line_dance_name, "", version, mood, level,
        user, occasion, rating, "Pending", "App", tempo, "", "", "",
        need_music, "", "", "", unique_id
    ]
    request_log_ws.append_row(new_row)
    st.success("🎉 Your request was submitted successfully!")
