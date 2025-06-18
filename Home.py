import streamlit as st

# 🎧 Display your actual welcome logo (filename must match GitHub exactly)
st.image("Vibe Zone with DJ Stefie Stef.png", use_container_width=True)

# 💬 Welcome message
st.markdown("""
## 🎉 Welcome to the Vibe Zone!
Request your favorite songs, earn badges, and keep the vibe alive!

Before you start, please review our event participation terms.
We use your name to track requests, award badges, and keep the queue running smoothly.
""")

# 📜 Terms & Conditions inside a scrollable section
with st.expander("📜 View Full Terms & Conditions"):
    st.markdown("""
**VibeQue App Terms & Conditions**

**1. Introduction**  
Welcome to the VibeQue App. This platform allows users to submit song and line dance requests during live events. By using this platform, you agree to the following terms.

**2. Acceptance of Terms**  
Before submitting a request, users must agree to these terms. A brief consent checkbox will appear at submission, and a full version of these terms will be viewable via popup.

**3. User Conduct & Guidelines**  
Users agree to submit respectful and appropriate content. VibeQue reserves the right to filter, remove, or reject submissions that violate community standards.

**4. Request Submission Policy**  
Each user may submit up to four (4) requests per session. Additional requests are not guaranteed and may be delayed or denied depending on queue volume.

**5. Data Use & Privacy**  
Your name and a unique ID will be stored alongside your request for identification, queue management, and recognition purposes. No personal emails are collected or shared.

**6. Badge and Recognition Disclaimer**  
Recognition (e.g., Viber of the Week, top requestor) is based on submission data. Badges and rankings are awarded automatically and subject to change without notice.

**7. Cancellation & Queue Disclaimer**  
Requests may be removed or postponed by the DJ due to time limits, duplicates, or event changes. Users can cancel requests with an optional reason using their request cart.

**8. Third-Party Tools Disclosure**  
This app utilizes Google Sheets and related tools to manage submissions and queue data. By using the app, you consent to non-sensitive data being logged for functionality.

**9. Changes to Terms**  
VibeQue may update these terms at any time. Continued use of the platform after changes constitutes acceptance of the new terms.

**10. Contact Information**  
For questions about these terms, please contact the DJ or app admin directly during the event.
""")

# ✅ Consent checkbox
agree = st.checkbox("I have read and agree to the Terms & Conditions")

# 🚪 Entry button (only enabled if checkbox is ticked)
if agree:
    if st.button("Enter Vibe Que"):
        st.success("Welcome to the Vibe Que experience! 🎉")
        st.markdown("👉 Use the sidebar to access the Request Form.")
else:
    st.button("Enter Vibe Que", disabled=True)
    st.info("You must agree to the Terms & Conditions to continue.")
