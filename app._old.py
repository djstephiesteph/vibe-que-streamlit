import streamlit as st
import pandas as pd
import datetime

# ---- Set Page Config ----
st.set_page_config(page_title="Vibe Que by DJ StephieSteph", layout="wide")

# ---- Load or Initialize Data ----
if 'requests' not in st.session_state:
    st.session_state.requests = pd.DataFrame(columns=[
        'Timestamp', 'Guest Name', 'Song Title', 'Artist Name', 'Line Dance Name',
        'Requested Song (Custom)', 'Vibe/Mood', 'Date of Event', 'Status'
    ])

# ---- Vibe Options ----
vibe_options = [
    '🎉 Turn Up / 💪 Hype',
    '😎 Smooth Vibe / 🧘🏾‍♀️ Mellow Groove',
    '🤠 Southern Soul',
    '🌬️ Moderate'
]

# ---- Song Request Form ----
st.title("🎧 Vibe Que by DJ StephieSteph")
st.markdown("_Drop your request and help shape the vibe tonight. LET'S WORK!_")

with st.form("song_request_form"):
    st.subheader("🎶 Submit a Song Request")
    guest_name = st.text_input("Your Name")
    song_title = st.text_input("Song Title")
    artist_name = st.text_input("Artist Name")
    line_dance_name = st.text_input("Line Dance Name (if known)")
    custom_song = st.text_input("Requested Song (if not in list)")
    vibe = st.selectbox("Vibe or Mood", options=vibe_options)
    event_date = st.date_input("Date of Event", value=datetime.date.today())
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        new_row = pd.DataFrame([{
            'Timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Guest Name': guest_name,
            'Song Title': song_title,
            'Artist Name': artist_name,
            'Line Dance Name': line_dance_name,
            'Requested Song (Custom)': custom_song,
            'Vibe/Mood': vibe,
            'Date of Event': event_date,
            'Status': 'Not Played'
        }])
        st.session_state.requests = pd.concat([st.session_state.requests, new_row], ignore_index=True)
        st.success("Your request has been submitted!")

# ---- Display Requests ----
st.subheader("📋 Live Request Queue")

if not st.session_state.requests.empty:
    for i, row in st.session_state.requests.iterrows():
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"**{row['Song Title']}** by *{row['Artist Name']}* ({row['Vibe/Mood']})")
        with col2:
            st.markdown(f"Status: {row['Status']}")
        with col3:
            if st.button(f"Mark Played #{i}"):
                st.session_state.requests.at[i, 'Status'] = 'Played'

# ---- Export Section ----
st.markdown("---")
st.subheader("📥 Export Requests")
st.download_button(
    label="Download as CSV",
    data=st.session_state.requests.to_csv(index=False).encode('utf-8'),
    file_name='vibe_que_requests.csv',
    mime='text/csv'
)

st.caption("Powered by Soulware Systems • Where culture meets code. 🔷")
