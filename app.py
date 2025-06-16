import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2 import service_account

# Setup Google Sheets Credentials
GOOGLE_CREDS = st.secrets["google_service_account"]
SHEET_ID = st.secrets["google_sheets"]["SHEET_ID"]

# Authorize Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = service_account.Credentials.from_service_account_info(GOOGLE_CREDS, scopes=scope)
client = gspread.authorize(credentials)

# Open Sheets
master_ws = client.open_by_key(SHEET_ID).worksheet("Master Song List")
requests_ws = client.open_by_key(SHEET_ID).worksheet("Requests")

# Load Song List as DataFrame
df = pd.DataFrame(master_ws.get_all_records())

# Streamlit App Config
st.set_page_config(page_title="VibeQué DJ App", layout="wide")
st.title("🎧 VibeQué with DJStefieStef")
st.caption("🔥 Check In. Request. Dance. Repeat. — #LETS WORK!!")

# Show Welcome Splash Once
if "welcome_shown" not in st.session_state:
    st.session_state["welcome_shown"] = True
    st.success("🎉 Welcome to VibeQué! Ready to turn up the vibe?")

# Request or Check-In Toggle
submission_type = st.radio("What would you like to do?", ["Request a Song", "Just Checking In"], index=0)

# Start Form
with st.form("request_form"):
    user_name = st.text_input("Your Name")
    song_options = [""] + df["Song"].dropna().unique().tolist()
    song = st.selectbox("Pick a Song", options=song_options)
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

        # Pull additional song info safely
        row = df[df["Song"] == song]
        category = row["Category"].values[0] if not row.empty else ""
        tempo = row["Tempo"].values[0] if not row.empty else ""
        bpm = row["BPM"].values[0] if not row.empty else ""

        entry = [
            timestamp,
            song,
            artist,
            line_dance,
            category,
            remix,
            mood,
            level,
            user_name,
            occasion,
            rating,
            "Queued",
            submission_type,
            tempo,
            bpm,
            "", "", "", "", "",  # Empty fields for MP3, Source, etc.
            unique_id
        ]

        # Submit to Sheet
        requests_ws.append_row(entry)
        st.success("✅ Request Confirmed!")
        st.info("📝 You're on your way to top requester status! Keep the vibe going!")

# Show Live Queue
st.subheader("🎶 Live Request Queue")
request_df = pd.DataFrame(requests_ws.get_all_records())
request_df = request_df[request_df["Status"] == "Queued"]

if not request_df.empty:
    st.dataframe(request_df[["Timestamp", "Song", "Artist", "Mood", "User", "Submission Type"]].sort_values(by="Timestamp", ascending=False))
else:
    st.warning("⚠️ No current requests. Be the first to start the party!")

# User Cart Preview
with st.expander("🛒 View My Request Cart"):
    user_filter = st.text_input("Enter your name to view your request(s)")
    if user_filter:
        user_requests = request_df[request_df["User"].str.lower() == user_filter.lower()]
        st.write(user_requests[["Song", "Status", "Mood"]])

# DJ Tools
st.sidebar.title("DJ Tools")
if st.sidebar.button("📥 Export Requests"):
    st.sidebar.download_button(
        label="Download CSV",
        data=request_df.to_csv(index=False).encode("utf-8"),
        file_name="vibeque_requests_export.csv",
        mime="text/csv"
    )
