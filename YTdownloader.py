import streamlit as st
from pytube import youtube
import os

PASSWORD = "EarthRotates350$"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("Private YouTube Downloader")
    password = st.text_input("Enter password to continue:", type="password")
    if st.button("Login"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.success("Access granted.")
        else:
            st.error("Incorrect password.")

if not st.session_state.authenticated:
    login()
else:
    st.title("YouTube Downloader Bot")
    url = st.text_input("Paste your YouTube video URL:")

    if url:
        try:
            yt = YouTube(url)
            st.success(f"Title: {yt.title}")

            choice = st.radio("What do you want to download?", ("Audio", "Video"))

            if choice == "Audio":
                audio_stream = yt.streams.filter(only_audio=True).first()
                if st.button("Prepare Audio"):
                    audio_path = audio_stream.download(filename="audio.mp4")
                    with open(audio_path, "rb") as file:
                        st.download_button("Click to Save Audio", file, file_name="audio.mp4")
                    os.remove(audio_path)

            else:
                video_stream = yt.streams.get_highest_resolution()
                if st.button("Prepare Video"):
                    video_path = video_stream.download(filename="video.mp4")
                    with open(video_path, "rb") as file:
                        st.download_button("Click to Save Video", file, file_name="video.mp4")
                    os.remove(video_path)

        except Exception as e:
            st.error(f"Error: {e}")