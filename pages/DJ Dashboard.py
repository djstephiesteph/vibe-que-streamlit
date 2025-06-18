import streamlit as st

st.set_page_config(page_title="DJ Dashboard", layout="wide")

dj_key = st.text_input("Enter DJ Access Code", type="password")

if dj_key == "LETSDJ2025":
    st.title("🎛️ DJ Dashboard — VibeQue")
    st.success("Access granted. Welcome, DJ StephieSteph! 🎧")

    st.markdown("""
    - 🔁 View, queue, or skip song requests
    - ✅ Mark songs as played
    - 🏆 View top requestors
    - 📊 Track vibe stats (coming soon)
    """)

    st.subheader("📋 Request Queue")
    st.write("_(Live data from Google Sheets will show here in production.)_")
else:
    st.warning("This page is restricted. Please enter your DJ access code to continue.")
