mport streamlit as st
from pytube import YouTube

PASSWORD = "EarthRotates350$"

def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("Enter password to access the app:", type="password", key="password_input")
        if st.session_state.get("password_input") == PASSWORD:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.stop()
    elif not st.session_state.password_correct:
        st.text_input("Enter password to access the app:", type="password", key="password_input")
        st.error("Incorrect password")
        st.stop()

check_password()

st.title("YouTube Video Downloader")

url = st.text_input("Paste the YouTube video URL:")

if url:
    try:
        yt = YouTube(url)
        st.subheader(f"Title: {yt.title}")
        choice = st.radio("Download:", ["Audio", "Video"])

        if choice == "Audio":
            if st.button("Download Audio"):
                stream = yt.streams.filter(only_audio=True).first()
                stream.download()
                st.success("Audio downloaded successfully!")
        else:
            if st.button("Download Video"):
                stream = yt.streams.get_highest_resolution()
                stream.download()
                st.success("Video downloaded successfully!")
    except Exception as e:
        st.error(f"Error: {str(e)}")