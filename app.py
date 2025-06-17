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
creds_dict = st.secrets["GOOGLE_CREDS"]
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
    dance_level = st.selectbox("🕺🏽 Dance Level", ["Beginner", "Intermediate", "Trailride", "Sexy/Slow"])
    submitted_by = st.text_input("👤 Your Name")
    occasion = st.text_input("🎉 Occasion (optional)")

    submit = st.form_submit_button("Submit Request")

    if submit:
        if not song and not line_dance:
            st.warning("⚠️ You must enter at least a Song or Line Dance Name.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mood = "🔥" if "Remix" in remix or category in ["Club Banger", "Throwback"] else "💃🏾"
            rating = ""
            status = "Queued"
            submission_type = "Early"
            tempo = ""
            bpm = ""
            played = "No"
            date_played = ""
            need_music = "Yes"
            mp3_link = ""
            download_status = "Pending"
            source_platform = ""
            unique_id = f"{timestamp}_{submitted_by}"

            new_row = [
                timestamp, song, artist, line_dance, category, remix, mood,
                dance_level, submitted_by, occasion, rating, status,
                submission_type, tempo, bpm, played, date_played,
                need_music, mp3_link, download_status, source_platform, unique_id
            ]
            worksheet.append_row(new_row)
            st.success("✅ Request submitted successfully!")

# ---------- 6. Footer ----------
st.markdown("---")
st.caption("Powered by DJ StephieSteph • #LETS WORK!! 🎧🔥")
