# 🕒 [2025-06-16 | 1:10 PM EST] - Full Updated app.py for VibeQué

import streamlit as st
import pandas as pd
import datetime
import gspread
from gspread_pandas import Spread, Client
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheet Access
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

GOOGLE_CREDS = st.secrets["GOOGLE_CREDS"]
SHEET_ID = "1JkgaBwbmy7iT8iuEaekEIhWMyc4Su35GnFiRqw2pS9Y"

credentials = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDS, scope)
client = gspread.authorize(credentials)

master_ws = client.open_by_key(SHEET_ID).worksheet("Master Song List")
requests_ws = client.open_by_key(SHEET_ID).worksheet("Requests")

# Load the master song list
df = pd.DataFrame(master_ws.get_all_records())

# App Layout
st.set_page_config(page_title="VibeQué DJ App", layout="wide")
st.title("🎧 VibeQué with DJStefieStef")
st.caption("🔥 Check In. Request. Dance. Repeat. — #LETS WORK!!")

# Welcome Splash (if needed)
if "welcome_shown" not in st.session_state:
    st.session_state["welcome_shown"] = True
    st.success("🎉 Welcome to VibeQué! Ready to turn up the vibe?")

# Request or Check-In Toggle
submission_type = st.radio("What would you like to do?", ["Request a Song", "Just Checking In"], index=0)

# Submission Form
with st.form("request_form"):
    user_name = st.text_input("Your Name")
    song = st.selectbox("Pick a Song", options=[""] + df["Song"].dropna().unique().tolist())
    artist = st.text_input("Artist (optional)")
    line_dance = st.text_input("Line Dance Name (optional)")
    remix = st.radio("Remix or Original?", ["Original", "Remix"], index=0)
    mood = st.selectbox("What’s the mood?", ["🎉 Party", "💃🏾 Dance", "🔥 Hype", "🛋 Chill", "❤️ Sexy", "🙌 Classic"])
    level = st.selectbox("Dance Level", ["🔵 Beginner", "🟠 Intermediate", "🟤 Trailride", "🔴 Sexy/Slow"])
    occasion = st.text_input("Shoutout / Occasion? (optional)")
    rating = st.slider("Vibe Rating", 1, 5, 5)

    submitted = st.form_submit_button("🚀 Submit")

    if submitted:
        timestamp = datetime.datetime.now().strftime("%m/%d/%y @ %I:%M%p")
        unique_id = f"VQ{str(datetime.datetime.now().timestamp()).replace('.', '')[-5:]}"

        entry = [
            timestamp,
            song,
            artist,
            line_dance,
            df[df["Song"] == song]["Category"].values[0] if song in df["Song"].values else "",
            remix,
            mood,
            level,
            user_name,
            occasion,
            rating,
            "Queued",
            submission_type,
            df[df["Song"] == song]["Tempo"].values[0] if song in df["Song"].values else "",
            df[df["Song"] == song]["BPM"].values[0] if song in df["Song"].values else "",
            "",
            "",
            "",
            "",
            "",
            unique_id
        ]

        requests_ws.append_row(entry)

        st.success("✅ Request Confirmed!")
        st.info("📝 You're on your way to top requester status! Keep the vibe going!")

# Live Queue Display
st.subheader("🎶 Live Request Queue")
request_df = pd.DataFrame(requests_ws.get_all_records())
request_df = request_df[request_df["Status"] == "Queued"]
if not request_df.empty:
    st.dataframe(request_df[["Timestamp", "Song", "Artist", "Mood", "User", "Submission Type"]].sort_values(by="Timestamp", ascending=False))
else:
    st.warning("⚠️ No current requests. Be the first to start the party!")

# Request Cart Preview (mini queue view)
with st.expander("🛒 View My Request Cart"):
    user_filter = st.text_input("Enter your name to view your request(s)")
    if user_filter:
        user_requests = request_df[request_df["User"].str.lower() == user_filter.lower()]
        st.write(user_requests[["Song", "Status", "Mood"]])

# Export (for DJ only)
st.sidebar.title("DJ Tools")
if st.sidebar.button("📥 Export Requests"):
    st.sidebar.download_button(
        label="Download CSV",
        data=request_df.to_csv(index=False).encode("utf-8"),
        file_name="vibeque_requests_export.csv",
        mime="text/csv"
    )
