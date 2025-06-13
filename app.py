
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

# Dropdowns
song_options = master_df["Song"].dropna().unique()
dance_options = master_df["Line Dance Name"].dropna().unique()

col1, col2 = st.columns(2)
with col1:
    selected_song = st.selectbox("🎵 Song Title", [""] + list(song_options))
with col2:
    selected_dance = st.selectbox("🕺🏾 Line Dance Name", [""] + list(dance_options))

# Auto-fill logic
auto_row = None
if selected_song:
    auto_row = master_df[master_df["Song"] == selected_song].iloc[0]
elif selected_dance:
    auto_row = master_df[master_df["Line Dance Name"] == selected_dance].iloc[0]

if auto_row is not None:
    song = auto_row["Song"]
    artist = auto_row["Artist"]
    line_dance_name = auto_row["Line Dance Name"]
    mood = auto_row["Mood Tag"]
    level = auto_row["Dance Level"]
else:
    st.warning("⚠️ Please select a song or line dance, or fill out the 'If not listed' section.")
    song = ""
    artist = ""
    line_dance_name = ""
    mood = ""
    level = ""

# Fallback entry
unlisted = st.text_input("📝 If not listed, type full song + artist here")

# Remaining inputs
version = st.radio("🎚️ Version", ["Original", "Remix"])
occasion = st.text_input("📅 Occasion or Dedication (optional)")
user = st.text_input("🧍🏽 Your Name or Nickname")
rating = st.slider("How much are you vibin'? 🎧", 0, 5, 5)
need_music = st.radio("Do we need to find the track?", ["No", "Yes"])

if st.button("✅ Submit Request"):
    if not (selected_song or selected_dance or unlisted):
        st.error("🚫 Please select a song, line dance, or fill out the unlisted song field.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unique_id = f"VQ{int(datetime.now().timestamp())}"
        new_row = [
            timestamp, song, artist, line_dance_name, "", version, mood, level,
            user, occasion, rating, "Pending", "App", "", "", "", "",
            need_music, "", "", "", unique_id
        ]
        request_log_ws.append_row(new_row)
        st.success("🎉 Your request was submitted successfully!")
