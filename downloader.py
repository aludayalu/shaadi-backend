import os, shutil
import urllib.parse
from pytube import YouTube
from pydub import AudioSegment
import instaloader
import uuid

def download_youtube_audio(video_url, name):
    video_url=video_url.replace("/shorts/","/watch?v=").replace("youtu.be/","youtube.com/watch?v=")
    print(video_url)
    try:
        # Get YouTube video
        youtube = YouTube(video_url)

        # Get the highest resolution stream
        audio_stream = youtube.streams.filter(only_audio=True).first()

        # Download the audio
        profile_folder = uuid.uuid4().__str__()
        audio_stream.download(profile_folder)

        # Convert the downloaded audio to MP3
        mp4_path = f"{profile_folder}/"+os.listdir(profile_folder)[0]
        mp3_path = f"songs/{name}.mp3"

        audio = AudioSegment.from_file(mp4_path, format="mp4")
        audio.export(mp3_path, format="mp3")

        # Delete the original MP4 file
        shutil.rmtree(profile_folder)

        return True

    except Exception as e:
        import traceback
        traceback.print_exc()
        return False

def download_instagram_audio(post_url, name):
    try:
        # Parse the Instagram post URL to remove any random parameters
        parsed_url = urllib.parse.urlparse(post_url)
        post_shortcode = parsed_url.path.strip('/').split('/')[-1]

        # Create an Instaloader instance
        loader = instaloader.Instaloader()

        # Load the post by its shortcode
        post = instaloader.Post.from_shortcode(loader.context, post_shortcode)

        # Get the video URL
        video_url = post.url + "download/?force_landscape=1"

        # Create a folder with the profile's username
        profile_folder = uuid.uuid4().__str__()
        try:
            os.mkdir(profile_folder)
        except:
            pass

        # Download the video
        loader.download_post(post, target=profile_folder)

        # Identify the correct video file
        print(os.listdir(profile_folder), profile_folder)
        video_files = [f for f in os.listdir(profile_folder) if f.endswith(".mp4")]
        if not video_files:
            raise Exception("No video files found in the downloaded content.")

        video_file = os.path.join(profile_folder, video_files[0])

        # Convert the downloaded video to audio (MP3)
        mp3_path = f"songs/{name}.mp3"

        audio = AudioSegment.from_file(video_file, format="mp4")
        audio.export(mp3_path, format="mp3")

        # Delete the original MP4 file
        shutil.rmtree(profile_folder)

        return True

    except Exception as e:
        import traceback
        traceback.print_exc()
        return False