import streamlit as st
from pytube import YouTube
import io

PASSWORD = "EarthRotates350$"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.title("🔒 YouTube Downloader - Login")
        password = st.text_input("Enter password to access the app:", type="password")
        if st.button("Login"):
            if password == PASSWORD:
                st.session_state["password_correct"] = True
                st.experimental_rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
        return False
    else:
        return True


def main():
    st.set_page_config(page_title="YouTube Downloader", page_icon="🎥", layout="centered")

    st.title("🎥 YouTube Audio/Video Downloader")
    st.write("Paste YouTube video URL below to download audio or video.")

    url = st.text_input("YouTube Video URL")

    if url:
        try:
            yt = YouTube(url)
            st.write(f"**Title:** {yt.title}")
            st.write(f"**Author:** {yt.author}")
            st.write(f"**Length:** {yt.length // 60} min {yt.length % 60} sec")

            audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
            video_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

            if st.button("Download Audio"):
                audio_stream = audio_streams.first()
                if audio_stream:
                    with st.spinner("Downloading audio..."):
                        audio_bytes = io.BytesIO()
                        audio_stream.stream_to_buffer(audio_bytes)
                        audio_bytes.seek(0)
                        st.download_button(
                            label="Click to download audio",
                            data=audio_bytes,
                            file_name=f"{yt.title}_audio.mp3",
                            mime="audio/mp3"
                        )
                else:
                    st.error("No audio streams found for this video.")

            if st.button("Download Video (MP4)"):
                video_stream = video_streams.first()
                if video_stream:
                    with st.spinner("Downloading video..."):
                        video_bytes = io.BytesIO()
                        video_stream.stream_to_buffer(video_bytes)
                        video_bytes.seek(0)
                        st.download_button(
                            label="Click to download video",
                            data=video_bytes,
                            file_name=f"{yt.title}_video.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("No video streams found for this video.")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    if check_password():
        main()
