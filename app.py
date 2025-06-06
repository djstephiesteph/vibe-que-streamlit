import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ---- SETUP GOOGLE SHEETS ACCESS ---- #
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
creds_dict = json.loads(st.secrets["credentials"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)

# OPEN GOOGLE SHEET & WORKSHEETS (make sure names match your sheet and tabs)
sheet = client.open("VibeQue_DJ_Master")  # <-- your Google Sheet title
master_songs = sheet.worksheet("Master Songs")
requests_sheet = sheet.worksheet("Song Requests")

# LOAD MASTER SONG DATA
song_data = master_songs.get_all_records()
df = pd.DataFrame(song_data)

# ---- STREAMLIT USER INTERFACE ---- #
st.image("logo.png", width=300)
st.markdown("### 🎧 Welcome to Vibe Que - The Ultimate DJ Request Experience")

name = st.text_input("Your Name (optional)", placeholder="Enter name or nickname")

# SELECT UP TO 4 SONGS
selected_songs = []
remix_choices = []
artist_matches = []
dance_matches = []
mood_tags = []

for i in range(1, 5):
    song = st.selectbox(f"Select Song {i}", ["---"] + sorted(df['Song Title'].unique()), key=f"song_{i}")
    if song != "---":
        remix = st.radio(f"Remix or Original for {song}?", ["Original", "Remix"], key=f"version_{i}")
        match = df[df['Song Title'] == song].iloc[0]

        selected_songs.append(song)
        remix_choices.append(remix)
        artist_matches.append(match['Artist'])
        dance_matches.append(match['Line Dance Name'])
        mood_tags.append(match['Mood Tag'])
    else:
        selected_songs.append("")
        remix_choices.append("")
        artist_matches.append("")
        dance_matches.append("")
        mood_tags.append("")

# CUSTOM REQUEST SECTION
custom_entry = st.text_input("Request a song or line dance NOT listed")
custom_artist = st.text_input("Who is the artist? (Required if above is filled)")

# SUBMIT BUTTON
if st.button("Submit Request"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, name] + \
          [val for group in zip(selected_songs, remix_choices, artist_matches, dance_matches, mood_tags) for val in group] + \
          [custom_entry, custom_artist, "No", "", "", "", "", "", ""]

    requests_sheet.append_row(row)
st.success("✅ Your request has been added to the Vibe Que queue!")



