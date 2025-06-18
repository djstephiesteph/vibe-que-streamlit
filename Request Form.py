import streamlit as st

st.title("🎧 VibeQue Request Form")

st.markdown("""
Use the form below to request up to 4 songs or line dances for tonight’s event! 💃🏾🕺🏽

_(This is just a placeholder. The full dynamic form will be built soon.)_
""")

with st.form("request_form"):
    name = st.text_input("Your Name")
    song1 = st.text_input("Song or Line Dance #1")
    song2 = st.text_input("Song or Line Dance #2")
    song3 = st.text_input("Song or Line Dance #3")
    song4 = st.text_input("Song or Line Dance #4")
    submit = st.form_submit_button("Submit")

if submit:
    st.success(f"Thanks {name}! Your request has been submitted. 🎶")